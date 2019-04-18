from datetime import datetime,timedelta
from apscheduler.schedulers.blocking import BlockingScheduler
import time
from super_spider import SuperSpider
def lhb_rank_spider():
	lhb_rank_list=[]
	lhb_rank=SuperSpider(host='47.102.40.81',passwd='Abc12345',db='bryframe',table_name='lhb_rank',field_list=('spider_date','up_date','code','name','close_price','up_down','buy_amount','change_rate','currency_market'))
	page=1
	while True:
		try:
			json_data=lhb_rank.get_html(url=f'http://data.eastmoney.com/DataCenter_V3/stock2016/TradeDetail/pagesize=200,page={page},sortRule=-1,sortType=,startDate={lhb_rank.spider_date},endDate={lhb_rank.spider_date},gpfw=0,js=var%20data_tab_1.html?rt=25754497',charset='GB2312')
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
			if lhb_rank.code not in lhb_rank_list:
				lhb_rank_list.append(lhb_rank.code)
			else:
				print(f'{lhb_rank.code}-{lhb_rank.name}-数据重复')
				continue
			sql=f'select code from lhb_rank where code="{lhb_rank.code}" and spider_date="{lhb_rank.spider_date}"'
			same_data=lhb_rank.sql_search(sql)
			if same_data:
				lhb_rank.sql_search(f'delete from lhb_rank where code="{lhb_rank.code}" and spider_date="{lhb_rank.spider_date}"')
				print(f'重新爬取-{lhb_rank.spider_date}-{lhb_rank.code}-{lhb_rank.name}')
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
	institution_business_list=[]
	institution_business=SuperSpider(host='47.102.40.81',passwd='Abc12345',db='bryframe',table_name='institution_business',field_list=('spider_date','up_date','code','name','buy_number','sell_number','buy_sum','sell_sum','buy_amount'))
	page=1
	while True:
		try:
			json_data=institution_business.get_html(f'http://data.eastmoney.com/DataCenter_V3/stock2016/DailyStockListStatistics/pagesize=50,page={page},sortRule=-1,sortType=PBuy,startDate={institution_business.spider_date},endDate={institution_business.spider_date},gpfw=0,js=var%20data_tab_1.html?rt=25754580','GB2312')
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
			if institution_business.code not in institution_business_list:
				institution_business_list.append(institution_business.code)
			else:
				print(f'{institution_business.code}-{institution_business.name}-数据重复')
				continue
			sql=f'select code from institution_business where code="{institution_business.code}" and spider_date="{institution_business.spider_date}"'
			same_data=institution_business.sql_search(sql)
			if same_data:
				institution_business.sql_search(f'delete from institution_business where code="{institution_business.code}" and spider_date="{institution_business.spider_date}"')
				print(f'重新爬取-{institution_business.spider_date}-{institution_business.code}-{institution_business.name}')
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
	stock_count_list=[]
	stock_count=SuperSpider(host='47.102.40.81',passwd='Abc12345',db='bryframe',table_name='stock_count',field_list=('spider_date','up_date','code','name','list_time','buy_sum','sell_sum','buy_amount'))
	month_ago=stock_count.date_ago(30)
	page=1
	while True:
		try:
			json_data=stock_count.get_html(f'http://data.eastmoney.com/DataCenter_V3/stock2016/StockStatistic/pagesize=50,page={page},sortRule=-1,sortType=,startDate={month_ago},endDate={stock_count.spider_date},gpfw=0,js=var%20data_tab_3.html?rt=25754758','GB2312')
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
			if (stock_count.up_date,stock_count.code) not in stock_count_list:
				stock_count_list.append((stock_count.up_date,stock_count.code))
			else:
				print(f'{stock_count.up_date}-{stock_count.code}-{stock_count.name}-数据重复')
				continue
			sql=f'select code from stock_count where code="{stock_count.code}" and spider_date="{stock_count.spider_date}" and up_date="{stock_count.up_date}"'
			same_data=stock_count.sql_search(sql)
			if same_data:
				stock_count.sql_search(f'delete from stock_count where code="{stock_count.code}" and spider_date="{stock_count.spider_date}" and up_date="{stock_count.up_date}"')
				print(f'重新爬取-{stock_count.spider_date}-{stock_count.code}-{stock_count.name}')
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
	department_track_list=[]
	department_track=SuperSpider(host='47.102.40.81',passwd='Abc12345',db='bryframe',table_name='department_track',field_list=('spider_date','up_date','code','name','list_time','buy_sum','buy_time','sell_time','buy_amount','up_down'))
	month_ago=department_track.date_ago(30)
	page=1
	while True:
		try:
			json_data=department_track.get_html(f'http://data.eastmoney.com/DataCenter_V3/stock2016/JgStatistic/pagesize=50,page={page},sortRule=-1,sortType=,startDate={month_ago},endDate={department_track.spider_date},gpfw=0,js=var%20data_tab_3.html?rt=25754592','GB2312')
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
			if department_track.code not in department_track_list:
				department_track_list.append(department_track.code)
			else:
				print(f'{department_track.code}-{department_track.name}-数据重复')
				continue
			sql=f'select code from department_track where code="{department_track.code}" and spider_date="{department_track.spider_date}"'
			same_data=department_track.sql_search(sql)
			if same_data:
				department_track.sql_search(f'delete from department_track where code="{department_track.code}" and spider_date="{department_track.spider_date}"')
				print(f'重新爬取-{department_track.spider_date}-{department_track.code}-{department_track.name}')
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
	active_department_list=[]
	active_department=SuperSpider(host='47.102.40.81',passwd='Abc12345',db='bryframe',table_name='active_department',field_list=('spider_date','up_date','name','buy_number','sell_number','buy_sum','sell_sum','business_amount','code','stock_name'))
	page=1
	while True:
		try:
			json_data=active_department.get_html(f'http://data.eastmoney.com/DataCenter_V3/stock2016/ActiveStatistics/pagesize=50,page={page},sortRule=-1,sortType=JmMoney,startDate={active_department.spider_date},endDate={active_department.spider_date},gpfw=0,js=var%20data_tab_1.html?rt=25754772','GB2312')
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
			if active_department.name not in active_department_list:
				active_department_list.append(active_department.name)
			else:
				print(f'{active_department.name}-数据重复')
				continue
			sql=f'select name from active_department where name="{active_department.name}" and spider_date="{active_department.spider_date}"'
			same_data=active_department.sql_search(sql)
			if same_data:
				active_department.sql_search(f'delete from active_department where name="{active_department.name}" and spider_date="{active_department.spider_date}"')
				print(f'重新爬取-{active_department.spider_date}-{active_department.name}')
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

def business_detail_spider():
	business_detail_list=[]
	business_detail=SuperSpider(host='47.102.40.81',passwd='Abc12345',db='bryframe',table_name='business_detail',field_list=('spider_date','up_date','code','name','department_name','amount'))
	business_detail.up_date=business_detail.spider_date
	page=1
	while True:
		try:
			json_data=business_detail.get_html(f'http://data.eastmoney.com/DataCenter_V3/stock2016/ActiveStatistics/pagesize=50,page={page},sortRule=-1,sortType=JmMoney,startDate={business_detail.spider_date},endDate={business_detail.spider_date},gpfw=0,js=var%20data_tab_1.html?rt=25861061','GB2312')
			data_list=business_detail.json_to_py(json_data,deal=True)['data']
		except:
			print(f'第{page}页获取失败')
			page+=1
			continue
		if not data_list or page == 500:
			break
		print(f'第{page}页')
		for data in data_list:
			if not data['SName']:
				continue
			stock_data_list=business_detail.json_to_py(data['SName'])
			for stock_data in stock_data_list:			
				if stock_data['CodeName'] not in business_detail_list:
					business_detail_list.append(stock_data['CodeName'])
				else:
					continue
				business_detail.name=stock_data['CodeName']
				business_detail.code=stock_data['SCode']
				sql=f'select code from business_detail where code="{business_detail.code}" and spider_date="{business_detail.spider_date}"'
				same_data=business_detail.sql_search(sql)
				if same_data:
					business_detail.sql_search(f'delete from business_detail where code="{business_detail.code}" and spider_date="{business_detail.spider_date}"')
					print(f'重新爬取-{business_detail.spider_date}-{business_detail.code}-{business_detail.name}')
				try:
					url_code=business_detail.re_find(r'\d+',business_detail.code).__next__().group()
				except:
					continue
				url=f'http://data.eastmoney.com/stock/lhb,{business_detail.spider_date},{url_code}.html'
				try:
					detail_data_list=[i for i in business_detail.data_search(url,'//div[@class="content-sepe"]//td//text()','gb2312') if i.strip() and '\r' not in i]
					for i in range(6):
						if '(买入前5名与卖出前5名)' in detail_data_list:
							error_index=detail_data_list.index('(买入前5名与卖出前5名)')
							del detail_data_list[error_index:error_index+6]
				except:
					print(f'{business_detail.code}-{business_detail.name}-获取失败')
					continue
				# print(detail_data_list)
				department_list=[]
				for i,j in zip(range(1,1000,8),range(7,1000,8)):
					try:
						business_detail.department_name=detail_data_list[i]
						if business_detail.department_name not in department_list:
							department_list.append(business_detail.department_name)
						else:
							print(f'{business_detail.name}-{business_detail.department_name}-信息重复')
							continue
						business_detail.amount=detail_data_list[j]
						# print(business_detail.amount)
					except:
						break
					business_detail.data_save()
					print(f'每日成交明细——{business_detail.up_date}——{business_detail.code}——{business_detail.name}——{business_detail.department_name}——导入完成')
		page+=1
	business_detail.spider_end()

def department_count_spider():
	department_count_list=[]
	department_count=SuperSpider(host='47.102.40.81',passwd='Abc12345',db='bryframe',table_name='department_count',field_list=('spider_date','up_date','name','list_time','buy_time','buy_sum','sell_time','sell_sum'))
	month_ago=department_count.date_ago(30)
	page=1
	while True:
		try:
			json_data=department_count.get_html(f'http://data.eastmoney.com/DataCenter_V3/stock2016/TraderStatistic/pagesize=50,page={page},sortRule=-1,sortType=,startDate={month_ago},endDate={department_count.spider_date},gpfw=0,js=var%20data_tab_1.html?rt=25754789','GB2312')
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
			if department_count.name not in department_count_list:
				department_count_list.append(department_count.name)
			else:
				print(f'{department_count.name}-数据重复')
				continue
			sql=f'select name from department_count where name="{department_count.name}" and spider_date="{department_count.spider_date}"'
			same_data=department_count.sql_search(sql)
			if same_data:
				department_count.sql_search(f'delete from department_count where name="{department_count.name}" and spider_date="{department_count.spider_date}"')
				print(f'重新爬取-{department_count.spider_date}-{department_count.name}')
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
	stock_info_list=[]
	stock_info=SuperSpider(host='47.102.40.81',passwd='Abc12345',db='bryframe',table_name='stock_info',field_list=('code','name','spider_date','up_date','highest','lowest','today','yesterday'))
	for page in range(1,181):
		try:
			json_data=stock_info.get_html(f'http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?cb=jQuery11240974473783255319_1545290975192&type=CT&token=4f1862fc3b5e77c150a2b985b12db0fd&sty=FCOIATC&js=(%7Bdata%3A%5B(x)%5D%2CrecordsFiltered%3A(tot)%7D)&cmd=C._A&st=(ChangePercent)&sr=-1&p={page}&ps=20&_=1545290975206')
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
			if stock_info.code not in stock_info_list:
				stock_info_list.append(stock_info.code)
			else:
				print(f'{stock_info.code}-{stock_info.name}-数据重复')
				continue
			sql=f'select code from stock_info where code="{stock_info.code}" and spider_date="{stock_info.spider_date}"'
			same_data=stock_info.sql_search(sql)
			if same_data:
				stock_info.sql_search(f'delete from stock_info where code="{stock_info.code}" and spider_date="{stock_info.spider_date}"')
				print(f'重新爬取-{stock_info.spider_date}-{stock_info.code}-{stock_info.name}')
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
	stock_report_list=[]
	stock_report=SuperSpider(host='47.102.40.81',passwd='Abc12345',db='bryframe',table_name='stock_report',field_list=('code','name','spider_date','up_date','report','grade','grade_change','institution','income_2018','rate_2018','income_2019','rate_2019'))
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
			json_data=stock_report.get_html(url)
			data_list=stock_report.json_to_py(json_data,deal=True)['data']
		except:
			print(f'第{page}页获取失败')
			page+=1
			continue
		for data in data_list:
			time1=data['datetime'][:10]
			stock_report.code=data['secuFullCode']
			stock_report.name=data['secuName']
			stock_report.up_date=time1
			title=data['title']
			datetime1=datetime.strptime(time1,'%Y-%m-%d')
			if datetime1<=latest_datetime:
				print('暂无数据更新')
				is_end=True
				break
			infocode=data['infoCode']
			time2=time1.replace('-','')
			try:
				stock_report.report=(''.join(stock_report.data_search(f'http://data.eastmoney.com/report/{time2}/{infocode}.html','//div[@id="ContentBody"]//div[@class="newsContent"]//text()','gb2312'))).strip()
			except:
				pass
			sql=f'select code from stock_report where code="{stock_report.code}" and spider_date="{stock_report.spider_date}" and up_date="{stock_report.up_date}" and report="{stock_report.report}"'
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
	profession_report_list=[]
	profession_report=SuperSpider(host='47.102.40.81',passwd='Abc12345',db='bryframe',table_name='profession_report',field_list=('name','spider_date','up_date','up_down','report','grade','grade_change','institution'))
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
			json_data=profession_report.get_html(url)
			data_list=profession_report.json_to_py(json_data,deal=True)['data']
		except Exception as error:
			print(f'第{page}页获取失败')
			print(error)
			page+=1
			continue
		for data in data_list:
			data=data.split(',')
			time1=data[1].split(' ')[0].replace('/','-')
			profession_report.name=data[10]
			profession_report.up_date=time1
			datetime1=datetime.strptime(time1,'%Y-%m-%d')
			if datetime1<=latest_datetime:
				print('暂无数据更新')
				is_end=True
				break
			infocode=data[2]
			time2=time1.replace('-','')
			profession_report.up_down=profession_report.to_null(data[11])
			try:
				profession_report.report=(''.join(profession_report.data_search(f'http://data.eastmoney.com/report/{time2}/{infocode}.html','//div[@class="newsContent"]/text()','gb2312'))).strip()
			except:
				pass
			sql=f'select name from profession_report where name="{profession_report.name}" and spider_date="{profession_report.spider_date}" and up_date="{profession_report.up_date}" and report="{profession_report.report}"'
			same_data=profession_report.sql_search(sql)
			profession_report.grade=data[7]
			profession_report.grade_change=data[0]
			profession_report.institution=data[4]
			profession_report.data_save()
			print(f'行业研报：{profession_report.up_date}-{profession_report.name}-{profession_report.institution}-导入完成')
		if is_end == True:
			break
	profession_report.spider_end()
	print('end:行业研报')

def bonus_data_spider():
	bonus_data=SuperSpider(host='139.224.115.44',passwd='A9Vg+Dr*nP^fR=1V',db='bryframe3',table_name='bonus_data',field_list=('spider_date','bonus_report_date','code','name','cash_bonus_rate','transfer_rate','plan_announce_date','stock_register_date','remove_date','plan_scheduler','latest_announce_date'))
	date_list=bonus_data.data_search('http://data.eastmoney.com/yjfp/201812.html','//select[@id="sel_bgq"]/option/text()','gb2312')
	year_ago_datetime=bonus_data.to_datetime(bonus_data.date_ago(365))
	date_list2=[]
	for aim_date in date_list:
		if year_ago_datetime<=bonus_data.to_datetime(str(aim_date)):
			date_list2.append(aim_date)
		else:
			break
	for use_date in date_list2:
		bonus_data.bonus_report_date=use_date
		page=1
		while True:
			print(f'第{page}页')
			try:
				json_data=bonus_data.get_html(f'http://data.eastmoney.com/DataCenter_V3/yjfp/getlist.ashx?js=var%20aTnZIWfZ&pagesize=50&page={page}&sr=-1&sortType=YAGGR&mtk=%C8%AB%B2%BF%B9%C9%C6%B1&filter=(ReportingPeriod=^{use_date}^)&rt=51742239','GB2312')
				data_list=bonus_data.json_to_py(json_data,deal=True)['data']
			except:
				print(f'第{page}页获取失败')
				page+=1
				continue
			if not data_list or page == 500:
				break
			for data in data_list:
				bonus_data.code=data['Code']
				bonus_data.name=data['Name']
				bonus_data.latest_announce_date=bonus_data.to_null(data['NoticeDate'][:10])
				sql=f'select code from bonus_data where code="{bonus_data.code}" and spider_date="{bonus_data.spider_date}" and latest_announce_date="{bonus_data.latest_announce_date}"'
				same_data=bonus_data.sql_search(sql)
				if same_data:
					bonus_data.sql_search(f'delete from bonus_data where code="{bonus_data.code}" and spider_date="{bonus_data.spider_date}" and latest_announce_date="{bonus_data.latest_announce_date}"')
					print(f'重新爬取-{bonus_data.spider_date}-{bonus_data.code}-{bonus_data.name}')
				bonus_data.plan_announce_date=bonus_data.to_null(data['ResultsbyDate'][:10])
				bonus_data.stock_register_date=bonus_data.to_null(data['GQDJR'][:10])
				bonus_data.remove_date=bonus_data.to_null(data['CQCXR'][:10])
				bonus_data.plan_scheduler=data['ProjectProgress']
				group_data=data['AllocationPlan']
				try:
					bonus_data.cash_bonus_rate='10'+bonus_data.re_find(r'派[\d\.]+',group_data).__next__().group()+'元(含税)'
				except:
					bonus_data.cash_bonus_rate='null'		
				try:
					transfer_rate1=bonus_data.re_find(r'转[\d\.]+',group_data).__next__().group()
				except:
					transfer_rate1=''
				try:
					transfer_rate2=bonus_data.re_find(r'送[\d\.]+',group_data).__next__().group()
				except:
					transfer_rate2=''
				if not transfer_rate1 and not transfer_rate2:
					bonus_data.transfer_rate='null'
				else:
					bonus_data.transfer_rate='10'+transfer_rate2+transfer_rate1
				bonus_data.data_save()
				print(f'{bonus_data.bonus_report_date}-{bonus_data.code}-{bonus_data.name}-导入完成')
			page+=1
	bonus_data.spider_end()
	
def stock_data_spider():
	data_end=None
	stock_data=SuperSpider(host='139.224.115.44',passwd='A9Vg+Dr*nP^fR=1V',db='bryframe3',table_name='stock_data',field_list=('spider_date','up_date','code','name','stock_rate','stock_price'))
	page=1
	while True:
		print(f'第{page}页')
		url='http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?type=NS&sty=NSA&st=6&sr=-1&p='+str(page)+'&ps=50&js=var%20inHqdtrZ={pages:(pc),data:[(x)]}&rt=5174'
		try:
			json_data=stock_data.get_html(url)
			data_list=stock_data.json_to_py(json_data,deal=True)['data']
			if data_list[:3] == data_end:
				break
			else:
				data_end=data_list[:3]
		except:
			print(f'第{page}页获取失败')
			page+=1
			continue
		if not data_list or page == 500:
			break
		for data in data_list:
			field_list=data.split(',')
			stock_data.code=field_list[2]
			stock_data.name=field_list[3]
			stock_data.stock_rate='10配'+field_list[6]
			stock_data.stock_price=stock_data.to_null(field_list[7])
			stock_data.up_date=field_list[14] if field_list[14] else 'null'
			sql=f'select code from stock_data where code="{stock_data.code}" and spider_date="{stock_data.spider_date}" and up_date="{stock_data.up_date}"'
			same_data=stock_data.sql_search(sql)
			if same_data:
				stock_data.sql_search(f'delete from stock_data where code="{stock_data.code}" and spider_date="{stock_data.spider_date}" and up_date="{stock_data.up_date}"')
				print(f'重新爬取-{stock_data.spider_date}-{stock_data.code}-{stock_data.name}')
			stock_data.data_save()
			print(f'{stock_data.up_date}-{stock_data.code}-{stock_data.name}-导入完成')
		page+=1
	stock_data.spider_end()



def run_all_spider():
	run_all=SuperSpider(host='47.102.40.81',passwd='Abc12345',db='bryframe')
	while True:
		now=datetime.now()
		aim_date=f"{now.strftime('%m')}月{now.strftime('%d')}日"
		data_date=run_all.data_search('http://data.eastmoney.com/stock/tradedetail.html','//ul[contains(@class,"cate_type_date")]/li[@class="at"]/text()','gb2312')[0]
		print(data_date)
		if aim_date != data_date:
			print('————今日数据未更新————')
			run_all.spider_end()
			return
		else:
			break
	for i in range(3):
		lhb_rank_spider()
		institution_business_spider()
		stock_count_spider()
		department_track_spider()
		active_department_spider()
		business_detail_spider()
		department_count_spider()
		stock_info_spider()
		stock_report_spider()
		profession_report_spider()
		bonus_data_spider()
		stock_data_spider()
		time.sleep(1800)
	run_all.spider_end()

if __name__ == '__main__':
	# run_all_spider()
	scheduler=BlockingScheduler()
	print('正在等待~')
	scheduler.add_job(func=run_all_spider,trigger='cron',hour=17,minute=20)
	scheduler.start()