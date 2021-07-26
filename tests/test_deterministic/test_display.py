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

""" Test for utility functions. """

# isort: STDLIB
import unittest

# isort: LOCAL
from justbases import BasesConfig, BasesError
from justbases._display import Digits


class TestDigits(unittest.TestCase):
    """
    Test Digits methods.
    """

    def test_exceptions(self):
        """
        Test exceptions.
        """
        with self.assertRaises(BasesError):
            # pylint: disable=protected-access
            Digits(
                BasesConfig.DISPLAY_CONFIG.digits_config,
                Digits._MAX_SIZE_BASE_FOR_CHARS + 1,
            )
