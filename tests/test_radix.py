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

""" Test for rational conversions. """

# isort: STDLIB
import unittest
from fractions import Fraction
from os import sys

# isort: THIRDPARTY
from hypothesis import given, settings, strategies

# isort: LOCAL
from justbases import BasesError, Radix, Rationals, RoundingMethods

# isort considers this third party, but it is not
from tests._utils import build_base, build_radix  # isort:skip

if sys.gettrace() is not None:
    settings.load_profile("tracing")


class RadixTestCase(unittest.TestCase):
    """ Tests for radix. """

    @given(build_radix(16, 3), build_base(16))
    @settings(max_examples=50, deadline=None)
    def testInBase(self, radix, base):
        """
        Test that roundtrip is identity modulo number of 0s in
        non repeating part.
        """
        result = radix.in_base(base).in_base(radix.base)
        assert (
            result.sign == radix.sign
            and result.integer_part == radix.integer_part
            and result.repeating_part == radix.repeating_part
            and result.base == radix.base
        )

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

    @given(build_radix(1024, 10))
    @settings(max_examples=10)
    def testRepr(self, radix):
        """
        Make sure that result is evalable.
        """
        assert eval(repr(radix)) == radix  # pylint: disable=eval-used

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
            Radix(1, [1], [], [], 2), Radix(1, [1], [], [], 2),
        )

    def testInEquality(self):
        """
        Test != operator.
        """
        self.assertNotEqual(
            Radix(0, [], [], [], 3), Radix(0, [], [], [], 2),
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
        strategies.sampled_from(RoundingMethods.METHODS()),
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

    @given(build_radix(16, 10), strategies.integers(min_value=0, max_value=64))
    @settings(max_examples=50)
    def testRoundRelation(self, radix, precision):
        """
        Test that all results have the correct relation.
        """
        results = dict(
            (method, radix.rounded(precision, method)[0])
            for method in RoundingMethods.METHODS()
        )

        for _, result in results.items():
            assert len(result.non_repeating_part) == precision

        if radix.sign in (0, 1):
            assert (
                results[RoundingMethods.ROUND_DOWN]
                == results[RoundingMethods.ROUND_TO_ZERO]
            )
            assert (
                results[RoundingMethods.ROUND_HALF_DOWN]
                == results[RoundingMethods.ROUND_HALF_ZERO]
            )
        else:
            assert (
                results[RoundingMethods.ROUND_UP]
                == results[RoundingMethods.ROUND_TO_ZERO]
            )
            assert (
                results[RoundingMethods.ROUND_HALF_UP]
                == results[RoundingMethods.ROUND_HALF_ZERO]
            )

        order = [
            RoundingMethods.ROUND_UP,
            RoundingMethods.ROUND_HALF_UP,
            RoundingMethods.ROUND_HALF_DOWN,
            RoundingMethods.ROUND_DOWN,
        ]
        for index in range(len(order) - 1):
            assert (
                results[order[index]].as_rational()
                >= results[order[index + 1]].as_rational()
            )

    @given(build_radix(64, 5), strategies.sampled_from(RoundingMethods.METHODS()))
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
            Radix(0, [], [], [], 2).rounded(-1, RoundingMethods.ROUND_DOWN)
        with self.assertRaises(BasesError):
            Radix(0, [], [], [], 2).rounded(0, None)
