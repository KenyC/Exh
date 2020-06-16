from exh.prop    import Or, And
from exh.fol     import Existential, Universal

# Default scalar scales
scales = [{Or, And}, {Existential, Universal}]

# Whether Exh computes innocent inclusion by default
ii_on = False

# Whether automatic alternatives use subconstituents alternatives by default
sub = True