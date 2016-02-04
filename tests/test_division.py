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

import fractions
import unittest

from hypothesis import example
from hypothesis import given
from hypothesis import settings
from hypothesis import strategies

from justbases import BasesError
from justbases import NatDivision
from justbases import Nats


class NatDivisionTestCase(unittest.TestCase):
    """ Tests for division. """

    @given(
       strategies.integers(min_value=1, max_value=2 ** 16),
       strategies.integers(min_value=0, max_value=2 ** 64),
       strategies.integers(min_value=3)
    )
    @settings(max_examples=50)
    @example(divisor=2**17, dividend=2, base=2)
    def testInverses(self, divisor, dividend, base):
        """
        Test that division and undivision are inverses.
        """
        frac = fractions.Fraction(dividend, divisor)
        divisor = Nats.convert_from_int(divisor, base)
        dividend = Nats.convert_from_int(dividend, base)
        (integer_part, non_repeating_part, repeating_part) = \
           NatDivision.division(divisor, dividend, base)
        (denominator, numerator) = NatDivision.undivision(
           integer_part,
           non_repeating_part,
           repeating_part,
           base
        )
        assert frac == fractions.Fraction(
           Nats.convert_to_int(numerator, base),
           Nats.convert_to_int(denominator, base)
        )

    def testExceptionsDivision(self):
        """
        Test division exceptions.
        """
        with self.assertRaises(BasesError):
            NatDivision.division([1], [1], -2)
        with self.assertRaises(BasesError):
            NatDivision.division([1], [-1], 3)
        with self.assertRaises(BasesError):
            NatDivision.division([-1], [1], 3)
        with self.assertRaises(BasesError):
            NatDivision.division([], [1], 3)
        with self.assertRaises(BasesError):
            NatDivision.division([0], [1], 3)
        with self.assertRaises(BasesError):
            NatDivision.division([2], [1], 3, -1)

    def testExceptionsUndivision(self):
        """
        Test undivision exceptions.
        """
        with self.assertRaises(BasesError):
            NatDivision.undivision([1], [1], [1], -2)
        with self.assertRaises(BasesError):
            NatDivision.undivision([1], [1], [-1], 2)
        with self.assertRaises(BasesError):
            NatDivision.undivision([1], [-1], [1], 2)
        with self.assertRaises(BasesError):
            NatDivision.undivision([-1], [1], [1], 2)
        with self.assertRaises(BasesError):
            NatDivision.undivision([2], [1], [1], 2)

    @given(
       strategies.integers(min_value=1, max_value=2 ** 16),
       strategies.integers(min_value=0, max_value=2 ** 64),
       strategies.integers(min_value=3),
       strategies.integers(min_value=0, max_value=32)
    )
    @settings(max_examples=50)
    def testTruncation(self, divisor, dividend, base, precision):
        """
        Test just truncating division result to some precision.

        Integer parts of truncated and non-truncated are always the same.

        The length of repeating and non-repeating is always less than the
        precision.

        If precision limit was reached before repeating portion was
        calculated, then the non-repeating portion has ``precision`` digits
        and is a prefix of non-repeating-part + repeating part when
        precision is not bounded.
        """
        divisor = Nats.convert_from_int(divisor, base)
        dividend = Nats.convert_from_int(dividend, base)
        (integer_part, non_repeating_part, repeating_part) = \
           NatDivision.division(divisor, dividend, base, precision)
        (integer_part_2, non_repeating_part_2, repeating_part_2) = \
           NatDivision.division(divisor, dividend, base, None)

        assert integer_part == integer_part_2
        assert len(repeating_part) + len(non_repeating_part) <= precision

        assert not(repeating_part_2 != [] and repeating_part == []) or \
           (len(non_repeating_part) == precision and \
            non_repeating_part == \
            (non_repeating_part_2 + repeating_part_2)[:precision])
