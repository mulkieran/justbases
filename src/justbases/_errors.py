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
Errors.
"""

from __future__ import absolute_import

import abc

from six import add_metaclass


@add_metaclass(abc.ABCMeta)
class BasesError(Exception):
    """
    Supertype of all errors for this package.
    """
    pass


class BasesValueError(BasesError):
    """ Raised when a parameter has an unacceptable value.

        May also be raised when the parameter has an unacceptable type.
    """
    _FMT_STR = "value '%s' for parameter %s is unacceptable"

    def __init__(self, value, param, msg=None):
        """ Initializer.

            :param object value: the value
            :param str param: the parameter
            :param str msg: an explanatory message
        """
        # pylint: disable=super-init-not-called
        self._value = value
        self._param = param
        self._msg = msg

    def __str__(self): # pragma: no cover
        if self._msg:
            fmt_str = self._FMT_STR + ": %s"
            return fmt_str % (self._value, self._param, self._msg)
        else:
            return self._FMT_STR % (self._value, self._param)
