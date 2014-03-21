#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
"""
Helper for Database

Author: Tianyi Wu <tywtyw2002@gmail.com>
"""


import cx_Oracle


class db_Error(Exception):
    '''Base class for error exceptions.'''

    pass


class my_db(db_Error):
    """Use for connect db and do search with db."""

    def __init__(self, host, user, passwd, sid):
        connStr = "%s/%s@%s/%s" % (user, passwd, host, sid)
        
        self.conn = cx_Oracle.connect(connStr)


    def query(self, sql = None):
        """Use for sql query. If successful return a cursor, 
            otherwis return None."""

        if sql == None:
            return None

        cursor = self.conn.cursor()
        try:
            cursor.execute(sql)
            rows = cursor.fetchall()

            cursor.close()   #after query, close cursor

            return rows

        except cx_Oracle.DatabaseError as e:
            raise db_Error(e, sql)

    def query_dict(self, sql=None):
        """Use for sql query. If successful return a cursor, 
            otherwis return None."""

        if sql == None:
            return None

        cursor = self.conn.cursor()
        try:
            cursor.execute(sql)
            desc = [d[0].lower() for d in cursor.description]
            result = [dict(zip(desc,line)) for line in cursor]

            cursor.close()   #after query, close cursor

            return result

        except cx_Oracle.DatabaseError as e:
            raise db_Error(e, sql)

    def update(self, sql = None):
        """update data"""

        if sql == None:
            return None

        cursor = self.conn.cursor()
        try:
            cursor.execute(sql)
            self.conn.commit()
            cursor.close()   #after query, close cursor


        except cx_Oracle.DatabaseError as e:
            raise db_Error(e, sql)

    def insert(self, sql = None):
        """Use for insert row into database"""

        if sql == None:
            return None

        cursor = self.conn.cursor()

        #set attr
        try: 
            cursor.execute(sql)
            #cursor.commit()
            self.conn.commit()

            cursor.close

        except cx_Oracle.DatabaseError as e:
            raise db_Error(e, sql)


    def close(self):
        self.conn.close()
