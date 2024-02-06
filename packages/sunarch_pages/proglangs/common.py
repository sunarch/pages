# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Proglangs - common"""

# requirements
from lektor.db import Pad, Page, Query

# package
from proglangs.model import PATH_PROGLANGS


def language_pages(pad: Pad) -> list[Page]:
    """Generate a list of all language pages"""

    q_languages = Query(PATH_PROGLANGS, pad)

    return q_languages.all()


def path_language(language_slug: str) -> str:
    """Create a path to a specific language"""

    return f'{PATH_PROGLANGS}/{language_slug}'
