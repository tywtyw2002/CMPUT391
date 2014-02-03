#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
# work with python 2.7

import tornado.ioloop
import tornado.web


class login(tornado.web.RequestHandler):
    
    def post(self):
        a = self.get_argument("USERID","")
        b = self.get_argument("PASSWD","")
        if a == "123":
            self.write("inviled user")
        else:
            self.write("123    "+ a + "    123123123     " + b)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        a = '''

<HTML>
<HEAD>


<TITLE>Your Login Result</TITLE>
</HEAD>

<BODY>
<!--A simple example to demonstrate how to use JSP to 
    connect and query a database. 
    @author  Hong-Yu Zhang, University of Alberta
 -->

<form method=post action="/login">
UserName: <input type=text name=USERID maxlength=20><br>
Password: <input type=password name=PASSWD maxlength=20><br>
<input type=submit name=bSubmit value=Submit>
</form>




</BODY>
</HTML>
'''
        self.write(a)


application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/login", login),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()


