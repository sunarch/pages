# -*- coding: utf-8 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from datetime import date

from lektor.types.base import BadValue

KEY_FOR_FIRST_APPEARED: str = 'first_appeared'
KEY_FOR_AGE: str = 'age'


def calculate_age(page, debug: int = 0) -> int:

    first_appeared: int = page[KEY_FOR_FIRST_APPEARED]

    if isinstance(first_appeared, BadValue):
        return 0

    current_year: int = date.today().year

    return current_year - first_appeared
