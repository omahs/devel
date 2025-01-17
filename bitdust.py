#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# bitdust.py
#
# Copyright (C) 2008 Veselin Penev, https://bitdust.io
#
# This file (bitdust.py) is part of BitDust Software.
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

from __future__ import absolute_import
import os
import sys

try:
    import locale
    locale.setlocale(locale.LC_CTYPE, 'en_US.UTF-8')
except:
    pass


def main():
    executable_path = os.getcwd()

    if executable_path not in sys.path:
        sys.path.append(executable_path)

    # try:
    #     os.chdir(os.path.dirname(__file__))
    # except:
    #     pass

    # try:
    #     from bitdust.main.bpmain import main
    # except:
    #     dirpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    #     sys.path.insert(0, os.path.abspath(os.path.join(dirpath, '..')))
    #     from distutils.sysconfig import get_python_lib
    #     sys.path.append(os.path.join(get_python_lib(), 'bitdust'))
    #     try:
    #         from bitdust.main.bpmain import main
    #     except:
    #         print('ERROR! can not import working code.  Python Path:')
    #         print('\n'.join(sys.path))
    #         return 1

    from bitdust.main.bpmain import main

    ret = main(executable_path)

    os._exit(ret)

    return ret


if __name__ == '__main__':
    main()
