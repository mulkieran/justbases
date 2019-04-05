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
Methods dealing with rationals.
"""
import copy
import itertools

from fractions import Fraction

from ._constants import RoundingMethods
from ._division import NatDivision
from ._errors import BasesInvalidOperationError
from ._errors import BasesValueError
from ._nats import Nats
from ._rounding import Rounding


class Radices(object):
    """
    Methods for Radices.
    """
    # pylint: disable=too-few-public-methods

    @staticmethod
    def from_rational(
       value,
       to_base,
       precision=None,
       method=RoundingMethods.ROUND_DOWN
    ):
        """
        Convert rational value to a Radix.

        :param Rational value: the value to convert
        :param int to_base: base of result, must be at least 2
        :param precision: number of digits in total or None
        :type precision: int or NoneType
        :param method: rounding method
        :type method: element of RoundingMethods.METHODS()
        :returns: the conversion result and its relation to actual result
        :rtype: Radix * Rational
        :raises BasesValueError: if to_base is less than 2

        Complexity: Uncalculated.
        """
        if to_base < 2:
            raise BasesValueError(to_base, "to_base", "must be at least 2")

        if precision is not None and precision < 0:
            raise BasesValueError(precision, "precision", "must be at least 0")

        if value == 0:
            non_repeating_part = [] if precision is None else precision * [0]
            return (Radix(0, [], non_repeating_part, [], to_base), 0)

        denominator = Nats.convert_from_int(value.denominator, to_base)

        sign = -1 if value < 0 else 1
        if sign == -1:
            use_value = -value
            use_method = Rounding.reverse(method)
        else:
            use_value = value
            use_method = method

        numerator = Nats.convert_from_int(use_value.numerator, to_base)

        (integer_part, non_repeating_part, repeating_part, relation) = \
           NatDivision.division(
              denominator,
              numerator,
              to_base,
              precision,
              use_method
           )

        result = Radix(
           sign,
           integer_part,
           non_repeating_part,
           repeating_part,
           to_base
        )

        if precision is not None:
            (result, rel) = result.rounded(precision, method)
            relation = relation * sign if rel == 0 else rel

        return (result, relation)


class Rationals(object):
    """
    Miscellaneous methods for rationals.
    """
    # pylint: disable=too-few-public-methods

    @staticmethod
    def round_to_int(value, method):
        """
        Round ``value`` to an int according to ``method``.

        :param Rational value: the value to round
        :param method: the rounding method (of RoundingMethods.METHODS())

        :returns: rounded value and relation of rounded value to actual value.
        :rtype: (int * Rational)

        Complexity: O(1)
        """
        if value.denominator == 1:
            return (value.numerator, 0)

        if value < 0:
            use_value = -value
            use_method = Rounding.reverse(method)
        else:
            use_method = method
            use_value = value

        int_value = int(use_value)
        (lower, upper) = (int_value, int_value + 1)

        if Rounding.rounding_up(use_value - lower, Fraction(1, 2), use_method):
            (use_result, relation) = (upper, upper - use_value)
        else:
            (use_result, relation) = (lower, lower - use_value)

        if value != use_value:
            return (-use_result, -relation)
        else:
            return (use_result, relation)


class Radix(object):
    """
    An object containing information about a rational representation.

    A Radix is a numeral, not a number, and in general it is impossible to
    compute with it. Radices can not be ordered, but can be compared for
    equality. There are some unary arithmetic operations, which make sense,
    and are convenient, on a numeral, e.g., abs. These operations are
    implemented. However, no binary arithmetic operations, other than equality
    and inequality are implemented. Different representation of the same
    number are considered unequal.
    """

    _FMT_STR = "".join([
       "%(sign)s",
       "%(left)s",
       "%(radix)s",
       "%(non_repeat)s",
       "%(repeat)s",
       "_",
       "%(base)s"
    ])

    try: # pragma: no cover
        import justbases_string
        STR_CONFIG = justbases_string.DisplayConfig()
        STR_IMPL = justbases_string.String
    except ImportError: # pragma: no cover
        STR_CONFIG = None
        STR_IMPL = None

    @classmethod
    def _validate( # pylint: disable=too-many-arguments
        cls,
        sign,
        integer_part,
        non_repeating_part,
        repeating_part,
        base
    ):
        """
        Check if radix is valid.

        :param int sign: -1, 0, or 1 as appropriate
        :param integer_part: the part on the left side of the radix
        :type integer_part: list of int
        :param non_repeating_part: non repeating part on left side
        :type non_repeating_part: list of int
        :param repeating_part: repeating part
        :type repeating_part: list of int
        :param int base: base of the radix, must be at least 2

        :returns: BasesValueError if invalid values
        :rtype: BasesValueError or NoneType

        Complexity: O(len(integer_part + non_repeating_part + repeating_part))
        """
        # pylint: disable=too-many-return-statements
        if any(x < 0 or x >= base for x in integer_part):
            return BasesValueError(
               integer_part,
               "integer_part",
               "values must be between 0 and %s" % base
            )
        if any(x < 0 or x >= base for x in non_repeating_part):
            return BasesValueError(
               non_repeating_part,
               "non_repeating_part",
               "values must be between 0 and %s" % base
            )
        if any(x < 0 or x >= base for x in repeating_part):
            return BasesValueError(
               repeating_part,
               "repeating_part",
               "values must be between 0 and %s" % base
            )
        if base < 2:
            return BasesValueError(base, "base", "must be at least 2")

        if sign not in (-1, 0, 1) or sign is True or sign is False:
            return BasesValueError(
               sign,
               "sign",
               "must be an int between -1 and 1"
            )

        if sign == 0 and \
           (any(x != 0 for x in integer_part) or \
           any(x != 0 for x in non_repeating_part) or \
           any(x != 0 for x in repeating_part)):
            return BasesValueError(
               sign,
               "sign",
               "can not be 0 unless number is also zero"
            )

        return None

    @classmethod
    def _repeat_length(cls, part):
        """
        The length of the repeated portions of ``part``.

        :param part: a number
        :type part: list of int
        :returns: the first index at which part repeats
        :rtype: int

        If part does not repeat, result is the length of part.

        Complexity: O(len(part)^2)
        """
        repeat_len = len(part)
        if repeat_len == 0:
            return repeat_len

        first_digit = part[0]
        limit = repeat_len // 2 + 1
        indices = (i for i in range(1, limit) if part[i] == first_digit)
        for index in indices:
            (quot, rem) = divmod(repeat_len, index)
            if rem == 0:
                first_chunk = part[0:index]
                if all(first_chunk == part[x:x + index] \
                   for x in range(index, quot * index, index)):
                    return index
        return repeat_len

    @classmethod
    def _canonicalize_fraction(cls, non_repeating, repeating):
        """
        If the same fractional value can be represented by stripping repeating
        part from ``non_repeating``, do it.

        :param non_repeating: non repeating part of fraction
        :type non_repeating: list of int
        :param repeating: repeating part of fraction
        :type repeating: list of int
        :returns: new non_repeating and repeating parts
        :rtype: tuple of list of int * list of int

        Complexity: O(len(non_repeating))
        """
        if repeating == []:
            return (non_repeating, repeating)

        repeat_len = len(repeating)

        # strip all exact matches:
        # * for [6, 1, 2, 1, 2], [1,2] end is 1
        # * for [1, 2, 1, 2], [1,2] end is 0
        # * for [6, 2, 1, 2], [1,2] end is 2
        indices = range(len(non_repeating), -1, -repeat_len)
        end = next( # pragma: no cover
           i for i in indices if non_repeating[(i - repeat_len):i] != repeating
        )

        # for remaining, find partial match and shift repeating
        # * for [6, 2, 1, 2], [1, 2] initial end is 2, result is [6], [2, 1]
        indices = range(min(repeat_len - 1, end), 0, -1)
        index = next(
           (i for i in indices \
              if repeating[-i:] == non_repeating[(end-i):end]),
           0
        )
        return (
           non_repeating[:(end - index)],
           repeating[-index:] + repeating[:-index]
        )

    def __init__( # pylint: disable=too-many-arguments
        self,
        sign,
        integer_part,
        non_repeating_part,
        repeating_part,
        base,
        validate=True,
        canonicalize=True
    ):
        """
        Initializer.

        :param int sign: -1, 0, or 1 as appropriate
        :param integer_part: the part on the left side of the radix
        :type integer_part: list of int
        :param non_repeating_part: non repeating part on left side
        :type non_repeating_part: list of int
        :param repeating_part: repeating part
        :type repeating_part: list of int
        :param int base: base of the radix, must be at least 2
        :param bool validate: if True, validate the arguments
        :param bool canonicalize: if True, canonicalize

        Validation and canonicalization are expensive and may be omitted.

        Complexity: polynomial in number of digits if canonicalize is True,
        linear if validate is True, otherwise constant time
        """
        if validate:
            error = self._validate(
               sign,
               integer_part,
               non_repeating_part,
               repeating_part,
               base
            )
            if error is not None:
                raise error

        if canonicalize:
            if all(x == 0 for x in integer_part):
                integer_part = []

            repeating_part = \
               repeating_part[0:self._repeat_length(repeating_part)]
            (non_repeating_part, repeating_part) = \
                self._canonicalize_fraction(non_repeating_part, repeating_part)
            if all(x == 0 for x in repeating_part):
                repeating_part = []

            if repeating_part == [base - 1]:
                repeating_part = []
                (carry_out, non_repeating_part) = \
                   Nats.carry_in(non_repeating_part, 1, base)
                if carry_out != 0:
                    (carry_out, integer_part) = \
                       Nats.carry_in(integer_part, 1, base)
                    if carry_out != 0:
                        integer_part = [carry_out] + integer_part

            if integer_part == [] and repeating_part == [] and \
               all(x == 0 for x in non_repeating_part):
                sign = 0

        self.sign = sign
        self.base = base
        self.integer_part = integer_part
        self.non_repeating_part = non_repeating_part
        self.repeating_part = repeating_part

    def __str__(self):
        if self.STR_CONFIG is None or self.STR_IMPL is None: # pragma: no cover
            return repr(self)
        else: # pragma: no cover
            return self.STR_IMPL(self.STR_CONFIG, self.base).xform(
               self.sign,
               self.integer_part,
               self.non_repeating_part,
               self.repeating_part,
               0
            )

    def __repr__(self):
        return 'Radix(%s,%s,%s,%s,%s)' % \
           (
              self.sign,
              self.integer_part,
              self.non_repeating_part,
              self.repeating_part,
              self.base
           )

    def __eq__(self, other):
        if not isinstance(other, Radix):
            raise BasesInvalidOperationError("!=", other)
        return self.sign == other.sign and \
           self.integer_part == other.integer_part and \
           self.non_repeating_part == other.non_repeating_part and \
           self.repeating_part == other.repeating_part and \
           self.base == other.base

    def __ne__(self, other):
        if not isinstance(other, Radix):
            raise BasesInvalidOperationError("!=", other)
        return self.sign != other.sign or \
           self.integer_part != other.integer_part or \
           self.non_repeating_part != other.non_repeating_part or \
           self.repeating_part != other.repeating_part or \
           self.base != other.base

    def __lt__(self, other):
        raise BasesInvalidOperationError("<")

    def __gt__(self, other):
        raise BasesInvalidOperationError(">")

    def __le__(self, other):
        raise BasesInvalidOperationError("<=")

    def __ge__(self, other):
        raise BasesInvalidOperationError(">=")

    def __abs__(self):
        return Radix(
           abs(self.sign),
           self.integer_part[:],
           self.non_repeating_part[:],
           self.repeating_part[:],
           self.base
        )

    def __neg__(self):
        return Radix(
           -self.sign,
           self.integer_part[:],
           self.non_repeating_part[:],
           self.repeating_part[:],
           self.base
        )

    def __pos__(self):
        return Radix(
           self.sign,
           self.integer_part[:],
           self.non_repeating_part[:],
           self.repeating_part[:],
           self.base
        )

    def __copy__(self): # pragma: no cover
        return Radix(
           self.sign,
           self.integer_part,
           self.non_repeating_part,
           self.repeating_part,
           self.base
        )

    def __deepcopy__(self, memo):
        return Radix(
           self.sign,
           self.integer_part[:],
           self.non_repeating_part[:],
           self.repeating_part[:],
           self.base
        )

    def __hash__(self):
        blob = [self.sign] + \
           self.integer_part + self.non_repeating_part + self.repeating_part + \
           [self.base]
        return hash(sum(blob))

    def as_rational(self):
        """
        Return this value as a Rational.

        :returns: this radix as a rational
        :rtype: Rational
        """
        (denominator, numerator) = \
           NatDivision.undivision(
              self.integer_part,
              self.non_repeating_part,
              self.repeating_part,
              self.base
           )
        result = Fraction(
           Nats.convert_to_int(numerator, self.base),
           Nats.convert_to_int(denominator, self.base)
        )
        return result * self.sign

    def as_int(self, method):
        """
        This value as an int, rounded according to ``method``.

        :param method: rounding method
        :raises BasesValueError: on bad parameters

        :returns: corresponding int value and relation to original value
        :rtype: int * Rational
        """
        (new_radix, relation) = self.rounded(0, method)
        value = Nats.convert_to_int(new_radix.integer_part, new_radix.base)
        return (value * self.sign, relation)

    def rounded(self, precision, method):
        """
        This value with fractional part rounded to ``precision`` digits
        according to ``method``.

        :param int precision: number of digits in total
        :param method: rounding method
        :returns: a rounded value and its relation to the actual
        :rtype: Radix * Rational
        :raises BasesValueError: on bad parameters

        Precondition: Radix is valid and canonical

        Complexity: O(len(components))
        """
        return _Rounding.roundFractional(self, precision, method)

    def in_base(self, base):
        """
        Return value in ``base``.

        :returns: Radix in ``base``
        :rtype: Radix
        :raises ConvertError: if ``base`` is less than 2
        """
        if base == self.base:
            return copy.deepcopy(self)
        (result, _) = Radices.from_rational(self.as_rational(), base)
        return result

    @property
    def ulp(self):
        """
        The unit of least precision of this value.

        If the Radix has a repeating portion, then there is no ULP, by
        definition, and None is returned.

        If the radix has no digits in the non-repeating portion, then its
        ULP is 1.

        :return: the ULP or None
        :rtype: Rational or NoneType
        """
        if self.repeating_part != []:
            return None

        return Fraction(1, self.base ** len(self.non_repeating_part))


class _Rounding(object):
    """
    Rounding of radix objects.
    """
    # pylint: disable=too-few-public-methods

    @staticmethod
    def _truncated(value, precision):
        """
        Get ``value`` truncated to ``precision``.

        :param Radix value: the value to truncate
        :param int precision: the precision to truncate to

        :returns: the truncated value
        :rtype: Radix

        Preconditions: value.sign > 0
        """
        digits = itertools.chain(
           value.non_repeating_part,
           itertools.cycle(value.repeating_part)
        )

        non_repeating_part = list(itertools.islice(digits, 0, precision))
        non_repeating_part += (precision - len(non_repeating_part)) * [0]

        return Radix(1, value.integer_part, non_repeating_part, [], value.base)

    @classmethod
    def _round_positive(cls, value, precision, method):
        """
        Round ``value`` to ``precision`` using ``method`` assuming positive.

        :param Radix value: the value, must be positive
        :param int precision: the precision
        :param method: the rounding method
        :type method: member of RoundingMethods.METHODS()

        :returns: the rounded value and its relation
        :rtype: Radix * Rational
        """
        base = value.base

        truncated = cls._truncated(value, precision)

        len_non_repeating = len(value.non_repeating_part)
        if precision <= len_non_repeating:
            fractional_part = Radix(
               1,
               [],
               value.non_repeating_part[precision:],
               value.repeating_part,
               base
            )
        elif value.repeating_part == []:
            fractional_part = Radix(0, [], [], [], base)
        else:
            index = \
               (precision - len_non_repeating) % len(value.repeating_part)
            repeating_part = value.repeating_part[index:] + \
               value.repeating_part[:index]
            fractional_part = Radix(1, [], [], repeating_part, base)

        remainder = fractional_part.as_rational()
        if remainder == 0:
            return (truncated, 0)

        if Rounding.rounding_up(remainder, Fraction(1, 2), method):
            (carry_out, non_repeating_part) = \
               Nats.carry_in(truncated.non_repeating_part, 1, base)

            integer_part = truncated.integer_part
            if carry_out != 0:
                (carry_out, integer_part) = \
                   Nats.carry_in(integer_part, carry_out, base)
            if carry_out != 0:
                integer_part = [carry_out] + integer_part

            return (
               Radix(1, integer_part, non_repeating_part, [], base),
               1 - remainder
            )
        else:
            return (truncated, -remainder)

    @classmethod
    def roundFractional(cls, value, precision, method):
        """
        Round to precision as number of digits after radix.

        :param Radix value: value to round
        :param int precision: number of digits in total
        :param method: rounding method
        :raises BasesValueError: on bad parameters

        :returns: the rounded value and its relation to the actual
        :rtype: Radix * Rational

        Precondition: Radix is valid and canonical

        Complexity: O(len(components))
        """

        if precision < 0:
            raise BasesValueError(
               precision,
               "precision",
               "must be at least 0"
            )

        if method not in RoundingMethods.METHODS():
            raise BasesValueError(
               method,
               "method",
               "must be one of RoundingMethod.METHODS()"
            )

        if value.sign == 0:
            return (Radix(0, [], precision * [0], [], value.base), 0)

        use_value = abs(value)
        use_method = method if value.sign > 0 else Rounding.reverse(method)

        (result, relation) = \
           cls._round_positive(use_value, precision, use_method)

        if value != use_value:
            return (-result, -relation)
        else:
            return (result, relation)
