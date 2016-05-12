# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions of
# the GNU General Public License v.2, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY expressed or implied, including the implied warranties of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.  You should have received a copy of the
# GNU General Public License along with this program; if not, write to the
# Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#
# Author: Anne Mulhern <mulhern@cs.wisc.edu>

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
          build_strip_config()
       ),
       build_relation()
    )
    @settings(max_examples=100)
    def testFormat(self, radix, display, relation):
        """
        Verify that a xformed string with a repeating part shows that part.
        """
        result = String(display).xform(radix, relation)
        assert (radix.repeating_part != [] and \
           not display.base_config.use_subscript) == (result[-1] == ")")


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
            Digits(BasesConfig.DISPLAY_CONFIG.digits_config).xform(
               [],
               Digits._MAX_SIZE_BASE_FOR_CHARS + 1
            )


class TestNumber(unittest.TestCase):
    """
    Test Number.
    """

    @given(
       strategies.text(alphabet=strategies.characters(), max_size=10),
       strategies.text(
          alphabet=strategies.characters(),
          min_size=1,
          max_size=10
       ),
       strategies.text(alphabet=strategies.characters(), max_size=10),
       build_base_config(),
       build_base(16),
       build_sign()
    )
    @settings(max_examples=100)
    def testXform(
       self,
       integer_part,
       non_repeating_part,
       repeating_part,
       config,
       base,
       sign
    ):
        """
        Test xform.
        """
        # pylint: disable=too-many-arguments

        result = Number(config).xform(
           integer_part,
           non_repeating_part,
           repeating_part,
           base,
           sign
        )
        if config.use_prefix and base == 16 and sign != -1:
            self.assertTrue(result.startswith('0x'))
        if config.use_prefix and base == 8 and sign != -1:
            self.assertTrue(result.startswith('0'))
        if config.use_subscript:
            base_str = str(base)
            self.assertEqual(
               result.rfind(base_str) + len(base_str),
               len(result)
            )


class TestStrip(unittest.TestCase):
    """
    Test Strip.
    """

    @given(
       build_nat(10, 3),
       build_strip_config(),
       build_relation(),
    )
    @settings(max_examples=100)
    def testXform(self, number, config, relation):
        """
        Confirm that option strip strips more than other options.
        """
        result = Strip(config).xform(number, relation)
        most = Strip(StripConfig(strip=True)).xform(number, relation)

        self.assertTrue(len(most) <= len(result))

        if config.strip and number != []:
            self.assertTrue(result[-1] != 0)
