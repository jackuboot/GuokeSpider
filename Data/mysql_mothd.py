import configparser as ConfigParser
import pymysql

import re
import json
import collections
import sys

def get_cfg(cfg_name, db_name):
	cfg = ConfigParser.ConfigParser()
	cfg.read(cfg_name)
	tuple_list = cfg.items(db_name)
	dict_data = {}
	for i in tuple_list:
		dict_data[i[0]] = i[1]
	return dict_data


def connect_mysql(cfg_dict):
	conn = pymysql.connect( user= cfg_dict["db_user"], password=cfg_dict["db_pwd"], host = cfg_dict["db_ip"], database= cfg_dict["db_databases"])
	cursor = conn.cursor()
	cursor.execute("show databases")
	result_list = cursor.fetchall() #remeber to fechall data,if not get all, there will get a error:"unread result found",but if you just insert data,you don't care
	#for i in result_list:
	#	print i
	#conn.commit()
	#cursor.close()
	#conn.close()
	return conn, cursor
	
def exit_mysql(conn, cursor):
	conn.commit()
	cursor.close()
	conn.close()	

def create_table(conn, cursor):
	#cursor.execute('create database if not exists guoke_1')#create "guoke" databases
	order_1 = "CREATE DATABASE if not exists `guoke_2` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;"
	cursor.execute(order_1)
	conn.commit()

	# conn.set_database('guoke_2')
	order =	"CREATE TABLE if not exists guokecontent_1 (url varchar(64) DEFAULT NULL,title varchar(64) DEFAULT  NULL,titledesc varchar(64) DEFAULT NULL, autorname varchar(64) DEFAULT NULL)ENGINE=MyISAM DEFAULT CHARSET=utf8"
	#order = "CREATE TABLE `person_2` (`number` int(11) DEFAULT NULL, `name` varchar(255) DEFAULT NULL,`birthday` date DEFAULT NULL) ENGINE=MyISAM DEFAULT CHARSET=utf8;"
	cursor.execute(order)


def	insert_data(conn, cursor, string_oder):
	#oder = "INSERT INTO guokecontent ( field1, field2,...fieldN ) VALUES( value1, value2,...valueN )"
	cursor.execute(string_oder)
	conn.commit()

	
#if __name__ == "__main__":
#	#get mysql cfg
#	cfg_dict = get_cfg("mysql_cfg.conf", "db")
#	print cfg_dict
#
#	#connect_mysql
#	conn, cursor = connect_mysql(cfg_dict)
#
#	#create databases;
#	create_table(conn, cursor)
#
#	#exit mysql
#	exit_mysql(conn, cursor)
