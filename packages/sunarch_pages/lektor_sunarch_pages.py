# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""sunarch pages"""

# requirements
from lektor.pluginsystem import Plugin
from lektor.build_programs import BuildProgram
from lektor.builder import Builder, BuildState
from lektor.db import Pad, Page
from lektor.sourceobj import SourceObject
from lektor.types import Type

# package
from common.model import KEY_FOR_TITLE
from proglangs.common import language_pages
from proglangs.age import calculate_age, set_age
from proglangs.comparison import calculate_comparison_score, set_comparison_score
from proglangs.rankings import verify_rankings, calculate_sum_rankings, set_sum_rankings
import competitions.y2024_uefa_euro

DEBUG: int = 0


class PluginDataType(Type):
    """Plugin-data type

    Results in name 'plugindata', derived from class name.
    """

    widget = 'multiline-text'

    def value_from_raw(self, raw):
        """Value from raw"""
        return raw


class SunarchPagesPlugin(Plugin):
    """sunarch pages plugin"""

    name = 'sunarch-pages'
    description = f'{name} - Personal website SSG plugin'

    def on_setup_env(self, **extra):
        """Event handler: on-setup-env"""

        self.env.add_type(PluginDataType)

    def on_before_build(self,
                        builder: Builder,
                        build_state: BuildState,
                        source: SourceObject,
                        prog: BuildProgram,
                        **extra):
        """Event handler: before-build"""

        if not isinstance(source, Page):
            return

        if DEBUG > 3:
            print('  => building', source.source_filename)

        pad: Pad = builder.pad

        match source.url_path:
            case competitions.y2024_uefa_euro.URL_PATH:
                competitions.y2024_uefa_euro.setup(source, debug=DEBUG)

    def on_before_build_all(self, builder: Builder, **extra) -> None:
        """Event handler: before-build-all"""

        pad: Pad = builder.pad

        verify_rankings(pad, debug=DEBUG)

        for child in language_pages(pad):
            if DEBUG > 0:
                print(child[KEY_FOR_TITLE])

            age: int = calculate_age(child, debug=DEBUG)
            set_age(child, age, debug=DEBUG)

            comparison_score: int = calculate_comparison_score(child, debug=DEBUG)
            set_comparison_score(child, comparison_score, debug=DEBUG)

            sum_rankings: int = calculate_sum_rankings(child, debug=DEBUG)
            set_sum_rankings(child, sum_rankings, debug=DEBUG)
