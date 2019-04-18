from super_spider import SuperSpider

def business_detail_spider():
	stock_list=[]
	business_detail=SuperSpider(host='47.102.40.81',passwd='Abc12345',db='bryframe',table_name='business_detail',field_list=('spider_date','up_date','code','name','department_name','amount'))
	business_detail.up_date=business_detail.spider_date
	page=1
	while True:
		try:
			json_data=business_detail.use_requests_to_html(f'http://data.eastmoney.com/DataCenter_V3/stock2016/ActiveStatistics/pagesize=50,page={page},sortRule=-1,sortType=JmMoney,startDate={business_detail.spider_date},endDate={business_detail.spider_date},gpfw=0,js=var%20data_tab_1.html?rt=25861061','GB2312')
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
				if stock_data['CodeName'] not in stock_list:
					stock_list.append(stock_data['CodeName'])
				else:
					continue
				business_detail.name=stock_data['CodeName']
				business_detail.code=stock_data['SCode']
				try:
					url_code=business_detail.re_find(r'\d+',business_detail.code).__next__().group()
				except:
					continue
				print(url_code)
				url=f'http://data.eastmoney.com/stock/lhb,{business_detail.spider_date},{url_code}.html'
				try:
					business_detail.get_request(url)
				except:
					continue
				detail_data_list=list(business_detail.data_search('find','table tbody td'))
				for i,j in zip(range(1,71,7),range(6,71,7)):
					try:
						business_detail.department_name=detail_data_list[i].split('\n')[0]
					except:
						break
					business_detail.amount=detail_data_list[j]
					business_detail.data_save()
					print(f'每日成交明细——{business_detail.up_date}——{business_detail.code}——{business_detail.name}——{business_detail.department_name}——导入完成')
		page+=1
	business_detail.spider_end()
business_detail_spider()