from get_information import get_item_specifics, get_items_by_keyword
from math import log
import os
import re

#for online use
def get_structed_items(keyword, pageNumber=1):
	false = False
	true = True
	items = eval(get_items_by_keyword(keyword, pageNumber))
	structed_items = []
	if items["findItemsByKeywordsResponse"][0]["ack"][0] != "Success":
		print "Error"
	else:
		for item in items["findItemsByKeywordsResponse"][0]["searchResult"][0]["item"]:
			oneitem = {}
			oneitem["itemid"] = item["itemId"][0]
			oneitem["title"] = item["title"][0]
			oneitem["url"] = item["viewItemURL"][0]
			oneitem["price"] = item["sellingStatus"][0]["currentPrice"][0]["__value__"]
			structed_items.append(oneitem)

	return structed_items

#for online use
def get_attribute_info(structed_items):
	i = 0
	attribute_info = {}
	#attribute_info["brand"] = [{"canon":[1,2,3]}, {"nikon":[4,5,6]}]
	for item in structed_items:
		false = False
		true = True
		info = eval(get_item_specifics(item["itemid"]))
		for attr_value in info["Item"]["ItemSpecifics"]["NameValueList"]:
			if attribute_info.has_key(attr_value["Name"]):
				if attribute_info[attr_value["Name"]].has_key(attr_value["Value"][0]):
					attribute_info[attr_value["Name"]][attr_value["Value"][0]].append(i)
				else:
					attribute_info[attr_value["Name"]][attr_value["Value"][0]] = [i]
			else:
				attribute_info[attr_value["Name"]] = {}
				attribute_info[attr_value["Name"]][attr_value["Value"][0]] = [i]

	return attribute_info

#for offline use
def get_structed_items_local(keyword = "", pageNumber = 1, path = "/home/zxdhuge/django/sigirdemo/temp_data/canon/test_data/"):
	false = False
	true = True

	f = open(path+"items.json")
	c = f.read()
	f.close()
	
	items = eval(c)
	structed_items = []
	useful_list = os.listdir(path)
	if items["findItemsByKeywordsResponse"][0]["ack"][0] != "Success":
		print "Error"
	else:
		for item in items["findItemsByKeywordsResponse"][0]["searchResult"][0]["item"]:
			if item["itemId"][0]+'.json' not in useful_list:
				continue
			oneitem = {}
			oneitem["itemid"] = item["itemId"][0]
			oneitem["title"] = item["title"][0]
			oneitem["url"] = item["viewItemURL"][0].replace('\\', '')
			oneitem["image"] = item["galleryURL"][0].replace('\\', '')
			oneitem["price"] = item["sellingStatus"][0]["currentPrice"][0]["__value__"]
			structed_items.append(oneitem)

	return structed_items

#for offline use
def get_attribute_info_local(structed_items, path = "/home/zxdhuge/django/sigirdemo/temp_data/canon/test_data/"):
	i = 0
	attribute_info = {}
	desc = []

	item_cnt = 0
	for item in structed_items:
		false = False
		true = True
		if item['itemid']+'.json' not in os.listdir(path):
			continue
		item_cnt+=1
		#print item['itemid']
		f = open(path+item['itemid']+'.json')
		c = f.read()
		f.close()

	
		pattern = re.compile(r'<.*?>')
		info = eval(c)
		desc.append(pattern.sub('', info["Item"]["Description"]).replace('&nbsp;', ' '))
		try:
			for attr_value in info["Item"]["ItemSpecifics"]["NameValueList"]:
				#print attr_value["Name"], attr_value["Value"]
				if attribute_info.has_key(attr_value["Name"]):
					if attribute_info[attr_value["Name"]].has_key(attr_value["Value"][0]):
						attribute_info[attr_value["Name"]][attr_value["Value"][0]].append(i)
					else:
						attribute_info[attr_value["Name"]][attr_value["Value"][0]] = [i]
				else:
					attribute_info[attr_value["Name"]] = {}
					attribute_info[attr_value["Name"]][attr_value["Value"][0]] = [i]
		except:
			print "information error!"	
		i+=1
	for attr_name in attribute_info.keys():
		for attr_value in attribute_info[attr_name].keys():
			attribute_info[attr_name][attr_value].append(log(float(item_cnt)/float(len(attribute_info[attr_name][attr_value]))))
	
	return attribute_info, desc, item_cnt

def desc_process(desc):
	pass
#	words = {}
#	i = 0
#	for one_desc in desc:
#		tmp = one_desc.lower().split()
#		for w in tmp:
#			if words.has_key(w):
#				words[w]

def main():
	keywords = 'canon'
	structed_items = get_structed_items_local()
	attribute_info,desc,item_cnt = get_attribute_info_local(structed_items)
	i = 0
	for item in structed_items:
		print item['title']
		i+=1
	print len(desc), item_cnt


	pattern = re.compile(r'<.*?>')
#	print pattern.sub('', desc[0]).replace('&nbsp;', ' ')
	print desc[1]

	for onedesc in desc:
		tmp = pattern.sub('', onedesc).replace('&nbsp;', ' ')
		for i in re.finditer(':', tmp):
			span = i.span()
#			print tmp[span[0]-20:span[0]+20]
#	for attr_name in attribute_info.keys():
#		for attr_value in attribute_info[attr_name].keys():
#			print attribute_info[attr_name][attr_value][-1]

#	structed_items_more = get_structed_items_local(keywords, 2, path)  #the second page
#	attribute_info_more,desc_more,item_cnt_more = get_attribute_info_local(structed_items_more, path)
#	sim_matrix, sim = cal_similarity(attribute_info, item_cnt)
#	item_set = entity_resolution(sim_matrix, item_cnt, sim)

if __name__ == "__main__":
	main()
