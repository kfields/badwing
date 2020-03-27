import os
import zipfile

#assets_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../assets')
assets_dir = None
# print(assets_dir)

def asset(filename):
    return os.path.join(assets_dir, filename)

def load_asset(filename, mode='rb'):
    return open(os.path.join(assets_dir, filename), mode)

def load_asset_zip(filename):
    return zipfile.ZipFile(os.path.join(assets_dir, filename))