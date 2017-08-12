#!/usr/bin/python
# -*- coding: UTF-8 -*-

from conf import Conf  #input class
import requests
from lxml import etree
from collections import Iterable
import hashlib
import re
import sys

class Creator(object):
	
	def __init__(self):
		self.name = "Creator" 

	def input_data(self, queue):
		#get config
		conf_instance = self.load_conf()

		#requst index url
		content = self.request_index_url(conf_instance)

		#analysis html,get links
		links = self.analysis_html(content)

		#put useful url son url in queue
		self.queue_put(queue, links)	
		
	def load_conf(self):
		print "loading conf ing"
		conf_instance = Conf()
		return conf_instance
	
	def request_index_url(self, conf_instance):
		#----------get html------------------------------
		url = conf_instance.url
		print url
		#data={"user":"user","password":"pass"}
		headers = { "Accept":"text/html,application/xhtml+xml,application/xml;",
	    	        "Accept-Encoding":"gzip",
					"Accept-Language":"zh-CN,zh;q=0.8",
	            	"Referer":"http://www.example.com/",
	            	"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"
					}
		res = requests.get(url,  headers=headers)
		print res
		content = res.content
		return  content 
	
	def analysis_html(self, content):
		data_list = []
		#---------change html to xml --------
		selector = etree.HTML(content)
	
		#get Title
		titles = selector.xpath('//h2[@class="content-title"]//text()')
		titles_new = []
		#print "111111111111"
		for i in titles:
			if len(i) != 0:
				titles_new.append(i.encode("utf-8"))
		data_list.append(titles_new)
		#print isinstance(titles,Iterable)
		
		#get Article url
		#links = selector.xpath('//a[@data-gaevent="home_recommend_asks:v1.1.1.1:ask"]//@href')#('//div/a[@class="j_th_tit"]/@href')	
		links = selector.xpath('//div[@class="content"]//ul//li//a[@title]//@href')#('//div/a[@class="j_th_tit"]/@href')	
		links_new  =[]
		#print "222222222222"
		for i in links:
			j = i.strip()
			if len(j) != 0:
				links_new.append(i)
	
		if len(links_new) != 0:
			data_list.append(links_new)	
	
	
		#get Article describle
		describes = selector.xpath('//div[@class="content"]//ul//li//a//text()')
		describes_new = []
		#print "3333333333"
		for i in describes:
			j = i.strip()
			if len(j) != 0 and j != u'\u8be6\u7ec6':
				print type(i)
				print type(i.encode('utf-8'))
				print i.encode('utf-8')
				describes_new.append(i.encode('utf-8'))
	
		if len(describes) != 0:
			data_list.append(describes_new)
		
		#create token
		end_data = {}
		j = 0
		for i in links_new:
		#	if len(i) != 0:
		#		print "**********"
			tmp = []
			hash = hashlib.md5()
			hash.update(i)
			token = hash.hexdigest()
			tmp.append(i)
			#tmp.append(titles_new[j].decode('utf-8'))
			#print "**********" + describes_new[j]	
			tmp.append(describes_new[j].decode('utf-8'))
			end_data[token] = tmp
			j = j + 1
		
		#for i in end_data():
		#	print i
		
		return end_data
		
		
	def queue_put(self, queue, data_dict):
		print "This is producer, will input data:"
		dir_file = sys.path[0]
		f = open(dir_file + '/Data/text/data.txt','a+')
		for value in data_dict.values():
			queue.put(value)
			if re.match("https://www.15yan.com/", value[0]):
				#get 15yan html
				content = self.request_leve2(value[0])
				
				#get title
				data_txt = []
				for i in  self.analysis_2_title(content):
					#print i.encode("utf-8")
					data_txt.append("<<" + i.encode("utf-8") + ">>")
					print "today we find  new data:   %s"%(i.encode("utf-8"))
	
				#set title as key, the article content as value, to create dict of list 			
				for i in self.anakysis_2_body(content):
					#print i.encode("utf-8")
					data_txt.append(i.encode("utf-8"))
			
				for i in data_txt:
					#print i
					#print type(i)
					f.write(i + '\r\n')
			
		f.close()
	
	def request_leve2(self, url):
		headers = { "Accept":"text/html,application/xhtml+xml,application/xml;",
	                  "Accept-Encoding":"gzip",
	                  "Accept-Language":"zh-CN,zh;q=0.8",
	                  "Referer":"http://www.example.com/",
	                  "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"
	                  }
		res = requests.get(url,  headers=headers)
		content = res.content
		return  content
	
	
	def analysis_2_title(self, content):
		selector = etree.HTML(content)
		title = selector.xpath("//header[@class='post-header']//h1//text()")
		return title
	
	def anakysis_2_body(self, content):
		selector = etree.HTML(content)
		body = selector.xpath("//div[@class='noteable post-body']//section//div[@class='section-inner']//p//text()")
		return body
