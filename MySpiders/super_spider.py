from requests_html import HTMLSession
from selenium import webdriver
import demjson
import time
from datetime import datetime,timedelta
import pymysql
import logging
import re
import requests
from retrying import retry

class SuperSpider:
	def __init__(self,host='localhost',user='root',passwd='never1019120542,',db='jsn_data',charset='utf8',table_name='phone_library',
		headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
				'Accept-Encoding': 'gzip, deflate, br',
				'Accept-Language': 'zh-CN,zh;q=0.9',
				'Connection': 'keep-alive',
				'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'},
		field_list=('source','company_name','person_name','cell_phone','phone_code','fax','qq','business_mode',
					'register_money','company_type','main_product','website','address','spider_datetime')):
		self.table_name=table_name
		self.db=pymysql.connect(host=host,user=user,passwd=passwd,db=db,charset=charset)
		self.db.autocommit(True)
		self.cursor=self.db.cursor()
		self.headers=headers
		self.session=HTMLSession()
		self.field_list=field_list
		for field in field_list:
			exec(f'self.{field}=""')
		self.spider_date=datetime.now().strftime('%Y-%m-%d')
		self.spider_datetime=datetime.now().strftime('%Y-%m-%d %X')
		print('——————————开始爬取——————————	')

	@retry(stop_max_attempt_number=5)
	def get_request(self,url):
		html=self.session.get(url,headers=self.headers).html
		return html

	def data_search(self,html,search_type=None,location=None,attr='text'):
		if attr=='text':
			search_list=eval(f'(i.text for i in html.{search_type}("{location}"))')
		else:
			search_list=eval(f'(i.attrs["{attr}"] for i in html.{search_type}(\'{location}\'))')
		return search_list

	@retry(stop_max_attempt_number=5)
	def use_requests_to_html(self,url,encoding,error='ignore'):
		html=requests.get(url,headers=self.headers).content.decode(encoding,error)
		return html

	def use_selenium(self):
		self.dr=webdriver.Chrome()

	def selenium_js(self,url,js):
		self.dr.get(url)
		self.dr.implicitly_wait(5)
		self.dr.execute_script(js)
		time.sleep(2)

	def selenium_search(self,search_type,location,attr='text'):
		if attr == 'text':
			search_list=eval(f'(i.text for i in self.dr.find_elements_by_{search_type}(\'{location}\'))')
		else:
			search_list=eval(f'(i.get_attribute("{attr}") for i in self.dr.find_elements_by_{search_type}(\'{location}\'))')
		return search_list

	def json_to_py(self,json_data,deal=False):
		if deal == True:
			start_index=json_data.find('{')
			end_index=json_data.rfind('}')
			json_data=json_data[start_index:end_index+1]
		py_data=demjson.decode(json_data)
		return py_data

	def date_ago(self,ago_number):
		aim_date=(datetime.strptime(self.spider_date,'%Y-%m-%d')-timedelta(days=ago_number)).strftime('%Y-%m-%d')
		return aim_date

	def to_null(self,data):
		value=data if data!='-' and data else 'null'
		return value

	def sql_search(self,sql):
		self.cursor.execute(sql)
		sql_data=self.cursor.fetchall()
		return sql_data

	def data_save(self):
		for field in self.field_list:
			if field == self.field_list[0]:
				field_list_str='('+field+','
			elif field == self.field_list[-1]:
				field_list_str=field_list_str+field+')'
			else:
				field_list_str=field_list_str+field+','
		self_field_list=[]
		for field in self.field_list:
			eval(f'self_field_list.append(self.{field})')
		sql=f'insert into {self.table_name} {field_list_str} values {tuple(self_field_list)}'.replace("'null'",'null')
		self.cursor.execute(sql)

	def spider_end(self):
		self.db.close()
		print('——————————爬取完成——————————')

