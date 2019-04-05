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
Methods to handle rounding.
"""

from ._constants import RoundingMethods

from ._errors import BasesAssertError
from ._errors import BasesValueError


class Rounding(object):
    """
    Methods to handle rounding abstractly.
    """
    # pylint: disable=too-few-public-methods

    @staticmethod
    def rounding_up(value, middle, method):
        """
        Find rounding direction base on ``method``.

        :param Fraction value: the value that determines the direction
        :param Fraction middle: the middle possible value
        :param method: the rounding method

        :returns: True if rounding up, False if down
        :rtype: boolean
        """
        # pylint: disable=too-many-return-statements
        if value <= 0:
            raise BasesValueError(value, "value", "must be greater than 0")

        if method is RoundingMethods.ROUND_DOWN:
            return False

        if method is RoundingMethods.ROUND_TO_ZERO:
            return False

        if method is RoundingMethods.ROUND_UP:
            return True

        if value < middle:
            return False

        if value > middle:
            return True

        if value == middle:
            if method is RoundingMethods.ROUND_HALF_UP:
                return True
            if method is RoundingMethods.ROUND_HALF_DOWN:
                return False
            if method is RoundingMethods.ROUND_HALF_ZERO:
                return False

        raise BasesAssertError('unknown method') # pragma: no cover
