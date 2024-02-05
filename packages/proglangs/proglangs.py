# -*- coding: utf-8 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from typing import Any, Callable

from lektor.db import Pad, Page, Query

KEY_FOR_SLUG: str = '_slug'
KEY_FOR_TITLE: str = 'title'

PATH_PROGLANGS: str = '/tech/programming/languages'


def path_language(language_slug: str) -> str:
    return f'{PATH_PROGLANGS}/{language_slug}'


def set_field(page, field_name: str, new_value: Any, debug: int = 0):
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


def closure_page_title_lookup(pad: Pad) -> Callable[[str], str]:

    query: Query = Query(PATH_PROGLANGS, pad)

    def page_title_lookup(language_slug: str) -> str:
        page: Page = query.get(language_slug)

        if page is None:
            raise ValueError(f'[Title lookup] Page not found: {language_slug}')

        return page['title']

    return page_title_lookup
