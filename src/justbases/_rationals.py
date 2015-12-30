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
Methods dealing with rationals.
"""
from fractions import Fraction

from ._division import NatDivision
from ._errors import ConvertValueError
from ._nats import Nats
from ._radix import Radix


class Rationals(object):
    """
    Methods to convert non-negative ints.
    """

    @classmethod
    def convert(cls, value, to_base):
        """
        Convert value from a base to a base.

        :param Radix value: the value to convert
        :param int to_base: base of result
        :returns: the conversion result
        :rtype: Radix of int
        :raises ConvertError: if to_base is less than 2
        """
        return cls.convert_from_rational(
           cls.convert_to_rational(value),
           to_base
        )

    @staticmethod
    def convert_to_rational(value):
        """
        Convert value to a rational.

        :param Radix value: the value to convert
        :returns: the conversion result
        :rtype: Rational
        :raises ConvertError: if from_base is less than 2
        """
        (denominator, numerator) = \
           NatDivision.undivision(
              value.integer_part,
              value.non_repeating_part,
              value.repeating_part,
              value.base
           )
        result = Fraction(
           Nats.convert_to_int(numerator, value.base),
           Nats.convert_to_int(denominator, value.base)
        )
        return result * (1 if value.positive else -1)

    @staticmethod
    def convert_from_rational(value, to_base):
        """
        Convert rational value to a base.

        :param Rational value: the value to convert
        :param int to_base: base of result, must be at least 2
        :returns: the conversion result
        :rtype: Radix
        :raises ConvertValueError: if to_base is less than 2
        """
        if to_base < 2:
            raise ConvertValueError(to_base, "to_base", "must be at least 2")

        positive = True if value >= 0 else False
        value = abs(value)

        numerator = Nats.convert_from_int(value.numerator, to_base)
        denominator = Nats.convert_from_int(value.denominator, to_base)

        (integer_part, non_repeating_part, repeating_part) = \
           NatDivision.division(denominator, numerator, to_base)

        return Radix(
           positive,
           integer_part,
           non_repeating_part,
           repeating_part,
           to_base
        )
