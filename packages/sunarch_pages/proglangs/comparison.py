# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Proglangs - comparison"""

# requirements
from lektor.db import Page

# package
from common.page import set_field
from proglangs.model import KEY_FOR_COMPARISON_SCORE, KEY_FOR_AGE

skip: tuple[str, ...] = (
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
    '(to Lua)': 0,
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
    '1st': 40,
    '2nd': 30,
    '(2nd)': 30,
    '2.a': 25,
    '3rd': 20,
    '3.a': 15,
    '4th': 10
}

feature_hof: dict[str, int] = {

}

feature_immutable: dict[str, int] = {
    'compile-time': 90,
    'part': 1,
    'macro': 0
}

feature_jargon: dict[str, int] = {
    '(yes)': 50,
    'small': 30,
    'old': 10,
    '(loss)': -10
}

feature_static_typing: dict[str, int] = {
    'typeless': 1,
    'untyped': 1,
    'hybrid': 1
}

all_features: dict[str, dict[str, int]] = {
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


def set_comparison_score(page: Page, value: int) -> None:
    """Set comparison score field of a page"""

    set_field(page, KEY_FOR_COMPARISON_SCORE, value)


def calculate_comparison_score(page, debug: int = 0) -> int:
    """Calculate the comparison score of a language"""

    comparison_score = 0

    for feature_name, feature_values in all_features.items():
        if not page[feature_name]:
            continue

        field_value = page[feature_name]

        if field_value in skip:
            continue

        value: int = feature_values[field_value]
        comparison_score += value

        if debug > 1:
            print(' ' * 3, feature_name, ':', value, '->', comparison_score)

        new_field_value: str = field_value + f' ({value})'
        set_field(page, feature_name, new_field_value)

    comparison_score += page[KEY_FOR_AGE]

    if debug > 2:
        print(' ' * 3, '[', KEY_FOR_COMPARISON_SCORE, ']')

    return comparison_score