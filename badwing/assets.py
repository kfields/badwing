import os
import zipfile

data_dir = 'assets'

def filepath(filename):
    return os.path.join(data_dir, filename)

def load(filename, mode='rb'):
    return open(os.path.join(data_dir, filename), mode)

def load_zip(filename):
    return zipfile.ZipFile(os.path.join(data_dir, filename))