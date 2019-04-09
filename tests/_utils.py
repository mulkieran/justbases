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
        return strategies.builds(
           Radix,
           strategies.sampled_from((-1, 1)),
           list1,
           list2,
           list3,
           strategies.just(base)
        )

    return build_base(max_base).flatmap(make_radix)


def build_display_config(base_config, digits_config, strip_config):
    """
    Builds a well-formed display configuration.

    :param BaseConfig base_config: the base config
    :param DigitsConfig digits_config: the digits config
    :param StripConfig strip_config: the strip config
    """
    return strategies.builds(
       DisplayConfig,
       show_approx_str=strategies.booleans(),
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
