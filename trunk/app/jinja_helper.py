#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
"""
Helper for jinja2

Author: Tianyi Wu <tywtyw2002@gmail.com>
"""

from jinja2 import evalcontextfilter, Markup, escape


class Filters():
	def __init__(self, jinja2_env):
		self.jinja2 = jinja2_env

	def class2str(self, c):
		if c == 'a':
			return "<span class=\"label label-sm label-danger\">Admin</span>"
		elif c == "d":
			return "<span class=\"label label-sm label-warning\">Doctor</span>"
		elif c == "r":
			return "<span class=\"label label-sm label-success\">Radiologist</span>"
		else:
			return "<span class=\"label label-sm label-default\">Patient</span>"

	def register(self):
		self.jinja2.filters['dump_errors'] = self.dump_errors
		self.jinja2.filters['dump_infos'] = self.dump_infos
		self.jinja2.filters['shortif'] = self.shortif
		self.jinja2.filters['class2str'] = self.class2str

		return self.jinja2


	def shortif(self, var, value, text):
		if var == None or var == '':
			return ""
		if var == value:
			return text
		else:
			return ""

	def dump_infos(self, errors):
		t = self.jinja2.from_string("""
			{% if errors %}
			<!-- BEGIN ERROR MSG -->
			
				{% for error in errors %}
					<div class="alert alert-success">
						<button class="close" data-dismiss="alert"></button>
						<span>{{ ",".join(errors[error]) }} </span>
					</div>
				{% endfor %}
			
			<!-- END ERROR MSG -->
			{% endif %}
			""")

		return t.render(errors = errors)

	def dump_errors(self, errors):
		t = self.jinja2.from_string("""
			{% if errors %}
			<!-- BEGIN ERROR MSG -->
			
				{% for error in errors %}
					<div class="alert alert-danger">
						<button class="close" data-dismiss="alert"></button>
						<span>{{ ",".join(errors[error]) }} </span>
					</div>
				{% endfor %}
			
			<!-- END ERROR MSG -->
			{% endif %}
			""")

		return t.render(errors = errors)