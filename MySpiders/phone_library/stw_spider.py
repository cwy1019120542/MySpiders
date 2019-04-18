from super_spider import SuperSpider
from collections import deque

def stw_spider():
	stw=SuperSpider()
	stw_list=deque([],maxlen=30)
	stw.source_name='商泰网'
	url_list1=stw.data_search(r'https://cn.made-in-china.com/','//div[@class="sub-cata"]//dd[@class="sub-cata-item-bd"]//a/@href')
	# print(url_list1)
	for url1 in url_list1:
		url1='https://cn.made-in-china.com'+url1
		code=stw.data_search(url1,'//input[@name="code"]/@value')
		print(code)

stw_spider()
# https://cn.made-in-china.com/productdirectory.do?propertyValues=&action=hunt&senior=0&certFlag=0&code=EEnxEJQbMJmm&code4BrowerHistory=EEnxEJQbMJmm&order=0&style=b&page=2&comProvince=nolimit&comCity=&size=40&viewType=1&sizeHasChanged=0&uniqfield=1&priceStart=&priceEnd=&quantityBegin=&tradeType=&word=%B1%B1%BE%A9%CF%B4%CD%EB%BB%FA&from=hunt&hotflag=0&newFlag=0&wordPinyin4QP=%B1%B1%BE%A9%CF%B4%CD%EB%BB%FA
# https://cn.made-in-china.com/productdirectory.do?propertyValues=&action=hunt&senior=0&certFlag=0&code=EEnxEJQbMJmm&code4BrowerHistory=EEnxEJQbMJmm&order=0&style=b&page=1&comProvince=nolimit&comCity=&size=40&viewType=1&sizeHasChanged=0&uniqfield=1&priceStart=&priceEnd=&quantityBegin=&tradeType=&word=%C4%B8%D6%ED%B6%A8%CE%BB%C0%B8&from=hunt&hotflag=0&newFlag=0&wordPinyin4QP=muzhudwl
# https://cn.made-in-china.com/productdirectory.do?propertyValues=&action=item&senior=0&certFlag=0&code=EOwfuQTGoRmx&code4BrowerHistory=EOwfuQTGoRmx&order=3&style=b&page=1&comProvince=&comCity=&size=40&viewType=3&sizeHasChanged=0&uniqfield=1&priceStart=&priceEnd=&quantityBegin=&tradeType=&from=item&flag=999&channel=jixie
# https://cn.made-in-china.com/productdirectory.do?propertyValues=&action=item&senior=0&certFlag=0&code=xbXPJEmOofQn&code4BrowerHistory=xbXPJEmOofQn&order=3&style=b&page=1&comProvince=&comCity=&size=40&viewType=1&sizeHasChanged=0&uniqfield=1&priceStart=&priceEnd=&quantityBegin=&tradeType=&flag=999&from=item
# https://cn.made-in-china.com/productdirectory.do?propertyValues=&action=item&senior=0&certFlag=0&code=nuhGrxEbUcQJ&code4BrowerHistory=nuhGrxEbUcQJ&order=3&style=b&page=1&comProvince=&comCity=&size=40&viewType=1&sizeHasChanged=0&uniqfield=1&priceStart=&priceEnd=&quantityBegin=&tradeType=&flag=999&from=item
https://cn.made-in-china.com/productdirectory.do?propertyValues=&xcase=market&senior=0&certFlag=0&code=EEnxEJQbMJmm&code4BrowerHistory=EEnxEJQbMJmm&order=0&style=b&page=1&comProvince=nolimit&comCity=&size=40&viewType=3&sizeHasChanged=0&uniqfield=1&priceStart=&priceEnd=&quantityBegin=&word=%B8%DF%CB%D9%BB%EC%BA%CF%BB%FA&tradeType=&from=hunt&hotflag=0&newFlag=1&wordPinyin4QP=gshhj
https://cn.made-in-china.com/productdirectory.do?propertyValues=&action=hunt&senior=0&certFlag=0&code=EEnxEJQbMJmm&code4BrowerHistory=EEnxEJQbMJmm&order=0&style=b&page=1&comProvince=nolimit&comCity=&size=40&viewType=1&sizeHasChanged=0&uniqfield=1&priceStart=&priceEnd=&quantityBegin=&tradeType=&word=%B1%B1%BE%A9%CF%B4%CD%EB%BB%FA&from=hunt&hotflag=0&newFlag=0&wordPinyin4QP=xiwanjsl