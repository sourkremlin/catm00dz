import os

from catm00dz.calendar_images import (
    get_blank_calendar_path
)


def test_blank_calendar_exists():
    assert os.path.exists(
        get_blank_calendar_path()
    )