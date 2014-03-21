#!/usr/bin/env python
# -*- coding: utf-8 -*-


import logging
import os
import tornado.web
import tornado.ioloop
import tornado.httpserver
from tornado.options import define, options
import config
from urls import urls
from jinja2 import Environment, FileSystemLoader
from libs.dbhelper import my_db 
import model.UserModel



define("debug", default=config.debug, help="run in debug mode", type=bool)
define("port",  default=config.port, help="run on the given port", type=int)




class Application(tornado.web.Application):
	def __init__(self):


		template_path = os.path.join(os.path.dirname(__file__), "templates")

		settings = dict(
			template_path = template_path,
			static_path   = os.path.join(os.path.dirname(__file__), "static"),
			xsrf_cookies  = config.xsrf_cookies,
			cookie_secret = config.cookie_secret,
			autoescape    = config.autoescape,
			jinja2        = Environment(loader = 
				            FileSystemLoader(template_path), trim_blocks = True),
			debug 		  = options.debug,
			login_url     = "/login",
		)

		handlers = urls

		tornado.web.Application.__init__(self, handlers, **settings)


		#init the database connection.
		self.db = my_db(config.host, config.user, config.password, config.sid)

		#define model
		self.UserModel = model.UserModel.UserModel(self.db)
		#self.UserModel = model.UserModel.UserModel(None)

def application():
	tornado.options.parse_command_line()
	http_server = tornado.httpserver.HTTPServer(Application())

	logging.info("Starting tornado on port=%s"%options.port)
	http_server.listen(options.port)

	try:
		tornado.ioloop.IOLoop.instance().start()
	except KeyboardInterrupt:
		pass

	logging.info("Tornado Terminated!")



if __name__ == '__main__':
	main()