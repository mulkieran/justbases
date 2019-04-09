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
Errors.
"""

from __future__ import absolute_import

import abc


class BasesError(Exception, metaclass=abc.ABCMeta):
    """
    Supertype of all errors for this package.
    """


class BasesInvalidOperationError(BasesError): # pragma: no cover
    """
    Invalid operation.
    """

    def __init__(self, op, other=None):
        # pylint: disable=super-init-not-called
        self._operator = op
        self._other = other

    def __str__(self):
        if self._other is None:
            return "invalid operation for Radix: %s" % self._operator
        return "invalid operation %s for Radix and %s" % \
           (self._operator, type(self._other).__name__)


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
        return self._FMT_STR % (self._value, self._param)


class BasesAssertError(BasesError):
    """
    For assertion failures.
    """
