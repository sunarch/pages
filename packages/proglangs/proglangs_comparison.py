# -*- coding: utf-8 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from proglangs import set_field
from proglangs_age import KEY_FOR_AGE

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
    'library': 80,
    'sealed interface + record': 20,
    'interface': 20,
    'struct': 1
}

feature_compiled: dict[str, int] = {
    'via C': 99,
    'by LLVM': 90,
    'optional': 70,
    'multi-step': 50,
    'BEAM VM': 30,
    'Java VM': 20,
    'CLI/.NET': 10,
    'Python BC': 1,
    'bytecode': 1,
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
    'pointer return': 0,
    '(return)': 0
}

feature_hacker: dict[str, int] = {
    '1st': 130,
    '2nd': 120,
    '(2nd)': 120,
    '2.a': 115,
    '3rd': 110,
    '3.a': 105,
    '4th': 100
}

feature_hof: dict[str, int] = {

}

feature_immutable: dict[str, int] = {
    'compile-time': 90,
    'part': 1,
    'macro': 0
}

feature_jargon: dict[str, int] = {
    '(yes)': 100,
    'small': 60,
    'old': 50,
    '(loss)': -90
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


def negative_score(value: int) -> int:
    return (-1) * len(all_features) * feature['yes'] + value


def calculate_comparison_score(page, debug: int = 0) -> int:
    comparison_score = 0

    for feature_name, feature_values in all_features.items():
        if not page[feature_name]:
            continue

        field_value = page[feature_name]

        if field_value in skip:
            continue

        value: str = feature_values[field_value]
        comparison_score += value

        if debug > 1:
            print(' ' * 3, feature_name, ':', value, '->', comparison_score)

        new_field_value: str = field_value + f' ({value})'
        set_field(page, feature_name, new_field_value)

    comparison_score += page[KEY_FOR_AGE]

    if 'disqualified' in page['sunarch']:
        if debug > 1:
            print(' ' * 3, '(negative score) :', comparison_score, end='')
        comparison_score = negative_score(comparison_score)
        if debug > 1:
            print(' ->', comparison_score)

    if debug > 2:
        print(' ' * 3, '[', KEY_FOR_COMAPRISON_SCORE, ']')

    return comparison_score
