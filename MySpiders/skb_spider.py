import requests,time,pymysql
from pyquery import PyQuery as pq
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
word_lists=['医疗美容','证券','教育','餐饮加盟','呼叫中心','房产买卖','保险中介','信贷']
db=pymysql.connect(host='localhost',db='jsn_data',user='root',passwd='never1019120542,',charset='utf8')
db.autocommit(True)
cursor=db.cursor()
dr=webdriver.Chrome()
dr.maximize_window()
dr.get('https://biz.lixiaoskb.com/search')
input_lists=dr.find_elements_by_class_name('el-input__inner')
input_lists[0].clear()
input_lists[0].send_keys('13861956774')
input_lists[1].clear()
input_lists[1].send_keys('skb666666')
dr.find_element_by_xpath('//*[@id="app"]/div[1]/div/div/div[1]/div[2]/div[3]/button').click()
time.sleep(2)
for word in word_lists:
	print('开始爬取关键字:——{}——'.format(word))
	search_input=dr.find_element_by_xpath('//*[@id="searchDeInput"]/div[1]/div/input')
	search_input.clear()
	search_input.send_keys(word)
	search_input.send_keys(Keys.ENTER)
	time.sleep(2)
	page_number=dr.find_element_by_xpath('//*[@id="jumpWrapper"]/div/div[1]/ul/li[6]').text
	#print(page_number)
	for page in range(1,int(page_number)+1):
		print('{}——第{}页'.format(word,page))
		page_input=dr.find_element_by_xpath('//*[@id="jumpPage"]/div/div/input')
		page_input.clear()
		page_input.send_keys('{}'.format(page))
		page_input.send_keys(Keys.ENTER)
		time.sleep(2)
		for i in range(1,11):
			url=dr.find_element_by_xpath('//*[@id="homeMainContent"]/div/div[2]/div/div[7]/div[1]/div[{}]/div/div[2]/span[1]/a'.format(i)).get_attribute('href')
			js="window.open('{}')".format(url)
			dr.execute_script(js)
			time.sleep(3)
			all_windows=dr.window_handles
			dr.switch_to.window(all_windows[-1])
			company=dr.find_element_by_xpath('//*[@id="homeMainContent"]/div/div[1]/div/div/div[2]/div/div/div[2]/div[1]').text
			print('开始爬取——{}——信息'.format(company))
			legal_person=dr.find_element_by_xpath('//*[@id="report"]/div[2]/div[3]/div[1]/div[2]/div[1]/div[2]/div[1]/div[2]/div').text
			for i in range(3):
				try:
					dr.find_element_by_xpath('//*[@id="report"]/div[1]/div/div/div/div/div[3]/span').click()
				except:
					pass
			time.sleep(1)
			j=0
			while True:
				j+=1
				try:
					phone=dr.find_element_by_xpath('//*[@id="report"]/div[1]/div/div/div[2]/div/div[1]/ul/div/div/div[{}]/div[1]/span[1]'.format(j)).text
					person=dr.find_element_by_xpath('//*[@id="report"]/div[1]/div/div/div[2]/div/div[1]/ul/div/div/div[{}]/div[2]/div[1]/div/div/div/div[1]/div[2]'.format(j)).text
					qq=dr.find_element_by_xpath('//*[@id="report"]/div[1]/div/div/div[2]/div/div[1]/ul/div/div/div[{}]/div[2]/div[1]/div/div/div/div[2]/div[2]'.format(j)).text
					mail=dr.find_element_by_xpath('//*[@id="report"]/div[1]/div/div/div[2]/div/div[1]/ul/div/div/div[{}]/div[2]/div[1]/div/div/div/div[3]/div[2]/span'.format(j)).text
					address=dr.find_element_by_xpath('//*[@id="report"]/div[1]/div/div/div[2]/div/div[1]/ul/div/div/div[{}]/div[2]/div[1]/div/div/div/div[4]/div[2]/span[1]'.format(j)).text
				except:
					break
				cursor.execute('insert into skb_data (company,legal_person,phone,person,qq,mail,address) values ("{}","{}","{}","{}","{}","{}","{}")'.format(company,legal_person,phone,person,qq,mail,address))
				print('{}——第{}个联系方式导入完成'.format(company,j))
			dr.close()
			dr.switch_to.window(all_windows[0])
db.close()
dr.quit()
print('end')