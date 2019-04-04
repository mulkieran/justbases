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
Constants required by the package.
"""


class _RoundingMethod():
    """ Class to generate rounding method enumeration. """
    # pylint: disable=too-few-public-methods

    def __init__(self, doc):
        """ Initializer.

            :param str doc: explanation of the rounding method
        """
        self._doc = doc

    def __str__(self):
        return self.__class__.__name__

    def __repr__(self):
        return "%s(%s)" % (str(self), self.doc)

    # pylint: disable=protected-access
    doc = property(lambda s: s._doc, doc="explanation of rounding method")


class RoundingMethods():
    """ Static class for accessing rounding methods. """
    # pylint: disable=too-few-public-methods

    ROUND_DOWN = _RoundingMethod("Round down.")
    ROUND_HALF_DOWN = _RoundingMethod("Round to nearest, down on a tie.")
    ROUND_HALF_UP = _RoundingMethod("Round to nearest, up on a tie.")
    ROUND_HALF_ZERO = _RoundingMethod("Round to nearest, to zero on a tie.")
    ROUND_TO_ZERO = _RoundingMethod("Round to zero.")
    ROUND_UP = _RoundingMethod("Round up.")

    _METHODS = [
       ROUND_DOWN,
       ROUND_HALF_DOWN,
       ROUND_HALF_UP,
       ROUND_HALF_ZERO,
       ROUND_TO_ZERO,
       ROUND_UP
    ]

    @classmethod
    def METHODS(cls):
        """ Methods of this class. """
        return cls._METHODS[:]

    @classmethod
    def CONDITIONAL_METHODS(cls):
        """ Conditional rounding methods. """
        return [cls.ROUND_HALF_DOWN, cls.ROUND_HALF_UP, cls.ROUND_HALF_ZERO]
