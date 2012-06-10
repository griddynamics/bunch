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


import os.path, pkgutil
from nose.util import isclass
from lettuce_bunch.plugins.base import BaseOutputPlugin
from collections import OrderedDict
import traceback


PLUGIN_CLASS_NAME = 'OutputPlugin'
MODULE_PREFIX = 'lettuce_bunch.plugins'

def plugins_list():
    def filter_no_plugins(module):
        name =  MODULE_PREFIX + ".%s" % module
        try:
            module = __import__(name, fromlist=[PLUGIN_CLASS_NAME])
            module_attrs = dir(module)
            if 'OutputPlugin' in module_attrs:
                plugin = getattr(module, PLUGIN_CLASS_NAME)
                if isclass(plugin):
                    return True
        except ImportError, e:
            str_reason = traceback.format_exc(e)
            return False

        return False

    pkgpath = os.path.dirname(__file__)
    pkglist = filter(filter_no_plugins,[name for _, name, _ in pkgutil.iter_modules([pkgpath])])

    return pkglist

def load_plugin(name, params):
    params = {} if params is None else params
    if name is not None:
        name =  MODULE_PREFIX + ".%s" % name
        module = __import__(name, fromlist=[PLUGIN_CLASS_NAME])
        plugin_class = getattr(module, PLUGIN_CLASS_NAME)
        return plugin_class(**params)
    return BaseOutputPlugin(**params)

class BunchDetails(object):
    def __init__(self, name="", description=""):
        self.name = name
        self.description = description

class BunchResultItem(object):
    def __init__(self, item):
        self.item = item

    def result(self):
        item_result = self.item.find('result')
        if item_result is not None:
            return item_result.text
        return ''

    def get_type(self):
        if self.item.tag == 'feature':
            return 'features'
        elif self.item.tag == 'scenario':
            return 'scenarios'
        elif self.item.tag == 'step':
            return 'steps'

        return None

    def name(self):
        name_path = 'properties/sentence' if self.item.tag == 'step' else 'properties/name'
        item_name = self.item.find(name_path)
        if item_name is not None:
            return item_name.text
        return ''


class BunchResults(object):
    def __init__(self, et):
        self.et = et.find('.')

    def __get_result_map(self, items):
        map = OrderedDict()
        for item in items:
            item_result = item.find('result')
            name_path = 'properties/sentence' if item.tag == 'step' else 'properties/name'
            item_name = item.find(name_path)
            if item_name is not None and item_name.text != '':
                #map[item_name.text] = item_result.text
                map[item] = (item_name.text, item_result.text)
        return map

    def get_by_type(self, item_type):
        type_map = {'features': self.features,
                    'scenarios' : self.scenarios,
                    'steps' : self.steps}

        rez = type_map[item_type]()
        return rez

    def __self_result_map(self):
        return self.__get_result_map(self.et.findall('.'))

    def __len__(self):
        return len(self.features()) + len(self.scenarios()) + len(self.steps())

    def features(self):
        #return self.__get_result_map(self.et.findall('feature'))
        rez =  self.__get_result_map(self.et.findall('.//feature'))
#        if len(rez) == 0 and self.et.tag == 'feature':
#            rez = self.__get_result_map(self.et.findall('.'))
        return rez

    def scenarios(self):
        #return self.__get_result_map(self.et.findall('feature/scenarios/scenario'))
        rez =  self.__get_result_map(self.et.findall('.//scenario'))
#        if len(rez) == 0 and self.et.tag == 'scenario':
#            rez = self.__get_result_map(self.et.findall('.'))
        return rez

    def steps(self):
        #return self.__get_result_map(self.et.findall('feature/scenarios/scenario/steps/step'))
        rez = self.__get_result_map(self.et.findall('.//step'))
#        if len(rez) == 0 and self.et.tag == 'step':
#            rez = self.__get_result_map(self.et.findall('.'))
        return rez

