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

# isort: LOCAL
from justbases import BasesError, Nats


class NatsTestCase(unittest.TestCase):
    """ Tests for ints. """

    def test_exceptions(self):
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
