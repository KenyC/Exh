import numpy as np
from IPython.core.display import display, HTML


def to_str_list(list_vars):
	return list(map(str, list_vars))

"""
Helper class to draw tables in HTML
"""
class Table:

	HLINE = 0
	style ="""
	border: 1px solid black; 
    border-collapse: collapse;
    font-weight: normal; 
	"""

	def __init__(self, **kwargs):

		self.options = {"html": True, "char_col": "|", "char_bold_col": "#", "char_line": "-", "row_lines": False}
		self.options.update(kwargs)

		self.rows = []
		self.strong_cols = []
		self.header = None


	def set_header(self, list_header):
		self.header = to_str_list(list_header)

	def add_row(self, row):
		self.rows.append(to_str_list(row))
		if self.options["row_lines"]:
			self.insert_hline()

	# 0 means leftmost border ; ncols + 1 rightmost border
	def set_strong_col(self, i):
		self.strong_cols.append(i)

	def insert_hline(self):
		self.rows.append(Table.HLINE)

	def print(self, html = None):
		if html is None:
			html = self.options["html"]
		
		if html:
			self.print_html()
		else:
			self.print_console()

	def print_html(self):

		def cell(i, content):
			style = ""
			if i in self.strong_cols:
				style += "border-left-style: double !important;"
			if i+1 in self.strong_cols:
				style += "border-right-style: double !important;"

			self.add('<th style ="{}">'.format(style))
			self.add(content)
			self.add("</th>")

		self.cache = ""

		self.add('<table style = "{}">'.format(Table.style))

		if self.header is not None:

			self.add("<thead>")
			self.add("<tr>")
			for t in enumerate(self.header):
				cell(*t)
			self.add("</tr>")
			self.add("</thead>")


			for row in self.rows:
				if isinstance(row, list):
					self.add("<tr>")
					for t in enumerate(row):
						cell(*t)
					self.add("</tr>")

		self.add("</table>")

		display(HTML(self.cache))

	def add(self, string):
		self.cache += string
