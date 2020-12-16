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

""" Test for rational conversions. """

# isort: STDLIB
import unittest
from fractions import Fraction

# isort: LOCAL
from justbases import BasesError, Radices, Rationals


class RationalsTestCase(unittest.TestCase):
    """ Tests for rationals. """

    def testExceptions(self):
        """
        Test exceptions.
        """
        with self.assertRaises(BasesError):
            Radices.from_rational(Fraction(1, 2), 0)
        with self.assertRaises(BasesError):
            Radices.from_rational(Fraction(1, 2), 2, -1)

    def testRoundingExceptions(self):
        """
        Test exceptions.
        """
        # pylint: disable=pointless-statement
        with self.assertRaises(BasesError):
            Rationals.round_to_int(Fraction(1, 2), None)
