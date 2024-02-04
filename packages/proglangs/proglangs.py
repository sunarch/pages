# -*- coding: utf-8 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from typing import Any


def set_field(page, field_name: str, new_value: Any, debug: int = 0):
    if debug > 1:
        print(' ' * 7, '_bound_data', ': ', end='')
        if field_name in page._bound_data:
            print(page._bound_data[field_name], end='')
    page._bound_data[field_name] = new_value
    if debug > 1:
        print(' ->', page._bound_data[field_name])

    if debug > 1:
        print(' ' * 7, '_data', ': ', end='')
        if field_name in page._data:
            print(page._data[field_name], end='')
    page._data[field_name] = new_value
    if debug > 1:
        print(' ->', page._data[field_name])
