import exh.model.options as options

### DISPLAY METHODS ####


class Display:
	"""
	Returns string representation of the object, in plain text or Latex
	"""
	def display(self, latex = None):
		if latex is None:
			latex = options.latex_display

		if latex:
			return "${}$".format(self.display_aux(latex))
		else:
			return self.display_aux(latex)

	def display_aux(self, latex):

		if latex:
			display_dict = self.__class__.latex_dict
		else:
			display_dict = self.__class__.plain_dict

		def paren(typeF, child):
			if (typeF == child.type) or (child.type == "pred") or (child.type == "not"):
				return child.display_aux(display_dict)
			else:
				return "({})".format(child.display_aux(display_dict))

		if self.type == "not" or self.type == "exh":
			return "{}[{}]".format(display_dict[self.type], self.children[0].display_aux(latex))
		else:
			return " {type} ".format(type = display_dict[self.type]).join([paren(self.type,	child) for child in self.children])
	"""
	Display object, in plain text or LateX
	"""
	def show(self, latex = None):
		if latex is None: # we cannot use "options.latex_display" as default lest we lose dynamic binding
			latex = options.latex_display 

		if latex:
			display(Math(self.display(latex)))
		else:
			print(self.display(latex))

