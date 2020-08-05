Contributing 
=================================

Thanks! All and any contributions are welcome. 

# How?

## Pointing out problems

There is an "Issues" tab in the repository. You can post any and all problems here. Make sure to indicate the necessary information to reproduce your problem. This includes:

  - The version of the package you use 
```python
import exh
print(exh.__version__)
```
  - A complete code fragment which reproduces the bug.

## Modifying the code

 1. Fork the repository
 2. Do desired modifications
 3. Make sure to run "test.py" when you're done. If it runs fully without exceptions, you're unlikely to have broken anything. (If you find test cases not already included in "test.py", feel free to add them to "test.py")
 3. Create pull request in this repository

# Info about the structure of the package

This is more in-depth info about the package for the purpose of modification

## Modules and submodules
  * **model**: defines *Universe* and *VarManager*, keeps track of all logical possibilities
  	- *Universe*: essentially a big truth-table, a wrapper around big numpy array of booleans 
  	- *VarManager*: maps human-readable predicates and propositions (e.g. "p(0)" or "a") to positions in memory (e.g. the 7th bit)
  * **prop**: defines abstract base class *Formula* and important sub-class *Pred*, implements propositional calculus
    - *Formula* : overrides binary operators (|, &, ~), keep track of open variables, defines display methods (implementation is split across *formula.py*, *evaluate.py*, *display.py*)
    - *Pred* : Base class for n-ary predicates (implementation in *predicate.py*)
  * **fol**: appends to *prop* the class *Quantifier* to deal with 1st order logic
  * **utils**: class Table for displaying pretty HTML or text tables (used for truth tables)
  * **exhaust.py**
    - *Exhaust* : this class comports all the methods to compute IE and II
    - *Exh* : wraps *Exhaust* in *Formula* wrapping
  * **alternatives.py**: defines a number of methods for automatic generation of alternatives (these methods is called whenever *Exh* is built with no *alts* argument), + find maximal sets of consistent alternatives