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

""" Test manipulations to show approximation. """

import unittest

from justbases._approx_display import ApproxPrefix

from hypothesis import given
from hypothesis import settings
from hypothesis import strategies

class TestApproxPrefix(unittest.TestCase):
    """
    Test calculation of approximation prefix.
    """

    @given(
       strategies.fractions().filter(lambda x: x > -1 and x < 1),
       strategies.lists(
          elements=strategies.fractions().filter(lambda x: x > 0 and x < 1),
          max_size=3
       ).map(sorted)
    )
    @settings(max_examples=50)
    def testXformValue(self, relation, limits):
        """
        Make sure xform() yields the correct sort of characters.
        """
        result = ApproxPrefix(limits).xform(relation, '')
        if relation == 0:
            assert result == ''
        elif relation < 0:
            assert result.startswith('>')
        elif relation > 0:
            assert result.startswith('<')

    @given(
       strategies.fractions().filter(lambda x: x > -1 and x < 1),
       strategies.lists(
          elements=strategies.fractions().filter(lambda x: x > 0 and x < 1),
          max_size=3
       ).map(sorted)
    )
    @settings(max_examples=50)
    def testXformMagnitude(self, relation, limits):
        """
        Make sure xform() yields the correct amount of characters.
        """
        result = ApproxPrefix(limits).xform(relation, '')
        if relation == 0:
            assert result == ''
        else:
            num_chars = len(result) - 1
            abs_relation = abs(relation)
            assert (num_chars == len(limits) + 1 and \
               (limits == [] or abs_relation >= limits[-1])) or \
               abs_relation < limits[num_chars - 1]
