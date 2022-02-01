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
from justbases import RoundingMethods


class RoundingMethodsTestCase(unittest.TestCase):
    """Tests for RoundingMethods constants."""

    def test_str(self):
        """
        Test __str__ and __repr__ method.
        """
        for method in RoundingMethods.METHODS():
            self.assertIsNotNone(str(method))
            self.assertIsNotNone(repr(method))
