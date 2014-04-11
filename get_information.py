import urllib2
import sys
import os
import pycurl
import cStringIO

def get_item_specifics(itemID):
	url = "http://open.api.ebay.com/shopping?callname=GetSingleItem&responseencoding=JSON&appid=hit4199c1-c6e0-4ab6-9407-d8be4d23922&siteid=0&version=825&IncludeSelector=Description,ItemSpecifics&ItemID="+itemID
	r = urllib2.urlopen(url).read()
	return r

def get_items_by_keyword(keyword, pageNumber=1):
	url = "http://svcs.ebay.com/services/search/FindingService/v1?OPERATION-NAME=findItemsByKeywords&SERVICE-VERSION=1.12.0&SECURITY-APPNAME=hit4199c1-c6e0-4ab6-9407-d8be4d23922&RESPONSE-DATA-FORMAT=JSON&REST-PAYLOAD&keywords="+keyword+"&paginationInput.entriesPerPage=40&paginationInput.pageNumber="+str(pageNumber)
	r = urllib2.urlopen(url).read()
	return r

#for test
def local_download(keyword, more = '0'):
	folder = keyword.replace(' ', '')

	path = "/home/zxdhuge/django/sigirdemo/temp_data/"+folder+'/'
	#we have search this keyword before.
	if os.path.exists(path):
		if more == '0':
			path = '/home/zxdhuge/django/sigirdemo/temp_data/'+folder+'/test_data/'
			if not os.path.exists(path):
				os.system('mkdir '+path)
			else:
				return path
		else:
			path = '/home/zxdhuge/django/sigirdemo/temp_data/'+folder+'/'+'test_data_more'+more+'/'
			if not os.path.exists(path):
				os.system('mkdir '+path)
			else:
				return path 
	else:
		os.system('mkdir '+path)
		path += 'test_data/'
		os.system('mkdir '+path)

	false = False
	true = True

	#if never search this keyword before, then we have to get items from web.
	r = get_items_by_keyword(keyword, int(more)+1)
	f = open(path+"items.json", "w")
	f.write(r)
	f.close()
	items = eval(r)
	structed_items = []
	if items["findItemsByKeywordsResponse"][0]["ack"][0] != "Success":
		print "Error"
	else:
		for item in items["findItemsByKeywordsResponse"][0]["searchResult"][0]["item"]:
			oneitem = {}
			oneitem["itemid"] = item["itemId"][0]
			oneitem["title"] = item["title"][0]
			oneitem["url"] = item["viewItemURL"][0]
			oneitem["image"] = item["galleryURL"][0]
			oneitem["price"] = item["sellingStatus"][0]["currentPrice"][0]["__value__"]
			structed_items.append(oneitem)
			
			rs = get_item_specifics(oneitem["itemid"])
			f = open(path+oneitem["itemid"]+".json", "w")
			f.write(rs)
			f.close()
	return path

def main(key, more):
	return local_download(key, more)

if __name__ == "__main__":
	print main(sys.argv[1], sys.argv[2])
