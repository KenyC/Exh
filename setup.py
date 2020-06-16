from setuptools import setup

setup(name             = "Exh",
      version          = "0.5",
      description      = "Computes innocent exclusion/inclusions exhaustivity",
      url              = "http://github.com/KenyC/Exh",
      author           = "Keny Chatain",
      author_email     = "kchatain@mit.edu",
      license          = "MIT",
      packages         = ["exh", 
                          "exh.model", 
                          "exh.utils", 
                          "exh.prop", 
                          "exh.fol"],
      install_requires = [
          "numpy",
          "IPython"
      ],
      zip_safe         = True)