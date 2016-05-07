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
from justbases import DigitsConfig
from justbases import DisplayConfig
from justbases import Radix
from justbases import StripConfig

from justbases._display import Digits
from justbases._display import Number
from justbases._display import String
from justbases._display import Strip

from hypothesis import given
from hypothesis import settings
from hypothesis import strategies


class TestString(unittest.TestCase):
    """
    Test display of Radix given display configuration.
    """

    @given(
       strategies.integers(min_value=2, max_value=1024).flatmap(
          lambda n: strategies.builds(
             Radix,
             strategies.integers(min_value=1, max_value=1),
             strategies.lists(
                elements=strategies.integers(min_value=0, max_value=n-1),
                min_size=0,
                max_size=10
             ),
             strategies.lists(
                elements=strategies.integers(min_value=0, max_value=n-1),
                min_size=0,
                max_size=10
             ),
             strategies.lists(
                elements=strategies.integers(min_value=0, max_value=n-1),
                min_size=0,
                max_size=10
             ),
             strategies.just(n)
          )
       ),
       strategies.builds(
          DisplayConfig,
          show_approx_str=strategies.booleans(),
          show_base=strategies.booleans(),
          digits_config=strategies.just(DigitsConfig(use_letters=False)),
          strip_config=strategies.just(StripConfig())
       ),
       strategies.integers(min_value=-1, max_value=1)
    )
    @settings(max_examples=100)
    def testFormat(self, radix, display, relation):
        """
        Verify that a xformed string with a repeating part shows that part.
        """
        result = String.xform(radix, display, relation)
        assert (radix.repeating_part != []) == (result[-1] == ")")


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
            Digits.xform(
               [],
               BasesConfig.DISPLAY_CONFIG.digits_config,
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
       strategies.builds(
          DisplayConfig,
          show_approx_str=strategies.booleans(),
          show_base=strategies.booleans(),
          digits_config=strategies.just(DigitsConfig(use_letters=False)),
          strip_config=strategies.just(StripConfig())
       ),
       strategies.integers(min_value=2, max_value=16),
       strategies.booleans()
    )
    @settings(max_examples=100)
    def testXform(
       self,
       integer_part,
       non_repeating_part,
       repeating_part,
       config,
       base,
       positive
    ):
        """
        Test xform.
        """
        # pylint: disable=too-many-arguments

        result = Number.xform(
           integer_part,
           non_repeating_part,
           repeating_part,
           config,
           base,
           positive
        )
        if config.show_base and base == 16 and positive:
            self.assertTrue(result.startswith('0x'))
        if config.show_base and base == 8 and positive:
            self.assertTrue(result.startswith('0'))


class TestStrip(unittest.TestCase):
    """
    Test Strip.
    """

    @given(
       strategies.lists(
          elements=strategies.integers(min_value=0, max_value=10),
          max_size=10
       ),
       strategies.builds(
          StripConfig,
          strategies.booleans(),
          strategies.booleans(),
          strategies.booleans()
       ),
       strategies.integers(min_value=-1, max_value=1)
    )
    @settings(max_examples=100)
    def testXform(self, number, config, relation):
        """
        Test xform.
        """
        result = Strip.xform(number, config, relation)
        most = Strip.xform(number, StripConfig(strip=True), relation)

        self.assertTrue(len(most) <= len(result))
