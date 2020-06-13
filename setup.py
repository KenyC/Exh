from setuptools import setup

setup(name             = "Exh",
      version          = "0.3",
      description      = "Computes innocent exclusion/inclusions exhaustivity",
      url              = "http://github.com/KenyC/Exh",
      author           = "Keny Chatain",
      author_email     = "kchatain@mit.edu",
      license          = "MIT",
      packages         = ["exh", "exh.formula"],
      install_requires = [
          "numpy",
          "IPython"
      ],
      zip_safe         = True)