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
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

class SuperSpider:
	def __init__(self,host='localhost',user='root',passwd='never1019120542,',db='jsn_data',charset='utf8',table_name='phone_library',use_selenium=False,log_file='log.txt',
		headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
				'Accept-Encoding': 'gzip, deflate, br',
				'Accept-Language': 'zh-CN,zh;q=0.9',
				'Connection': 'keep-alive',
				'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'},
		field_list=('source_name','source_page','company_name','person_name','phone_number','fax','qq','mail','business_mode',
					'register_money','company_type','main_product','website','address','staff_number','spider_datetime')):
		self.use_selenium=use_selenium
		if use_selenium:
			chrome_options = webdriver.ChromeOptions()
			chrome_options.add_argument("--headless")
			chrome_options.add_argument('--no-sandbox')
			self.dr=webdriver.Chrome(options=chrome_options)
			# self.dr=webdriver.Chrome()
			# self.dr.maximize_window()
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
		self.spider_datetime=datetime.now().strftime('%Y-%m-%d %X')		#datetime在初始化里面非常尴尬，因为这就导致不是实时的，对于运行时间很长的爬虫，时间会非常不准确
		#logging.basicConfig(level=logging.CRITICAL,filename=log_file,filemode='a',format='%(asctime)s %(message)s',datefmt='%Y-%m-%d %H:%M:%S')
		print('——————————开始爬取——————————	')

	@retry(stop_max_attempt_number=3)
	def get_request(self,url):
		self.html=self.session.get(url,headers=self.headers).html    			#注意，这里的html改成了实例属性，没有了返回值，相应的下面方法可直接调用html而不用作为参数传递

	# def post_request(self,url,data):
	# 	self.html=self.session.post(url,headers=self.headers,data=data).html

	def data_search(self,search_type,location,attr='text'):
		if attr=='text':
			search_list=eval(f'(i.text for i in self.html.{search_type}(\'{location}\'))')
		else:
			search_list=eval(f'(i.attrs["{attr}"] for i in self.html.{search_type}(\'{location}\'))')
		return search_list

	@retry(stop_max_attempt_number=3)
	def use_requests_to_html(self,url,encoding,error='ignore'):
		html=requests.get(url,headers=self.headers).content.decode(encoding,error)
		return html

	def selenium_open(self,url):				#selenium的打开网页的部分还是要独立出来，比较灵活一点
		self.dr.get(url)
		self.dr.implicitly_wait(5)

	def selenium_js(self,js_list,sleep_time=1):		#这里的js改为列表，动态等待时间，方便在一个页面执行多步js操作，传参时要注意	
		for js in js_list:
			self.dr.execute_script(js)
			time.sleep(sleep_time)

	def selenium_click(self,search_type,location,sleep_time=1):			
		eval(f'self.dr.find_element_by_{search_type}(\'{location}\').click()')
		time.sleep(sleep_time)

	@retry(stop_max_attempt_number=5)
	def selenium_input(self,search_type,location,key_word,sleep_time=1,enter=False):
		input_obj=eval(f'self.dr.find_element_by_{search_type}(\'{location}\')')
		for i in range(3):
			input_obj.clear()
		input_obj.send_keys(key_word)
		if enter:
			input_obj.send_keys(Keys.ENTER)
		time.sleep(sleep_time)

	def selenium_search(self,search_type,location,attr='text'):
		if attr == 'text':
			search_list=eval(f'(i.text for i in self.dr.find_elements_by_{search_type}(\'{location}\'))')
		else:
			search_list=eval(f'(i.get_attribute("{attr}") for i in self.dr.find_elements_by_{search_type}(\'{location}\'))')
		return search_list

	def switch_window(self,sleep_time=1):
		all_windows=self.dr.window_handles
		self.dr.switch_to.window(all_windows[-1])
		time.sleep(sleep_time)

	def current_url(self):
		return self.dr.current_url()

	def window_close(self):
		self.dr.close()

	def json_to_py(self,json_data,deal=False):
		if deal == True:
			start_index=json_data.find('{')
			end_index=json_data.rfind('}')
			json_data=json_data[start_index:end_index+1]
		print(json_data)
		py_data=demjson.decode(json_data)
		return py_data

	def re_find(self,re_data,data):
		return re.finditer(re_data,data)

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
		self.spider_datetime=datetime.now().strftime('%Y-%m-%d %X')				#datetime在这里更新了一下，这样才是实时的datetime
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

	def spider_log(self,message):				#添加了日志，在初始化里面记得要修改文件路径
		logging.critical(message)

	def spider_end(self):
		if self.use_selenium:
			self.dr.quit()
		self.db.close()
		print('——————————爬取完成——————————')