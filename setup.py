from setuptools import setup

setup(name='Exh',
      version='0.1',
      description='Computes innocent exclusion/inclusions exhaustivity using minimal worlds',
      url='http://github.com/KenyC/Exh',
      author='Keny Chatain',
      author_email='kchatain@mit.edu',
      license='MIT',
      packages=['exh'],
      install_requires=[
          'numpy',
          'IPython'
      ],
      zip_safe=False)