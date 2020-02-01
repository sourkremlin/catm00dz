from abc import ABC
import calendar
from dataclasses import dataclass
import datetime

from PIL import Image, ImageDraw


@dataclass
class Pixel:
    ''' We'll be reading from pixel locations in an image. Nota bene,
    the module we're using for images (PIL) uses a coordinate system
    that starts (0, 0) in the upper left '''
    x: float
    y: float


@dataclass
class Color:
    ''' The color values are determined by red, green, and blue values.
    Each value ranges from 0-255, where 255 is the maximum intensity
    of the color.
    '''
    r: int
    g: int
    b: int

    def abs_diff(self, other) -> float:
        ''' Used as a measure of how 'close' one color is to another.
        We will basically be grabbing a color and matching it to the
        closest 'known' color. '''
        return (
            abs(self.r - other.r) +
            abs(self.g - other.g) +
            abs(self.b - other.b)
        )


@dataclass
class Mood:
    ''' A mood is assigned to a color. The calendar has a bunch of
    little boxes that correspond to moods on a particular day.
    The game will be collecting colors from certain pixel locations
    in the calendar that map to dates, then using these Moods to
    decode the mood on a particular day. '''

    color: Color

    @dataclass
    class _PlatonicMood:
        ''' Platonic is used here in the sense of 'idealized' --
        that is, it's the idealized Color values for a particular
        mood. When we are trying to decide the mood from a color,
        we will decide how close we are to an 'ideal' mood using
        the abs_diff function of the color and then snap to it.
        '''

        color: Color    # The idealized color! Hand-chosen!
        english: str    # What is this mood, in english?!
        gpa: float      # 4.0 based scale for mood positivity.
                        # used for numerics e.g. averaging 
                        # over moods

    # The 'ideal' moods we can match against. There is a
    # 'blank' mood for days that are not filled out.
    # Generally this will be used to filter out days
    # that shouldn't be counted.
    PLATONICS = [
        _PlatonicMood(
            Color(238, 109, 140), 'Amazing', 4.0
        ),
        _PlatonicMood(
            Color(255, 157, 74), 'Good', 3.0
        ),
        _PlatonicMood(
            Color(251, 194, 45), 'Ok', 2.0
        ),
        _PlatonicMood(
            Color(117, 200, 254), 'Sad', 1.0
        ),
        _PlatonicMood(
            Color(255, 255, 255), 'Blank', float('NaN')
        )
    ]

    @property
    def is_blank(self) -> bool:
        ''' Blank means we have no mood data! '''
        return self._closest_platonic_mood.english == 'Blank'

    @property
    def gpa(self) -> float:
        ''' What is the GPA of the closest idealized mood? Hmm! '''
        return self._closest_platonic_mood.gpa

    @property
    def english(self) -> str:
        ''' What is the english translation of the closest
        idealized mood, hmmm!? '''
        return self._closest_platonic_mood.english

    @property
    def _closest_platonic_mood(self):
        ''' Ah yes, this is a very important function.

        Let's take the abs_diff of the given color against
        all idealized moods, and choose the idealized mood
        we match best against! '''
        cat_metric = [
            self.color.abs_diff(platonic.color)
            for platonic
            in self.PLATONICS
        ]

        index, min_val = -1, 10000
        for i in range(len(cat_metric)):
            if cat_metric[i] < min_val:
                index, min_val = i, cat_metric[i]
        return self.PLATONICS[index]

    def __str__(self) -> str:
        return self.english


@dataclass
class YMDW:
    ''' A simple wrapper for year/month/day/weekday information
    that we'll generally be retrieving from the standard calendar
    module. '''

    year: int       # The current year, this is basically
                    # fixed but we'll be getting this given
                    # to us by functions and we might as well
                    # store it.
    month: int      # 1-based indexing, starts at January
                    # and goes to December!
    day: int        # 1-based indexing for the day, starting
                    # at the first of the month!
    weekday: int    # This helps us with which day of the week
                    # it is. Monday is zero, then it runs up to
                    # Sunday.

    @property
    def english_month(self) -> str:
        ''' What is the name of the month, in english!? '''
        return calendar.month_name[self.month]

    @property
    def english_day(self) -> str:
        ''' What is the name of the day, in english!?

        Example would be like... Monday or Tuesday '''
        return calendar.day_name[self.day]


@dataclass
class MoodExperience:
    ''' It'll be fun to do some statistics about moods on
    particular days, so let's wrap a mood and a date together
    into an... experience. This will be the atom of mood
    analysis '''

    mood: Mood
    date: YMDW

    @classmethod
    def from_color_and_date(cls, color: Color, date: YMDW):
        ''' One could justifiably ask why this is used instead
        of the implicit __init__ function made by the dataclass.

        I might want to decode colors from an image into something
        other than moods. Essentially information gathered from
        the calendar will be along the lines of a color on a date
        though. So I wouldn't want my calendar to be hardcore
        tied to a particular class (e.g. MoodExperience).

        In the calendar, we will take whatever given class
        can decode a color and date into information using
        this more generalized function. '''
        return cls(Mood(color), date)


class ImageCalendar:
    ''' It's an image, but it's also a calendar! There are
    locations on the image that map to dates. The thing
    that we'd really like to do is iterate over all of
    the dates in the calendar and read the pixels. '''

    # There are a bunch of little squares that hold the
    # day's color. The boxes are fixed width and height
    # for a particular calendar (this is an assumption!).
    # Someone will need to take a look at the picture
    # and figure this out.
    _BOX_WIDTH = 65
    _BOX_HEIGHT = 57
    _CALENDAR_START = Pixel(1130, 245)
    _PIXEL_DECODER = None

    def __init__(self, img: Image):
        super(ImageCalendar, self).__init__()
        self._img = img

    @property
    def iter_dates(self):
        cal = calendar.Calendar(
            firstweekday=2 # Wednesday!
        )

        # Calendar is intended to make views of a yearly calendar
        # by month. Days are duplicated, because the monthly
        # views show the same day multiple times. We can still use
        # it to cheat on iteration of months/days, but need to
        # not yield junk we have already seen.
        already_seen = set()
        for month_idx in range(1, 13):
            for date_info in cal.itermonthdays4(2020, month_idx):
                if date_info in already_seen:
                    continue
                else:
                    already_seen.add(date_info)

                yield YMDW(*date_info)

    @property
    def iter_box_centers(self):
        for date in self.iter_dates:
            yield self.center_pixel_from_date(
                date
            )

    @property
    def iter_box_center_decoded(self):
        assert self._PIXEL_DECODER is not None

        for date in self.iter_dates:
            yield self._PIXEL_DECODER.from_color_and_date(
                Color(
                    *self._img.getpixel((
                        self.center_pixel_x_from_date(
                            date
                        ),
                        self.center_pixel_y_from_date(
                            date
                        )
                    ))
                ),
                date
            )

    def center_pixel_x_from_date(self, date) -> int:
        stride = self._BOX_WIDTH * (date.month - 1)
        return self._CALENDAR_START.x + stride

    def center_pixel_y_from_date(self, date) -> int:
        stride = self._BOX_HEIGHT * (date.day - 1)
        return self._CALENDAR_START.y + stride

    def draw_point(self, pixel:Pixel, color:Color, radius:float):
        img_writer = ImageDraw.Draw(self._img)

        top_left = Pixel(
            pixel.x - radius / 2.0,
            pixel.y - radius / 2.0
        )
        bottom_right = Pixel(
            pixel.x + radius / 2.0,
            pixel.y + radius / 2.0
        )
        img_writer.ellipse(
            [           
                top_left.x,
                top_left.y,
                bottom_right.x,
                bottom_right.y
            ],
            fill=(color.r, color.g, color.b),
            outline=None
        )
        del img_writer

    def save_img(self, img_path:str):
        self._img.save(img_path, 'PNG')

    @classmethod
    def from_path(cls, img_path:str):
        return cls(Image.open(img_path))


class MoodExperienceImageCalendar(ImageCalendar):
    _PIXEL_DECODER = MoodExperience
