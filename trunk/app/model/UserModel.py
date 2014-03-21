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

	def get_user_level_by_name(self, name):
		row = self.get_user_by_name(name)

		#user not found
		if not row:
			return -1

		c = row[0][2]
		level = 0
		if c == "a":
			level = 4
		elif c == "d":
			level = 2
		elif c == "r":
			level = 3

		return level



	def get_user_by_name(self, name):
		if name == None:
			return None
		sql = "select * from %s where user_name = '%s'" % (self.table, name)
		return self.db.query(sql)


	def auth_user_with_passwd(self, user, passwd):
		sql = "select user_name from %s where user_name = '%s' and password = '%s'" % (
				self.table, user, passwd)
		return self.db.query(sql)



	def get_profile_by_name(self, user):
		sql = "select * from users u left join persons p on " \
			  "u.person_id = p.person_id where user_name = '%s'" % user

		return self.db.query(sql)

	def get_profile_with_doctor_by_id(self, id):
		sql = "select * from users u left join persons p on " \
			  "u.person_id = p.person_id left join family_doctor f on "\
			  "u.person_id = f.patient_id where u.person_id = %s" % id

		return self.db.query_dict(sql)[0]


	def update_persons_by_id(self, id, f):

		sql = "update persons set "
		sql += "first_name = '%s', " % f.first_name.data
		sql += "last_name = '%s',  " % f.last_name.data
		sql += "email = '%s', "      % f.email.data
		sql += "phone = '%s', "      % f.phone.data
		sql += "address = '%s' "    %   f.address.data
		sql += "where person_id = '%s'"  % id

		self.db.update(sql)
		return True

	def update_profile_by_name(self, f):

		item = {'first_name': 'fname', 'last_name': 'lname', 
				'address': 'address', 'email': 'email', 'phone': 'phone'}

		#get person id first.
		person_id = self.get_user_by_name(f.puser.data)
		if person_id:
				person_id = person_id[0][3]
		else:
			#Not person_id find.
			return False

		return self.update_persons_by_id(person_id, f)


	def get_family_doctor_by_id(self, id):
		sql = "select doctor_id from family_doctor where patient_id = %s" % id
		return self.db.query(sql)

	def update_class_by_id(self, id, c):
		sql = "update users set class = '%s' where person_id = %s" %(c, id)
		self.db.update(sql)
		return True

	def insert_users(self, id, form):
		sql = "insert into users "
		sql+= "VALUES('%s', '%s', '%s', '%s', sysdate)" % (form.user_name.data, 
											        form.password.data,
											   		form.user_class.data,
											  		id)
		self.db.insert(sql)
		return True



	def get_current_id(self):
		sql = "select max(person_id) from persons"
		a = self.db.query(sql)
		if not a:
			return 1
		else:
			return int(a[0][0]) + 1


	def insert_persons(self, id, form):
		sql = "insert into persons "
		sql+= "VALUES(%s, '%s', '%s', '%s', '%s', '%s') "%(id, form.first_name.data,
												 form.last_name.data,
												 form.address.data,
												 form.email.data,
												 form.phone.data)
		self.db.insert(sql)
		return True


	def update_family_doctor_by_id(self, id, doctor_id):
		#check is there exist family doctor log.
		old_doctor_id = self.get_family_doctor_by_id(id)
		if old_doctor_id:
			if old_doctor_id[0] == doctor_id:
				return True
			
			elif int(doctor_id) == 0:
				sql = "delete from family_doctor where patient_id = %s" %id
				self.db.update(sql)
			else:
				sql = "update family_doctor set doctor_id = %s where "\
						"patient_id = %s" %( doctor_id, id)
				self.db.update(sql)
		#not doctor log
		#
		
		else:
			#do not write no doctor into database
			if int(doctor_id) == 0:
				return True

			print doctor_id==0
			sql = "insert into family_doctor VALUES(%s, %s)"%(doctor_id, id)
			self.db.insert(sql)
		
		return True

	def update_password_by_name(self, name, password):
		if password == "":
			return False

		sql = "update users set password = '%s' where user_name = '%s'" % \
				(name, password)

		self.db.update(sql)
		return True

	def get_all_user_list(self):
		sql = "select * from users u left join persons p on " \
			  "u.person_id = p.person_id"
		return self.db.query_dict(sql)

	def get_doctor_list(self):
		sql = "select p.person_id, p.first_name, p.last_name from users u left "\
			  "join persons p on u.person_id = p.person_id where "\
			  "u.class = 'd'"
		return self.db.query_dict(sql)