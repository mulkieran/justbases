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
from justbases import Radices, Rationals, RoundingMethods

if sys.gettrace() is not None:
    settings.load_profile("tracing")


class RationalsTestCase(unittest.TestCase):
    """Tests for rationals."""

    @given(
        strategies.fractions().map(lambda x: x.limit_denominator(100)),
        strategies.integers(min_value=2),
    )
    @settings(max_examples=50)
    def test_inverses(self, value, to_base):
        """
        Test that functions are inverses of each other.
        """
        (result, relation) = Radices.from_rational(value, to_base)
        self.assertTrue(result.sign in (0, 1) or value < 0)
        self.assertEqual(relation, 0)
        self.assertEqual(result.as_rational(), value)

    @given(
        strategies.fractions().map(lambda x: x.limit_denominator(100)),
        strategies.integers(min_value=2, max_value=64),
        strategies.integers(min_value=0, max_value=64),
        strategies.sampled_from(RoundingMethods.METHODS()),
    )
    @settings(max_examples=500)
    def test_rounding_conversion(self, value, base, precision, method):
        """
        Test that converting and then rounding is the same as converting
        with rounding.
        """
        (rounded, rel) = Radices.from_rational(value, base, precision, method)
        (unrounded, urel) = Radices.from_rational(value, base)

        self.assertEqual(urel, 0)

        (frounded, frel) = unrounded.rounded(precision, method)

        self.assertEqual(frounded, rounded)
        self.assertEqual(rel, frel)

        rounded_value = rounded.as_rational()

        if rounded_value > value:
            self.assertEqual(rel, 1)
        elif rounded_value < value:
            self.assertEqual(rel, -1)
        else:
            self.assertEqual(rel, 0)

    @given(strategies.fractions(), strategies.sampled_from(RoundingMethods.METHODS()))
    @settings(max_examples=50)
    def test_rounding(self, value, method):
        """
        Test rounding to int.
        """
        (result, _) = Rationals.round_to_int(value, method)
        self.assertIsInstance(result, int)

        (lower, upper) = (result - 1, result + 1)
        self.assertTrue((lower <= value <= result) or (result <= value <= upper))

    @given(strategies.integers(min_value=1, max_value=9))
    @settings(max_examples=20)
    def test_rounding_precise(self, numerator):
        """
        Test with predicted value.
        """
        # pylint: disable=too-many-statements
        value = Fraction(numerator, 10)
        (result, rel) = Rationals.round_to_int(value, RoundingMethods.ROUND_DOWN)
        self.assertEqual(result, 0)
        self.assertEqual(rel, -1)

        (result, rel) = Rationals.round_to_int(-value, RoundingMethods.ROUND_DOWN)
        self.assertEqual(result, -1)
        self.assertEqual(rel, -1)

        (result, rel) = Rationals.round_to_int(value, RoundingMethods.ROUND_UP)
        self.assertEqual(result, 1)
        self.assertEqual(rel, 1)

        (result, rel) = Rationals.round_to_int(-value, RoundingMethods.ROUND_UP)
        self.assertEqual(result, 0)
        self.assertEqual(rel, 1)

        (result, rel) = Rationals.round_to_int(value, RoundingMethods.ROUND_TO_ZERO)
        self.assertEqual(result, 0)
        self.assertEqual(rel, -1)

        (result, rel) = Rationals.round_to_int(-value, RoundingMethods.ROUND_TO_ZERO)
        self.assertEqual(result, 0)
        self.assertEqual(rel, 1)

        (result, rel) = Rationals.round_to_int(value, RoundingMethods.ROUND_HALF_UP)
        if numerator < 5:
            self.assertEqual(result, 0)
            self.assertEqual(rel, -1)
        else:
            self.assertEqual(result, 1)
            self.assertEqual(rel, 1)

        (result, rel) = Rationals.round_to_int(-value, RoundingMethods.ROUND_HALF_UP)
        if numerator <= 5:
            self.assertEqual(result, 0)
            self.assertEqual(rel, 1)
        else:
            self.assertEqual(result, -1)
            self.assertEqual(rel, -1)

        (result, rel) = Rationals.round_to_int(value, RoundingMethods.ROUND_HALF_DOWN)
        if numerator > 5:
            self.assertEqual(result, 1)
            self.assertEqual(rel, 1)
        else:
            self.assertEqual(result, 0)
            self.assertEqual(rel, -1)

        (result, rel) = Rationals.round_to_int(-value, RoundingMethods.ROUND_HALF_DOWN)
        if numerator >= 5:
            self.assertEqual(result, -1)
            self.assertEqual(rel, -1)
        else:
            self.assertEqual(result, 0)
            self.assertEqual(rel, 1)

        (result, rel) = Rationals.round_to_int(value, RoundingMethods.ROUND_HALF_ZERO)
        if numerator > 5:
            self.assertEqual(result, 1)
            self.assertEqual(rel, 1)
        else:
            self.assertEqual(result, 0)
            self.assertEqual(rel, -1)

        (result, rel) = Rationals.round_to_int(-value, RoundingMethods.ROUND_HALF_ZERO)
        if numerator > 5:
            self.assertEqual(result, -1)
            self.assertEqual(rel, -1)
        else:
            self.assertEqual(result, 0)
            self.assertEqual(rel, 1)
