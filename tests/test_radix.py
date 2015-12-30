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

import unittest

from justbases import ConvertError
from justbases import Radix


class RadixTestCase(unittest.TestCase):
    """ Tests for radix. """

    def testExceptions(self):
        """
        Test exceptions.
        """
        with self.assertRaises(ConvertError):
            Radix(True, [], [], [], 0)
        with self.assertRaises(ConvertError):
            Radix(True, [], [], [2], 2)
        with self.assertRaises(ConvertError):
            Radix(True, [], [-1], [1], 2)
        with self.assertRaises(ConvertError):
            Radix(True, [-300], [1], [1], 2)
