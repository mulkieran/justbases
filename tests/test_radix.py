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
from justbases import Radix
from justbases import Rationals
from justbases import RoundingMethods

from ._utils import build_base
from ._utils import build_radix


class RadixTestCase(unittest.TestCase):
    """ Tests for radix. """

    @given(
       build_radix(16, 3),
       build_base(16)
    )
    @settings(max_examples=50)
    def testInBase(self, radix, base):
        """
        Test that roundtrip is identity modulo number of 0s in
        non repeating part.
        """
        result = radix.in_base(base).in_base(radix.base)
        assert result.sign == radix.sign and \
           result.integer_part == radix.integer_part and \
           result.repeating_part == radix.repeating_part and \
           result.base == radix.base

        length = len(result.non_repeating_part)
        assert result.non_repeating_part == radix.non_repeating_part[:length]
        assert all(x == 0 for x in radix.non_repeating_part[length:])

    def testExceptions(self):
        """
        Test exceptions.
        """
        with self.assertRaises(BasesError):
            Radix(0, [], [], [], 0)
        with self.assertRaises(BasesError):
            Radix(1, [], [], [2], 2)
        with self.assertRaises(BasesError):
            Radix(1, [], [-1], [1], 2)
        with self.assertRaises(BasesError):
            Radix(1, [-300], [1], [1], 2)
        with self.assertRaises(BasesError):
            Radix(True, [1], [0], [1], 2)
        with self.assertRaises(BasesError):
            Radix(1, [1], [0], [1], 2).in_base(0)

    @given(build_radix(36, 10))
    @settings(max_examples=10)
    def testStr(self, radix):
        """
        Check basic properties of __str__.
        """
        result = str(radix)
        assert result.startswith("-") == (radix.sign == -1)
        assert (result[-1] == ")") == (radix.repeating_part != [])

    @given(build_radix(1024, 10))
    @settings(max_examples=10)
    def testRepr(self, radix):
        """
        Make sure that result is evalable.
        """
        assert eval(repr(radix)) == radix # pylint: disable=eval-used

    def testOptions(self):
        """
        Skip validation and canonicalization.
        """
        self.assertIsNotNone(Radix(-1, [], [], [], 4, False, False))

    def testEquality(self):
        """
        Test == operator.
        """
        self.assertEqual(
           Radix(1, [1], [], [], 2),
           Radix(1, [1], [], [], 2),
        )

    def testInEquality(self):
        """
        Test != operator.
        """
        self.assertNotEqual(
           Radix(0, [], [], [], 3),
           Radix(0, [], [], [], 2),
        )

    def testOperatorExceptions(self):
        """
        Test that comparsion operators yield exceptions.
        """
        radix1 = Radix(0, [], [], [], 3)
        radix2 = Radix(0, [], [], [], 2)
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

    def testCarryOnRepeatingPart(self):
        """
        Carry from non_repeating_part to integer_part and then out.
        """
        assert Radix(1, [3], [3], [3], 4) == Radix(1, [1, 0], [], [], 4)

    def testRepeatingRepeatPart(self):
        """
        Repeat part is made up of repeating parts.
        """
        radix = Radix(1, [], [], [1, 1], 4)
        self.assertEqual(radix.repeating_part, [1])
        radix = Radix(1, [], [], [1, 1, 2], 4)
        self.assertEqual(radix.repeating_part, [1, 1, 2])
        radix = Radix(1, [], [], [1, 2, 1, 2, 1, 2], 4)
        self.assertEqual(radix.repeating_part, [1, 2])
        radix = Radix(1, [], [3, 1, 2, 1, 2], [1, 2], 4)
        self.assertEqual(radix.non_repeating_part, [3])
        self.assertEqual(radix.repeating_part, [1, 2])
        radix = Radix(1, [], [3, 2, 1, 2, 1, 2], [1, 2], 4)
        self.assertEqual(radix.non_repeating_part, [3])
        self.assertEqual(radix.repeating_part, [2, 1])
        radix = Radix(1, [], [3, 3, 2, 3, 1, 2, 3, 1, 2, 3], [1, 2, 3], 4)
        self.assertEqual(radix.non_repeating_part, [3, 3])
        self.assertEqual(radix.repeating_part, [2, 3, 1])


class RoundingTestCase(unittest.TestCase):
    """ Tests for rounding Radixes. """

    @given(
       build_radix(16, 10),
       strategies.integers(min_value=0, max_value=64),
       strategies.sampled_from(RoundingMethods.METHODS())
    )
    @settings(max_examples=50)
    def testRoundFraction(self, radix, precision, method):
        """
        Test that rounding yields the correct number of digits.

        Test that rounded values are in a good range.
        """
        value = radix.as_rational()
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
       build_radix(16, 10),
       strategies.integers(min_value=0, max_value=64)
    )
    @settings(max_examples=50)
    def testRoundRelation(self, radix, precision):
        """
        Test that all results have the correct relation.
        """
        results = dict(
           (method, radix.rounded(precision, method)[0]) for \
              method in RoundingMethods.METHODS()
        )

        for _, result in results.items():
            assert len(result.non_repeating_part) == precision

        if radix.sign in (0, 1):
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
       build_radix(64, 5),
       strategies.sampled_from(RoundingMethods.METHODS())
    )
    @settings(max_examples=50)
    def testAsInt(self, radix, method):
        """
        Test equivalence with two paths.
        """
        result1 = Rationals.round_to_int(radix.as_rational(), method)
        result2 = radix.as_int(method)
        assert result1 == result2

    def testExceptions(self):
        """
        Test exception.
        """
        with self.assertRaises(BasesError):
            Radix(0, [], [], [], 2).rounded(
               -1,
               RoundingMethods.ROUND_DOWN
            )
        with self.assertRaises(BasesError):
            Radix(0, [], [], [], 2).rounded(
               0,
               None
            )
