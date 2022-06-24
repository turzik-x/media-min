#!/usr/bin/python
import mediaConvert

import os
import shutil


def mediaConvert_jpg(testFolderPath):
    os.mkdir(testFolderPath)
    shutil.copy("./data/a.jpg",testFolderPath)
    sizeBefore = mediaConvert.human_readable_size(os.path.getsize(f"{testFolderPath}/a.jpg"),0)
    assert sizeBefore=="12MiB"
    mediaConvert.media_convert(f"{testFolderPath}/a.jpg")
    sizeAfter = mediaConvert.human_readable_size(os.path.getsize(f"{testFolderPath}/a.jpg"),0)
    assert sizeAfter=="1MiB"

def test_mediaConvert_jpg():
    if os.path.exists("data_test1"):
        shutil.rmtree("data_test1")   
    mediaConvert_jpg("data_test1")
    shutil.rmtree("data_test1")   
    

def test_mediaConvert_jpg_secondConvertIsSkipped():
    if os.path.exists("data_test2"):
        shutil.rmtree("data_test2")   
    mediaConvert_jpg("data_test2")
    mtimeBefore = os.path.getmtime("./data_test2/a.jpg")
    sizeBefore = os.path.getsize("./data_test2/a.jpg")
    mediaConvert.media_convert("./data_test2/a.jpg")
    assert mtimeBefore == os.path.getmtime("./data_test2/a.jpg")
    assert sizeBefore == os.path.getsize("./data_test2/a.jpg")
    shutil.rmtree("data_test2")   
