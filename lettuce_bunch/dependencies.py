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

from exceptions import CyclicDependencySpecification
from topsort import topsort_levels,CycleError
from itertools import chain, tee, izip, product

def pairwise(iterable):
    a, b = tee(iterable)
    next(b)
    return izip(a, b)

def dependency_lists_to_pairs(dependency_lists):
    return chain(*(pairwise(dep_list) for dep_list in dependency_lists))

def dependency_groups_to_pairs(groups):
    return chain(*(product(a,b) for a,b in pairwise(groups)))

def split_solitaries(deps):
    solitaries = []
    linked = []
    for dep in deps:
        if len(dep) == 1 and len(dep[0]) > 0:
            solitaries.append(dep[0])
        else:
            linked.append(dep)
    return solitaries, linked

def filter_empties(deps):
    return filter(None, deps)

def combine_fixture_deps(deps):
    solitaries, linked = split_solitaries(filter_empties(deps))
    try:
        result = [sorted(group) for group in topsort_levels(chain(*map(dependency_groups_to_pairs, linked)))]
        for solitary in solitaries:
            if solitary not in result:
                result.append(solitary)
    except CycleError as cycle_details:
        raise CyclicDependencySpecification(cycle_details)

    return result

