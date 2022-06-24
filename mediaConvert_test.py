#!/usr/bin/python
import mediaConvert

import os
import shutil

def test_mediaConvert():
    os.mkdir("data_test")
    shutil.copy("./data/a.jpg","./data_test/")
    mediaConvert.media_convert("./data_test/a.jpg")
    print ("test_mediaConvert() done")

