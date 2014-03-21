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

		row = self.UserModel.get_profile_by_name(argkw["user_name"])
		if not row:
			return "ERROR: CANNOT GET USER %s" % argkw['user_name']
		row = row[0]
		argkw['p_user_name'] = row[0] #current edit user's name.
		argkw['fname'] = row[6] 
		argkw['lname'] = row[7]
		argkw['email'] = row[9]
		argkw['address'] = row[8]
		argkw['phone'] = row[10]

		self.render("profile.html", **argkw)

	@tornado.web.authenticated
	def post(self):
		argkw = {}
		argkw['user_level'] = 0;
		argkw['user_name']  = self.get_secure_cookie("user") 

		errors = {}

		form = ProfileForm(self)
		# print form.puser.data
		# print form.lname.data
		# print dir(form)
		# print self.request.arguments
		if not form.validate():
			self.get({"errors": form.errors})
			return	

		#edit password	
		if form.password.data:
			s = self.UserModel.update_password_by_name(form.puser.data,
													  form.password.data)
			if not s:
				errors ['p'] = ["Update password NOT Successful!"]

		#update user info.
		s = self.UserModel.update_profile_by_name(form)
		if not s:
			errors ['pp'] = ["Update profile NOT Successful!"]

		if errors:
			self.get({"errors": errors})
		else:
			self.get({"infos": {'s' : ["User Profile Update Successful."]}})






class ProfileForm(Form):
    #f = "Username or password is incorrect"

    address =  TextField('address', [
        validators.Required(message = "Address is Required"),
    ])

    puser =  TextField('puser', [
        validators.Required(message = "Missing Argument [_USER]"),
    ])


    first_name = TextField('first_name', [
        validators.Required(message = "FirstName is Required"),
    ])

    last_name = TextField('last_name', [
        validators.Required(message = "LastName is Required"),
    ])

    email = TextField('email', [
        validators.Required(message = "Email is Required"),
        validators.Email(message = "Email address incorrect"),
    ])

    phone =  TextField('phone', [
        validators.Required(message = "Phone is Required"),
    ])

    password = TextField('password', [
        validators.Optional(),
        validators.Length(min = 6, message = "Password too short"),
    	validators.Length(max = 64, message = "Password too long"),
    	validators.EqualTo('password2', message='Passwords must match'),
    ])

    password2 = TextField('password2')