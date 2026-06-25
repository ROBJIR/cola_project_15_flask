# lib_datababse.py
# - exam2
# robert.jiranek@gmail.com
#
import sys

import psycopg2
from psycopg2.errors import DuplicateDatabase
from psycopg2.extras import RealDictCursor
import logging
# my librares

class DatabasePostgresql():
    def __init__(self):
        self.database_name=""
        self.database_host=""
        self.database_port=""
        self.database_username=""
        self.database_userpwd=""

    def sys_message(self, messagetype: str = "ERROR", message: str = "", messageno: int = 0):
        messagetype=messagetype.upper()
        msgno=""
        if messageno > 0:
            msgno = (f" [{str(messageno)}]")
        sepchar = ""
        msg = (f"{98 * sepchar}\n{messagetype}:{msgno} {message}\n{98 * sepchar}")
        match messagetype:
            case "ERROR":
                sepchar = "="
                msg = (f"{98 * sepchar}\n{messagetype}:{msgno} \n{message}\n{98 * sepchar}")
            case "WARNING":
                sepchar = "="
                msg = (f"{98 * sepchar}\n{messagetype}:{msgno} {message}\n{98 * sepchar}")
            case "INFO":
                sepchar = "-"
                msg = (f"{98 * sepchar}\n{messagetype}:{msgno} {message}\n{98 * sepchar}")
            case "SYSINFO":
                sepchar = "_"
                msg = (f"--- sysinfo {86 * sepchar}\n{msgno} {message}")
            case _:
                msg = (f">>> {messagetype}:{msgno} {message} <<<")
        print(msg)

        if messagetype=="ERROR" and messageno>0:
            sys.exit(messageno)

    def connect(self, connect_string):

        try:
            self.database_host=connect_string["host"]
            self.database_port=connect_string["port"]
            self.database_username=connect_string["username"]
            self.database_userpwd=connect_string["userpwd"]
            self.database_name = connect_string["database"]

            self.conn = psycopg2.connect(
                host=self.database_host,
                port=self.database_port,
                database=self.database_name,
                user=self.database_username,
                password=self.database_userpwd
            )

            self.conn.autocommit = True

            return self.conn

        except Exception as err:
            self.sys_message("Error", err, 81)

    def close(self):

        try:
            self.conn.close()

        except Exception as err:
            self.sys_message ("Error",err, 82)

    def sqlcommand_execute(self, sqlcommand: str):

        try:
            sqlresponse = ""
            cur=self.conn.cursor()
            cur.execute(sqlcommand)

            if sqlcommand.split()[0].lower() == "select":
                columns = [col[0].lower() for col in cur.description]
                sqlresponse = [
                    dict(zip(columns, row))
                    for row in cur.fetchall()
                ]
                cur.close()
                return sqlresponse
            else:
                return True

        except Exception as err:
            self.sys_message ("Error",err, 90)

    def sys_database_info(self,onscreen: bool = False):
        try:
            sqlcommand = f"""SELECT current_database() as current_database,
                               current_user as current_user,
                               trim(substr(version(),1,position('(' in version())-1)) as version,
                               pg_backend_pid() as sid
                          """
            sqlresponse = self.sqlcommand_execute(sqlcommand)

            for sysinfo in sqlresponse:
                self.current_database = sysinfo["current_database"]
                self.current_username = sysinfo["current_user"]
                self.current_database_version = sysinfo["version"]
                self.current_session_id = sysinfo["sid"]

            if onscreen:
                self.sys_message("SysInfo",f"DATABASE INFO / database: {self.current_database} | username: {self.current_username} | sid: {self.current_session_id} | version: {self.current_database_version}")

            return sysinfo

        except Exception as err:
            self.sys_message ("Error",err, 93)

    def create_database(self, database_name: str):
        try:
            sqlcommand = f"create database {database_name}"
            self.sqlcommand_execute(sqlcommand)

            self.sys_message("Info",f"Database {database_name} created")

        except DuplicateDatabase:
            self.sys_message ("Warning",f"Database {database_name} exists!", 92)
        except Exception as err:
            self.sys_message ("Error",err, 91)

    def drop_database(self, database_name: str):
        try:
            sqlcommand = f"drop database {database_name}"
            self.sqlcommand_execute(sqlcommand)

            self.sys_message("Info",f"Database {database_name} dropped")

        except Exception as err:
            self.sys_message ("Error",err, 91)