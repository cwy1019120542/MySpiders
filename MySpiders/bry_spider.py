import requests,json,pymysql,chardet,json,pymysql,time,demjson
from pyquery import PyQuery as pq
from datetime import datetime,timedelta
from apscheduler.schedulers.blocking import BlockingScheduler
db=pymysql.connect(host='139.224.115.44',user='root',passwd='A9Vg+Dr*nP^fR=1V',db='bryframe3',charset='utf8')
db.autocommit(True)
cursor=db.cursor()
headers={
'Accept-Encoding':'gzip, deflate',
'Accept-Language':'zh-CN,zh;q=0.9',
'Connection':'keep-alive',
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}
def to_null(data,key):
	value=data[key] if data[key]!='-' and data[key] else 'null'
	if value != 'null':
		value=round(float(value),4)
	return value
def lhb_rank():
	q=pq(url=r'http://data.eastmoney.com/stock/tradedetail.html',encoding='gb2312')
	aim_date=q('.cate_type_ul.cate_type_date .at').text()
	while True:
		today=datetime.now()
		month_day='{}月{}日'.format(today.month,today.day)
		print(month_day)
		if aim_date != month_day:
			print('数据暂未刷新,等待5分钟')
			time.sleep(300)
		else:
			break
	date=today.strftime('%Y-%m-%d')
	url1=r'http://data.eastmoney.com/DataCenter_V3/stock2016/TradeDetail/pagesize=200,page={0},sortRule=-1,sortType=,startDate={1},endDate={1},gpfw=0,js=var%20data_tab_1.html?rt=25754497'.format('{}',date)
	#print(url1)
	page=1
	sql1='insert into lhb_rank (date,code,name,close_price,up_down,buy_amount,change_rate,currency_market) values ("{}","{}","{}",{},{},{},{},{})'
	while True:
		url2=url1.format(page)
		#print(url2)
		json_data=requests.get(url2,headers=headers).text.strip('var data_tab_0123456789=')
		#print(json_data)
		data_lists=demjson.decode(json_data)['data']
		if not data_lists:
			break
		else:
			for data in data_lists:
				sql2=sql1.format(date,data['SCode'],data['SName'],to_null(data,'ClosePrice'),to_null(data,'Chgradio'),to_null(data,'JmMoney'),to_null(data,'Dchratio'),to_null(data,'Ltsz'))
				cursor.execute(sql2)
				print('当日龙虎榜涨跌幅排名：{}-{}-{}-导入完成'.format(aim_date,data['SCode'],data['SName']))
		page+=1
	print('end：龙虎榜当日跌幅排名')
#lhb_rank()

def institution_business():
	q=pq(url=r'http://data.eastmoney.com/stock/jgmmtj.html',encoding='gb2312')
	aim_date=q('.cate_type_ul.cate_type_date .at').text()
	while True:
		today=datetime.now()
		month_day='{}月{}日'.format(today.month,today.day)
		print(month_day)
		if aim_date != month_day:
			print('数据暂未刷新,等待5分钟')
			time.sleep(300)
		else:
			break
	date=today.strftime('%Y-%m-%d')
	url1=r'http://data.eastmoney.com/DataCenter_V3/stock2016/DailyStockListStatistics/pagesize=50,page={0},sortRule=-1,sortType=PBuy,startDate={1},endDate={1},gpfw=0,js=var%20data_tab_1.html?rt=25754580'.format('{}',date)
	#print(url1)
	page=1
	sql1='insert into institution_business (date,code,name,buy_number,sell_number,buy_sum,sell_sum,buy_amount) values ("{}","{}","{}",{},{},{},{},{})'
	while True:
		url2=url1.format(page)
		json_data=requests.get(url2,headers=headers).text.strip('var data_tab_0123456789=')
		#print(json_data)
		data_lists=demjson.decode(json_data)['data']
		if not data_lists:
			break
		else:
			for data in data_lists:
				sql2=sql1.format(date,data['SCode'],data['SName'],to_null(data,'BSL'),to_null(data,'SSL'),to_null(data,'BMoney'),to_null(data,'SMoney'),to_null(data,'PBuy'))
				cursor.execute(sql2)
				print('机构买卖情况：{}-{}-{}-导入完成'.format(aim_date,data['SCode'],data['SName']))
		page+=1
	print('end：机构买卖情况')
#institution_business()
def stock_count():
	cursor.execute('delete from stock_count')
	print('stock_count表已清空')
	today=datetime.now()
	date=today.strftime('%Y-%m-%d')
	month_ago=(today+timedelta(days=-30)).strftime('%Y-%m-%d')
	#print(month_ago)
	url1=r'http://data.eastmoney.com/DataCenter_V3/stock2016/StockStatistic/pagesize=50,page={},sortRule=-1,sortType=,startDate={},endDate={},gpfw=0,js=var%20data_tab_3.html?rt=25754758'.format('{}',month_ago,date)
	page=1
	sql1='insert into stock_count (date,code,name,list_time,buy_sum,sell_sum,buy_amount) values ("{}","{}","{}",{},{},{},{})'
	while True:
		print('第{}页'.format(page))
		url2=url1.format(page)
		json_data=requests.get(url2,headers=headers).text.strip('var data_tab_0123456789=')
		#print(json_data)
		data_lists=demjson.decode(json_data)['data']
		#print(data_lists)
		if not data_lists:
			break
		else:
			for data in data_lists:
				sql2=sql1.format(data['Tdate'],data['SCode'],data['SName'],to_null(data,'SumCount'),to_null(data,'Bmoney'),to_null(data,'Smoney'),to_null(data,'JmMoney'))
				cursor.execute(sql2)
				print('个股龙虎榜统计：{}-{}-{}-导入完成'.format(data['Tdate'],data['SCode'],data['SName']))
		page+=1
	print('end：个股龙虎榜统计')
#stock_count()

def department_track():
	cursor.execute('delete from department_track')
	print('department_track表已清空')
	today=datetime.now()
	date=today.strftime('%Y-%m-%d')
	month_ago=(today+timedelta(days=-30)).strftime('%Y-%m-%d')
	#print(month_ago)
	url1=r'http://data.eastmoney.com/DataCenter_V3/stock2016/JgStatistic/pagesize=50,page={},sortRule=-1,sortType=,startDate={},endDate={},gpfw=0,js=var%20data_tab_3.html?rt=25754592'.format('{}',month_ago,date)
	page=1
	sql1='insert into department_track (date,code,name,list_time,buy_sum,buy_time,sell_time,buy_amount,up_down) values ("{}","{}","{}",{},{},{},{},{},{})'
	while True:
		print('第{}页'.format(page))
		url2=url1.format(page)
		json_data=requests.get(url2,headers=headers).text.strip('var data_tab_0123456789=')
		#print(json_data)
		data_lists=demjson.decode(json_data)['data']
		#print(data_lists)
		if not data_lists:
			break
		else:
			for data in data_lists:
				sql2=sql1.format(date,data['SCode'],data['SName'],to_null(data,'UPCount'),to_null(data,'JGBMoney'),to_null(data,'JGBCount'),to_null(data,'JGSCount'),to_null(data,'JGPBuy'),to_null(data,'RChange1M'))
				cursor.execute(sql2)
				print('机构席位买卖追踪：{}-{}-{}-导入完成'.format(date,data['SCode'],data['SName']))
		page+=1
	print('end：机构席位买卖追踪')
#department_track()

def active_department():
	q=pq(url=r'http://data.eastmoney.com/stock/hyyyb.html',encoding='gb2312')
	aim_date=q('.cate_type_ul.cate_type_date .at').text()
	while True:
		today=datetime.now()+timedelta(days=-1)
		month_day='{}月{}日'.format(today.month,today.day)
		print(month_day)
		if aim_date != month_day:
			print('数据暂未刷新,等待5分钟')
			time.sleep(300)
		else:
			break
	date=today.strftime('%Y-%m-%d')
	url1=r'http://data.eastmoney.com/DataCenter_V3/stock2016/ActiveStatistics/pagesize=50,page={0},sortRule=-1,sortType=JmMoney,startDate={1},endDate={1},gpfw=0,js=var%20data_tab_1.html?rt=25754772'.format('{}',date)
	#print(url1)
	page=1
	sql1='insert into active_department (date,name,buy_number,sell_number,buy_sum,sell_sum,business_amount,code,stock_name) values ("{}","{}",{},{},{},{},{},"{}","{}")'
	while True:
		url2=url1.format(page)
		json_data=requests.get(url2,headers=headers).text.strip('var data_tab_0123456789=')
		#print(json_data)
		data_lists=demjson.decode(json_data)['data']
		if not data_lists:
			break
		else:
			for data in data_lists:
				if not data['SName']:
					sql2=sql1.format(date,data['YybName'],to_null(data,'YybBCount'),to_null(data,'YybSCount'),to_null(data,'Bmoney'),to_null(data,'Smoney'),to_null(data,'JmMoney'),'无','无')
					cursor.execute(sql2)
				else:
					for data_s in demjson.decode(data['SName']):
						sql2=sql1.format(date,data['YybName'],to_null(data,'YybBCount'),to_null(data,'YybSCount'),to_null(data,'Bmoney'),to_null(data,'Smoney'),to_null(data,'JmMoney'),data_s['SCode'],data_s['CodeName'])
						cursor.execute(sql2)
				print('每日活跃营业部：{}-{}-导入完成'.format(aim_date,data['YybName']))
		page+=1
	print('end：每日活跃营业部')
#active_department()

def department_count():
	cursor.execute('delete from department_count')
	print('department_count表已清空')
	today=datetime.now()
	date=today.strftime('%Y-%m-%d')
	month_ago=(today+timedelta(days=-30)).strftime('%Y-%m-%d')
	#print(month_ago)
	url1=r'http://data.eastmoney.com/DataCenter_V3/stock2016/TraderStatistic/pagesize=50,page={},sortRule=-1,sortType=,startDate={},endDate={},gpfw=0,js=var%20data_tab_1.html?rt=25754789'.format('{}',month_ago,date)
	page=1
	sql1='insert into department_count (date,name,list_time,buy_time,buy_sum,sell_time,sell_sum) values ("{}","{}",{},{},{},{},{})'
	while True:
		print('第{}页'.format(page))
		url2=url1.format(page)
		json_data=requests.get(url2,headers=headers).text.strip('var data_tab_0123456789=')
		#print(json_data)
		data_lists=demjson.decode(json_data)["data"]
		#print(data_lists)
		if not data_lists:
			print('第{}页不存在，结束'.format(page))
			break
		else:
			print('第{}页'.format(page))
			for data in data_lists:
				sql2=sql1.format(date,data['SalesName'],to_null(data,'UpCount'),to_null(data,'BCount'),to_null(data,'SumActBMoney'),to_null(data,'SCount'),to_null(data,'SumActSMoney'))
				cursor.execute(sql2)
				print('证券营业部上榜统计：{}-{}-导入完成'.format(date,data['SalesName']))
		page+=1
	print('end：证券营业部上榜统计')
#department_count()

def stock_info():
	cursor.execute('delete from stock_info')
	print('stock_info表已清空')
	sql1='insert into stock_info (code,name,highest,lowest,yesterday,today) values ("{}","{}",{},{},{},{})'
	for i in range(1,181):
		print('第{}页'.format(i))
		url1='http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?cb=jQuery11240974473783255319_1545290975192&type=CT&token=4f1862fc3b5e77c150a2b985b12db0fd&sty=FCOIATC&js=(%7Bdata%3A%5B(x)%5D%2CrecordsFiltered%3A(tot)%7D)&cmd=C._A&st=(ChangePercent)&sr=-1&p={}&ps=20&_=1545290975206'.format(i)
		json_data=requests.get(url1,headers=headers).text.strip('jQuery0123456789_()')
		#print(json_data)
		data_lists=demjson.decode(json_data)['data']
		for data_str in data_lists:
			data_str.replace('-','null')
			data=data_str.split(',')
			sql2=sql1.format(data[1],data[2],data[9],data[10],data[11],data[12])
			try:
				cursor.execute(sql2)
			except:
				continue
			print('行情中心：{}-{}-导入完成'.format(data[1],data[2]))
	print('end:行情中心')
#stock_info()

def spider_all():
	print('--------------------开始爬取--------------------')
	lhb_rank()
	institution_business()
	stock_count()
	department_track()
	active_department()
	department_count()
	stock_info()
	db.close()
	print('--------------------爬取结束--------------------')
if __name__ == '__main__':
	scheduler=BlockingScheduler()
	scheduler.add_job(func=spider_all,trigger='cron',hour='18',minute='0',second='10')
	scheduler.start()


