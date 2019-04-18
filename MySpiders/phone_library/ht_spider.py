from super_spider import SuperSpider
from selenium import webdriver
import time
def ht_spider(start_time='2019-01-02 00:00:00',end_time='2019-04-02 00:00:00'):
	ht=SuperSpider(use_selenium=True,default_field='null',field_list=('start_time','call_duration','connect_duration','talk_duration','ring_duration','call_direction','connect_status','sound_file','customer_id','caller','called','caller_department','caller_number','caller_user_name','project_name','call_type'),table_name='ht_data')
	ht.selenium_get(r'http://210.13.87.106:8088/ec2')
	ht.selenium_click('//td[@tabindex="-1"]//div[@class="v-captiontext"]',3)
	ht.selenium_input('//input[@class="v-textfield"]','mgrdefault8',index=3)
	ht.selenium_input('//input[@class="v-textfield"]','fuyan2018',index=-1)
	ht.selenium_click('//span[@class="v-button-caption"]',3,index=1)
	ht.selenium_click('//span[@class="v-nativebutton-caption"]',3,index=2)
	ht.selenium_input('//input[@class="v-textfield v-datefield-textfield"]',start_time,index=0)
	ht.selenium_input('//input[@class="v-textfield v-datefield-textfield"]',end_time,index=0)
	ht.selenium_click('//div[@class="v-filterselect-button"]',index=2)
	ht.selenium_click('//td[@class="gwt-MenuItem"]/span',index=0)
	ht.selenium_click('//div[@class="v-button v-button-default default"]//span[@class="v-button-caption"]',3,index=0)
	page_all=ht.selenium_search('//*[@id="ec2-100180"]/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/div[1]/div/div[2]/div/div[2]/div/div/div[2]/div/div/div/div[2]/div/div/div/div[2]/div/div/div/div[2]/div/div/div/div[7]/div/div')[0]
	page_number=ht.re_find(r'/(\d+)页',page_all).__next__().group(1)
	for page in range(1,int(page_number)):
		html=ht.page_source()
		data_list=ht.data_search(html=html,xpath='//td[@class="v-table-cell-content"]//text()')
		for i,index1,index2 in zip(range(1,1000),range(0,1000,18),range(18,1000,18)):
			split_list=data_list[index1:index2]
			if split_list:
				split_list.pop(8)
				split_list.pop(8)
				for field,data in zip(ht.field_list,split_list):
					exec(f'ht.{field}=data')
				ht.data_save()
				print(f'第{page}页——第{i}条数据——导入完成')
			else:
				break
		ht.selenium_click('//*[@id="ec2-100180"]/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/div[1]/div/div[2]/div/div[2]/div/div/div[2]/div/div/div/div[2]/div/div/div/div[2]/div/div/div/div[2]/div/div/div/div[3]/div/div/span/span',3)
	ht.spider_end()
ht_spider()