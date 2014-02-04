#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
"""
BaseHandler

Author: Tianyi Wu <tywtyw2002@gmail.com>

"""

import tornado.web
from app.jinja_helper import Filters

class BaseHandler(tornado.web.RequestHandler):


    def __init__(self, *argc, **argkw):
		super(BaseHandler, self).__init__(*argc, **argkw)
		self.jinja2 = self.settings.get("jinja2")
		self.jinja2 = Filters(self.jinja2).register()


    def render(self, template_name, **template_vars):
		html = self.render_string(template_name, **template_vars)
		self.write(html)


    def render_string(self, template_name, **template_vars):
        template_vars["xsrf_form_html"] = self.xsrf_form_html
        #template_vars["current_user"] = self.current_user
        template_vars["request"] = self.request
        template_vars["request_handler"] = self
        template = self.jinja2.get_template(template_name)
        return template.render(**template_vars)


    def render_from_string(self, template_string, **template_vars):
        template = self.jinja2.from_string(template_string)
        return template.render(**template_vars)


    def get_current_user(self):
        username = self.get_secure_cookie("user")
        if not username: return None
        return self.UserModel.get_user_by_name(str(username))


    @property
    def UserModel(self):
        return self.application.UserModel
