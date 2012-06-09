import sublime, sublime_plugin

class XPathFindCommand(sublime_plugin.TextCommand):

	xml_tree = None
	query_last = ""

	def run(self, edit):
		window = self.view.window()
		window.show_input_panel("XPath", self.query_last, self.on_input_done, self.on_input_change, self.on_input_cancel)

	def on_input_done(self, value):
		self.query_last = value
		self.xpath_find(value)

	def on_input_change(self, value):
		self.query_last = value
		self.xpath_find(value, False)

	def on_input_cancel(self, value):
		# Free memory
		self.xml_tree = None

	def xpath_find(self, expr, parse = True):

		if parse or not self.xml_tree:
			xml_raw = self.view.substr(sublime.Region(0, self.view.size()))

			from lxml import etree
			from StringIO import StringIO

			xml_raw_io = StringIO(xml_raw)

			try:
				self.xml_tree = etree.parse(xml_raw_io)
			except Exception as e:
				sublime.error_message(str(e.message))

		nodes = self.xml_tree.xpath(expr)

		sublime.status_message("XPath: found {0} match(es) for {1}".format(len(nodes), expr))

		self.view.sel().clear()

		for node in nodes:
			pt = self.view.text_point(node.sourceline - 1, 0)
			self.view.sel().add(sublime.Region(pt))
			self.view.show(pt)
			self.view.run_command("expand_selection", {'to': 'line'})

		return nodes



