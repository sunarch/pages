# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Page"""

# library
from typing import Any, Callable

# requirements
from lektor.db import Pad, Page, Query

# package
from common.model import KEY_FOR_TITLE


def closure_page_title_lookup(pad: Pad, path: str) -> Callable[[str], str]:

    query: Query = Query(path, pad)

    def page_title_lookup(language_slug: str) -> str:
        page: Page = query.get(language_slug)

        if page is None:
            raise ValueError(f'[Title lookup] Page not found: {language_slug}')

        return page[KEY_FOR_TITLE]

    return page_title_lookup


def set_field(page: Page, field_name: str, new_value: Any, debug: int = 0):
    if debug > 2:
        print(' ' * 7, '_bound_data', ': ', end='')
        if field_name in page._bound_data:
            print(page._bound_data[field_name], end='')
    page._bound_data[field_name] = new_value
    if debug > 2:
        print(' ->', page._bound_data[field_name])

    if debug > 2:
        print(' ' * 7, '_data', ': ', end='')
        if field_name in page._data:
            print(page._data[field_name], end='')
    page._data[field_name] = new_value
    if debug > 2:
        print(' ->', page._data[field_name])
