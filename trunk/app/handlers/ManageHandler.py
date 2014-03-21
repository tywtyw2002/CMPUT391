#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
"""
Manage Handler

Author: Tianyi Wu <tywtyw2002@gmail.com>

"""
from wtforms import TextField, validators
from app.libs.forms import Form
from BaseHandler import BaseHandler
import hashlib
import tornado.web




class ManageHandler(BaseHandler):

	def __init__(self, *argc, **argkw):
		super(ManageHandler, self).__init__(*argc, **argkw)
		self.private_auth()


	def private_auth(self):
		self.user = self.get_secure_cookie("user")
		self.private = self.UserModel.get_user_level_by_name(self.user)

		#not login
		if self.private == -1:
			return 

		if self.private != 4:
			self.render("404.html")
			self.finish()


	@tornado.web.authenticated
	def get(self, argkw={}):

		argkw['user_level'] = self.private
		argkw['user_name']  = self.user

		argkw['userlist'] = self.UserModel.get_all_user_list()

		self.render("manage_userlist.html", **argkw)



class ManageAddHandler(ManageHandler):
	def get(self, id = None, argkw={}):

		argkw['user_level'] = self.private
		argkw['user_name']  = self.user

		#edit method
		if id:
			argkw['item'] = self.UserModel.get_profile_with_doctor_by_id(id)
		else:
			argkw['item'] = {}
		argkw['doc_list'] = self.UserModel.get_doctor_list()
		
		self.render("manage_edit.html", **argkw)



	def post(self, id = None):
		argkw = {}
		errors = {}

		form = ManageForm(self)
		if not form.validate():
			self.get(id, {"errors": form.errors})
			return	

		#add new user
		if id == None:
			f = ["User Add Successful."]
			#get new id
			id = self.UserModel.get_current_id();

			#insert persons
			s = self.UserModel.insert_persons(id, form)
			if not s:
				error ['p'] = ["inser persons failed"]

			#insert users
			s = self.UserModel.insert_users(id, form)
			if not s:
				errors ['u'] = ["Update family octor NOT Successful!"]

			#update family doctor
			s = self.UserModel.update_family_doctor_by_id(id, 
														  form.doctor_id.data)
			if not s:
				errors ['pp'] = ["Update family octor NOT Successful!"]

			if errors:
				self.get(None, {"errors": errors})
			else:
				self.get(None, {"infos": {'s' : f}})

		#update user's profile
		else:
			f = ["Update Successful."]

			#update password
			if form.password.data:
				s = self.UserModel.update_password_by_name(form.user_name.data,
													  form.password.data)
				if not s:
					errors ['p'] = ["Update password NOT Successful!"]

			#update user profile
			s = self.UserModel.update_persons_by_id(id, form)
			if not s:
				errors ['pp'] = ["Update profile NOT Successful!"]		

			#update class
			s = self.UserModel.update_class_by_id(id, form.user_class.data)	
			if not s:
				errors ['u'] = ["Update Class NOT Successful!"]

			#update family doctor
			s = self.UserModel.update_family_doctor_by_id(id, 
														  form.doctor_id.data)
			if not s:
				errors ['r'] = ["Update family octor NOT Successful!"]
			
			if errors:
				self.get(id, {"errors": errors})
			else:
				self.get(id, {"infos": {'s' : f}})
	


class ManageForm(Form):
    #f = "Username or password is incorrect"

    user_name = TextField('user_name', [
        validators.Required(message = "FirstName is Required"),
    ])

    address =  TextField('address', [
        validators.Required(message = "Address is Required"),
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
    ])

    user_class = TextField('user_class', [
    	validators.Required(message = "Class is Required"),
    	validators.AnyOf(['a','d','r','p'], message = "class type invailed")
    ])

    doctor_id = TextField('doctor_id')




