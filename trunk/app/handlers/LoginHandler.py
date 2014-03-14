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




class LoginHandler(BaseHandler):

	def get(self, argkw = {} ):
		self.render("login.html", **argkw)

	def post(self):
		form = LoginForm(self)
		f = "Username or password is incorrect"

		#check form first.
		if not form.validate():
			
			self.get({"errors": { 'e' : [f]}})
			return

		secure_passwd = hashlib.sha1(form.password.data).hexdigest()
		
		auth =  self.UserModel.auth_user_with_passwd(form.username.data,
													 secure_passwd)

		auth = 1
		if(auth):
			self.set_current_user(form.username.data)
			print self.get_argument("next")
			self.redirect(self.get_argument("next","/"))
		else:
			self.get({"errors": { 'e' : [f]}})


	def set_current_user(self, username):
		self.set_secure_cookie("user", str(username))



class LogoutHandler(BaseHandler):

	def get(self):
		self.clear_cookie("user")
		self.redirect("/")



class LoginForm(Form):
    f = "Username or password is incorrect"
    username = TextField('username', [
        validators.Required(message = "Username is Required"),
        validators.Length(min = 4, message = f),
    ])

    password = TextField('password', [
        validators.Required(message = "Password is Required"),
        validators.Length(min = 6, message = f),
    	validators.Length(max = 64, message = f),
    ])
