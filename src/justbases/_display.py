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

""" Handling lists of digits. """

# isort: STDLIB
import itertools
import string
from collections import namedtuple

from ._errors import BasesValueError


class Digits:
    """
    Transforms digits as ints to corresponding symbols.
    """

    # pylint: disable=too-few-public-methods

    _LOWER_DIGITS = string.digits + string.ascii_lowercase
    _UPPER_DIGITS = string.digits + string.ascii_uppercase

    _MAX_SIZE_BASE_FOR_CHARS = len(string.digits + string.ascii_uppercase)

    def __init__(self, config, base):
        """
        Initializer.

        :param DigitsConfig config: configuration for displaying digits
        :param int base: the base of the values to display

        :raises BasesValueError: if config options are bad
        """
        if config.use_letters:
            if base > self._MAX_SIZE_BASE_FOR_CHARS:
                raise BasesValueError(
                    base,
                    "base",
                    "must be no greater than number of available characters",
                )
        self.CONFIG = config

    def xform(self, number, base):
        """
        Get a number as a string.

        :param number: a number
        :type number: list of int
        :param int base: the base in which this number is being represented
        :raises BasesValueError: if config is unsuitable for number
        """
        if self.CONFIG.use_letters:
            digits = self._UPPER_DIGITS if self.CONFIG.use_caps else self._LOWER_DIGITS
            return "".join(digits[x] for x in number)
        separator = "" if base <= 10 else self.CONFIG.separator
        return separator.join(str(x) for x in number)


class Strip:
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
            reversed(list(itertools.dropwhile(lambda x: x == 0, reversed(value))))
        )

    def __init__(self, config, base):
        """
        Initializer.

        :param StripConfig config: configuration for stripping zeros
        :param int base: the base
        """
        # pylint: disable=unused-argument
        self.CONFIG = config

    def xform(self, number, relation):
        """
        Strip trailing zeros from a number according to config and relation.

        :param number: a number
        :type number: list of int
        :param int relation: the relation of the display value to the actual
        """

        # pylint: disable=too-many-boolean-expressions
        if (
            (self.CONFIG.strip)
            or (self.CONFIG.strip_exact and relation == 0)
            or (
                self.CONFIG.strip_whole
                and relation == 0
                and all(x == 0 for x in number)
            )
        ):
            return Strip._strip_trailing_zeros(number)
        return number


class Number:
    """
    Handle generic number display stuff.

    Returns modifications to the number string.
    """

    # pylint: disable=too-few-public-methods

    _FMT_STR = "".join(
        [
            "%(sign)s",
            "%(base_prefix)s",
            "%(left)s",
            "%(radix)s",
            "%(right)s",
            "%(repeating)s",
            "%(base_separator)s",
            "%(base_subscript)s",
        ]
    )

    def __init__(self, config, base):
        """
        Initializer.

        :param BaseConfig config: display configuration
        :param int base: the base
        """
        # pylint: disable=unused-argument
        self.CONFIG = config

    def xform(self, left, right, repeating, base, sign):
        """
        Return prefixes for tuple.

        :param str left: left of the radix
        :param str right: right of the radix
        :param str repeating: repeating part
        :param int base: the base in which value is displayed
        :param int sign: -1, 0, 1 as appropriate
        :returns: the number string
        :rtype: str
        """
        # pylint: disable=too-many-arguments

        base_prefix = ""
        if self.CONFIG.use_prefix:
            if base == 8:
                base_prefix = "0"
            elif base == 16:
                base_prefix = "0x"
            else:
                base_prefix = ""

        base_subscript = str(base) if self.CONFIG.use_subscript else ""

        result = {
            "sign": "-" if sign == -1 else "",
            "base_prefix": base_prefix,
            "left": left,
            "radix": "." if (right != "" or repeating != "") else "",
            "right": right,
            "repeating": ("(%s)" % repeating) if repeating != "" else "",
            "base_separator": "" if base_subscript == "" else "_",
            "base_subscript": base_subscript,
        }

        return self._FMT_STR % result


_Decorators = namedtuple("_Decorators", ["approx_str"])


class Decorators:
    """
    Handle generic display stuff.

    Returns decorators for the value.
    """

    # pylint: disable=inconsistent-return-statements
    @staticmethod
    def relation_to_symbol(relation):
        """
        Change a numeric relation to a string symbol.

        :param int relation: the relation

        :returns: a symbol with the right relation to ``relation``
        :rtype: str
        """
        # pylint: disable=no-else-return
        if relation == 0:
            return ""
        elif relation == -1:
            return ">"
        elif relation == 1:
            return "<"
        else:
            assert False  # pragma: no cover

    def __init__(self, config, base):
        """
        Initializer.

        :param DisplayConfig config: the display configuration
        :param int base: the base
        """
        # pylint: disable=unused-argument
        self.CONFIG = config

    def decorators(self, relation):
        """
        Return prefixes for tuple.

        :param int relation: relation of string value to actual value
        """
        if self.CONFIG.show_approx_str:
            approx_str = Decorators.relation_to_symbol(relation)
        else:
            approx_str = ""

        return _Decorators(approx_str=approx_str)


class String:
    """
    Convert size components to string according to configuration.
    """

    # pylint: disable=too-few-public-methods

    _FMT_STR = "".join(["%(approx)s", "%(space)s", "%(number)s"])

    def __init__(self, display, base):
        """
        Initializer.

        :param DisplayConfig display: the display config
        :param int base: the base of the radix

        :raises BasesValueError: if the configuration cannot work
        """
        self.DECORATORS = Decorators(display, base)
        self.DIGITS = Digits(display.digits_config, base)
        self.NUMBER = Number(display.base_config, base)
        self.STRIP = Strip(display.strip_config, base)

        self.CONFIG = display

    def xform(self, radix, relation):
        """
        Transform a radix and some information to a str according to
        configurations.

        :param Radix radix: the radix
        :param int relation: relation of display value to actual value
        :param units: element of UNITS()
        :returns: a string representing the value
        :rtype: str

        :raises BasesValueError: if configuration does not work with value
        """
        right = radix.non_repeating_part
        left = radix.integer_part
        repeating = radix.repeating_part

        if repeating == []:
            right = self.STRIP.xform(right, relation)

        right_str = self.DIGITS.xform(right, radix.base)
        left_str = self.DIGITS.xform(left, radix.base) or "0"
        repeating_str = self.DIGITS.xform(repeating, radix.base)

        number = self.NUMBER.xform(
            left_str, right_str, repeating_str, radix.base, radix.sign
        )

        decorators = self.DECORATORS.decorators(relation)

        result = {
            "approx": decorators.approx_str,
            "space": " " if decorators.approx_str else "",
            "number": number,
        }

        return self._FMT_STR % result
