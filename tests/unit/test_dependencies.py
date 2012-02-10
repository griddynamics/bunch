from bunch.exceptions import CyclicDependencySpecification
from nose.tools import assert_equals, assert_raises
from bunch.dependencies import combine_fixture_deps, dependency_lists_to_pairs, dependency_groups_to_pairs
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
                'volume-services',
                'novaclient-flatnetwork',
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
        ['1', '3', '2', '4', '5'])

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
