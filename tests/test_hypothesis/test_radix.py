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
from justbases import Rationals, RoundingMethods

# isort considers this third party, but it is not
from tests.test_hypothesis._utils import build_base, build_radix  # isort:skip

if sys.gettrace() is not None:
    settings.load_profile("tracing")


class RadixTestCase(unittest.TestCase):
    """Tests for radix."""

    @given(build_radix(16, 3), build_base(16))
    @settings(max_examples=50, deadline=None)
    def test_in_base(self, radix, base):
        """
        Test that roundtrip is identity modulo number of 0s in
        non repeating part.
        """
        result = radix.in_base(base).in_base(radix.base)
        self.assertEqual(result.sign, radix.sign)
        self.assertEqual(result.integer_part, radix.integer_part)
        self.assertEqual(result.repeating_part, radix.repeating_part)
        self.assertEqual(result.base, radix.base)

        length = len(result.non_repeating_part)
        self.assertEqual(result.non_repeating_part, radix.non_repeating_part[:length])
        self.assertTrue(all(x == 0 for x in radix.non_repeating_part[length:]))

    @given(build_radix(36, 10))
    @settings(max_examples=10)
    def test_str(self, radix):
        """
        Check basic properties of __str__.
        """
        result = str(radix)
        self.assertEqual(result.startswith("-"), (radix.sign == -1))

    @given(build_radix(1024, 10))
    @settings(max_examples=10)
    def test_repr(self, radix):
        """
        Make sure that result is evalable.
        """
        # pylint: disable=import-outside-toplevel, unused-import
        # isort: LOCAL
        from justbases import Radix

        self.assertEqual(eval(repr(radix)), radix)  # pylint: disable=eval-used


class RoundingTestCase(unittest.TestCase):
    """Tests for rounding Radixes."""

    @given(
        build_radix(16, 10),
        strategies.integers(min_value=0, max_value=64),
        strategies.sampled_from(RoundingMethods.METHODS()),
    )
    @settings(max_examples=50)
    def test_round_fraction(self, radix, precision, method):
        """
        Test that rounding yields the correct number of digits.

        Test that rounded values are in a good range.
        """
        value = radix.as_rational()
        (result, relation) = radix.rounded(precision, method)
        self.assertEqual(len(result.non_repeating_part), precision)

        ulp = Fraction(1, radix.base**precision)
        rational_result = result.as_rational()
        self.assertLessEqual(value - ulp, rational_result)
        self.assertGreaterEqual(value + ulp, rational_result)

        if rational_result > value:
            self.assertEqual(relation, 1)
        elif rational_result < value:
            self.assertEqual(relation, -1)
        else:
            self.assertEqual(relation, 0)

    @given(build_radix(16, 10), strategies.integers(min_value=0, max_value=64))
    @settings(max_examples=50)
    def test_round_relation(self, radix, precision):
        """
        Test that all results have the correct relation.
        """
        results = dict(
            (method, radix.rounded(precision, method)[0])
            for method in RoundingMethods.METHODS()
        )

        for _, result in results.items():
            self.assertEqual(len(result.non_repeating_part), precision)

        if radix.sign in (0, 1):
            self.assertEqual(
                results[RoundingMethods.ROUND_DOWN],
                results[RoundingMethods.ROUND_TO_ZERO],
            )
            self.assertEqual(
                results[RoundingMethods.ROUND_HALF_DOWN],
                results[RoundingMethods.ROUND_HALF_ZERO],
            )
        else:
            self.assertEqual(
                results[RoundingMethods.ROUND_UP],
                results[RoundingMethods.ROUND_TO_ZERO],
            )
            self.assertEqual(
                results[RoundingMethods.ROUND_HALF_UP],
                results[RoundingMethods.ROUND_HALF_ZERO],
            )

        order = [
            RoundingMethods.ROUND_UP,
            RoundingMethods.ROUND_HALF_UP,
            RoundingMethods.ROUND_HALF_DOWN,
            RoundingMethods.ROUND_DOWN,
        ]
        for index in range(len(order) - 1):
            self.assertGreaterEqual(
                results[order[index]].as_rational(),
                results[order[index + 1]].as_rational(),
            )

    @given(build_radix(64, 5), strategies.sampled_from(RoundingMethods.METHODS()))
    @settings(max_examples=50)
    def test_as_int(self, radix, method):
        """
        Test equivalence with two paths.
        """
        result1 = Rationals.round_to_int(radix.as_rational(), method)
        result2 = radix.as_int(method)
        self.assertEqual(result1, result2)
