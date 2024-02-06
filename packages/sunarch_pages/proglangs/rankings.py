# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Proglangs - rankings"""

# library
from typing import Callable, Generator, OrderedDict, Union

# requirements
from lektor.databags import Databags
from lektor.db import Pad, Page, Query

# package
from common.model import KEY_FOR_SLUG, KEY_FOR_TITLE
from common.page import closure_page_title_lookup, set_field
from proglangs.common import PATH_PROGLANGS
from proglangs.model import KEY_FOR_SUM_RANKINGS


def set_sum_rankings(page: Page, value: int) -> None:
    set_field(page, KEY_FOR_SUM_RANKINGS, value)


def ranking_field_name(ranking_name: str) -> str:
    return f'ranking_{ranking_name}'


def ranking_databag_name(ranking_name: str) -> str:
    return f'proglang_rankings_{ranking_name}'


def latest_to_databag_label(latest: str) -> str:
    return latest.lower().replace(' ', '_')


def bag_path(*args):
    return '.'.join(args)


def comment_to_display(place: int, comment: str) -> str:
    if not comment:
        return f'{place}'

    return f'{place} ({comment.strip()})'


def display_add_equivalence(display: str, title: str) -> str:
    return f'{display} ({title})'


def parse_value(value: str) -> tuple[int, str]:
    values: list[str] = list(map(lambda x: x.strip(), value.split('|')))
    if len(values) < 2:
        values.append('')
    place_str, comment = values
    place: int = int(place_str)

    return place, comment_to_display(place, comment)


def parse_equivalence(value: str) -> tuple[str, Union[str, None]]:
    values: list[str] = list(map(lambda x: x.strip(), value.split('|')))
    equivalent_language: str = values[0]
    equivalent_language_title: Union[str, None] = None

    if len(values) > 1:
        equivalent_language_title = values[1]

    return equivalent_language, equivalent_language_title


def closure_rankings_lookup(rankings: OrderedDict,
                            equivalences: OrderedDict,
                            page_title_lookup: Callable[[str], str]
                            ) -> Callable[[str], tuple[int, str]]:

    rankings: dict[str, tuple[int, str]] = {
        language: parse_value(value)
        for language, value in rankings.items()
    }

    def rankings_lookup(language: str) -> tuple[int, str]:
        if language in rankings:
            return rankings[language]

        if equivalences is not None and language in equivalences:
            equivalent_language, equivalent_language_title = parse_equivalence(equivalences[language])
            if not equivalent_language_title:
                equivalent_language_title = page_title_lookup(equivalent_language)
            place, display = rankings[equivalent_language]
            return place, display_add_equivalence(display, equivalent_language_title)

        def gen_places() -> Generator[int, None, None]:
            for place, _ in rankings.values():
                yield place

        last_place: int = max(gen_places())

        def filter_last_place(place: int) -> bool:
            return place == last_place

        count_top_place: int = len(list(filter(filter_last_place, gen_places())))
        place_after_last: int = last_place + count_top_place

        return place_after_last, comment_to_display(place_after_last, 'n/a')

    return rankings_lookup


def closure_databag_section_lookup(databags: Databags) -> Callable[[str, str], OrderedDict]:

    def databag_section_lookup(ranking_name: str, section_label: str) -> OrderedDict:
        databag_name: str = ranking_databag_name(ranking_name)
        databag_path: str = bag_path(databag_name, section_label)

        return databags.lookup(databag_path)

    return databag_section_lookup


def calculate_sum_rankings(page, debug: int = 0) -> int:

    pad: Pad = page.pad

    page_title_lookup: Callable[[str], str] = closure_page_title_lookup(pad, PATH_PROGLANGS)

    databags: Databags = pad.databags

    databag_section_lookup: Callable[[str, str], OrderedDict] = \
        closure_databag_section_lookup(databags)

    all_rankings: dict[str, Callable[[str], tuple[int, str]]] = {}

    rankings_meta: OrderedDict = databags.lookup('proglang_rankings')

    for ranking_name, ranking_data in rankings_meta.items():
        field_name: str = ranking_field_name(ranking_name)
        latest: str = ranking_data['latest']
        latest_label: str = latest_to_databag_label(latest)

        rankings: OrderedDict = databag_section_lookup(ranking_name, latest_label)
        equivalences: OrderedDict = databag_section_lookup(ranking_name, 'equivalence')

        rankings_lookup: Callable[[str], tuple[int, str]] = \
            closure_rankings_lookup(rankings, equivalences, page_title_lookup)

        all_rankings[field_name] = rankings_lookup

    sum_rankings = 0

    language: str = page[KEY_FOR_SLUG]
    language_name: str = page[KEY_FOR_TITLE]
    if debug > 1:
        print(language_name, f'({language})')

    for field_name, rankings_lookup in all_rankings.items():

        place, display = rankings_lookup(language)

        sum_rankings += place

        set_field(page, field_name, display)

        if debug > 1:
            print(' ' * 3, field_name, ':', display)

    if debug > 1:
        print(' ' * 3, '[', KEY_FOR_SUM_RANKINGS, '=', page[KEY_FOR_SUM_RANKINGS], ']')

    return sum_rankings


def get_all_languages(pad: Pad) -> list[str]:
    q_languages = Query(PATH_PROGLANGS, pad)
    return [child[KEY_FOR_SLUG] for child in q_languages.all()]


def get_rankings_info(databags: Databags) -> list[tuple[str, str]]:
    return [
        (ranking_name, ranking_data['latest'])
        for ranking_name, ranking_data
        in databags.lookup('proglang_rankings').items()
    ]


def get_languages_in_ranking(databags: Databags, ranking_name: str, latest: str) -> set[str]:

    databag_section_lookup: Callable[[str, str], OrderedDict] = \
        closure_databag_section_lookup(databags)

    latest_label: str = latest_to_databag_label(latest)

    rankings: OrderedDict = databag_section_lookup(ranking_name, latest_label)
    languages: set[str] = set(rankings.keys())

    equivalences: OrderedDict = databag_section_lookup(ranking_name, 'equivalence')
    if equivalences is not None:
        for language, equivalence_value in equivalences.items():
            languages.add(language)
            equivalent_language, equivalent_language_title = parse_equivalence(equivalence_value)

            if equivalent_language_title is not None:
                if equivalent_language in languages:
                    languages.remove(equivalent_language)

    return languages


def verify_rankings(pad: Pad, debug: int = 0) -> None:
    if debug > 0:
        print('Verifying rankings')

    error_count: int = 0

    all_languages: set[str] = set(get_all_languages(pad))

    databags: Databags = pad.databags

    rankings_info: list[tuple[str, str]] = get_rankings_info(databags)

    for ranking_name, latest in rankings_info:
        if debug > 1:
            print(' ' * 3, 'Ranking', ranking_name)

        languages: set[str] = get_languages_in_ranking(databags, ranking_name, latest)

        if not languages.issubset(all_languages):
            difference: set[str] = languages.difference(all_languages)
            print(f'Unrecognized languages in ranking "{ranking_name}":')
            for item in difference:
                print(' ' * 3, '-', item)
            error_count += len(difference)

    if error_count:
        print(f'Found {error_count} error{"s" if error_count > 1 else ""} in rankings databags')
