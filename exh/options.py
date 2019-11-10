# Which formulas cannot be erased with doing sub-constituent replacement
non_subst = {"some", "all", "exh"}

# Default scalar scales
scales = [{"or", "and"}, {"some", "all"}]

# Whether Exh computes innocent inclusion by default
ii_on = False

# Whether automatic alternatives use subconstituents alternatives by default
sub = True

# Default size of the domain of quantification of quantifiers
dom_quant = 3 

# Whether display is in Latex by default
latex_display = True

# LateX display for the different formulas
latex_dict = {"and": r"\wedge", "or": r"\vee", "not": r"\neg",
			 "some": r"\exists", "all": r"\forall", "quant": r"Q",
			 "exh": r"Exh"}
# Plain text display for the different formulas
normal_dict = {"and": "and", "or": "or", "not": "not",
			 "some": "\u2203", "all": "\u2200", "quant": "Q",
			 "exh": r"Exh"}