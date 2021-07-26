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

# isort: LOCAL
from justbases import BasesError, Radix, RoundingMethods


class RadixTestCase(unittest.TestCase):
    """ Tests for radix. """

    def test_exceptions(self):
        """
        Test exceptions.
        """
        with self.assertRaises(BasesError):
            Radix(0, [], [], [], 0)
        with self.assertRaises(BasesError):
            Radix(1, [], [], [2], 2)
        with self.assertRaises(BasesError):
            Radix(1, [], [-1], [1], 2)
        with self.assertRaises(BasesError):
            Radix(1, [-300], [1], [1], 2)
        with self.assertRaises(BasesError):
            Radix(True, [1], [0], [1], 2)
        with self.assertRaises(BasesError):
            Radix(1, [1], [0], [1], 2).in_base(0)

    def test_options(self):
        """
        Skip validation and canonicalization.
        """
        self.assertIsNotNone(Radix(-1, [], [], [], 4, False, False))

    def test_equality(self):
        """
        Test == operator.
        """
        self.assertEqual(
            Radix(1, [1], [], [], 2),
            Radix(1, [1], [], [], 2),
        )

    def test_in_equality(self):
        """
        Test != operator.
        """
        self.assertNotEqual(
            Radix(0, [], [], [], 3),
            Radix(0, [], [], [], 2),
        )

    def test_operator_exceptions(self):
        """
        Test that comparsion operators yield exceptions.
        """
        radix1 = Radix(0, [], [], [], 3)
        radix2 = Radix(0, [], [], [], 2)
        # pylint: disable=pointless-statement
        with self.assertRaises(BasesError):
            radix1 > radix2
        with self.assertRaises(BasesError):
            radix1 < radix2
        with self.assertRaises(BasesError):
            radix1 <= radix2
        with self.assertRaises(BasesError):
            radix1 >= radix2
        with self.assertRaises(BasesError):
            radix1 >= 1
        with self.assertRaises(BasesError):
            radix1 == 1
        with self.assertRaises(BasesError):
            radix1 != 1

    def test_carry_on_repeating_part(self):
        """
        Carry from non_repeating_part to integer_part and then out.
        """
        assert Radix(1, [3], [3], [3], 4) == Radix(1, [1, 0], [], [], 4)

    def test_repeating_repeat_part(self):
        """
        Repeat part is made up of repeating parts.
        """
        radix = Radix(1, [], [], [1, 1], 4)
        self.assertEqual(radix.repeating_part, [1])
        radix = Radix(1, [], [], [1, 1, 2], 4)
        self.assertEqual(radix.repeating_part, [1, 1, 2])
        radix = Radix(1, [], [], [1, 2, 1, 2, 1, 2], 4)
        self.assertEqual(radix.repeating_part, [1, 2])
        radix = Radix(1, [], [3, 1, 2, 1, 2], [1, 2], 4)
        self.assertEqual(radix.non_repeating_part, [3])
        self.assertEqual(radix.repeating_part, [1, 2])
        radix = Radix(1, [], [3, 2, 1, 2, 1, 2], [1, 2], 4)
        self.assertEqual(radix.non_repeating_part, [3])
        self.assertEqual(radix.repeating_part, [2, 1])
        radix = Radix(1, [], [3, 3, 2, 3, 1, 2, 3, 1, 2, 3], [1, 2, 3], 4)
        self.assertEqual(radix.non_repeating_part, [3, 3])
        self.assertEqual(radix.repeating_part, [2, 3, 1])


class RoundingTestCase(unittest.TestCase):
    """ Tests for rounding Radixes. """

    def test_exceptions(self):
        """
        Test exception.
        """
        with self.assertRaises(BasesError):
            Radix(0, [], [], [], 2).rounded(-1, RoundingMethods.ROUND_DOWN)
        with self.assertRaises(BasesError):
            Radix(0, [], [], [], 2).rounded(0, None)
