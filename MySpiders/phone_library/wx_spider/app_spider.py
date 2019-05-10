import sys
sys.path.append(r'C:\Users\Administrator\Desktop\phone_library')
from appium import webdriver
from time import sleep
import base64
from faker import Faker
from datetime import datetime
import requests
from super_spider import SuperSpider
class AppSpider:
	def __init__(self):
		print('------start------')

	def open_app(self,appium_ip,desired_caps,time_sleep=5):
		self.dr = webdriver.Remote(appium_ip, desired_caps)  # 连接Appium
		sleep(time_sleep)

	def xpath_elements(self,xpath):
		return self.dr.find_elements_by_xpath(xpath)

	def xpath_click(self,xpath=None,element=None,index=0,time_sleep=1):
		if xpath:
			element=self.xpath_elements(xpath)[index]
		element.click()
		sleep(time_sleep)

	def xpath_input(self,xpath=None,word=None,element=None,index=0,time_sleep=1):
		if xpath:
			element=self.xpath_elements(xpath)[index]
		element.clear()
		element.send_keys(word)
		sleep(time_sleep)

	def xpath_search(self,xpath=None,attr=None,element=None,index=None):
		if xpath:
			if not index:
				return [i.get_attribute(attr) for i in self.xpath_elements(xpath)]
			else:
				return self.xpath_elements(xpath)[index].get_attribute(attr)
		else:
			return element.get_attribute(attr)

	def percent_swipe(self,width_percent1,height_percent1,width_percent2,height_percent2,during=500):
		screen=self.dr.get_window_size()
		width=screen['width']
		height=screen['height']
		self.dr.swipe(width*width_percent1,height*height_percent1,width*width_percent2,height*height_percent2,during)

	def save_screenshot(self,path):
		self.dr.save_screenshot(path)


	def end(self):
		print('------end------')
		self.dr.quit()

	def get_phone_number():
		wx=SuperSpider()
		html=wx.get_html('http://192.168.30.200/api/check_wx/get_mobile.html?max_id=6000000&num=5000')
		data_list=wx.json_to_py(html)
		print(data_list)
	