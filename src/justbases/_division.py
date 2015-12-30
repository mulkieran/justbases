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

"""
Long division in any bases.
"""

from __future__ import absolute_import

import fractions
import itertools

from ._errors import ConvertValueError
from ._nats import Nats


class NatDivision(object):
    """
    Methods for division in arbitrary bases.
    """

    @staticmethod
    def _fractional_division(divisor, remainder, base):
        """
        Get the repeating and non-repeating part.

        :param int divisor: the divisor
        :param int remainder: the remainder
        :param int base: the base

        :returns: non_repeating and repeating parts
        :rtype: tuple of list of int * list of int
        """
        quotient = []
        remainders = []

        remainder = remainder * base
        while remainder != 0 and remainder not in remainders:
            remainders.append(remainder)
            (quot, rem) = divmod(remainder, divisor)
            quotient.append(quot)
            if quot > 0:
                remainder = rem * base
            else:
                remainder = remainder * base

        if remainder == 0:
            return (quotient, [])
        else:
            start = remainders.index(remainder)
            return (quotient[:start], quotient[start:])

    @staticmethod
    def _division(divisor, dividend, remainder, base):
        """
        Get the quotient and remainder

        :param int divisor: the divisor
        :param dividend: the divident
        :type dividend: sequence of int
        :param int remainder: initial remainder
        :param int base: the base

        :returns: quotient and remainder
        :rtype: tuple of (list of int) * int
        """
        quotient = []
        for value in dividend:
            remainder = remainder * base + value
            (quot, rem) = divmod(remainder, divisor)
            quotient.append(quot)
            if quot > 0:
                remainder = rem
        return (quotient, remainder)

    @classmethod
    def division(cls, divisor, dividend, base):
        """
        Division of natural numbers.

        :param divisor: the divisor
        :type divisor: list of int
        :param dividend: the dividend
        :type dividend: list of int
        :returns: the result
        :rtype: tuple of list of int * list of int * list of int
        :raises ConvertError: on invalid values
        """
        if base < 2:
            raise ConvertValueError(base, "base", "must be at least 2")

        if any(x < 0 or x >= base for x in divisor):
            raise ConvertValueError(
               divisor,
               "divisor",
               "for all elements, e, 0 <= e < base required"
            )

        if any(x < 0 or x >= base for x in dividend):
            raise ConvertValueError(
               divisor,
               "divisor",
               "for all elements, e, 0 <= e < base required"
            )

        if all(x == 0 for x in divisor):
            raise ConvertValueError(
               divisor,
               "divisor",
               "must be greater than 0"
            )

        divisor = Nats.convert_to_int(divisor, base)

        (integer_part, rem) = cls._division(divisor, dividend, 0, base)
        (non_repeating_part, repeating_part) = cls._fractional_division(
           divisor,
           rem,
           base
        )

        return (
           list(itertools.dropwhile(lambda x: x == 0, integer_part)),
           non_repeating_part,
           repeating_part
        )

    @classmethod
    def undivision(
       cls,
       integer_part,
       non_repeating_part,
       repeating_part,
       base
    ):
        """
        Find divisor and dividend that yield component parts.

        :param integer_part: the integer part
        :type integer_part: list of int
        :param non_repeating_part: the non_repeating_part
        :type non_repeating_part: list of int
        :param repeating_part: the repeating part
        :type repeating_part: list of int
        :param int base: the base

        :returns: divisor and dividend in lowest terms
        :rtype: tuple of list of int * list of int
        """
        if base < 2:
            raise ConvertValueError(base, "base", "must be at least 2")

        if any(x < 0 or x >= base for x in integer_part):
            raise ConvertValueError(
               integer_part,
               "integer_part",
               "for all elements, e, 0 <= e < base required"
            )

        if any(x < 0 or x >= base for x in non_repeating_part):
            raise ConvertValueError(
               non_repeating_part,
               "non_repeating_part",
               "for all elements, e, 0 <= e < base required"
            )

        if any(x < 0 or x >= base for x in repeating_part):
            raise ConvertValueError(
               repeating_part,
               "repeating_part",
               "for all elements, e, 0 <= e < base required"
            )

        shift_length = len(repeating_part)
        frac_length = len(non_repeating_part)

        top = fractions.Fraction(
           Nats.convert_to_int(
              integer_part + non_repeating_part + repeating_part,
              base
           ),
           base ** frac_length
        )

        if shift_length == 0:
            return (
               Nats.convert_from_int(top.denominator, base),
               Nats.convert_from_int(top.numerator, base)
            )

        bottom = fractions.Fraction(
           Nats.convert_to_int(integer_part + non_repeating_part, base),
           base ** frac_length
        )
        result = (top - bottom) / ((base ** shift_length) - 1)
        return (
           Nats.convert_from_int(result.denominator, base),
           Nats.convert_from_int(result.numerator, base)
        )
