try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name="PythonTSquareAPI",
      version='0.1',
      description='Python TSquare API bindings',
      author='Sean Gillespie',
      author_email='sean.william.g@gmail.com',
      url='https://github.com/swgillespie/tsquare-webapp',
      py_modules=['tsquare_api'],
      requires=['requests'],
      license='MIT',
      )