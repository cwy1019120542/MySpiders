import requests,time,pymysql
from pyquery import PyQuery as pq
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from apscheduler.schedulers.blocking import BlockingScheduler
def skb_func(phone,passwd,word,page):
	db=pymysql.connect(host='localhost',db='jsn_data',user='root',passwd='never1019120542,',charset='utf8')
	db.autocommit(True)
	cursor=db.cursor()
	dr=webdriver.Chrome()
	dr.maximize_window()
	dr.get('https://biz.lixiaoskb.com/search')
	time.sleep(3)
	input_lists=dr.find_elements_by_class_name('el-input__inner')
	input_lists[0].clear()
	input_lists[0].send_keys(phone)
	input_lists[1].clear()
	input_lists[1].send_keys(passwd)
	dr.find_element_by_xpath('//*[@id="app"]/div[1]/div/div/div[1]/div[2]/div[3]/button').click()
	time.sleep(2)
	print('开始爬取关键字:——{}——'.format(word))
	search_input=dr.find_element_by_xpath('//*[@id="searchDeInput"]/div[1]/div/input')
	search_input.clear()
	search_input.send_keys(word)
	time.sleep(1)
	search_input.send_keys(Keys.ENTER)
	time.sleep(2)
	page_number=dr.find_element_by_xpath('//*[@id="jumpWrapper"]/div/div[1]/ul/li[6]').text
	#print(page_number)
	for p in range(page,int(page_number)+1):
		print('{}——第{}页'.format(word,p))
		page_input=dr.find_element_by_xpath('//*[@id="jumpPage"]/div/div/input')
		for i in range(3):
			page_input.clear()
		time.sleep(1)
		page_input.send_keys('{}'.format(p))
		page_input.send_keys(Keys.ENTER)
		time.sleep(2)
		for i in range(1,11):
			url=dr.find_element_by_xpath('//*[@id="homeMainContent"]/div/div[2]/div/div[7]/div[1]/div[{}]/div/div[2]/span[1]/a'.format(i)).get_attribute('href')
			js="window.open('{}')".format(url)
			dr.execute_script(js)
			all_windows=dr.window_handles
			dr.switch_to.window(all_windows[-1])
			time.sleep(3)
			try:
				company=dr.find_element_by_xpath('//*[@id="homeMainContent"]/div/div[1]/div/div/div[2]/div/div/div[2]/div[1]').text
			except:
				company=dr.find_element_by_xpath('//*[@id="homeMainContent"]/div/div[1]/div/div/div[2]/div/div/div[2]/div[1]/span').text	
			company_type=dr.find_element_by_xpath('//*[@id="homeMainContent"]/div/div[1]/div/div/div[2]/div/div/div[2]/div[2]/span[1]/span[2]').text
			date=dr.find_element_by_xpath('//*[@id="homeMainContent"]/div/div[1]/div/div/div[2]/div/div/div[2]/div[2]/span[2]/span[2]').text
			profession=dr.find_element_by_xpath('//*[@id="homeMainContent"]/div/div[1]/div/div/div[2]/div/div/div[2]/div[2]/span[3]/span[2]').text
			website=dr.find_element_by_xpath('//*[@id="homeMainContent"]/div/div[1]/div/div/div[2]/div/div/div[2]/div[3]/span[1]/span[2]/span').text
			company_address=dr.find_element_by_xpath('//*[@id="homeMainContent"]/div/div[1]/div/div/div[2]/div/div/div[2]/div[3]/span[2]/span[2]').text
			try:
				number=dr.find_element_by_xpath('//*[@id="report"]/div[2]/div[3]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div/span').text
				capital=dr.find_element_by_xpath('//*[@id="report"]/div[2]/div[3]/div[1]/div[2]/div[1]/div[2]/div[2]/div[1]/div').text[4:]
				legal_person=dr.find_element_by_xpath('//*[@id="report"]/div[2]/div[3]/div[1]/div[2]/div[1]/div[2]/div[1]/div[2]/div').text[6:]
			except:
				number=capital=legal_person='-'
			try:
				dr.find_element_by_xpath('//*[@id="report"]/div[1]/div/div/div/div/div[3]/span').click()
			except:
				pass
			time.sleep(2)
			try:
				dr.find_element_by_xpath('//*[@id="report"]/div[1]/div/div/div/div/div[3]/span')
			except:
				j=0
				while True:
					j+=1
					try:
						phone=dr.find_element_by_xpath('//*[@id="report"]/div[1]/div/div/div[2]/div/div[1]/ul/div/div/div[{}]/div[1]/span[1]'.format(j)).text
						person=dr.find_element_by_xpath('//*[@id="report"]/div[1]/div/div/div[2]/div/div[1]/ul/div/div/div[{}]/div[2]/div[1]/div/div/div/div[1]/div[2]'.format(j)).text
						qq=dr.find_element_by_xpath('//*[@id="report"]/div[1]/div/div/div[2]/div/div[1]/ul/div/div/div[{}]/div[2]/div[1]/div/div/div/div[2]/div[2]'.format(j)).text
						mail=dr.find_element_by_xpath('//*[@id="report"]/div[1]/div/div/div[2]/div/div[1]/ul/div/div/div[{}]/div[2]/div[1]/div/div/div/div[3]/div[2]/span'.format(j)).text
						person_address=dr.find_element_by_xpath('//*[@id="report"]/div[1]/div/div/div[2]/div/div[1]/ul/div/div/div[{}]/div[2]/div[1]/div/div/div/div[4]/div[2]/span[1]'.format(j)).text
					except:
						if j == 1:
							cursor.execute('insert into skb_data (company,type,date,profession,website,company_address,capital,number) values ("{}","{}","{}","{}","{}","{}","{}","{}")'.format(company,company_type,date,profession,website,company_address,capital,number))
							print(f'{company}——信息导入完成')
						break
					try:
						cursor.execute('insert into skb_data (company,type,date,profession,website,company_address,capital,number,legal_person,phone,person,qq,mail,person_address) values ("{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}")'.format(company,company_type,date,profession,website,company_address,capital,number,legal_person,phone,person,qq,mail,person_address))
					except:
						continue
					print('{}——第{}个联系方式导入完成'.format(company,j))
				dr.close()
				dr.switch_to.window(all_windows[0])
			else:
				print(f'{phone}在{p}页{i}位置次数用完')
				db.close()
				dr.quit()
				return p
	db.close()
	dr.quit()
	print('end')
	return 0

def start_spider(phone,passwd,word,line):
	f=open(r'C:\Users\Administrator\Desktop\skb_log.txt','r+',encoding='utf8')
	word_lists=f.readlines()
	data_lists=word_lists[line].strip().split(' ')
	page=data_lists[1]
	if page == '0':
		f.close()
		print(f'{word}关键字已爬完')
		return
	page=skb_func(phone,passwd,word,int(page))
	f.seek(0)
	new_data=word+' '+str(page)+'\n'
	word_lists[line]=new_data
	f.writelines(word_lists)
	f.close()

def run():
	print('----------开始爬取----------')
	start_spider('13514987518','jsn95279527','医疗美容',0)
	start_spider('13155291086','jsn952727','证券',1)
	start_spider('18326601878','jsn95279527','教育',2)
	start_spider('18551107173','jsn95279527','餐饮加盟',3)
	start_spider('18856895487','jsn95279527','呼叫中心',4)
	start_spider('17621862011','jsn95279527','房产买卖',5)
	print('----------结束爬取----------')

if __name__ == '__main__':
	scheduler=BlockingScheduler()
	scheduler.add_job(func=run,trigger='cron',hour='19',minute='0',second='10')
	scheduler.start()