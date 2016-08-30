# Copyright (C) 2016  Red Hat, Inc.
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
# Red Hat Author(s): Anne Mulhern <amulhern@redhat.com>

""" Generating approximation indicators. """


class ApproxPrefix(object):
    """
    Class that transforms numeric value by prepending an approximation prefix,
    based on the relation. The approximation prefix varies, based on the
    amount of the difference indicated by the relation.
    """
    # pylint: disable=too-few-public-methods

    def __init__(self, limits):
        """
        Initializer.

        :param limits: the limits of the various buckets
        :type limits: list of Rational, may be the empty list

        The limits must be all non-zero and in ascending order.
        """
        self.limits = limits

    @staticmethod
    def _relation_to_symbol(relation):
        """
        Change a numeric relation to a string symbol.

        :param Rational relation: the relation

        :returns: a symbol with the right relation to ``relation`` or None
        :rtype: str or NoneType
        """
        if relation == 0:
            return None
        elif relation < 0:
            return '>'
        elif relation > 0:
            return '<'
        else:
            assert False # pragma: no cover

    def _amount(self, relation):
        """
        Convert relation to an int value.

        :param Rational relation: the relation
        :returns: an int, indicating the category of the relation
        :rtype: int
        """
        if relation == 0: # pragma: no cover
            return 0

        abs_relation = abs(relation)
        return next(
           (i for i, l in enumerate(self.limits) if abs_relation < l),
           len(self.limits)
        ) + 1


    def xform(self, relation, value):
        """
        Decorate ``value`` with approximation indicator for ``relation``.

        :param Rational relation: relation of ``value`` to value it represents
        :param str value: a value to decorate
        """
        approx_str = ApproxPrefix._relation_to_symbol(relation)
        if approx_str is not None:
            return "%s %s" % (approx_str * self._amount(relation), value)
        else:
            return value
