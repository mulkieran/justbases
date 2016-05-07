# Copyright (C) 2016  Red Hat, Inc.
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
# 02110-1301, USA.  Any Red Hat trademarks that are incorporated in the
# source code or documentation are not subject to the GNU General Public
# License and may only be used or replicated with the express permission of
# Red Hat, Inc.
#
# Red Hat Author(s): Anne Mulhern <amulhern@redhat.com>

""" Handling lists of digits. """

import itertools
import string

from collections import namedtuple

from ._errors import BasesValueError

class Digits(object):
    """
    Transforms digits as ints to corresponding symbols.
    """
    # pylint: disable=too-few-public-methods

    _LOWER_DIGITS = string.digits + string.ascii_lowercase
    _UPPER_DIGITS = string.digits + string.ascii_uppercase

    _MAX_SIZE_BASE_FOR_CHARS = len(string.digits + string.ascii_uppercase)

    @classmethod
    def xform(cls, number, config, base):
        """
        Get a number as a string.

        :param number: a number
        :type number: list of int
        :param DigitsConfig config: configuration for displaying digits
        :param int base: the base in which this number is being represented
        :raises: BasesValueError
        """
        if config.use_letters:
            if base > cls._MAX_SIZE_BASE_FOR_CHARS:
                raise BasesValueError(
                   base,
                   "base",
                   "must be no greater than number of available characters"
                )
            digits = \
               cls._UPPER_DIGITS if config.use_caps else cls._LOWER_DIGITS
            return ''.join(digits[x] for x in number)
        else:
            separator = '' if base <= 10 else config.separator
            return separator.join(str(x) for x in number)


class Strip(object):
    """
    Handle stripping digits.
    """
    # pylint: disable=too-few-public-methods

    @staticmethod
    def _strip_trailing_zeros(value):
        """
        Strip trailing zeros from a list of ints.

        :param value: the value to be stripped
        :type value: list of str

        :returns: list with trailing zeros stripped
        :rtype: list of int
        """
        return list(
           reversed(
              list(itertools.dropwhile(lambda x: x == 0, reversed(value)))
           )
        )

    @classmethod
    def xform(cls, number, config, relation):
        """
        Strip trailing zeros from a number according to config and relation.

        :param number: a number
        :type number: list of int
        :param StripConfig config: configuration for stripping zeros
        :param int relation: the relation of the display value to the actual
        """

        # pylint: disable=too-many-boolean-expressions
        if (config.strip) or \
           (config.strip_exact and relation == 0) or \
           (config.strip_whole and relation == 0 and \
            all(x == 0 for x in number)):
            return cls._strip_trailing_zeros(number)
        else:
            return number


class Number(object):
    """
    Handle generic number display stuff.

    Returns modifications to the number string.
    """
    # pylint: disable=too-few-public-methods

    _FMT_STR = "".join([
       "%(sign)s",
       "%(base_str)s",
       "%(left)s",
       "%(radix)s",
       "%(right)s",
       "%(repeating)s"
    ])

    @classmethod
    def xform(cls, left, right, repeating, config, base, positive):
        """
        Return prefixes for tuple.

        :param str left: left of the radix
        :param str right: right of the radix
        :param str repeating: repeating part
        :param DisplayConfig config: display configuration
        :param int base: the base in which value is displayed
        :param bool positive: whether value is non-negative
        :returns: the number string
        :rtype: str
        """
        # pylint: disable=too-many-arguments

        base_str = ''
        if config.show_base:
            if base == 8:
                base_str = '0'
            elif base == 16:
                base_str = '0x'
            else:
                base_str = ''

        sign = '' if positive else '-'

        result = {
           'sign' : sign,
           'base_str' : base_str,
           'left' : left,
           'radix' : '.' if right else "",
           'right' : right,
           'repeating' : ("(%s)" % repeating) if repeating != "" else ""
        }

        return cls._FMT_STR % result


_Decorators = namedtuple('_Decorators', ['approx_str'])


class Decorators(object):
    """
    Handle generic display stuff.

    Returns decorators for the value.
    """

    @staticmethod
    def relation_to_symbol(relation):
        """
        Change a numeric relation to a string symbol.

        :param int relation: the relation

        :returns: a symbol with the right relation to ``relation``
        :rtype: str
        """
        if relation == 0:
            return ''
        elif relation == -1:
            return '>'
        elif relation == 1:
            return '<'
        else:
            assert False # pragma: no cover

    @classmethod
    def decorators(cls, config, relation):
        """
        Return prefixes for tuple.

        :param DisplayConfig config: display configuration
        :param int relation: relation of string value to actual value
        """
        if config.show_approx_str:
            approx_str = cls.relation_to_symbol(relation)
        else:
            approx_str = ''

        return _Decorators(approx_str=approx_str)


class String(object):
    """
    Convert size components to string according to configuration.
    """
    # pylint: disable=too-few-public-methods

    _FMT_STR = "".join([
       "%(approx)s",
       "%(space)s",
       "%(number)s"
    ])

    @classmethod
    def xform(cls, radix, display, relation):
        """
        Transform a radix and some information to a str according to
        configurations.

        :param Radix radix: the radix
        :param DisplayConfig display: the display config
        :param int relation: relation of display value to actual value
        :param units: element of UNITS()
        :returns: a string representing the value
        :rtype: str
        """
        right = radix.non_repeating_part
        left = radix.integer_part
        repeating = radix.repeating_part

        if repeating == []:
            right = Strip.xform(right, display.strip_config, relation)

        right_str = Digits.xform(right, display.digits_config, radix.base)
        left_str = Digits.xform(left, display.digits_config, radix.base) or '0'
        repeating_str = \
           Digits.xform(repeating, display.digits_config, radix.base)

        number = Number.xform(
           left_str,
           right_str,
           repeating_str,
           display,
           radix.base,
           radix.positive
        )

        decorators = Decorators.decorators(display, relation)

        result = {
           'approx' : decorators.approx_str,
           'space' : ' ' if decorators.approx_str else '',
           'number' : number
        }

        return cls._FMT_STR % result
