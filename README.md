# Exh

You can find a Jupyter notebook tutorial in the main folder to get a headstart for using the library.

## Features 

  - Innocent inclusion, innocent exclusion of propositional formulas
  - Computing maximal consistent sets of formulas
  - Recursively exhaustified formulas
  - Quantifiers 
  
## Caveats
 
  - The problem of finding maximally consistent sets of formulas is computationally hard. The algorithm scales up poorly if the number of independent variables is big. It however handles large number of alternatives well enough.
  
## Module needed

  - Numpy 1.14 
  - Jupyter 1.0.0