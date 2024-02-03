# -*- coding: utf-8 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from lektor.pluginsystem import Plugin
from lektor.db import Query

DEBUG: int = 0
KEY_FOR_COMAPRISON_SCORE: str = 'comparison_score'

skip: tuple[str] = (
    '',
    '--',
    'N/A'
)

feature: dict[str, int] = {
    'yes': 100,
    'new': 50
}

feature_adt: dict[str, int] = {

}

feature_compiled: dict[str, int] = {
    'via C': 99,
    'Java VM': 2,
    'BEAM VM': 2,
    'CLI/.NET': 1,
    'Python BC': 1,
    'Ethereum VM': 0,
    '(to JavaScript)': 0
}

feature_explicit_errors: dict[str, int] = {
    'Result': 100,
    'Maybe': 100,
    'union': 100,
    'value': 90,
    'nil return': 50,
    'try/catch + Option': 10,
    'try/throw': 1,
    'try/catch': 1,
    '(return)': 0
}

feature_hacker: dict[str, int] = {
    '1st': 100,
    '2nd': 100,
    '(2nd)': 100,
    '2.a': 50,
    '3rd': 100,
    '3.a': 50,
    '4th': 100
}

feature_hof: dict[str, int] = {

}

feature_immutable: dict[str, int] = {
    'part': 1
}

feature_jargon: dict[str, int] = {
    '(yes)': 100,
    'small': 50,
    'old': 50,
    '(loss)': -1
}

feature_static_typing: dict[str, int] = {
    'untyped': 1,
    'hybrid': 1
}

all_features: dict[str, dict[str, int]] =  {
    'feature_adt': feature_adt,
    'feature_compiled': feature_compiled,
    'feature_explicit_errors': feature_explicit_errors,
    'feature_hacker': feature_hacker,
    'feature_hof': feature_hof,
    'feature_immutable': feature_immutable,
    'feature_jargon': feature_jargon,
    'feature_static_typing': feature_static_typing
}

for dict_feature in all_features.values():
    dict_feature.update(feature)


def negative_score(value: int):
    return (-1) * len(all_features) * feature['yes'] + value


class ProglangsPlugin(Plugin):
    name = 'proglangs'
    description = u'Enhance programmin language info'

    def on_before_build_all(self, builder, **extra):
        q_languages = Query('/tech/programming/languages', builder.pad)

        for child in q_languages.all():
            if DEBUG > 0:
                print(child['title'])

            comparison_score = 0

            for feature_name, feature_values in all_features.items():
                if not child[feature_name]:
                    continue

                field_value = child[feature_name]

                if field_value in skip:
                    continue

                value = feature_values[field_value]
                comparison_score += value

                if DEBUG > 0:
                    print(' ' * 3, feature_name, ':', value, '->', comparison_score)

                if DEBUG > 1:
                    print(' ' * 7, '_bound_data', ':', child._bound_data[feature_name], end='')
                child._bound_data[feature_name] += f' ({value})'
                if DEBUG > 1:
                    print(' ->', child._bound_data[feature_name])

                if DEBUG > 1:
                    print(' ' * 7, '_data', ':', child._data[feature_name], end='')
                child._data[feature_name] += f' ({value})'
                if DEBUG > 1:
                    print(' ->', child._data[feature_name])

            if 'disqualified' in child['sunarch']:
                if DEBUG > 0:
                    print(' ' * 3, '(negative score) :', comparison_score, end='')
                comparison_score = negative_score(comparison_score)
                if DEBUG > 0:
                    print(' ->', comparison_score)

            if DEBUG > 1:
                print(' ' * 3, '[', KEY_FOR_COMAPRISON_SCORE, ']')

            if DEBUG > 1:
                print(' ' * 7, '_bound_data', ': ', end='')
                if KEY_FOR_COMAPRISON_SCORE in child._bound_data:
                    print(child._bound_data[KEY_FOR_COMAPRISON_SCORE], end='')
            child._bound_data[KEY_FOR_COMAPRISON_SCORE] = comparison_score
            if DEBUG > 1:
                print(' ->', child._bound_data[KEY_FOR_COMAPRISON_SCORE])

            if DEBUG > 1:
                print(' ' * 7, '_data', ': ', end='')
                if KEY_FOR_COMAPRISON_SCORE in child._data:
                    print(child._data[KEY_FOR_COMAPRISON_SCORE], end='')
            child._data[KEY_FOR_COMAPRISON_SCORE] = comparison_score
            if DEBUG > 1:
                print(' ->', child._data[KEY_FOR_COMAPRISON_SCORE])
