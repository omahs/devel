#!/usr/bin/python
# message_index.py
#
# Copyright (C) 2008-2018 Veselin Penev, https://bitdust.io
#
# This file (message_index.py) is part of BitDust Software.
#
# BitDust is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# BitDust Software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with BitDust Software.  If not, see <http://www.gnu.org/licenses/>.
#
# Please contact us if you have any questions at bitdust.io@gmail.com
#
#
#
#

"""
..

module:: message_index
"""

#------------------------------------------------------------------------------

_Debug = True

#------------------------------------------------------------------------------

import os

from hashlib import md5

from CodernityDB.hash_index import HashIndex
from CodernityDB.tree_index import TreeBasedIndex

#------------------------------------------------------------------------------

if __name__ == '__main__':
    import sys
    import os.path as _p
    sys.path.insert(0, _p.abspath(_p.join(_p.dirname(_p.abspath(sys.argv[0])), '..')))

#------------------------------------------------------------------------------

from logs import lg

#------------------------------------------------------------------------------

def definitions():
    return [
        ('creator', Creator, ),
        ('signer', Signer, ),
        ('miner', Miner, ),
        ('hash', HashID, ),
        ('prev', PrevHashID, ),
        ('time_created', TimeCreated, ),
        ('time_signed', TimeSigned, ),
        ('time_mined', TimeMined, ),
        ('body_hash', MessageBodyHash, ),
    ]

#------------------------------------------------------------------------------

def make_custom_header():
    src = '\n'
    src += 'from chat.message_index import BaseHashIndex\n'
    src += 'from chat.message_index import BaseMD5Index\n'
    src += 'from chat.message_index import BaseTimeIndex\n'
    return src

#------------------------------------------------------------------------------

class BaseHashIndex(HashIndex):
    role = None
    field = None
    key_format = '16s'

    def __init__(self, *args, **kwargs):
        kwargs['key_format'] = self.key_format
        super(BaseHashIndex, self).__init__(*args, **kwargs)

    def transform_key(self, key):
        return key

    def make_key_value(self, data):
        try:
            return self.transform_key(data[self.role][self.field]), None
        except (AttributeError, ValueError, KeyError, IndexError, ):
            return None
        except Exception:
            lg.exc()

    def make_key(self, key):
        return self.transform_key(key)

#------------------------------------------------------------------------------

class BaseMD5Index(BaseHashIndex):

    def transform_key(self, key):
        return md5(key).digest()

#------------------------------------------------------------------------------

class BaseTimeIndex(TreeBasedIndex):
    role = None

    def __init__(self, *args, **kwargs):
        kwargs['key_format'] = 'I'
        kwargs['node_capacity'] = 128
        super(BaseTimeIndex, self).__init__(*args, **kwargs)

    def make_key_value(self, data):
        try:
            return data[self.role]['time'], None
        except (ValueError, KeyError, IndexError, ):
            return None
        except Exception:
            lg.exc()

    def make_key(self, key):
        return key

#------------------------------------------------------------------------------

class Creator(BaseMD5Index):
    role = 'creator'
    field = 'idurl'

#------------------------------------------------------------------------------

class Signer(BaseMD5Index):
    role = 'signer'
    field = 'idurl'

#------------------------------------------------------------------------------

class Miner(BaseMD5Index):
    role = 'miner'
    field = 'idurl'

#------------------------------------------------------------------------------

class MessageBodyHash(BaseMD5Index):
    role = 'payload'
    field = 'body'

#------------------------------------------------------------------------------

class HashID(BaseHashIndex):
    role = 'miner'
    field = 'hash'
    key_format = '40s'

#------------------------------------------------------------------------------

class PrevHashID(BaseHashIndex):
    role = 'miner'
    field = 'prev'
    key_format = '40s'

#------------------------------------------------------------------------------

class TimeCreated(BaseTimeIndex):
    role = 'creator'

#------------------------------------------------------------------------------

class TimeSigned(BaseTimeIndex):
    role = 'signer'

#------------------------------------------------------------------------------

class TimeMined(BaseTimeIndex):
    role = 'miner'
