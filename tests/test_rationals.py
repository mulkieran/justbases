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

""" Test for rational conversions. """

from __future__ import absolute_import

from fractions import Fraction

import unittest

from hypothesis import given
from hypothesis import strategies

from justbases import ConvertError
from justbases import Radix
from justbases import Rationals


class RationalsTestCase(unittest.TestCase):
    """ Tests for rationals. """

    @given(
       strategies.fractions(),
       strategies.integers().filter(lambda x: x > 1)
    )
    def testInverses(self, value, to_base):
        """
        Test that functions are inverses of each other.
        """
        result = Rationals.convert_from_rational(value, to_base)
        assert Rationals.convert_to_rational(result) == value

    def testExceptions(self):
        """
        Test exceptions.
        """
        with self.assertRaises(ConvertError):
            Rationals.convert_from_rational(Fraction(1, 2), 0)
        with self.assertRaises(ConvertError):
            Rationals.convert(Radix(True, [], [], [], 2), 0)
