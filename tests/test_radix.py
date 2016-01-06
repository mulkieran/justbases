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

""" Test for rational conversions. """

from __future__ import absolute_import

from fractions import Fraction

import unittest

from hypothesis import given
from hypothesis import strategies
from hypothesis import Settings

from justbases import BasesError
from justbases import Radix
from justbases import Rationals
from justbases import Rounding
from justbases import RoundingMethods


class RadixTestCase(unittest.TestCase):
    """ Tests for radix. """

    def testExceptions(self):
        """
        Test exceptions.
        """
        with self.assertRaises(BasesError):
            Radix(True, [], [], [], 0)
        with self.assertRaises(BasesError):
            Radix(True, [], [], [2], 2)
        with self.assertRaises(BasesError):
            Radix(True, [], [-1], [1], 2)
        with self.assertRaises(BasesError):
            Radix(True, [-300], [1], [1], 2)

    def testStr(self):
        """
        Make sure that __str__ executes.
        """
        assert str(Radix(True, [1], [2], [3], 4)) != ''

    def testOptions(self):
        """
        Skip validation and canonicalization.
        """
        self.assertIsNotNone(Radix(False, [], [], [], 4, False, False))


class RoundingTestCase(unittest.TestCase):
    """ Tests for rounding Radixes. """

    @given(
       strategies.fractions(),
       strategies.integers(min_value=2),
       strategies.integers(min_value=0),
       strategies.sampled_from(RoundingMethods.METHODS()),
       settings=Settings(max_examples=50)
    )
    def testRoundFraction(self, value, base, precision, method):
        """
        Test that rounding yields the correct number of digits.

        Test that rounded values are in a good range.
        """
        radix = Rationals.convert_from_rational(value, base)
        result = Rounding.roundFractional(radix, precision, method)
        assert len(result.non_repeating_part) == precision

        ulp = Fraction(1, radix.base ** precision)
        rational_result = Rationals.convert_to_rational(result)
        assert value - ulp <= rational_result
        assert value + ulp >= rational_result

    @given(
       strategies.fractions(),
       strategies.integers(min_value=2),
       strategies.integers(min_value=0),
       settings=Settings(max_examples=50)
    )
    def testExpandFraction(self, value, base, precision):
        """
        Test that the expanded fraction has the correct length.

        Test some values in the expanded fraction.
        """
        # pylint: disable=protected-access
        radix = Rationals.convert_from_rational(value, base)
        result = Rounding._expandFraction(radix, precision)
        assert len(result) == precision

        start = radix.non_repeating_part[:precision]
        assert start == result[:len(start)]

        nr_length = len(radix.non_repeating_part)
        assert precision <= nr_length or \
           (radix.repeating_part == [] and result[nr_length] == 0) or \
           (radix.repeating_part != [] and \
              result[nr_length] == radix.repeating_part[0])

    def testOverflow(self):
        """
        Ensure that rounding causes overflow.
        """
        radix = Radix(True, [], [], [1], 2)
        result = Rounding.roundFractional(
           radix,
           3,
           RoundingMethods.ROUND_UP
        )
        assert result.integer_part == [1]
        assert result.non_repeating_part == [0, 0, 0]
        assert result.repeating_part == []

    def testMiddles(self):
        """
        Ensure that there is no tie breaker.
        """
        radix = Radix(True, [], [1, 1, 1, 1], [], 2)
        result = Rounding.roundFractional(
           radix,
           3,
           RoundingMethods.ROUND_HALF_UP
        )
        assert result.integer_part == [1]
        assert result.non_repeating_part == [0, 0, 0]
        assert result.repeating_part == []

    def testLeadingZeros(self):
        """
        Require conversion, but do not carry out of repeating_part.
        """
        radix = Radix(True, [], [0, 0, 1, 1], [], 2)
        result = Rounding.roundFractional(
           radix,
           3,
           RoundingMethods.ROUND_UP
        )
        assert result.integer_part == []
        assert result.non_repeating_part == [0, 1, 0]
        assert result.repeating_part == []

    def testExactLength(self):
        """
        Require conversion, but do not carry out of repeating_part.
        Ensure that the intermediate result is exactly the required
        precision.
        """
        radix = Radix(True, [], [1, 0, 1, 1], [], 2)
        result = Rounding.roundFractional(
           radix,
           3,
           RoundingMethods.ROUND_UP
        )
        assert result.integer_part == []
        assert result.non_repeating_part == [1, 1, 0]
        assert result.repeating_part == []

    def testAdd(self):
        """
        Test overflow with addition.
        """
        # pylint: disable=protected-access
        (carry, res) = Rounding._add([1], 2, 1)
        assert carry == 1 and res == [0]

    def testExceptions(self):
        """
        Test exception.
        """
        with self.assertRaises(BasesError):
            Rounding.roundFractional(
               Radix(True, [], [], [], 2),
               -1,
               RoundingMethods.ROUND_DOWN
            )
        # pylint: disable=protected-access
        with self.assertRaises(BasesError):
            Rounding._increment_unconditional(True, None)
        with self.assertRaises(BasesError):
            Rounding._increment_conditional(True, None, Fraction(1, 2), 0)
