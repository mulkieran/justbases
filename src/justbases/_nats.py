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

"""
Methods dealing exclusively with natural numbers.
"""
# isort: STDLIB
from functools import reduce  # pylint: disable=redefined-builtin

from ._errors import BasesValueError


class Nats:
    """
    Methods to convert non-negative ints.
    """

    @classmethod
    def convert(cls, value, from_base, to_base):
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
        return cls.convert_from_int(cls.convert_to_int(value, from_base), to_base)

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
            raise BasesValueError(from_base, "from_base", "must be greater than 2")

        if any(x < 0 or x >= from_base for x in value):
            raise BasesValueError(
                value,
                "value",
                "elements must be at least 0 and less than %s" % from_base,
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
                value, "value", "elements must be at least 0 and less than %s" % base
            )

        if carry < 0 or carry >= base:
            raise BasesValueError(carry, "carry", "carry must be less than %s" % base)

        result = []
        for val in reversed(value):
            (carry, new_val) = divmod(val + carry, base)
            result.append(new_val)

        return (carry, list(reversed(result)))
