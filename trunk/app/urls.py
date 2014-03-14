"""
URL router for tornado server

Author: tywtyw2002
"""

#handlers
from handlers.LoginHandler import LoginHandler, LogoutHandler
from handlers.ProfileHandler import ProfileHandler
from handlers.BaseHandler import DashHandler

urls = [
		# (r'/', HomeHandler.HomeHandler),
		(r'/login', LoginHandler),
		(r'/logout', LogoutHandler),
		(r'/profile', ProfileHandler),
		(r'/', DashHandler),
		]