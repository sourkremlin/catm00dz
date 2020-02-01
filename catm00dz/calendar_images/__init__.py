import os


def _get_calendar_path(fname):
    return os.path.join(
        os.path.dirname(
            __file__
        ),
        fname
    )


def get_blank_calendar_path():
    return _get_calendar_path(
        'cat_calendar_blank.png'
    )