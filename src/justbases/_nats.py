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
Methods dealing exclusively with natural numbers.
"""
from fractions import Fraction
from functools import reduce # pylint: disable=redefined-builtin
from itertools import dropwhile

from ._constants import RoundingMethods
from ._errors import BasesValueError
from ._rounding import Rounding


class Nats(object):
    """
    Methods to convert non-negative ints.
    """

    @staticmethod
    def convert(value, from_base, to_base):
        """
        Convert value from a base to a base.

        :param value: the value to convert
        :type value: sequence of int
        :param int from_base: base of value
        :param int to_base: base of result
        :returns: the conversion result
        :rtype: list of int
        :raises ConvertError: if from_base is less than 2
        :raises ConvertError: if to_base is less than 2
        :raises ConvertError: if elements in value outside bounds

        Preconditions:
          * all integers in value must be no less than 0
          * from_base, to_base must be at least 2

        Complexity: O(len(value))
        """
        return Nats.convert_from_int(
           Nats.convert_to_int(value, from_base),
           to_base
        )

    @staticmethod
    def convert_to_int(value, from_base):
        """
        Convert value to an int.

        :param value: the value to convert
        :type value: sequence of int
        :param int from_base: base of value
        :returns: the conversion result
        :rtype: int
        :raises ConvertError: if from_base is less than 2
        :raises ConvertError: if elements in value outside bounds

        Preconditions:
          * all integers in value must be at least 0
          * all integers in value must be less than from_base
          * from_base must be at least 2

        Complexity: O(len(value))
        """
        if from_base < 2:
            raise BasesValueError(
               from_base,
               "from_base",
               "must be greater than 2"
            )

        if any(x < 0 or x >= from_base for x in value):
            raise BasesValueError(
               value,
               "value",
               "elements must be at least 0 and less than %s" % from_base
            )
        return reduce(lambda x, y: x * from_base + y, value, 0)

    @staticmethod
    def convert_from_int(value, to_base):
        """
        Convert int value to a base.

        :param int value: the value to convert, must be at least 0
        :param int to_base: base of result, must be at least 2
        :returns: the conversion result
        :rtype: list of int
        :raises BasesValueError: if value is less than 0
        :raises BasesValueError: if to_base is less than 2

        Preconditions:
          * to_base must be at least 2

        Complexity: O(log_{to_base}(value))
        """
        if value < 0:
            raise BasesValueError(value, "value", "must be at least 0")

        if to_base < 2:
            raise BasesValueError(to_base, "to_base", "must be at least 2")

        result = []
        while value != 0:
            (value, rem) = divmod(value, to_base)
            result.append(rem)
        result.reverse()
        return result

    @staticmethod
    def carry_in(value, carry, base):
        """
        Add a carry digit to a number represented by ``value``.

        :param value: the value
        :type value: list of int
        :param int carry: the carry digit (>= 0)
        :param int base: the base (>= 2)

        :returns: carry-out and result
        :rtype: tuple of int * (list of int)

	Complexity: O(len(value))
        """
        if base < 2:
            raise BasesValueError(base, "base", "must be at least 2")

        if any(x < 0 or x >= base for x in value):
            raise BasesValueError(
               value,
               "value",
               "elements must be at least 0 and less than %s" % base
            )

        if carry < 0 or carry >= base:
            raise BasesValueError(
               carry,
               "carry",
               "carry must be less than %s" % base
            )

        result = []
        for val in reversed(value):
            (carry, new_val) = divmod(val + carry, base)
            result.append(new_val)

        return (carry, list(reversed(result)))

    @staticmethod
    def roundTo(value, base, precision, method):
        """
        Round a natural number to ``precision`` using ``method``.

        :param value: the value to round
        :type value: list of int
        :param int base: the base of ``value``, must be at least 2
        :param precision: the precision to round to or None
        :type precision: int or NoneType
        :param method: the rounding method
        :type method: one of RoundingMethods.METHODS()

        :returns: the rounded value and the relation to actual
        :rtype: (list of int) * Fraction

        The relation of the rounded number to the actual is indicated by
        a Rational value in the range -1 to 1. This number indicates the
        proportion of the amount rounded by which the rounded value differs
        from the actual. If the two are the same, the relation is 0.

        For example, suppose the actual number is 350 and the precision is -2.
        Then, the rounded number must be either 300 or 400 depending on the
        method. If it is 300, then the relation is -1/2, if 400, +1/2.
        """
        if base < 2:
            raise BasesValueError(base, "base", "must be at least 2")

        if any(x < 0 or x >= base for x in value):
            raise BasesValueError(
               value,
               "value",
               "elements must be at least 0 and less than %s" % base
            )

        if not method in RoundingMethods.METHODS():
            raise BasesValueError(
               method,
               "method",
               "must be among RoundingMethods.METHODS()"
            )

        if precision is None or precision >= 0:
            return (value, 0)

        (left, right) = (value[:precision], value[precision:])

        if all(x == 0 for x in right):
            return (value, 0)

        num_digits = -precision
        ulp = base ** num_digits
        middle = Fraction(ulp, 2)
        fractional_value = Nats.convert_to_int(right, base)

        if Rounding.rounding_up(fractional_value, middle, method):
            (carry_out, new_left) = Nats.carry_in(left, 1, base)
            if carry_out != 0:
                new_left = [carry_out] + new_left
            relation = Fraction(ulp - fractional_value, ulp)
        else:
            new_left = left
            relation = -Fraction(fractional_value, ulp)

        new_left = new_left + num_digits * [0]
        new_left = [x for x in dropwhile(lambda x: x == 0, new_left)]
        return (new_left, relation)
