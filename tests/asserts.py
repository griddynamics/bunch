from nose.tools import assert_equals, assert_not_equals


def flatten(obj):
    if isinstance(obj, basestring):
        yield obj
    try:
        it = iter(obj)
    except TypeError:
        yield obj
    else:
        for i in it:
            if isinstance(i, basestring):
                yield i
            else:
                for j in flatten(i):
                    yield j

def print_iterable(it):
    for item in it:
        print item

def test_flatten():
    assert_equals(list(flatten([1, [2, [3]]])), [1,2,3])


def assert_element_wise_equals(original, expected):
    assert_equals(list(flatten(original)), list(flatten(expected)))




