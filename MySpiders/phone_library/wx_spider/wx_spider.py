from time import sleep
from app_spider import AppSpider
import requests
import demjson
def wx_spider(phone_number_list,search_wait_time):
	wx=AppSpider()
	wx.open_app(desired_caps = {'platformName': 'Android','platformVersion': '5.1.1','deviceName': '127.0.0.1:62001','appPackage': 'com.tencent.mm','appActivity': 'com.tencent.mm.ui.LauncherUI'})
	wx.xpath_click("//android.widget.Button[@text='登录']",time_sleep=3)
	wx.xpath_input("//android.widget.EditText[@text='请填写手机号']",'17101558981')
	wx.xpath_click("//android.widget.Button[@text='下一步']",time_sleep=3)
	wx.xpath_input("//android.widget.EditText",'ooo123456')
	wx.xpath_click("//android.widget.Button[@text='登录']",time_sleep=5)
	wx.xpath_click("//android.widget.Button[@text='是']",time_sleep=20)
	wx.xpath_click("//android.widget.ImageView",index=-1)
	wx.xpath_click("//android.widget.TextView[@text='添加朋友']")
	change_input=wx.xpath_elements("//android.widget.TextView[@text='微信号/QQ号/手机号']")[0]
	wx.xpath_click(element=change_input)
	start_id=None
	for phone_id,phone_number in phone_number_list:
		if not start_id:
			start_id=phone_id
		while True:		
			wx.xpath_input("//android.widget.EditText",phone_number,time_sleep=2)
			search_btn=wx.xpath_elements("//android.widget.TextView[contains(@text,'搜索')]")
			if search_btn:
				wx.xpath_click(element=search_btn[0])
				break		
			else:
				try:
					wx.xpath_click("//android.widget.ImageView")
				except Exception as error:
					print(error)
					wx.save_screenshot('error.png')
					sleep(9999)
				wx.xpath_click(element=change_input)
		none_element=wx.xpath_elements("//android.widget.TextView[@text='该用户不存在']")
		end_element=wx.xpath_elements("//android.widget.TextView[@text='操作过于频繁，请稍后再试']")
		if none_element:
			data_dic={"phone_number":phone_number,"sex":"","is_useful":0}
		elif end_element:
			end_id=phone_id
			print(f"开始id为{start_id},结束id为{end_id},搜索个数为{end_id-start_id},等待时间为{search_wait_time}s")
			break
		else:
			element_list=wx.xpath_elements("//android.widget.ImageView")
			sex=wx.xpath_search(element=element_list[1],attr="contentDescription")
			if sex == '男':
				sex=1
			elif sex == '女':
				sex=0
			else:
				sex=''
			data_dic={"phone_number":phone_number,"sex":sex,"is_useful":1}
			wx.xpath_click(element=element_list[-1])
		print(f'第{phone_id-start_id+1}次完成')
		print(data_dic)
		print(f'等待{search_wait_time}s......')
		sleep(search_wait_time)
	wx.end()

def get_phone_number(max_id,number):
	json_data=requests.get(f'http://192.168.30.200/api/check_wx/get_mobile.html?max_id={max_id}&num={number}').text
	data_list=demjson.decode(json_data)
	return data_list

def start():
	data_list=get_phone_number(0,5000)
	phone_number_list=((i['id'],i['mobile']) for i in data_list)
	wx_spider(phone_number_list,search_wait_time=50)

start()




	# while True:
	# 	wx.xpath_click("//android.widget.TextView[@text='微信号/QQ号/手机号']")
	# 	wx.xpath_input("//android.widget.EditText[@text='微信号/QQ号/手机号']","1")
	# 	sleep(5)
	# 	element_list=wx.xpath_elements("//android.widget.TextView[contains(@text,'手机号:')]")
	# 	if element_list:
	# 		break
	# 	else:
	# 		wx.xpath_click("//android.widget.ImageView")
	# last_phone_number=None
	# while True:
	# 	person_list=[]
	# 	element_list=wx.xpath_elements("//android.widget.TextView[contains(@text,'手机号:')]")
	# 	last_element=element_list[-1]
	# 	aim_phone_number=wx.xpath_search(element=last_element,attr='text').strip('手机号: ')
	# 	if aim_phone_number == last_phone_number:
	# 		break
	# 	last_phone_number=aim_phone_number
	# 	for element in element_list:
	# 		phone_number=wx.xpath_search(element=element,attr='text').strip('手机号: ')
	# 		wx.xpath_click(element=element)
	# 		sleep(1)
	# 		is_exists=wx.xpath_search("//android.widget.Button[@text='发送邀请']",'text')
	# 		if is_exists:
	# 			person_list.append({"phone_number":phone_number,"is_useful":0,"sex":""})
	# 			wx.xpath_click("//android.widget.ImageView")
	# 		else:
	# 			is_useful=1
	# 			sex=wx.xpath_search("//android.widget.ImageView",'contentDescription',index=2)
	# 			print(sex)
	# 			if sex:
	# 				if sex == "男":
	# 					sex=1
	# 				else:
	# 					sex=0
	# 			else:
	# 				sex=''
	# 			person_list.append({"phone_number":phone_number,'sex':sex,"is_useful":1})
	# 			wx.xpath_click("//android.widget.ImageView",index=-1)
	# 	print(person_list)
	# 	response=requests.get(f"http://192.168.30.200/api/check_wx/put_mobile.html?mobiles={demjson.encode(person_list)}",headers={'user-agent':'User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'})
	# 	print(response.text)
	# 	wx.percent_swipe(0.5,0.9,0.5,0.1,2000)

# def get_phone_number():
# 	max_id=0
# 	number=5000
# 	work_book=openpyxl.load_workbook('pattern.xlsx')
# 	sheet=work_book['Sheet1']
# 	get_obj=SuperSpider()
# 	json_data=get_obj.get_html(f'http://192.168.30.200/api/check_wx/get_mobile.html?max_id={max_id}&num={number}')
# 	data_list=get_obj.json_to_py(json_data)
# 	for data,row_id in zip(data_list,range(2,5003)):
# 		phone_number=data['mobile']
# 		number_id=data['id']+1
# 		sheet[f'B{row_id}'].value=sheet[f'E{row_id}'].value=sheet[f'AO{row_id}'].value=phone_number
# 		print(f'{phone_number}-导入完成')
# 	work_book.save(f'{max_id+number}.xlsx')
# get_phone_number()

