# Copyright (C) 2016 Anne Mulhern
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

""" Test utilities. """

from __future__ import absolute_import

import itertools

from hypothesis import strategies


def build_nat(base, max_len):
    """
    Build a well-formed nat strategy from ``base``.
    """
    ints = strategies.integers(min_value=0, max_value=(base - 1))
    nats = strategies.lists(ints, min_size=1, max_size=max_len)
    nats = \
       nats.map(lambda l: list(itertools.dropwhile(lambda x: x == 0, l)))
    return nats.filter(lambda l: len(l) > 0)
