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

import six

from hypothesis import given
from hypothesis import settings
from hypothesis import strategies

from justbases import BasesError
from justbases import Radix
from justbases import Rationals
from justbases import Rounding
from justbases import RoundingMethods


class RationalsTestCase(unittest.TestCase):
    """ Tests for rationals. """

    @given(
       strategies.fractions().map(lambda x: x.limit_denominator(100)),
       strategies.integers(min_value=2)
    )
    @settings(max_examples=50)
    def testConvert(self, value, base):
        """
        Test that conversion from ``base`` to ``base`` is identity.
        """
        (radix, _) = Rationals.convert_from_rational(value, base)
        result = Rationals.convert(radix, base)
        assert radix == result

    @given(
       strategies.fractions().map(lambda x: x.limit_denominator(100)),
       strategies.integers(min_value=2)
    )
    @settings(max_examples=50)
    def testInverses(self, value, to_base):
        """
        Test that functions are inverses of each other.
        """
        (result, relation) = Rationals.convert_from_rational(value, to_base)
        assert result.positive or value < 0
        assert relation == 0
        assert Rationals.convert_to_rational(result) == value

    @given(
       strategies.fractions().map(lambda x: x.limit_denominator(100)),
       strategies.integers(min_value=2, max_value=64),
       strategies.integers(min_value=0, max_value=64),
       strategies.sampled_from(RoundingMethods.METHODS())
    )
    @settings(max_examples=500)
    def testRoundingConversion(self, value, base, precision, method):
        """
        Test that converting and then rounding is the same as converting
        with rounding.
        """
        (rounded, rel) = \
           Rationals.convert_from_rational(value, base, precision, method)
        (unrounded, urel) = Rationals.convert_from_rational(value, base)

        assert urel == 0

        (frounded, frel) = \
           Rounding.roundFractional(unrounded, precision, method)

        assert frounded == rounded
        assert rel == frel

        rounded_value = Rationals.convert_to_rational(rounded)

        if rounded_value > value:
            assert rel == 1
        elif rounded_value < value:
            assert rel == -1
        else:
            assert rel == 0

    def testExceptions(self):
        """
        Test exceptions.
        """
        with self.assertRaises(BasesError):
            Rationals.convert_from_rational(Fraction(1, 2), 0)
        with self.assertRaises(BasesError):
            Rationals.convert_from_rational(Fraction(1, 2), 2, -1)
        with self.assertRaises(BasesError):
            Rationals.convert(Radix(True, [], [], [], 2), 0)

    @given(
       strategies.fractions(),
       strategies.sampled_from(RoundingMethods.METHODS())
    )
    @settings(max_examples=50)
    def testRounding(self, value, method):
        """
        Test rounding to int.
        """
        result = Rationals.round_to_int(value, method)
        self.assertIsInstance(result, six.integer_types)

        (lower, upper) = (result - 1, result + 1)
        self.assertTrue(
           (lower <= value and value <= result) or \
           (result <= value and value <= upper)
        )

    @given(strategies.integers(min_value=1, max_value=9))
    @settings(max_examples=20)
    def testRoundingPrecise(self, numerator):
        """
        Test with predicted value.
        """
        value = Fraction(numerator, 10)
        self.assertEqual(
           Rationals.round_to_int(value, RoundingMethods.ROUND_DOWN),
           0
        )
        self.assertEqual(
           Rationals.round_to_int(-value, RoundingMethods.ROUND_DOWN),
           -1
        )
        self.assertEqual(
           Rationals.round_to_int(value, RoundingMethods.ROUND_UP),
           1
        )
        self.assertEqual(
           Rationals.round_to_int(-value, RoundingMethods.ROUND_UP),
           0
        )
        self.assertEqual(
           Rationals.round_to_int(value, RoundingMethods.ROUND_TO_ZERO),
           0
        )
        self.assertEqual(
           Rationals.round_to_int(-value, RoundingMethods.ROUND_TO_ZERO),
           0
        )

        result = Rationals.round_to_int(value, RoundingMethods.ROUND_HALF_UP)
        if numerator < 5:
            self.assertEqual(result, 0)
        else:
            self.assertEqual(result, 1)

        result = Rationals.round_to_int(-value, RoundingMethods.ROUND_HALF_UP)
        if numerator <= 5:
            self.assertEqual(result, 0)
        else:
            self.assertEqual(result, -1)

        result = Rationals.round_to_int(value, RoundingMethods.ROUND_HALF_DOWN)
        if numerator > 5:
            self.assertEqual(result, 1)
        else:
            self.assertEqual(result, 0)

        result = Rationals.round_to_int(-value, RoundingMethods.ROUND_HALF_DOWN)
        if numerator >= 5:
            self.assertEqual(result, -1)
        else:
            self.assertEqual(result, 0)

        result = Rationals.round_to_int(value, RoundingMethods.ROUND_HALF_ZERO)
        if numerator > 5:
            self.assertEqual(result, 1)
        else:
            self.assertEqual(result, 0)

        result = Rationals.round_to_int(-value, RoundingMethods.ROUND_HALF_ZERO)
        if numerator > 5:
            self.assertEqual(result, -1)
        else:
            self.assertEqual(result, 0)

    def testRoundingExceptions(self):
        """
        Test exceptions.
        """
        # pylint: disable=pointless-statement
        with self.assertRaises(BasesError):
            Rationals.round_to_int(Fraction(1, 2), None)
