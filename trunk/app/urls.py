"""
URL router for tornado server

Author: tywtyw2002
"""

#handlers
from handlers.LoginHandler import LoginHandler


urls = [
		# (r'/', HomeHandler.HomeHandler),
		(r'/login', LoginHandler),
		]