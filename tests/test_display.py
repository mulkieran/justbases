# Copyright (C) 2015 - 2019 Red Hat, Inc.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; If not, see <http://www.gnu.org/licenses/>.
#
# Red Hat Author(s): Anne Mulhern <amulhern@redhat.com>
# Other Author(s): Anne Mulhern <mulhern@cs.wisc.edu>

""" Test for utility functions. """

import unittest

from justbases import BasesConfig
from justbases import BasesError
from justbases import BaseConfig
from justbases import DigitsConfig
from justbases import StripConfig

from justbases._display import Digits
from justbases._display import Number
from justbases._display import String
from justbases._display import Strip

from hypothesis import given
from hypothesis import settings
from hypothesis import strategies

from ._utils import build_base
from ._utils import build_base_config
from ._utils import build_display_config
from ._utils import build_nat
from ._utils import build_radix
from ._utils import build_relation
from ._utils import build_sign
from ._utils import build_strip_config


class TestString(unittest.TestCase):
    """
    Test display of Radix given display configuration.
    """

    @given(
        build_radix(1024, 10),
        build_display_config(
            strategies.just(BaseConfig()),
            strategies.just(DigitsConfig(use_letters=False)),
            build_strip_config(),
        ),
        build_relation(),
    )
    @settings(max_examples=100)
    def testFormat(self, radix, display, relation):
        """
        Verify that a xformed string with a repeating part shows that part.
        """
        result = String(display, radix.base).xform(radix, relation)
        assert (
            radix.repeating_part != [] and not display.base_config.use_subscript
        ) == (result[-1] == ")")


class TestDigits(unittest.TestCase):
    """
    Test Digits methods.
    """

    def testExceptions(self):
        """
        Test exceptions.
        """
        with self.assertRaises(BasesError):
            # pylint: disable=protected-access
            Digits(
                BasesConfig.DISPLAY_CONFIG.digits_config,
                Digits._MAX_SIZE_BASE_FOR_CHARS + 1,
            )


class TestNumber(unittest.TestCase):
    """
    Test Number.
    """

    @given(
        strategies.text(alphabet=strategies.characters(), max_size=10),
        strategies.text(alphabet=strategies.characters(), min_size=1, max_size=10),
        strategies.text(alphabet=strategies.characters(), max_size=10),
        build_base_config(),
        build_base(16),
        build_sign(),
    )
    @settings(max_examples=100)
    def testXform(
        self, integer_part, non_repeating_part, repeating_part, config, base, sign
    ):
        """
        Test xform.
        """
        # pylint: disable=too-many-arguments

        result = Number(config, base).xform(
            integer_part, non_repeating_part, repeating_part, base, sign
        )
        if config.use_prefix and base == 16 and sign != -1:
            self.assertTrue(result.startswith("0x"))
        if config.use_prefix and base == 8 and sign != -1:
            self.assertTrue(result.startswith("0"))
        if config.use_subscript:
            base_str = str(base)
            self.assertEqual(result.rfind(base_str) + len(base_str), len(result))


class TestStrip(unittest.TestCase):
    """
    Test Strip.
    """

    @given(build_nat(10, 3), build_strip_config(), build_relation(), build_base(16))
    @settings(max_examples=100)
    def testXform(self, number, config, relation, base):
        """
        Confirm that option strip strips more than other options.
        """
        result = Strip(config, base).xform(number, relation)
        most = Strip(StripConfig(strip=True), base).xform(number, relation)

        self.assertTrue(len(most) <= len(result))

        if config.strip and number != []:
            self.assertTrue(result[-1] != 0)
