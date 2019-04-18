from selenium import webdriver
import demjson
import time
from datetime import datetime,timedelta,date
import pymysql
import logging
import re
import requests
from retrying import retry
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from lxml import etree
from fake_useragent import UserAgent
import aiohttp
import asyncio
import os
import pytesseract
from PIL import Image
from collections import deque
from selenium.webdriver.support.ui import Select

class SuperSpider:
	def __init__(self,host='localhost',user='root',passwd='never1019120542,',db='jsn_data',charset='utf8',table_name='phone_library',use_selenium=False,log_file='log.txt',default_field='',maxlen=50,
		headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
				'Accept-Encoding': 'gzip, deflate, br',
				'Accept-Language': 'zh-CN,zh;q=0.9',
				'Connection': 'keep-alive',
				'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'},
		field_list=('source_name','source_page','company_name','person_name','phone_number','fax','qq','mail','business_mode',
					'register_money','company_type','main_product','website','address','staff_number','spider_datetime')):
		self.use_selenium=use_selenium
		self.ua=UserAgent(verify_ssl=False)
		self.my_deque=deque([],maxlen=maxlen)
		if use_selenium:
			# chrome_options = webdriver.ChromeOptions()
			# chrome_options.add_argument("--headless")
			# chrome_options.add_argument('--no-sandbox')
			# self.dr=webdriver.Chrome(options=chrome_options)
			self.dr=webdriver.Chrome()
			self.dr.maximize_window()
		self.table_name=table_name
		self.db=pymysql.connect(host=host,user=user,passwd=passwd,db=db,charset=charset)
		self.db.autocommit(True)
		self.cursor=self.db.cursor()
		self.headers=headers
		self.session=requests.session()			#放弃了requests_html模块，因为现在解析也不需要它了
		self.field_list=field_list
		for field in field_list:
			exec(f'self.{field}="{default_field}"')
		self.spider_date=datetime.now().strftime('%Y-%m-%d')
		self.spider_datetime=datetime.now().strftime('%Y-%m-%d %X')		#datetime在初始化里面非常尴尬，因为这就导致不是实时的，对于运行时间很长的爬虫，时间会非常不准确
		self.now_datetime=datetime.now()			#增加了一个实例变量现在时间的datetime类型
		self.now_date=datetime.today()		#增加了一个实例变量现在时间的date类型
		#logging.basicConfig(level=logging.CRITICAL,filename=log_file,filemode='a',format='%(asctime)s %(message)s',datefmt='%Y-%m-%d %H:%M:%S')
		print('——————————start——————————	')

	def random_headers(self):
		self.headers['User-Agent']=self.ua.random			#请求之前会随机变换请求头
		return self.headers

	@retry(stop_max_attempt_number=3)
	def get_request(self,url,proxies=None,timeout=None):
		self.random_headers()
		if proxies and timeout:
			response=self.session.get(url,headers=self.headers,proxies=proxies,timeout=timeout)    		
		else:
			response=self.session.get(url,headers=self.headers)
		return response
	
	def post_request(self,url,data=None,json=None):
		self.random_headers()
		if data:
			self.session.post(url,headers=self.headers,data=data)
		elif json:
			self.session.post(url,headers=self.headers,json=json)

	def get_html(self,url=None,charset='utf8',error='ignore',proxies=None,timeout=None):
		html=self.get_request(url,proxies,timeout).content.decode(encoding=charset,errors=error)
		return html

	def get_content(self,url=None,proxies=None,timeout=None):
		content=self.get_request(url,proxies,timeout).content
		return content

	def data_search(self,url=None,xpath=None,charset='utf8',error='ignore',html=None,proxies=None,timeout=None):		#注意这里是xpath_list，支持请求一次页面实现多次解析
		if not html:
			html=self.get_html(url,charset,error,proxies,timeout)
		if type(xpath) != str:		
			data_list=[]
			for xp in xpath:
				data_list.append(etree.HTML(html,etree.HTMLParser()).xpath(xp))		#使用lxml解析，统一采用xpath
		else:
			data_list=etree.HTML(html,etree.HTMLParser()).xpath(xpath)
		return data_list

	@retry(stop_max_attempt_number=3)
	def use_tesseract(self,img=None,lang='chi_sim',url=None):
		if url:
			img=r'D:\tesseract_img\img.png'
			content=self.get_content(url)
			if not os.path.exists(r'D:\tesseract_img'):
				os.mkdir(r'D:\tesseract_img')
			with open(img,'wb') as f:
				f.write(content)
		pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR/tesseract.exe'
		text = pytesseract.image_to_string(Image.open(img),lang=lang)
		return text

	def selenium_get(self,url):				#selenium的打开网页的部分还是要独立出来，比较灵活一点
		self.dr.get(url)
		self.dr.implicitly_wait(10)

	def selenium_label(self,xpath):
		aim_label=self.dr.find_elements_by_xpath(xpath)
		return aim_label

	@retry(stop_max_attempt_number=5)
	def selenium_scroll(self,xpath,sleep_time=2):
		target=self.selenium_label(xpath)[0]
		self.dr.execute_script("arguments[0].scrollIntoView();", target)
		time.sleep(sleep_time)

	def selenium_js(self,js_list,sleep_time=1):		#这里的js改为列表，动态等待时间，方便在一个页面执行多步js操作，传参时要注意	
		for js in js_list:
			self.dr.execute_script(js)
			time.sleep(sleep_time)

	def selenium_click(self,location,sleep_time=1,index=0):			
		self.selenium_label(location)[index].click()
		time.sleep(sleep_time)

	@retry(stop_max_attempt_number=5)
	def selenium_input(self,location,key_word,sleep_time=1,enter=False,index=0):
		input_obj=self.selenium_label(location)[index]
		for i in range(3):
			input_obj.clear()
		input_obj.send_keys(key_word)
		if enter:
			input_obj.send_keys(Keys.ENTER)
		time.sleep(sleep_time)

	def selenium_search(self,location,attr='text'):
		if attr == 'text':
			search_list=[i.text for i in self.selenium_label(location)]
		else:
			search_list=[i.get_attribute(attr) for i in self.selenium_label(location)]
		return search_list

	def selenium_select(self,xpath,select_index,index=0):
		Select(self.selenium_label(xpath)[index]).select_by_index(select_index)

	def switch_window(self,sleep_time=1):
		all_windows=self.dr.window_handles
		self.dr.switch_to.window(all_windows[-1])
		time.sleep(sleep_time)

	def page_source(self):
		return self.dr.page_source

	def current_url(self):
		return self.dr.current_url()

	def window_close(self):
		self.dr.close()

	def json_to_py(self,json_data,deal=False):
		if deal == True:
			start_index=json_data.find('{')
			end_index=json_data.rfind('}')
			json_data=json_data[start_index:end_index+1]
		py_data=demjson.decode(json_data)
		return py_data

	def re_find(self,re_data,data):
		return re.finditer(re_data,data)

	def date_ago(self,ago_number):
		aim_date=(datetime.strptime(self.spider_date,'%Y-%m-%d')-timedelta(days=ago_number)).strftime('%Y-%m-%d')
		return aim_date

	def to_datetime(self,aim_date):
		if type(aim_date) == str:
			if len(aim_date)==10:
				result_date=datetime.strptime(aim_date,'%Y-%m-%d')
			elif len(aim_date)>10:
				result_date=datetime.strptime(aim_date,'%Y-%m-%d %H-%M-%S')
		elif type(aim_date) == date:
			result_date=datetime(aim_date.year,aim_date.month,aim_date.day)
		return result_date


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
			if field == self.field_list[0] and field == self.field_list[-1]:
				field_list_str='('+field+')'
			elif field == self.field_list[0]:
				field_list_str='('+field+','
			elif field == self.field_list[-1]:
				field_list_str=field_list_str+field+')'
			else:
				field_list_str=field_list_str+field+','
		self_field_list=[]
		for field in self.field_list:
			eval(f'self_field_list.append(self.{field})')
		if len(self.field_list)==1:
			sql=f'insert into {self.table_name} {field_list_str} values ("{self_field_list[0]}")'.replace("'null'",'null')
			self.cursor.execute(sql)
		else:	
			sql=f'insert into {self.table_name} {field_list_str} values {tuple(self_field_list)}'.replace("'null'",'null')
			self.cursor.execute(sql)

	def spider_log(self,message):				#添加了日志，在初始化里面记得要修改文件路径
		logging.critical(message)

	def spider_end(self):
		if self.use_selenium:
			self.dr.quit()
		self.db.close()
		print('——————————end——————————')