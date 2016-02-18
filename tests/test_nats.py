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

""" Test for integer conversions. """

from __future__ import absolute_import

import itertools
import unittest
import random

from hypothesis import given
from hypothesis import strategies

from justbases import BasesError
from justbases import Nats

class NatsTestCase(unittest.TestCase):
    """ Tests for ints. """

    @given(
       strategies.integers(min_value=0),
       strategies.integers(min_value=2),
    )
    def testFromInt(self, value, to_base):
        """
        convert_to_int(convert_from_int(value, to_base), 10) == value
        """
        result = Nats.convert_from_int(value, to_base)
        assert Nats.convert_to_int(result, to_base) == value

    @given(
       strategies.integers(min_value=1, max_value=63),
       strategies.integers(min_value=2, max_value=64),
       strategies.integers(min_value=2, max_value=64)
    )
    def testFromOther(self, length, from_base, to_base):
        """ Test roundtrip from number in arbitrary base. """
        subject = [random.randint(0, from_base - 1) for _ in range(length)]
        result = Nats.convert(subject, from_base, to_base)
        assert Nats.convert_to_int(result, to_base) == \
            Nats.convert_to_int(subject, from_base)

    def testExceptions(self):
        """ Test throwing exception. """
        with self.assertRaises(BasesError):
            Nats.convert_from_int(-32, 2)
        with self.assertRaises(BasesError):
            Nats.convert_from_int(32, -2)
        with self.assertRaises(BasesError):
            Nats.convert([1], 1, 2)
        with self.assertRaises(BasesError):
            Nats.convert([1], 2, 1)
        with self.assertRaises(BasesError):
            Nats.convert_to_int([1], 1)
        with self.assertRaises(BasesError):
            Nats.convert_to_int([-1], 2)
        with self.assertRaises(BasesError):
            Nats.carry_in([-1], 1, 2)
        with self.assertRaises(BasesError):
            Nats.carry_in([1], -1, 2)
        with self.assertRaises(BasesError):
            Nats.carry_in([1], 1, 1)

    @given(
       strategies.lists(strategies.integers(min_value=0)),
       strategies.integers(min_value=0)
    )
    def testCarryIn(self, value, carry):
        """
        Test carry_in.

        :param value: the value
        :type value: list of int
        :param int carry: the carry (>= 0)
        """
        value = list(itertools.dropwhile(lambda x: x == 0, value))

        base = max(max(value + [carry]) + 1, 2)
        (carry_out, result) = Nats.carry_in(value, carry, base)
        assert len(result) == len(value)

        result2 = Nats.convert_from_int(
           Nats.convert_to_int(value, base) + carry,
           base
        )

        assert len(result2) >= len(result)

        assert (len(result2) == len(result)) or \
           result2[0] == carry_out and result2[1:] == result

        assert not (len(result2) == len(result)) or result2 == result
