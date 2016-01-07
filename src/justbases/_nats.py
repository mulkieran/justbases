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
from functools import reduce # pylint: disable=redefined-builtin

from ._errors import BasesValueError


class Nats(object):
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
        """
        return cls.convert_from_int(
           cls.convert_to_int(value, from_base),
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
