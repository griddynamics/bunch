import re
from nose.tools import assert_equals, assert_not_equals, assert_false, assert_true
from utils import regex_exact_match


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

def assert_matches(text, regexp, msg=None):
    regexp = re.compile(regexp)
    msg = msg or "Regexp didn't match"
    msg = '%s: %r not found in %r' % (msg, regexp.pattern, text)
    assert_not_equals(regexp.search(text), None, msg)

def assert_not_matches(text, regexp, msg=None):
    regexp = re.compile(regexp)
    msg = msg or "Regexp matched"
    msg = '%s: %r was found in %r' % (msg, regexp.pattern, text)
    assert_equals(regexp.search(text), None, msg)

def assert_feature_matches(text, feature_regexp, msg=None):
    RE_ANYTHING = '([\s\S])*?'
    FEATURE_KEYWORD = "Feature:"
    feature_before_regex = "{anything}{feature}{anything}{pattern}{anything}".format(
        anything=RE_ANYTHING, feature=FEATURE_KEYWORD, pattern=feature_regexp)
    feature_after_regex = "{anything}{pattern}{anything}{feature}{anything}".format(
        anything=RE_ANYTHING, feature=FEATURE_KEYWORD, pattern=feature_regexp)

    assert_matches(text, feature_regexp, "Feature pattern did not match")
    assert_false(regex_exact_match(feature_before_regex, text), "Extra feature before expected feature pattern")
    assert_false(regex_exact_match(feature_after_regex, text), "Extra feature after expected feature pattern")









