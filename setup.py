"""
    py文件打包成so
"""
from distutils.core import setup
from Cython.Build import cythonize

setup(ext_modules=cythonize(
    ['config.py', 'devState.py', 'did.py', 'messageType.py', 'models.py', 'moniterCP.py', 'moniterFace.py',
     'readpcstate.py', 'rtmpPush.py', 'socketNet.py', 'startMain.py', 'state.py', 'toolCase.py', 'update.py']))

# setup(ext_modules=cythonize(['startMain.py']))
