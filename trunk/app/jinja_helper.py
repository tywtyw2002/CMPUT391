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


	def register(self):
		self.jinja2.filters['dump_errors'] = self.dump_errors

		return self.jinja2


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