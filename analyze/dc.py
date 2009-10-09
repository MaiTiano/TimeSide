# -*- coding: utf-8 -*-
#
# Copyright (c) 2007-2009 Guillaume Pellerin <yomguy@parisson.com>

# This file is part of TimeSide.

# TimeSide is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.

# TimeSide is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with TimeSide.  If not, see <http://www.gnu.org/licenses/>.

# Author: Guillaume Pellerin <yomguy@parisson.com>

from timeside.analyze.core import *
from timeside.analyze.api import IAnalyzer
import numpy

class MeanDCShiftAnalyser(AudioProcessor):
    """Media item analyzer driver interface"""

    implements(IAnalyzer)

    def id(self):
        return "dc"

    def name(self):
        return "Mean DC shift"

    def unit(self):
        return "%"

    def render(self, media_item, options=None):
        self.pre_process(media_item)
        samples = self.get_mono_samples()
        return numpy.round(100*numpy.mean(samples),4)