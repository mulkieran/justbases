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

"""
The public interface of justbases.

Contents:

  * RoundingMethods -- a list of available rounding methods
  * NatDivision -- long division of natural numbers and its inverse
  * BasesError -- supertype of errors raised by package methods
  * Nats

    - conversion between non-negative ints and sequences
    - conversion between sequences in one base to sequences in another
  * Radix -- representation of rational number as string of digits
  * Rationals

    - conversion between Rational and Radix objects
    - conversion between Radix objects in any base
  * String -- display of Radices
"""

from ._config import BaseConfig, BasesConfig, DigitsConfig, DisplayConfig, StripConfig
from ._constants import RoundingMethods
from ._display import String
from ._division import NatDivision
from ._errors import BasesError
from ._nats import Nats
from ._rationals import Radices, Radix, Rationals
from .version import __version__
