from nose.tools import assert_equals, assert_raises, assert_true, assert_false
from lettuce_bunch.mustfail import InplaceMustfailParser
from lettuce import Feature


def test_must_fails_scenario_step():
    txt = """
        #MF is the commented YAML text, having the following convention:
        #MF - field for MF id
        #Comment - field for comments
        #Other fields may be introduced in later versions
        #Regular comments should not break the MF feature
        Feature: feature for test
            As developer I want to have my feature tested

        #Example 1:
            #MF: BUG-45
            #Comment: |
            # first line of comment
            # second line
            # last line
            Scenario: some scenario
               Step 1
               Step 2

        #Example 2:
            Scenario: some another scenario
               #MF: http://mybugtracker/ID33
               #Comment: bla bla bla
               Some step
               Another step

        """
    feature = Feature.from_string(txt, with_file="dummy.txt")
    mfp = InplaceMustfailParser(feature)
    mustfails = mfp.as_dict()
    assert_true('MustFail' in mustfails, "No mustfails found")
    mustfails = mustfails['MustFail']
    assert_equals(len(mustfails), 2, "Not all inplace mustfails found")
    assert_true('scenarios' in mustfails)
    assert_true(len(mustfails['scenarios']) == 1)
    assert_true(len(mustfails['steps']) == 1)

def test_must_fails_feature_scenario_step():
    txt = """
        #MF is the commented YAML text, having the following convention:
        #MF - field for MF id
        #Comment - field for comments
        #Other fields may be introduced in later versions
        #Regular comments should not break the MF feature
        #Here the MF begins
        #MF: NOBUG
        #extrafield: 123
        Feature: feature for test
            As developer I want to have my feature tested

        #Example 1:
            #MF: BUG-45
            #Comment: |
            # first line of comment
            # second line
            # last line
            Scenario: some scenario
               Step 1
               Step 2

        #Example 2:
            Scenario: some another scenario
               #MF: http://mybugtracker/ID33
               #Comment: bla bla bla
               Some step
               Another step

        """
    feature = Feature.from_string(txt, with_file="dummy.txt")
    mfp = InplaceMustfailParser(feature)
    mustfails = mfp.as_dict()
    assert_true('MustFail' in mustfails, "No mustfails found")
    mustfails = mustfails['MustFail']
    assert_equals(len(mustfails), 3, "Not all inplace mustfails found")
    assert_true('scenarios' in mustfails)
    assert_true(len(mustfails['scenarios']) == 1)
    assert_true(len(mustfails['steps']) == 1)
    assert_true(len(mustfails['features']) == 1)

def test_no_must_fails():
    txt = """
        #MF is the commented YAML text, having the following convention:
        #MF - field for MF id
        #Comment - field for comments
        #Other fields may be introduced in later versions
        #Regular comments should not break the MF feature
        #Here the MF begins
        #MF NOBUG
        #extrafield: 123
        Feature: feature for test
            As developer I want to have my feature tested

        #Example 1:
            #MF BUG-45
            #Comment: |
            # first line of comment
            # second line
            # last line
            Scenario: some scenario
               Step 1
               Step 2

        #Example 2:
            Scenario: some another scenario
               #MF http://mybugtracker/ID33
               #Comment: bla bla bla
               Some step
               Another step

        """
    feature = Feature.from_string(txt, with_file="dummy.txt")
    mfp = InplaceMustfailParser(feature)
    mustfails = mfp.as_dict()
    assert_false('MustFail' in mustfails, "must not find mustfails")
