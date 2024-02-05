# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Proglangs -age"""

# library
from datetime import date

# requirements
from lektor.db import Page
from lektor.types.base import BadValue

# package
from common.page import set_field
from proglangs.model import KEY_FOR_AGE, KEY_FOR_FIRST_APPEARED


def set_age(page: Page, value: int) -> None:
    set_field(page, KEY_FOR_AGE, value)


def calculate_age(page, debug: int = 0) -> int:

    first_appeared: int = page[KEY_FOR_FIRST_APPEARED]

    if isinstance(first_appeared, BadValue):
        return 0

    current_year: int = date.today().year

    return current_year - first_appeared
