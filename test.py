# -*- coding: UTF-8 -*-
import sys

reload(sys)
sys.setdefaultencoding( "utf-8" )

list_test = ['a','b','c']

for i in list_test:
	print i

str = u'\u79d1\u5b66\xb7\u6280\u672f'
print str.encode("utf-8")


#f = open('./Data/text/15yandata','r+')
#print f.read()

str_test =  'a'
for i in range(5):
	print i
	str_test = str_test + '%s'%('b')
	print str_test


str_qie = "abcdf dad aggf123"
print str_qie[0:-2]

def iget_no_of_instance(ins_obj):
	return ins_obj.__class__.no_inst

class Kls(object):
	no_inst = 0
	def __init__(self):
		Kls.no_inst = Kls.no_inst + 1

ik1 = Kls()
ik2 = Kls()
print iget_no_of_instance(ik1)# print 2,because no_inst belong to CLASS Kls not belong to self, frist is Class, last is instance
