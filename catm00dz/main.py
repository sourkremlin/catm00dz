import argparse

from catm00dz.data import (
    Pixel,
    Color,
    ImageCalendar
)
from catm00dz.calendar_images import (
    get_blank_calendar_path
)
from catm00dz.statistics import (
    average_mood_by_weekday,
    average_mood_by_month,
    std_mood_by_weekday
)


def print_statistics():
    print(
        average_mood_by_weekday(
            'cat_calendar.png'
        )
    )
    print(
        average_mood_by_month(
            'cat_calendar.png'
        )
    )
    print(
        std_mood_by_weekday(
            'cat_calendar.png'
        )
    )


def show_points():
    cal_read = ImageCalendar.from_path(
        get_blank_calendar_path()
    )
    cal_write = ImageCalendar.from_path(
        get_blank_calendar_path()
    )

    for pixel in cal_read.iter_box_centers:
        cal_write.draw_point(
            pixel,
            Color(255, 255, 255),
            2
        )

    cal_write._img.show()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode')
    args = parser.parse_args()

    if args.mode == 'stats':
        print_statistics()
    elif args.mode == 'show_points':
        show_points()



if __name__ == '__main__':
    main()
