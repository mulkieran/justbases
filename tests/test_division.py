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

""" Test for integer conversions. """

from __future__ import absolute_import

import fractions
from os import environ
from os import sys
import unittest

from hypothesis import example
from hypothesis import given
from hypothesis import settings
from hypothesis import strategies

from justbases import BasesError
from justbases import NatDivision
from justbases import Nats
from justbases import RoundingMethods

from ._utils import build_nat
if sys.gettrace() is not None or environ.get('TRAVIS') is not None:
    settings.load_profile("tracing")


_DIVISION_STRATEGY = strategies.integers(min_value=2, max_value=17).flatmap(
   lambda n: strategies.tuples(
      build_nat(n, 4).filter(lambda l: len(l) > 0),
      build_nat(n, 4),
      strategies.just(n)
   )
)

class NatDivisionTestCase(unittest.TestCase):
    """ Tests for division. """

    @given(_DIVISION_STRATEGY)
    @settings(max_examples=50, deadline=None)
    def testInverses(self, strategy):
        """
        Test that division and undivision are inverses.
        """
        (divisor, dividend, base) = strategy
        (integer_part, non_repeating_part, repeating_part, relation) = \
           NatDivision.division(divisor, dividend, base)
        assert relation == 0

        (denominator, numerator) = NatDivision.undivision(
           integer_part,
           non_repeating_part,
           repeating_part,
           base
        )
        assert numerator == [] or numerator[0] != 0
        assert denominator != [] and denominator[0] != 0

        original = fractions.Fraction(
           Nats.convert_to_int(dividend, base),
           Nats.convert_to_int(divisor, base)
        )
        result = fractions.Fraction(
           Nats.convert_to_int(numerator, base),
           Nats.convert_to_int(denominator, base)
        )

        assert original == result

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
        with self.assertRaises(BasesError):
            NatDivision.division([3], [1], 10, 0, None)

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
       _DIVISION_STRATEGY,
       strategies.integers(min_value=0, max_value=32)
    )
    @settings(max_examples=50, deadline=None)
    def testTruncation(self, strategy, precision):
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
        (divisor, dividend, base) = strategy
        (integer_part, non_repeating_part, repeating_part, rel) = \
           NatDivision.division(divisor, dividend, base, precision)
        (integer_part_2, non_repeating_part_2, repeating_part_2, rel_2) = \
           NatDivision.division(divisor, dividend, base, None)

        assert rel_2 == 0
        assert integer_part == integer_part_2
        assert len(repeating_part) + len(non_repeating_part) <= precision

        assert repeating_part_2 == repeating_part or rel == -1

        assert not(repeating_part_2 != [] and repeating_part == []) or \
           (len(non_repeating_part) == precision and \
            non_repeating_part == \
            (non_repeating_part_2 + repeating_part_2)[:precision])

    @given(
       strategies.integers(min_value=1, max_value=2 ** 16),
       strategies.integers(min_value=0, max_value=2 ** 64),
       strategies.integers(min_value=3),
       strategies.integers(min_value=0, max_value=32)
    )
    @example(200, 10, 10, 1)
    @settings(max_examples=50)
    def testUpDown(self, divisor, dividend, base, precision):
        """
        Test that rounding up and rounding down have the right relationship.
        """
        # pylint: disable=too-many-locals
        divisor = Nats.convert_from_int(divisor, base)
        dividend = Nats.convert_from_int(dividend, base)
        (integer_part, non_repeating_part, repeating_part, rel) = \
           NatDivision.division(
              divisor,
              dividend,
              base,
              precision,
              RoundingMethods.ROUND_UP
           )
        (integer_part_2, non_repeating_part_2, repeating_part_2, rel_2) = \
           NatDivision.division(
              divisor,
              dividend,
              base,
              precision,
              RoundingMethods.ROUND_DOWN
           )
        (integer_part_3, non_repeating_part_3, repeating_part_3, rel_3) = \
           NatDivision.division(
              divisor,
              dividend,
              base,
              precision,
              RoundingMethods.ROUND_TO_ZERO
           )

        assert integer_part_2 == integer_part_3 and \
           non_repeating_part_2 == non_repeating_part_3 and \
           repeating_part_2 == repeating_part_3

        assert repeating_part != [] or repeating_part_2 == []
        assert rel >= rel_2 and rel_2 == rel_3

        round_up_int = \
           Nats.convert_to_int(integer_part + non_repeating_part, base)
        round_down_int = \
           Nats.convert_to_int(integer_part_2 + non_repeating_part_2, base)

        if repeating_part == []:
            assert round_up_int - round_down_int in (0, 1)

        if rel == 0:
            assert round_up_int == round_down_int
            assert rel_2 == 0
            assert rel_3 == 0


        for method in RoundingMethods.CONDITIONAL_METHODS():
            (integer_part_c, non_repeating_part_c, _, rel) = \
               NatDivision.division(
                  divisor,
                  dividend,
                  base,
                  precision,
                  method
               )
            rounded_int = \
               Nats.convert_to_int(integer_part_c + non_repeating_part_c, base)
            if repeating_part == []:
                assert round_down_int <= rounded_int <= round_up_int
                if rel == 0:
                    assert round_up_int == round_down_int
                elif rel == -1:
                    assert rounded_int == round_down_int
                else:
                    assert rounded_int == round_up_int
