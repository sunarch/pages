# -*- coding: utf-8 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from lektor.pluginsystem import Plugin
from lektor.db import Pad, Query

from proglangs import set_field, PATH_PROGLANGS
from proglangs_age import calculate_age, KEY_FOR_AGE
from proglangs_comparison import calculate_comparison_score, KEY_FOR_COMAPRISON_SCORE
from proglangs_rankings import verify_rankings, calculate_sum_rankings, KEY_FOR_SUM_RANKINGS

DEBUG: int = 0


class ProglangsPlugin(Plugin):
    name = 'proglangs'
    description = u'Enhance programmin language info'

    def on_before_build_all(self, builder, **extra):
        pad: Pad = builder.pad
        q_languages = Query(PATH_PROGLANGS, pad)

        verify_rankings(pad, debug=DEBUG)

        for child in q_languages.all():
            if DEBUG > 0:
                print(child['title'])

            age: int = calculate_age(child, debug=DEBUG)
            set_field(child, KEY_FOR_AGE, age)

            comparison_score: int = calculate_comparison_score(child, debug=DEBUG)
            set_field(child, KEY_FOR_COMAPRISON_SCORE, comparison_score)

            sum_rankings: int = calculate_sum_rankings(child, debug=DEBUG)
            set_field(child, KEY_FOR_SUM_RANKINGS, sum_rankings)
