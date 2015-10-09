#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  IkaLog
#  ======
#  Copyright (C) 2015 Takeshi HASEGAWA
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
import os
import sys
print(os.getcwd())
sys.path.append(os.getcwd())

import time
import numpy as np
from PIL import ImageGrab

import cv2

from ikalog.utils import IkaUtils


class ScreenCapture(object):
    ''' ScreenCapture input plugin
    This plugin depends on python-pillow ( https://pillow.readthedocs.org/ ).
    This plugin now supports only IkaLog.py.
    You can use this plugin if you modify IkaConfig.py
    ```
from ikalog.inputs.screencapture import ScreenCapture

class IkaConfig:
    def config(self):
        source = ScreenCapture()
    ```
    '''
    from_file = False

    _bbox = None
    _out_width = 1280
    _out_height = 720

    _launch = 0

    def read(self):
        img = ImageGrab.grab(self._bbox)
        img = np.asarray(img)
        img = cv2.resize(img, (self._out_width, self._out_height))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        t = self._time() - self._launch
        return (img, t)

    def set_bounding_box(bbox):
        '''
        bbox -- bbox Crop bounding box as (x, y, w, h)
        '''
        self._bbox = bbox

    def _time(self):
        return int(time.time() * 1000)

    def __init__(self, bbox=None):
        '''
        bbox -- bbox Crop bounding box as (x, y, w, h)
        '''
        self._bbox = bbox
        self._launch = self._time()
        IkaUtils.dprint('%s: initalizing screen capture' % (self))


if __name__ == "__main__":
    obj = ScreenCapture()

    k = 0
    while k != 27:
        frame, t = obj.read()
        cv2.imshow(obj.__class__.__name__, frame)
        print(t)
        k = cv2.waitKey(1)
