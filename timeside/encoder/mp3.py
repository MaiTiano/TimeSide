    # -*- coding: utf-8 -*-
#
# Copyright (C) 2007-2012 Parisson SARL
# Copyright (c) 2006-2012 Guillaume Pellerin <pellerin@parisson.com>
# Copyright (c) 2010-2012 Paul Brossier <piem@piem.org>
# Copyright (c) 2009-2010 Olivier Guilyardi <olivier@samalyse.com>


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

# Authors: Guillaume Pellerin <yomguy@parisson.com>
#          Paul Brossier <piem@piem.org>

from timeside.core import Processor, implements, interfacedoc
from timeside.encoder.core import GstEncoder
from timeside.api import IEncoder
from timeside.tools import *

import mutagen

class Mp3Encoder(GstEncoder):
    """ gstreamer-based mp3 encoder """
    implements(IEncoder)

    @interfacedoc
    def setup(self, channels=None, samplerate=None, blocksize=None, totalframes=None):
        super(Mp3Encoder, self).setup(channels, samplerate, blocksize, totalframes)

        self.pipe = '''appsrc name=src
                  ! audioconvert
                  ! lamemp3enc target=quality quality=2 encoding-engine-quality=standard
                  ! id3v2mux
                  '''

        if self.filename and self.streaming:
            self.pipe += ''' ! tee name=t
            ! queue ! filesink location=%s
            t. ! queue ! appsink name=app sync=False
            ''' % self.filename

        elif self.filename :
            self.pipe += '! filesink location=%s async=False sync=False ' % self.filename
        else:
            self.pipe += '! queue ! appsink name=app sync=False '

        self.start_pipeline(channels, samplerate)

    @staticmethod
    @interfacedoc
    def id():
        return "gst_mp3_enc"

    @staticmethod
    @interfacedoc
    def description():
        return "MP3 GStreamer based encoder"

    @staticmethod
    @interfacedoc
    def format():
        return "MP3"

    @staticmethod
    @interfacedoc
    def file_extension():
        return "mp3"

    @staticmethod
    @interfacedoc
    def mime_type():
        return "audio/mpeg"

    @interfacedoc
    def set_metadata(self, metadata):
        self.metadata = metadata

    def write_metadata(self):
        """Write all ID3v2.4 tags to file from self.metadata"""
        from mutagen import id3
        id3 = id3.ID3(self.filename)
        for tag in self.metadata.keys():
            value = self.metadata[tag]
            frame = mutagen.id3.Frames[tag](3,value)
            try:
                id3.add(frame)
            except:
                raise IOError('EncoderError: cannot tag "'+tag+'"')
        try:
            id3.save()
        except:
            raise IOError('EncoderError: cannot write tags')

