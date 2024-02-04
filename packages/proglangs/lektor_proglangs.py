# -*- coding: utf-8 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from lektor.pluginsystem import Plugin
from lektor.db import Query

from proglangs import set_field
from proglangs_age import calculate_age, KEY_FOR_AGE
from proglangs_comparison import calculate_comparison_score, KEY_FOR_COMAPRISON_SCORE

DEBUG: int = 0


class ProglangsPlugin(Plugin):
    name = 'proglangs'
    description = u'Enhance programmin language info'

    def on_before_build_all(self, builder, **extra):
        q_languages = Query('/tech/programming/languages', builder.pad)

        for child in q_languages.all():
            if DEBUG > 0:
                print(child['title'])

            age: int = calculate_age(child, debug=DEBUG)
            set_field(child, KEY_FOR_AGE, age)

            comparison_score: int = calculate_comparison_score(child, debug=DEBUG)
            set_field(child, KEY_FOR_COMAPRISON_SCORE, comparison_score)
