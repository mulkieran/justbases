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
# 02110-1301, USA.  Any Red Hat trademarks that are incorporated in the
# source code or documentation are not subject to the GNU General Public
# License and may only be used or replicated with the express permission of
# Red Hat, Inc.
#
# Anne Mulhern <mulhern@cs.wisc.edu>

"""
The public interface of justbases.

Contents:

  * RoundingMethods -- a list of available rounding methods
  * NatDivision -- long division of natural numbers and its inverse
  * ConvertError -- error raised by conversion functions
  * Nats

    - conversion between non-negative ints and sequences
    - conversion between sequences in one base to sequences in another
  * Radix -- representation of rational number as string of digits
  * Rationals

    - conversion between Rational and Radix objects
    - conversion between Radix objects in any base
  * Rounding -- rounding Radix values according to methods
"""

from ._constants import RoundingMethods
from ._division import NatDivision
from ._errors import ConvertError
from ._nats import Nats
from ._radix import Radix
from ._radix import Rounding
from ._rationals import Rationals

from .version import __version__
