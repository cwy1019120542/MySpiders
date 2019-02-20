import sys
from datetime import datetime,timedelta
from apscheduler.schedulers.blocking import BlockingScheduler
import time
sys.path.append(r'/root/bry_spider')
from super_spider import SuperSpider
def lhb_rank_spider():
	lhb_rank=SuperSpider(host='112.27.113.231',passwd='never1019120542,',db='jsn_data',table_name='lhb_rank',field_list=('spider_date','up_date','code','name','close_price','up_down','buy_amount','change_rate','currency_market'))
	page=1
	while True:
		try:
			json_data=lhb_rank.use_requests_to_html(f'http://data.eastmoney.com/DataCenter_V3/stock2016/TradeDetail/pagesize=200,page={page},sortRule=-1,sortType=,startDate={lhb_rank.spider_date},endDate={lhb_rank.spider_date},gpfw=0,js=var%20data_tab_1.html?rt=25754497','GB2312')
			data_list=lhb_rank.json_to_py(json_data,deal=True)['data']
		except:
			print(f'第{page}页获取失败')
			page+=1
			continue
		if not data_list or page == 500:
			break
		print(f'第{page}页')
		for data in data_list:
			lhb_rank.up_date=lhb_rank.spider_date
			lhb_rank.code=data['SCode']
			lhb_rank.name=data['SName']
			lhb_rank.close_price=lhb_rank.to_null(data['ClosePrice'])
			lhb_rank.up_down=lhb_rank.to_null(data['Chgradio'])
			lhb_rank.buy_amount=lhb_rank.to_null(data['JmMoney'])
			lhb_rank.change_rate=lhb_rank.to_null(data['Dchratio'])
			lhb_rank.currency_market=lhb_rank.to_null(data['Ltsz'])
			lhb_rank.data_save()
			print(f'当日龙虎榜涨跌幅排名：{lhb_rank.up_date}-{lhb_rank.code}-{lhb_rank.name}-导入完成')
		page+=1
	lhb_rank.spider_end()
	print('end：龙虎榜当日跌幅排名')

def institution_business_spider():
	institution_business=SuperSpider(host='112.27.113.231',passwd='never1019120542,',db='jsn_data',table_name='institution_business',field_list=('spider_date','up_date','code','name','buy_number','sell_number','buy_sum','sell_sum','buy_amount'))
	page=1
	while True:
		try:
			json_data=institution_business.use_requests_to_html(f'http://data.eastmoney.com/DataCenter_V3/stock2016/DailyStockListStatistics/pagesize=50,page={page},sortRule=-1,sortType=PBuy,startDate={institution_business.spider_date},endDate={institution_business.spider_date},gpfw=0,js=var%20data_tab_1.html?rt=25754580','GB2312')
			data_list=institution_business.json_to_py(json_data,deal=True)['data']
		except:
			print(f'第{page}页获取失败')
			page+=1
			continue
		if not data_list or page == 500:
			break
		print(f'第{page}页')
		for data in data_list:
			institution_business.up_date=institution_business.spider_date
			institution_business.code=data['SCode']
			institution_business.name=data['SName']
			institution_business.buy_number=institution_business.to_null(data['BSL'])
			institution_business.sell_number=institution_business.to_null(data['SSL'])
			institution_business.buy_sum=institution_business.to_null(data['BMoney'])
			institution_business.sell_sum=institution_business.to_null(data['SMoney'])
			institution_business.buy_amount=institution_business.to_null(data['PBuy'])
			institution_business.data_save()
			print(f'机构买卖情况：{institution_business.up_date}-{institution_business.code}-{institution_business.name}-导入完成')
		page+=1
	institution_business.spider_end()
	print('end：机构买卖情况')

def stock_count_spider():
	stock_count=SuperSpider(host='112.27.113.231',passwd='never1019120542,',db='jsn_data',table_name='stock_count',field_list=('spider_date','up_date','code','name','list_time','buy_sum','sell_sum','buy_amount'))
	month_ago=stock_count.date_ago(30)
	page=1
	while True:
		try:
			json_data=stock_count.use_requests_to_html(f'http://data.eastmoney.com/DataCenter_V3/stock2016/StockStatistic/pagesize=50,page={page},sortRule=-1,sortType=,startDate={month_ago},endDate={stock_count.spider_date},gpfw=0,js=var%20data_tab_3.html?rt=25754758','GB2312')
			data_list=stock_count.json_to_py(json_data,deal=True)['data']
		except:
			print(f'第{page}页获取失败')
			page+=1
			continue
		if not data_list or page == 500:
			break
		print(f'第{page}页')
		for data in data_list:
			stock_count.up_date=data['Tdate']
			stock_count.code=data['SCode']
			stock_count.name=data['SName']
			stock_count.list_time=stock_count.to_null(data['SumCount'])
			stock_count.buy_sum=stock_count.to_null(data['Bmoney'])
			stock_count.sell_sum=stock_count.to_null(data['Smoney'])
			stock_count.buy_amount=stock_count.to_null(data['JmMoney'])
			stock_count.data_save()
			print(f'个股龙虎榜统计：{stock_count.up_date}-{stock_count.code}-{stock_count.name}-导入完成')
		page+=1
	stock_count.spider_end()
	print('end：个股龙虎榜统计')

def department_track_spider():
	department_track=SuperSpider(host='112.27.113.231',passwd='never1019120542,',db='jsn_data',table_name='department_track',field_list=('spider_date','up_date','code','name','list_time','buy_sum','buy_time','sell_time','buy_amount','up_down'))
	month_ago=department_track.date_ago(30)
	page=1
	while True:
		try:
			json_data=department_track.use_requests_to_html(f'http://data.eastmoney.com/DataCenter_V3/stock2016/JgStatistic/pagesize=50,page={page},sortRule=-1,sortType=,startDate={month_ago},endDate={department_track.spider_date},gpfw=0,js=var%20data_tab_3.html?rt=25754592','GB2312')
			data_list=department_track.json_to_py(json_data,deal=True)['data']
		except:
			print(f'第{page}页获取失败')
			page+=1
			continue
		if not data_list or page == 500:
			break
		print(f'第{page}页')
		for data in data_list:
			department_track.up_date=department_track.spider_date
			department_track.code=data['SCode']
			department_track.name=data['SName']
			department_track.list_time=department_track.to_null(data['UPCount'])
			department_track.buy_sum=department_track.to_null(data['JGBMoney'])
			department_track.buy_time=department_track.to_null(data['JGBCount'])
			department_track.sell_time=department_track.to_null(data['JGSCount'])
			department_track.buy_amount=department_track.to_null(data['JGPBuy'])
			department_track.up_down=department_track.to_null(data['RChange1M'])
			department_track.data_save()
			print(f'机构席位买卖追踪：{department_track.up_date}-{department_track.code}-{department_track.name}-导入完成')
		page+=1
	department_track.spider_end()
	print('end：机构席位买卖追踪')

def active_department_spider():
	active_department=SuperSpider(host='112.27.113.231',passwd='never1019120542,',db='jsn_data',table_name='active_department',field_list=('spider_date','up_date','name','buy_number','sell_number','buy_sum','sell_sum','business_amount','code','stock_name'))
	page=1
	while True:
		try:
			json_data=active_department.use_requests_to_html(f'http://data.eastmoney.com/DataCenter_V3/stock2016/ActiveStatistics/pagesize=50,page={page},sortRule=-1,sortType=JmMoney,startDate={active_department.spider_date},endDate={active_department.spider_date},gpfw=0,js=var%20data_tab_1.html?rt=25754772','GB2312')
			data_list=active_department.json_to_py(json_data,deal=True)['data']
		except:
			print(f'第{page}页获取失败')
			page+=1
			continue
		if not data_list or page == 500:
			break
		print(f'第{page}页')
		for data in data_list:
			active_department.up_date=active_department.spider_date
			active_department.name=data['YybName']
			active_department.buy_number=active_department.to_null(data['YybBCount'])
			active_department.sell_number=active_department.to_null(data['YybSCount'])
			active_department.buy_sum=active_department.to_null(data['Bmoney'])
			active_department.sell_sum=active_department.to_null(data['Smoney'])
			active_department.business_amount=active_department.to_null(data['JmMoney'])
			if not data['SName']:
				active_department.code='null'
				active_department.stock_name='null'
				active_department.data_save()
			else:
				for data_s in active_department.json_to_py(data['SName']):
					active_department.code=data_s['SCode']
					active_department.stock_name=data_s['CodeName']
					active_department.data_save()
					print(f'每日活跃营业部：{active_department.up_date}-{active_department.name}-导入完成')
		page+=1
	active_department.spider_end()
	print('end：每日活跃营业部')
#active_department_spider()

def department_count_spider():
	department_count=SuperSpider(host='112.27.113.231',passwd='never1019120542,',db='jsn_data',table_name='department_count',field_list=('spider_date','up_date','name','list_time','buy_time','buy_sum','sell_time','sell_sum'))
	month_ago=department_count.date_ago(30)
	page=1
	while True:
		try:
			json_data=department_count.use_requests_to_html(f'http://data.eastmoney.com/DataCenter_V3/stock2016/TraderStatistic/pagesize=50,page={page},sortRule=-1,sortType=,startDate={month_ago},endDate={department_count.spider_date},gpfw=0,js=var%20data_tab_1.html?rt=25754789','GB2312')
			data_list=department_count.json_to_py(json_data,deal=True)['data']
		except:
			print(f'第{page}页获取失败')
			page+=1
			continue
		if not data_list or page == 500:
			break
		print(f'第{page}页')
		for data in data_list:
			department_count.up_date=department_count.spider_date
			department_count.name=data['SalesName']
			department_count.list_time=department_count.to_null(data['UpCount'])
			department_count.buy_time=department_count.to_null(data['BCount'])
			department_count.buy_sum=department_count.to_null(data['SumActBMoney'])
			department_count.sell_time=department_count.to_null(data['SCount'])
			department_count.sell_sum=department_count.to_null(data['SumActSMoney'])
			department_count.data_save()
			print(f'证券营业部上榜统计：{department_count.up_date}-{department_count.name}-导入完成')
		page+=1
	department_count.spider_end()
	print('end：证券营业部上榜统计')
#department_count_spider()

def stock_info_spider():
	stock_info=SuperSpider(host='112.27.113.231',passwd='never1019120542,',db='jsn_data',table_name='stock_info',field_list=('code','name','spider_date','up_date','highest','lowest','today','yesterday'))
	for page in range(1,181):
		try:
			json_data=stock_info.use_requests_to_html(f'http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?cb=jQuery11240974473783255319_1545290975192&type=CT&token=4f1862fc3b5e77c150a2b985b12db0fd&sty=FCOIATC&js=(%7Bdata%3A%5B(x)%5D%2CrecordsFiltered%3A(tot)%7D)&cmd=C._A&st=(ChangePercent)&sr=-1&p={page}&ps=20&_=1545290975206','utf8')
			data_list=stock_info.json_to_py(json_data,deal=True)['data']
		except:
			print(f'第{page}页获取失败')
			page+=1
			continue
		print(f'第{page}页')
		for data_str in data_list:
			data=data_str.replace('-','null').split(',')
			stock_info.code=data[1]
			stock_info.name=data[2]
			stock_info.spider_date=stock_info.spider_date
			stock_info.up_date=stock_info.spider_date
			stock_info.highest=stock_info.to_null(data[9])
			stock_info.lowest=stock_info.to_null(data[10])
			stock_info.today=stock_info.to_null(data[11])
			stock_info.yesterday=stock_info.to_null(data[12])
			stock_info.data_save()
			print(f'行情中心：{stock_info.up_date}-{stock_info.code}-{stock_info.name}-导入完成')
		page+=1
	stock_info.spider_end()
	print('end：行情中心')
#stock_info_spider()

def stock_report_spider():
	stock_report=SuperSpider(host='112.27.113.231',passwd='never1019120542,',db='jsn_data',table_name='stock_report',field_list=('code','name','spider_date','up_date','report','grade','grade_change','institution','income_2018','rate_2018','income_2019','rate_2019'))
	sql1='select MAX(up_date) from stock_report'
	latest_time=stock_report.sql_search(sql1)[0][0]
	if not latest_time:
		latest_datetime=datetime.now()-timedelta(days=1)
	else:
		latest_datetime=datetime(latest_time.year,latest_time.month,latest_time.day)
	is_end=False
	for page in range(1,254):
		url='http://datainterface.eastmoney.com//EM_DataCenter/js.aspx?type=SR&sty=GGSR&js=var%20MILbIdwm={"data":[(x)],"pages":"(pc)","update":"(ud)","count":"(count)"}&ps=50&p='+str(page)+'&mkt=0&stat=0&cmd=2&code=&rt=51552935'
		try:
			json_data=stock_report.use_requests_to_html(url,'utf8')
			data_list=stock_report.json_to_py(json_data,deal=True)['data']
		except:
			print(f'第{page}页获取失败')
			page+=1
			continue
		for data in data_list:
			time1=data['datetime'][:10]
			datetime1=datetime.strptime(time1,'%Y-%m-%d')
			if datetime1<=latest_datetime:
				print('暂无数据更新')
				is_end=True
				break
			infocode=data['infoCode']
			time2=time1.replace('-','')
			try:
				html1=stock_report.get_request(f'http://data.eastmoney.com/report/{time2}/{infocode}.html')
			except:
				continue
			report=''
			for par in stock_report.data_search(html1,'find','#ContentBody .newsContent p'):
				report=report+par
			stock_report.code=data['secuFullCode']
			stock_report.name=data['secuName']
			stock_report.up_date=stock_report.spider_date
			stock_report.report=report
			stock_report.grade=data['rate']
			stock_report.grade_change=data['change']
			stock_report.institution=data['insName']
			stock_report.income_2018=stock_report.to_null(data['sys'][0])
			stock_report.rate_2018=stock_report.to_null(data['syls'][0])
			stock_report.income_2019=stock_report.to_null(data['sys'][1])
			stock_report.rate_2019=stock_report.to_null(data['syls'][1])
			stock_report.data_save()
			print(f'个股研报：{stock_report.spider_date}-{stock_report.code}-{stock_report.name}-导入完成')
		if is_end == True:
			break
	stock_report.spider_end()
	print('end:个股研报')
#stock_report_spider()

def profession_report_spider():
	profession_report=SuperSpider(host='112.27.113.231',passwd='never1019120542,',db='jsn_data',table_name='profession_report',field_list=('name','spider_date','up_date','up_down','report','grade','grade_change','institution'))
	sql1='select MAX(up_date) from profession_report'
	latest_time=profession_report.sql_search(sql1)[0][0]
	if not latest_time:
		latest_datetime=datetime.now()-timedelta(days=1)
	else:
		latest_datetime=datetime(latest_time.year,latest_time.month,latest_time.day)
	is_end=False
	for page in range(1,1337):
		url='http://datainterface.eastmoney.com//EM_DataCenter/js.aspx?type=SR&sty=HYSR&mkt=0&stat=0&cmd=4&code=&sc=&ps=50&p='+str(page)+'&js=var%20vMcgaFDg={%22data%22:[(x)],%22pages%22:%22(pc)%22,%22update%22:%22(ud)%22,%22count%22:%22(count)%22}&rt=51553086'
		try:
			json_data=profession_report.use_requests_to_html(url,'utf8')
			data_list=profession_report.json_to_py(json_data,deal=True)['data']
		except:
			print(f'第{page}页获取失败')
			page+=1
			continue
		for data in data_list:
			data=data.split(',')
			time1=data[1].split(' ')[0].replace('/','-')
			datetime1=datetime.strptime(time1,'%Y-%m-%d')
			if datetime1<=latest_datetime:
				print('暂无数据更新')
				is_end=True
				break
			infocode=data[2]
			time2=time1.replace('-','')
			try:
				html1=profession_report.get_request(f'http://data.eastmoney.com/report/{time2}/{infocode}.html')
			except:
				continue
			report=''
			for par in profession_report.data_search(html1,'find','.newsContent p'):
				report=report+par
			profession_report.name=data[10]
			profession_report.up_date=time1
			profession_report.up_down=profession_report.to_null(data[11])
			profession_report.report=report
			profession_report.grade=data[7]
			profession_report.grade_change=data[0]
			profession_report.institution=data[4]
			profession_report.data_save()
			print(f'行业研报：{profession_report.up_date}-{profession_report.name}-{profession_report.institution}-导入完成')
		if is_end == True:
			break
	profession_report.spider_end()
	print('end:行业研报')

def run_all_spider():
	run_all=SuperSpider()
	while True:
		now=datetime.now()
		aim_date=f"{now.strftime('%m')}月{now.strftime('%d')}日"
		html=run_all.get_request('http://data.eastmoney.com/stock/tradedetail.html')
		data_date=run_all.data_search(html,'find','.cate_type_ul.cate_type_date .at').__next__()
		if aim_date != data_date:
			print('数据暂未刷新，等待10分钟')
			time.sleep(600)
		else:
			break
	lhb_rank_spider()
	institution_business_spider()
	stock_count_spider()
	department_track_spider()
	active_department_spider()
	department_count_spider()
	stock_info_spider()
	stock_report_spider()
	profession_report_spider()
	run_all.spider_end()

if __name__ == '__main__':
	scheduler=BlockingScheduler()
	print('正在等待~')
	scheduler.add_job(func=run_all_spider,trigger='cron',hour='11',minute='50',second='0')
	scheduler.start()
