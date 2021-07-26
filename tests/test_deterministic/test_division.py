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
from justbases import BasesError, NatDivision


class NatDivisionTestCase(unittest.TestCase):
    """ Tests for division. """

    def test_exceptions_division(self):
        """
        Test division exceptions.
        """
        with self.assertRaises(BasesError):
            NatDivision.division([1], [1], -2)
        with self.assertRaises(BasesError):
            NatDivision.division([1], [-1], 3)
        with self.assertRaises(BasesError):
            NatDivision.division([-1], [1], 3)
        with self.assertRaises(BasesError):
            NatDivision.division([], [1], 3)
        with self.assertRaises(BasesError):
            NatDivision.division([0], [1], 3)
        with self.assertRaises(BasesError):
            NatDivision.division([2], [1], 3, -1)
        with self.assertRaises(BasesError):
            NatDivision.division([3], [1], 10, 0, None)

    def test_exceptions_undivision(self):
        """
        Test undivision exceptions.
        """
        with self.assertRaises(BasesError):
            NatDivision.undivision([1], [1], [1], -2)
        with self.assertRaises(BasesError):
            NatDivision.undivision([1], [1], [-1], 2)
        with self.assertRaises(BasesError):
            NatDivision.undivision([1], [-1], [1], 2)
        with self.assertRaises(BasesError):
            NatDivision.undivision([-1], [1], [1], 2)
        with self.assertRaises(BasesError):
            NatDivision.undivision([2], [1], [1], 2)
