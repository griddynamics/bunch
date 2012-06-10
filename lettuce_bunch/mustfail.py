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

import re
import yaml

MF_ID_KEYWORD = "MF"
MF_COMMENT_KEYWORD = "Comment"
MF_SIGNATURE = "#MF:"
MF_PATTERN = re.compile("([ \t]*#MF:.*(\r\n?|\n)([ \t]*#([^M][^F][^:])?.*(\r\n?|\n))*)")

def occurence_ranges(occs, text):
    pairs = []
    for occ in occs:
        pos = text.find(occ, pairs[-1][-1] if len(pairs) > 0 else None)
        if pos >= 0:
            pairs.append((pos, pos+len(occ)))
    return pairs

def line_ranges(text):
    return occurence_ranges(text.splitlines(True), text)

def pattern_occurences(regexp, text):
    def filter_tuples(match):
        if isinstance(match, tuple):
            return match[0]
        return match

    matches = map(filter_tuples,regexp.findall(text))
    return occurence_ranges(matches, text)

class InplaceMustfailParser(object):
    """
    MF is the commented YAML text, having the following convention:
    MF - field for MF id
    Comment - field for comments
    Other fields may be introduced in later versions

    Example 1:
    #MF: BUG-45
    #Comment: |
    # first line of comment
    # last line

    Example 2:
    #MF: http://mybugtracker/ID33
    #Comment: bla bla bla
    """

    def __init__(self, feature):
        self.feature_text = feature.original_string
        self.mf_occs = pattern_occurences(MF_PATTERN, feature.original_string)
        self.line_occs = line_ranges(feature.original_string)
        self.linenum2mf = self.__map_lines_mfs()
        self.mf_dict = self.__as_dict(feature)

    def __map_lines_mfs(self):
        def mf_on_line(mf, line):
            line_start, line_end = line
            mf_start, mf_end = mf
            mf_end = mf_end if mf_start == mf_end else mf_end-1
            return line_start <= mf_end < line_end

        nline2mf = {}
        try:
            nlines = enumerate(self.line_occs)
            n, line = next(nlines)
            for mf in self.mf_occs:
                while True:
                    if mf_on_line(mf, line):
                        nline2mf[n+1] = mf
                        break
                    n, line = next(nlines)
        except StopIteration:
            pass
        return nline2mf

    def __len__(self):
        return len(self.mf_dict)

    def __item_under_mf(self,linenum):
        return (linenum-1) in self.linenum2mf

    def __mf_text_for_line(self, linenum):
        start, end =  self.linenum2mf[linenum-1]
        return self.feature_text[start:end]

    def __create_mf_item(self, pattern, mf_text, linenum):
        text = mf_text.replace("#", "")
        d = yaml.load(text)
        result = {'pattern' : pattern}
        if MF_ID_KEYWORD in d:
            result["id"] = d[MF_ID_KEYWORD]
        if MF_COMMENT_KEYWORD in d:
            result['comment'] = d[MF_COMMENT_KEYWORD]
        result['line'] = linenum
        return result

    def __check_add_mf(self, linenum, name, lst_to_add):
        if self.__item_under_mf(linenum):
            lst_to_add.append(
                self.__create_mf_item('.*?{name}.*?'.format(name=name),
                                        self.__mf_text_for_line(linenum),
                                        linenum))

    def as_dict(self):
        return self.mf_dict

    def __as_dict(self, feature):
        mf = {}
        mf_scenarios = []
        mf_steps = []
        mf_features = []

        self.__check_add_mf(feature.described_at.line, feature.name, mf_features)

        for scenario in feature.scenarios:
            self.__check_add_mf(scenario.described_at.line, scenario.name, mf_scenarios)
            for step in scenario.steps:
                self.__check_add_mf(step.described_at.line, step.sentence, mf_steps)

        if len(mf_features) > 0:
            mf['features'] = mf_features
        if len(mf_scenarios) > 0:
            mf['scenarios'] = mf_scenarios
        if len(mf_steps) > 0:
            mf['steps'] = mf_steps

        return {'MustFail': mf} if len(mf) > 0 else {}

