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
from hypothesis import settings
from hypothesis import strategies

from justbases import BasesError
from justbases import Radices
from justbases import Radix
from justbases import Rationals
from justbases import RoundingMethods


class RadixTestCase(unittest.TestCase):
    """ Tests for radix. """

    @given(
       strategies.fractions().map(lambda x: x.limit_denominator(100)),
       strategies.integers(min_value=2),
       strategies.integers(min_value=2)
    )
    @settings(max_examples=50)
    def testInBase(self, value, base1, base2):
        """
        Test that roundtrip is identity.
        """
        (radix, _) = Radices.from_rational(value, base1)
        radix2 = radix.in_base(base2)
        radix3 = radix2.in_base(base1)
        assert radix == radix3

    @given(
       strategies.fractions().map(lambda x: x.limit_denominator(100)),
       strategies.integers(min_value=2)
    )
    def testInBase2(self, value, base):
        """
        Test conversion to current base.
        """
        (radix, _) = Radices.from_rational(value, base)
        result = radix.in_base(base)
        assert radix == result

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
        with self.assertRaises(BasesError):
            Radix(True, [1], [0], [1], 2).in_base(0)

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

    def testEquality(self):
        """
        Test == operator.
        """
        self.assertEqual(
           Radix(True, [1], [], [], 2),
           Radix(True, [1], [], [], 2),
        )

    def testInEquality(self):
        """
        Test != operator.
        """
        self.assertNotEqual(
           Radix(False, [], [], [], 3),
           Radix(True, [], [], [], 2),
        )

    def testOperatorExceptions(self):
        """
        Test that comparsion operators yield exceptions.
        """
        radix1 = Radix(False, [], [], [], 3)
        radix2 = Radix(False, [], [], [], 2)
        # pylint: disable=pointless-statement
        with self.assertRaises(BasesError):
            radix1 > radix2
        with self.assertRaises(BasesError):
            radix1 < radix2
        with self.assertRaises(BasesError):
            radix1 <= radix2
        with self.assertRaises(BasesError):
            radix1 >= radix2
        with self.assertRaises(BasesError):
            radix1 >= 1
        with self.assertRaises(BasesError):
            radix1 == 1
        with self.assertRaises(BasesError):
            radix1 != 1

    def testRepeatingRepeatPart(self):
        """
        Repeat part is made up of repeating parts.
        """
        radix = Radix(True, [], [], [1, 1], 4)
        self.assertEqual(radix.repeating_part, [1])
        radix = Radix(True, [], [], [1, 1, 2], 4)
        self.assertEqual(radix.repeating_part, [1, 1, 2])
        radix = Radix(True, [], [], [1, 2, 1, 2, 1, 2], 4)
        self.assertEqual(radix.repeating_part, [1, 2])
        radix = Radix(True, [], [3, 1, 2, 1, 2], [1, 2], 4)
        self.assertEqual(radix.non_repeating_part, [3])
        self.assertEqual(radix.repeating_part, [1, 2])
        radix = Radix(True, [], [3, 2, 1, 2, 1, 2], [1, 2], 4)
        self.assertEqual(radix.non_repeating_part, [3])
        self.assertEqual(radix.repeating_part, [2, 1])
        radix = Radix(True, [], [3, 3, 2, 3, 1, 2, 3, 1, 2, 3], [1, 2, 3], 4)
        self.assertEqual(radix.non_repeating_part, [3, 3])
        self.assertEqual(radix.repeating_part, [2, 3, 1])


class RoundingTestCase(unittest.TestCase):
    """ Tests for rounding Radixes. """

    @given(
       strategies.fractions().map(lambda x: x.limit_denominator(100)),
       strategies.integers(min_value=2, max_value=64),
       strategies.integers(min_value=0, max_value=64),
       strategies.sampled_from(RoundingMethods.METHODS())
    )
    @settings(max_examples=500)
    def testRoundFraction(self, value, base, precision, method):
        """
        Test that rounding yields the correct number of digits.

        Test that rounded values are in a good range.
        """
        (radix, _) = Radices.from_rational(value, base)
        (result, relation) = radix.rounded(precision, method)
        assert len(result.non_repeating_part) == precision

        ulp = Fraction(1, radix.base ** precision)
        rational_result = result.as_rational()
        assert value - ulp <= rational_result
        assert value + ulp >= rational_result

        if rational_result > value:
            assert relation == 1
        elif rational_result < value:
            assert relation == -1
        else:
            assert relation == 0

    @given(
       strategies.fractions().map(lambda x: x.limit_denominator(100)),
       strategies.integers(min_value=2, max_value=64),
       strategies.integers(min_value=0, max_value=64)
    )
    @settings(max_examples=50)
    def testRoundRelation(self, value, base, precision):
        """
        Test that all results have the correct relation.
        """
        (radix, _) = Radices.from_rational(value, base)


        results = dict(
           (method, radix.rounded(precision, method)[0]) for \
              method in RoundingMethods.METHODS()
        )

        if radix.positive is True:
            assert results[RoundingMethods.ROUND_DOWN] == \
               results[RoundingMethods.ROUND_TO_ZERO]
            assert results[RoundingMethods.ROUND_HALF_DOWN] == \
               results[RoundingMethods.ROUND_HALF_ZERO]
        else:
            assert results[RoundingMethods.ROUND_UP] == \
               results[RoundingMethods.ROUND_TO_ZERO]
            assert results[RoundingMethods.ROUND_HALF_UP] == \
               results[RoundingMethods.ROUND_HALF_ZERO]

        order = [
           RoundingMethods.ROUND_UP,
           RoundingMethods.ROUND_HALF_UP,
           RoundingMethods.ROUND_HALF_DOWN,
           RoundingMethods.ROUND_DOWN
        ]
        for index in range(len(order) - 1):
            assert results[order[index]].as_rational() >= \
               results[order[index + 1]].as_rational()

    @given(
       strategies.fractions().map(lambda x: x.limit_denominator(100)),
       strategies.integers(min_value=2, max_value=64),
       strategies.sampled_from(RoundingMethods.METHODS())
    )
    @settings(max_examples=50)
    def testAsInt(self, value, base, method):
        """
        Test equivalence with two paths.
        """
        (radix, _) = Radices.from_rational(value, base)
        result1 = Rationals.round_to_int(radix.as_rational(), method)
        (result2, _) = radix.as_int(method)
        assert result1 == result2

    def testOverflow(self):
        """
        Ensure that rounding causes overflow.
        """
        radix = Radix(True, [], [], [1], 2)
        (result, relation) = radix.rounded(3, RoundingMethods.ROUND_UP)
        assert relation == 1
        assert result.integer_part == [1]
        assert result.non_repeating_part == [0, 0, 0]
        assert result.repeating_part == []

    def testMiddles(self):
        """
        Ensure that there is no tie breaker.
        """
        radix = Radix(True, [], [1, 1, 1, 1], [], 2)
        (result, relation) = radix.rounded(3, RoundingMethods.ROUND_HALF_UP)
        assert relation == 1
        assert result.integer_part == [1]
        assert result.non_repeating_part == [0, 0, 0]
        assert result.repeating_part == []

    def testLeadingZeros(self):
        """
        Require conversion, but do not carry out of repeating_part.
        """
        radix = Radix(True, [], [0, 0, 1, 1], [], 2)
        (result, relation) = radix.rounded(3, RoundingMethods.ROUND_UP)
        assert relation == 1
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
        (result, relation) = radix.rounded(3, RoundingMethods.ROUND_UP)
        assert relation == 1
        assert result.integer_part == []
        assert result.non_repeating_part == [1, 1, 0]
        assert result.repeating_part == []

    def testExceptions(self):
        """
        Test exception.
        """
        with self.assertRaises(BasesError):
            Radix(True, [], [], [], 2).rounded(
               -1,
               RoundingMethods.ROUND_DOWN
            )
        with self.assertRaises(BasesError):
            Radix(True, [], [], [], 2).rounded(
               0,
               None
            )

    def testFiveEighths(self):
        """
        Test 5/8 in base 3.
        """
        value = Fraction(5, 8)
        (radix, _) = Radices.from_rational(value, 3)
        (rounded, relation) = radix.rounded(0, RoundingMethods.ROUND_HALF_UP)

        assert relation == 1
        assert rounded.as_rational() == 1

    def testOneHalf(self):
        """
        Test 1/2 in base 3.
        """
        value = Fraction(1, 2)
        (radix, _) = Radices.from_rational(value, 3)
        (rounded, relation) = radix.rounded(0, RoundingMethods.ROUND_HALF_UP)

        assert relation == 1
        assert rounded.as_rational() == 1

        (rounded, relation) = radix.rounded(0, RoundingMethods.ROUND_HALF_DOWN)

        assert relation == -1
        assert rounded.as_rational() == 0
