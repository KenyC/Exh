Exh
====================

You can find a Jupyter notebook tutorial *Tutorial.ipynb* in the main folder to get a headstart on using the library.

## Description

*Exh* can represent first-order logic formula and can compute the result of applying innocent exclusion exahsutification to the formulas. Internally, it uses the algorithm suggested in Spector (2016), which is faster than simply applying the definition in Fox (2007).

## Installation (NEW)

The package is available on PyPI. Run the following to install it:

```bash
pip install exh
```

## Features 

  - Innocent inclusion, innocent exclusion of propositional formulas
  - Computing maximal consistent sets of formulas
  - Quantifiers 
  - Recursively exhaustified formulas (free choice example in tutorial)
  
## Caveats
 
  - The problem of finding maximally consistent sets of formulas is computationally hard. The algorithm scales up poorly if the number of independent variables is big. It however handles large number of alternatives well enough. However, most real-life examples run fast enough
  
## Dependencies

  - Numpy > 1.14 
  - Jupyter > 1.0.0

