import numpy as np
from IPython.core.display import display, HTML


def to_str_list(list_vars):
	return list(map(str, list_vars))

class Table:
	"""
	Helper class to draw tables in HTML and plain text

	Attributes:
		options (dict)
			html (bool)   -- whether to use HTML display or not
			char_col      -- in plain display, character for plain column
			char_bold_col -- in plain display, character for emphasized column
			char_line     -- in plain display, character for line
			row_lines     -- in plain display, whether to insert lines between every row

		header      (list[str])   -- list of cells in header
		rows        (list[list])  -- list of rows ; each row is either a list of strings of the constant HLINE (for horizontal lines)
		strong_col  (list[int])   -- list of indices of vertical lines to display bold (0 means before first column, n_cols means after last_column)
 	"""

	HLINE = 0 # Constant to reprensent line in 
	style ="""
	border: 1px solid black; 
    border-collapse: collapse;
    font-weight: normal; 
	"""

	def __init__(self, **kwargs):
		"""kwargs update class options"""

		self.options = {"html": True, "char_col": "|", "char_bold_col": "#", "char_line": "-", "row_lines": False}
		self.options.update(kwargs)

		self.rows = []
		self.strong_cols = []
		self.header = None




	def set_header(self, list_header):
		""" Set table header to "list_header" argument """
		self.header = to_str_list(list_header)

	def add_row(self, row):
		self.rows.append(to_str_list(row))
		if self.options["row_lines"]:
			self.insert_hline()

	def set_strong_col(self, i):
		# 0 means leftmost border ; ncols + 1 rightmost border
		self.strong_cols.append(i)

	def insert_hline(self):
		self.rows.append(Table.HLINE)




	def print(self, html = None):
		if html is None:
			html = self.options["html"]
		
		if html:
			self.print_html()
		else:
			self.print_plain()

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

	def print_plain(self):
		self.cache = ""

		def pad(string, width):
			l = width - len(string) 
			return (l//2 + l % 2) * " " + string + (l//2) * " "

		def print_row(strings, widths):
			for i, (string, width) in enumerate(zip(strings, widths)):
				if i in self.strong_cols:
					self.add(self.options["char_bold_col"])
				else:
					self.add(self.options["char_col"])

				self.add(pad(string, width))

			self.add(self.options["char_col"])
			self.add("\n")

		def print_line(widths):
			self.add((sum(widths) + len(widths) + 1) * self.options["char_line"] + "\n")

		rows_and_headers = ([self.header]  if self.header is not None else []) + [row for row in self.rows if isinstance(row, list)]
		widths = [max(len(row[i]) for row in rows_and_headers) + 2 for i in range(len(rows_and_headers[0]))]

		print_row(self.header, widths)
		print_line(widths)
		
		for row in self.rows:
			if isinstance(row, list):
				print_row(row, widths)

		print(self.cache)
		#self.rows_and_headers

	def add(self, string):
		self.cache += string