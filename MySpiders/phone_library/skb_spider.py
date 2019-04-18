from super_spider import SuperSpider
import json
import os
from apscheduler.schedulers.blocking import BlockingScheduler
def skb_spider(phone,passwd,word,page_now=1):
	skb=SuperSpider(use_selenium=True)
	skb.source_name='搜客宝'
	skb.fax='-'
	skb.staff_number='-'
	skb.selenium_open('https://biz.lixiaoskb.com/login')
	skb.selenium_input('xpath','//*[@id="app"]/div[1]/div/div/div[1]/div[2]/div[2]/form/div[1]/div/div/div/input',phone)
	skb.selenium_input('xpath','//*[@id="app"]/div[1]/div/div/div[1]/div[2]/div[2]/form/div[2]/div/div/div/input',passwd,enter=True,sleep_time=3)
	js3='document.querySelector("#tab-0").click();'
	skb.selenium_js([js3])
	skb.selenium_input('xpath','//*[@id="searchDeInput"]/div[1]/div/input',word,sleep_time=5,enter=True)
	all_page=500
	if int(page_now) == int(all_page):
		print(f'{word}——所有数据爬取结束')
		skb.spider_end()
		return word,int(all_page)
	for page in range(page_now,int(all_page)+1):
		print(f'{word}——第{page}页')
		try:
			skb.selenium_scroll('//div[@id="jumpPage"]//input[@class="el-input__inner"]')
			skb.selenium_input('css_selector','#jumpPage .el-input input',page,sleep_time=2,enter=True)
		except Exception as e:
			print(e)
			continue
		url_list=skb.selenium_search('xpath',f'//div[@class="card"]//span[@class="name"]//a',attr='href')
		for url in url_list:
			skb.source_page=url
			js1=f'window.open("{url}")'
			skb.selenium_js([js1],sleep_time=3)
			skb.switch_window()
			try:
				skb.company_name=skb.selenium_search('css_selector','.top .name').__next__()
			except Exception as e:
				print(e)
				skb.window_close()
				skb.switch_window(sleep_time=2)
				continue
			try:
				company_info_dict1={i.split(':')[0].strip():i.split(':')[-1].strip() for i in skb.selenium_search('css_selector','.line .group')}
				skb.company_type=company_info_dict1.get('公司类型','-')
				skb.address=company_info_dict1.get('通讯地址','-')
				business_mode=company_info_dict1.get('所属行业','-')
				skb.website=company_info_dict1.get('官方网站','-').strip('更多>> ')
			except:
				pass
			try:
				company_info_dict2={i.split('\n')[0].strip('/ '):i.split('\n')[-1].strip('/ ') for i in skb.selenium_search('css_selector','.gongshang-col')}
				skb.person_name=company_info_dict2.get('法人/负责人','-')
				skb.register_money=company_info_dict2.get('注册资本','-')
				skb.main_product=company_info_dict2.get('经营范围','-')
			except:
				pass
			js2='var open_btn=document.querySelector(".mask-box .action span");open_btn.click();'
			try:
				skb.selenium_js([js2],sleep_time=3)
			except Exception as e:
				print(e)
				phone_list=[]
				qq_list=[]
				try:
					phone_info=skb.selenium_search('css_selector','.el-scrollbar__view')
					phone_info_list=list(phone_info)[1].split('\n')
				except Exception as e:
					print(e)
					skb.window_close()
					skb.switch_window(sleep_time=2)
					continue
				#print(phone_info_list)
				for i,j in enumerate(phone_info_list):
					if j == '选 择':
						skb.phone_number=phone_info_list[i-1]
					elif j == '联系人':
						skb.person_name=phone_info_list[i+1]
					elif j == 'qq号码':
						skb.qq=phone_info_list[i+1].strip(',')
					elif j == '电子邮箱':
						skb.mail=phone_info_list[i+1].strip(',')
						try:
							skb.data_save()
						except:
							continue
				print(f'{word}——第{page}页——{skb.company_name}信息导入完成')
				skb.window_close()
				skb.switch_window(sleep_time=2)
				continue
			phone_list=[]
			qq_list=[]
			try:
				phone_info=skb.selenium_search('css_selector','.el-scrollbar__view')
				phone_info_list=list(phone_info)[1].split('\n')
			except Exception as e:
				print(e)
				skb.window_close()
				skb.switch_window(sleep_time=2)
				continue
			#print(phone_info_list)
			for i,j in enumerate(phone_info_list):
				if j == '选 择':
					skb.phone_number=phone_info_list[i-1]
				elif j == '联系人':
					skb.person_name=phone_info_list[i+1]
				elif j == 'qq号码':
					skb.qq=phone_info_list[i+1].strip(',')
				elif j == '电子邮箱':
					skb.mail=phone_info_list[i+1].strip(',')
					try:
						skb.data_save()
					except:
						continue
			print(f'{word}——第{page}页——{skb.company_name}信息导入完成')
			use_number=skb.selenium_search('css_selector','.inner-user .viewCount:first-child').__next__()
			print(use_number)
			if int(use_number) == 0:
				print(f'{word}——第{page}页——今日次数已用完')
				skb.spider_end()
				return word,page
			skb.window_close()
			skb.switch_window(sleep_time=2)
	skb.spider_end()
	print(f'{word}——所有数据爬取结束')
	return word,int(all_page)


user_pwd=(('18326601878','jsn95279527'),('18551107173','jsn95279527'),('18856895487','jsn95279527'),('13155291086','jsn952727'),('13514987518','jsn95279527'))
def run_all_spider():
	if not os.path.exists('skb_json.txt'):
		# json.dump({'合肥金融':76,'合肥咨询':76,'合肥网络':1,'合肥科技':1,'合肥管理':1,'合肥服务':1},open('skb_json.txt','w+'))
		# json.dump({'合肥教育':240,'合肥餐饮':240,'合肥技术':240,'合肥信贷':240,'合肥电销':240},open('skb_json.txt','w+'))
		json.dump({'上海股票':1,'上海咨询':1,'上海医美':1,'上海学历':1,'上海教育':1},open('skb_json.txt','w+'))
	skb_dict=json.load(open('skb_json.txt','r'))
	for login_info,key in zip(user_pwd,skb_dict.keys()):
		return_data=skb_spider(*login_info,key,int(skb_dict[key]))
		print(return_data)
		skb_dict[return_data[0]]=int(return_data[1])
		json.dump(skb_dict,open('skb_json.txt','w'))			#这里的json.dump应该放到循环里面，这样每执行完一个关键词都会保存一次，会及时保存运行状态，如果放到循环外面，只要中途一个关键词报错导致程序崩溃，就会丢失所有的运行状态数据
if __name__ == '__main__':
	# scheduler=BlockingScheduler()
	# scheduler.add_job(func=run_all_spider,trigger='cron',hour='4',minute='0',second='0')
	# scheduler.start()
	run_all_spider()