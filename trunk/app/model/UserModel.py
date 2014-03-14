#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
"""
Model for User

Author: Tianyi Wu <tywtyw2002@gmail.com>
"""



class UserModel():
	def __init__(self, db):
		self.db = db
		self.table = "users"


	def get_user_by_name(self, name):

		return 1


	def auth_user_with_passwd(self, user, passwd):
		return None
