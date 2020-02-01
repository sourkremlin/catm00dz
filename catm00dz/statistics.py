from catm00dz.data import MoodExperienceImageCalendar

import collections


def average_mood_by_weekday(img_path):
    weekday_counter = collections.defaultdict(int)
    gpa_counter = collections.defaultdict(float)

    experience_cal = MoodExperienceImageCalendar.from_path(
        img_path
    )

    for experience in experience_cal.iter_box_center_decoded:
        if experience.mood.is_blank:
            continue

        weekday_counter[experience.date.weekday] += 1
        gpa_counter[experience.date.weekday] += experience.mood.gpa

    return {
        weekday: (
            gpa_counter[weekday] / weekday_counter[weekday]
        )
        for weekday
        in weekday_counter.keys()
    }


def average_mood_by_month(img_path):
    month_counter = collections.defaultdict(int)
    gpa_counter = collections.defaultdict(float)

    experience_cal = MoodExperienceImageCalendar.from_path(
        img_path
    )

    for experience in experience_cal.iter_box_center_decoded:
        if experience.mood.is_blank:
            continue

        month_counter[experience.date.month] += 1
        gpa_counter[experience.date.month] += experience.mood.gpa

    return {
        month: (
            gpa_counter[month] / month_counter[month]
        )
        for month
        in month_counter.keys()
    }


def std_mood_by_weekday(img_path):
    avg_by_weekday = average_mood_by_weekday(
        img_path
    )

    experience_cal = MoodExperienceImageCalendar.from_path(
        img_path
    )

    weekday_counter = collections.defaultdict(int)
    sum_diff_pow2_from_avg_by_weekday = collections.defaultdict(int)
    for experience in experience_cal.iter_box_center_decoded:
        if experience.mood.is_blank:
            continue

        sum_diff_pow2_from_avg_by_weekday[experience.date.weekday] += (
            pow(experience.mood.gpa - avg_by_weekday[experience.date.weekday], 2.0)
        )
        weekday_counter[experience.date.weekday] += 1

    return {
        calendar.day_name[weekday]: pow(
            (1 / (weekday_counter[weekday] - 1)) *
            sum_diff_pow2_from_avg_by_weekday[weekday],
            0.5
        )
        for weekday
        in weekday_counter.keys()
    }