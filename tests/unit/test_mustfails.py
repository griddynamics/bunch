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
