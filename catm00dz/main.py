import argparse

from catm00dz.data import (
    Pixel,
    Color
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
    pass


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
