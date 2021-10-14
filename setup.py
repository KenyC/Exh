import exh
from setuptools import setup

long_desc = """\
Exh 
===========================

``Exh`` is a package for computing the exhaustification of logical formulas. 
You can write formulas in a convenient legible syntax. You can compute alternatives automatically. 
You can compute innocently excludable and includable alternatives.   

A introductory tutorial can be found [here](https://github.com/KenyC/Exh/blob/master/examples/tutorial/Tutorial.ipynb).
Other tutorials covering more advanced features and more complicated examples are  available in [the `examples` folder of the GitHub repository](https://github.com/KenyC/Exh/tree/master/examples).
"""

setup(
    name             = "Exh",
    version          = exh.__version__,
    description      = "Computes innocent exclusion/inclusions exhaustivity",
    long_description = long_desc,
    long_description_content_type = "text/markdown",
    url              = "http://github.com/KenyC/Exh",
    author           = "Keny Chatain",
    author_email     = "kchatain@mit.edu",
    license          = "MIT",
    packages         = [
      "exh", 
      "exh.model", 
      "exh.utils", 
      "exh.prop", 
      "exh.exts.gq", 
      "exh.exts.focus", 
      "exh.fol"
    ],
    install_requires = [
        "numpy",
        "IPython"
    ],
    zip_safe         = True
)