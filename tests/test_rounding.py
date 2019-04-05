# Copyright (C) 2015 Anne Mulhern
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions of
# the GNU General Public License v.2, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY expressed or implied, including the implied warranties of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.  You should have received a copy of the
# GNU General Public License along with this program; if not, write to the
# Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# Anne Mulhern <mulhern@cs.wisc.edu>

""" Test for integer conversions. """

from __future__ import absolute_import

import unittest

from fractions import Fraction

from hypothesis import given
from hypothesis import strategies

from justbases import BasesError
from justbases import RoundingMethods

from justbases._rounding import Rounding


class RoundingTestCase(unittest.TestCase):
    """ Tests for rounding methods. """

    def testExceptions(self):
        """
        Test exceptions.
        """
        with self.assertRaises(BasesError):
            Rounding.rounding_up(0, Fraction(1, 3), RoundingMethods.ROUND_DOWN)

    @given(
       strategies.one_of(
          strategies.fractions().filter(lambda x: x > 0 and x < 1),
          strategies.just(Fraction(1, 2))
       ),
       strategies.one_of(
          strategies.sampled_from(RoundingMethods.METHODS()),
          strategies.sampled_from(RoundingMethods.CONDITIONAL_METHODS())
       )
    )
    def testRoundingUp(self, value, method):
        """
        Verify results.
        """
        middle = Fraction(1, 2)
        result = Rounding.rounding_up(value, middle, method)
        if method is RoundingMethods.ROUND_UP:
            self.assertTrue(result)
            return

        if method is RoundingMethods.ROUND_DOWN:
            self.assertFalse(result)
            return

        if method is RoundingMethods.ROUND_TO_ZERO:
            self.assertFalse(result)
            return

        if method is RoundingMethods.ROUND_HALF_ZERO:
            self.assertEqual(result, value > middle)
            return

        if method is RoundingMethods.ROUND_HALF_DOWN:
            self.assertEqual(result, value > middle)
            return

        if method is RoundingMethods.ROUND_HALF_UP:
            self.assertEqual(result, value >= middle)
            return
