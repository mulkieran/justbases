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

from justbases import BaseConfig
from justbases import DisplayConfig
from justbases import Radix
from justbases import StripConfig

from hypothesis import strategies


def build_nat(base, max_len):
    """
    Build a well-formed nat strategy from ``base``.
    """
    ints = strategies.integers(min_value=0, max_value=(base - 1))
    nats = strategies.lists(ints, min_size=1, max_size=max_len)
    return \
       nats.map(lambda l: list(itertools.dropwhile(lambda x: x == 0, l)))

def build_base(max_base):
    """
    Builds a base.

    :param int max_base: the maximum base
    """
    return strategies.integers(min_value=2, max_value=max_base)

def build_nat_with_base(max_base, max_len):
    """
    Builds a nat and its base.
    :param int max_base: the maximum base
    :param int max_len: the maximum number of digits in the nat

    :returns: a strategy from which can be drawn a pair, a nat and its base
    """
    return build_base(max_base).flatmap(
       lambda n: strategies.tuples(
          build_nat(n, max_len),
          strategies.just(n)
       )
    )

def build_nat_with_base_and_carry(max_base, max_len):
    """
    Build a nat with a base and also a valid carry in value.
    :param int max_base: the maximum base
    :param int max_len: the maximum number of digits in the nat

    :returns: a strategy from which is drawn a triple, nat, base, carry-in
    """
    def the_func(x):
        """
        From a nat and base generally a valid carry-in value.

        :param x: a nat and a corresponding base
        :type x: tuple of (list of int) * int
        :returns: strategies that yields triple of nat, base, carry-in
        """
        (nat, base) = x
        return strategies.tuples(
           strategies.just(nat),
           strategies.just(base),
           strategies.integers(min_value=0, max_value=base - 1)
        )

    return build_nat_with_base(max_base, max_len).flatmap(the_func)

def build_precision(min_value, max_value):
    """
    Build a precision value.

    :param int min_value: the minimum allowable precision, may be negative
    :param int max_value: the maximum allowable precision, may be negative

    May return None, which means no precision specified.
    """
    return strategies.one_of(
       strategies.just(None),
       strategies.integers(min_value, max_value)
    )

def build_sign():
    """
    Build a sign value.
    """
    return strategies.integers(min_value=-1, max_value=1)

build_relation = build_sign

def build_radix(max_base, max_len):
    """
    Build a well-formed Radix strategy.

    :param int max_base: maximum value for a numeric base
    :param int max_len: the maximum length for the component lists
    """

    def make_radix(base):
        """
        Build a radix from base.

        :param int base: the base of the radix
        """
        list1 = build_nat(base, max_len)
        list2 = build_nat(base, max_len)
        list3 = build_nat(base, max_len)
        if list1 == [] and list2 == [] and list3 == []:
            return strategies.builds(
               Radix,
               strategies.just(0),
               list1,
               list2,
               list3,
               strategies.just(base)
            )
        else:
            return strategies.builds(
               Radix,
               strategies.sampled_from((-1, 1)),
               list1,
               list2,
               list3,
               strategies.just(base)
            )

    return build_base(max_base).flatmap(make_radix)


def build_display_config(
   approx_config,
   base_config,
   digits_config,
   strip_config
):
    """
    Builds a well-formed display configuration.

    :param BaseConfig base_config: the base config
    :param DigitsConfig digits_config: the digits config
    :param StripConfig strip_config: the strip config
    """
    return strategies.builds(
       DisplayConfig,
       approx_config=approx_config,
       base_config=base_config,
       digits_config=digits_config,
       strip_config=strip_config
    )

def build_strip_config():
    """
    Build strip config.
    """
    return strategies.builds(
       StripConfig,
       strategies.booleans(),
       strategies.booleans(),
       strategies.booleans()
    )

def build_base_config():
    """
    Build base config.
    """
    return strategies.builds(
       BaseConfig,
       strategies.booleans(),
       strategies.booleans()
    )
