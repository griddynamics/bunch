# -*- coding: utf-8 -*-
# <Bunch - BDD test tool for Lettuce scenarios>
# Copyright (c) 2012 Grid Dynamics Consulting Services, Inc, All Rights Reserved
# http://www.griddynamics.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


from lettuce_bunch.exceptions import CyclicDependencySpecification
from nose.tools import assert_equals, assert_raises
from lettuce_bunch.dependencies import combine_fixture_deps, dependency_lists_to_pairs, dependency_groups_to_pairs
from tests.asserts import assert_element_wise_equals, flatten, print_iterable

def test_deplist_to_pairs():
    deplist1 = ['adf', 'abc', 'gh', 'ceg', 'bdeh']
    result = dependency_lists_to_pairs(deplist1)
    expected = [('a', 'd'),
        ('d', 'f'),
        ('a', 'b'),
        ('b', 'c'),
        ('g', 'h'),
        ('c', 'e'),
        ('e', 'g'),
        ('b', 'd'),
        ('d', 'e'),
        ('e', 'h')]
    assert_equals(list(result), expected)

def test_dependency_grops_to_pairs():
    assert_equals(
        list(dependency_groups_to_pairs([['a', 'b'], ['c'], ['d']])),
        [('a', 'c'), ('b', 'c'), ('c', 'd')])
    assert_equals(
        list(dependency_groups_to_pairs([['a', 'b'], [], ['d']])),
        [])
    assert_equals(
        list(dependency_groups_to_pairs([[1, 2], [3, 4], [5, 6]])),
        [(1, 3), (1, 4), (2, 3), (2, 4), (3, 5), (3, 6), (4, 5), (4, 6)])

#TODO: Convert flattened assert to structured one when concurrent is ready

def test_combine_fixtures_basic():
    grouplist1 = [
        [   ['single-node'],
            ['novaclient-users' , 'novaclient-network'],
            ['novaclient-images'] , ['novaclient-keys'], ['novaclient-flatnetwork']  ],
        [   ['single-node'],
            ['novaclient-users' , 'novaclient-network'],
            ['novaclient-images'],
            ['novaclient-keys']  ],
        [   ['single-node'],
            ['novaclient-users', 'novaclient-network'],
            ['novaclient-images'],
            ['novaclient-keys'],
            ['volume-services'],
            ['volume']  ]   ]
    result = combine_fixture_deps(grouplist1)
    expected = ['single-node',
                'novaclient-network',
                'novaclient-users',
                'novaclient-images',
                'novaclient-keys',
                'novaclient-flatnetwork',
                'volume-services',
                'volume']
    assert_equals(list(flatten(result)), expected)

def test_combine_fixtures_cyclic():
    grouplist2 = [
        [   ['a'], ['b'], ['c']  ],
        [   ['c'], ['b'], ['a']  ]  ]
    #print_iterable(combine_fixture_deps(grouplist2))
    assert_raises(CyclicDependencySpecification, combine_fixture_deps, grouplist2)

def test_one_solitary_dep():
    grouplist = [
        [   ['one'] ]  ]
    assert_equals(list(flatten(combine_fixture_deps(grouplist))), ['one'])

def test_several_solitary_deps():
    grouplist = [
        [   ['one'] ], [   ['two'] ], [   ['three'] ]  ]
    assert_equals(list(flatten(combine_fixture_deps(grouplist))), ['one', 'two', 'three'])

def test_empty_deps():
    grouplist = [
        [ [] ]  ]
    assert_equals(list(flatten(combine_fixture_deps(grouplist))), [])

def test_several_empty_deps():
    grouplist = [
        [ [] ]  ]
    assert_equals(
        list(flatten(combine_fixture_deps(grouplist))),
        [])

def test_empties_and_solitaries_deps():
    grouplist = [
        [ [] ], [   ['one'] ], [ [] ], [   ['two'] ], [ [] ],[   ['three'] ], [ [] ]  ]
    assert_equals(
        list(flatten(combine_fixture_deps(grouplist))),
        ['one', 'two', 'three'])

def test_empties_solitaries_and_usual_deps():
    grouplist = [
        [ [] ], [   ['one'] ], [ [] ], [   ['two'] ], [ [] ],[   ['three'] ], [ [] ], [['four'], ['five'], ['six']], [ [] ]  ]
    assert_equals(
        list(flatten(combine_fixture_deps(grouplist))),
        ['four', 'five', 'six', 'one', 'two', 'three'])

def test_independent_deps():
    grouplist = [
        [ ['1','2','3'], ['4'], ['5'] ]   ]
    assert_equals(
        list(flatten(combine_fixture_deps(grouplist))),
        ['1', '2', '3', '4', '5'])

def test_independent_single_deps():
    grouplist = [
        [ ['1','2','3' ,'4', '5'] ]   ]
    assert_equals(
        list(flatten(combine_fixture_deps(grouplist))),
        ['1', '2', '3', '4', '5'])

def test_empties_solitaries_indepent_and_usual_deps():
    grouplist = [
        [ [] ],
        [ ['one'] ],
        [ [] ],
        [ ['two'] ],
        [ [] ],
        [ ['three'] ],
        [ [] ],
        [ ['four'], ['five'], ['six']],
        [ [] ],
        [ ['seven','eight', 'nine'] ],
        [ [] ] ]
    assert_equals(
        list(flatten(combine_fixture_deps(grouplist))),
        ['four', 'five', 'six', 'one', 'two', 'three', 'seven', 'eight', 'nine'])

def test_no_solitary_duplication():
    grouplist =[[],
        [[u'single-node.clean.setup'], [u'keystone-init.setup'], [u'keystone-user.setup'], [u'novaclient-network.setup'], [u'novarc-keystone.setup'], [u'novaclient-images.setup'], [u'novaclient-keys.setup']],
        [[u'novaclient-keys.setup']],
        [],
        [[u'single-node.clean.setup'], [u'novaclient-users.setup'], [u'novaclient-network.setup'], [u'novaclient-images.setup'], [u'novaclient-keys.setup']],
        [[u'lvm.setup']]]
    assert_equals(
        list(flatten(combine_fixture_deps(grouplist))),
        list(flatten([[u'single-node.clean.setup'],
            [u'keystone-init.setup', u'novaclient-users.setup'],
            [u'keystone-user.setup'],
            [u'novaclient-network.setup'],
            [u'novarc-keystone.setup'],
            [u'novaclient-images.setup'],
            [u'novaclient-keys.setup'],
            [u'lvm.setup']])))
