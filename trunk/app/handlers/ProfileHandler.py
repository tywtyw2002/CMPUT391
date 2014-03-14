#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
"""
Login Handler

Author: Tianyi Wu <tywtyw2002@gmail.com>

"""
from wtforms import TextField, validators
from app.libs.forms import Form
from BaseHandler import BaseHandler
import hashlib
import tornado.web



class ProfileHandler(BaseHandler):

	@tornado.web.authenticated
	def get(self, argkw = {}):
		argkw['user_level'] = 0;
		argkw['user_name']  = self.get_secure_cookie("user") 
		self.render("profile.html", **argkw)
