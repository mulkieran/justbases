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
A type for holding a non-integer rational.
"""

from ._errors import ConvertValueError


class Radix(object):
    """
    An object containing information about a rational representation.
    """
    # pylint: disable=too-few-public-methods

    def __init__( # pylint: disable=too-many-arguments
        self,
        positive,
        integer_part,
        non_repeating_part,
        repeating_part,
        base
    ):
        """
        Initializer.

        :param bool positive: True if value is positive, otherwise False
        :param integer_part: the part on the left side of the radix
        :type integer_part: list of int
        :param non_repeating_part: non repeating part on left side
        :type non_repeating_part: list of int
        :param repeating_part: repeating part
        :type repeating_part: list of int
        :param int base: base of the radix, must be at least 2
        """
        self.positive = positive

        if any(x < 0 or x >= base for x in integer_part):
            raise ConvertValueError(
               integer_part,
               "integer_part",
               "values must be between 0 and %s" % base
            )
        if any(x < 0 or x >= base for x in non_repeating_part):
            raise ConvertValueError(
               non_repeating_part,
               "non_repeating_part",
               "values must be between 0 and %s" % base
            )
        if any(x < 0 or x >= base for x in repeating_part):
            raise ConvertValueError(
               repeating_part,
               "repeating_part",
               "values must be between 0 and %s" % base
            )
        if base < 2:
            raise ConvertValueError(base, "base", "must be at least 2")

        self.base = base
        self.integer_part = integer_part
        self.non_repeating_part = non_repeating_part
        self.repeating_part = repeating_part
