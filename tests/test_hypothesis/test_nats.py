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

""" Test for integer conversions. """

# isort: STDLIB
import unittest
from os import sys

# isort: THIRDPARTY
from hypothesis import given, settings, strategies

# isort: LOCAL
from justbases import Nats

# isort considers this third party, but it is not
from tests.test_hypothesis._utils import build_nat  # isort:skip

if sys.gettrace() is not None:
    settings.load_profile("tracing")

_NATS_STRATEGY = strategies.integers(min_value=2).flatmap(
    lambda n: strategies.tuples(build_nat(n, 64), strategies.just(n))
)


class NatsTestCase(unittest.TestCase):
    """Tests for ints."""

    @given(
        strategies.integers(min_value=0),
        strategies.integers(min_value=2),
    )
    def test_from_int(self, value, to_base):
        """
        convert_to_int(convert_from_int(value, to_base), 10) == value
        No leading zeros in convert_from_int(value, to_base)
        """
        result = Nats.convert_from_int(value, to_base)
        self.assertNotEqual(result[:1], [0])
        self.assertEqual(Nats.convert_to_int(result, to_base), value)

    @given(_NATS_STRATEGY, strategies.integers(min_value=2, max_value=64))
    def test_from_other(self, nat, to_base):
        """Test roundtrip from number in arbitrary base."""
        (subject, from_base) = nat
        result = Nats.convert(subject, from_base, to_base)
        self.assertEqual(
            Nats.convert_to_int(result, to_base),
            Nats.convert_to_int(subject, from_base),
        )

    _CARRY_STRATEGY = strategies.integers(min_value=2).flatmap(
        lambda n: strategies.tuples(
            build_nat(n, 64),
            strategies.integers(min_value=1, max_value=(n - 1)),
            strategies.just(n),
        )
    )

    @given(_CARRY_STRATEGY)
    def test_carry_in(self, strategy):
        """
        Test carry_in.

        :param strategy: the strategy (tuple of value, carry, base)
        """
        (value, carry, base) = strategy
        (carry_out, result) = Nats.carry_in(value, carry, base)
        self.assertEqual(len(result), len(value))

        result2 = Nats.convert_from_int(Nats.convert_to_int(value, base) + carry, base)

        self.assertGreaterEqual(len(result2), len(result))

        self.assertTrue(
            (len(result2) == len(result))
            or result2[0] == carry_out
            and result2[1:] == result
        )

        self.assertTrue(not (len(result2) == len(result)) or result2 == result)
