import os
from pydicom import dcmread

def batch_rename(path):
    for fname in os.listdir(path):
        dcm_file = path + fname
        ds       = dcmread(dcm_file)
        print(ds.SOPInstanceUID)
        new_fname = str(ds.SOPInstanceUID)
        #print(os.path.join(path, fname))
        os.rename(os.path.join(path, fname), os.path.join(path, new_fname) + ".dcm")
    print("StudyUID is " + ds.StudyInstanceUID)
    print("SeriesUID is " + ds.SeriesInstanceUID)
batch_rename("./rename_SOPInstanceUID/")