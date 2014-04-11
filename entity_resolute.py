from info_process import get_structed_items, get_attribute_info, get_structed_items_local, get_attribute_info_local
from math import log
import os

def rawsim(itemi,itemj,words):
	wordsi = itemi["title"].lower().split() 
	wordsj = itemj["title"].lower().split()

	divisor = 0
	divident = 0
	for word in wordsi:
		if wordsj.count(word) != 0:
			divident += words[word][-1]
		divisor += words[word][-1]
	for word in wordsj:
		if wordsi.count(word) == 0:
			divisor += words[word][-1]

	sim = divident / divisor
	return sim

def cal_similarity(attribute_info, item_cnt, structed_items, words):
	sim_matrix = []
	for i in range(0, item_cnt):
		one = []
		for j in range(0, item_cnt):
#			one.append(rawsim(structed_items[i], structed_items[j], words))
			one.append(0)
		sim_matrix.append(one)
	#sim_matrix = [[0]*item_cnt]*item_cnt
	n = len(attribute_info)
	w = 1.0/n
	for attr_name in attribute_info.keys():
		for attr_value in attribute_info[attr_name].keys():
			for i in attribute_info[attr_name][attr_value][:-1]:
				for j in attribute_info[attr_name][attr_value][:-1]:
					if i != j:
						#sim_matrix[i][j] += attribute_info[attr_name][attr_value][-1]
						sim_matrix[i][j] += w
#	for i in range(0, item_cnt):
#		for j in range(i+1, item_cnt):
#			print i, j, sim_matrix[i][j]
	max_sim = sim_matrix[0][1]
	min_sim = sim_matrix[0][1]
	for i in range(0, item_cnt):
		for j in range(i, item_cnt):
			#print sim_matrix[i][j]
			if sim_matrix[i][j] < min_sim:
				min_sim = sim_matrix[i][j]
			if sim_matrix[i][j] > max_sim:
				max_sim = sim_matrix[i][j]
	return sim_matrix, (max_sim+min_sim)/2.0

def entity_resolution(sim_matrix, item_cnt, threshold):
	item_set = []
	item_set.append([0])

	for i in range(1, item_cnt):
		#j = 0
		flag = False
		for j in range(0, len(item_set)):
			#print i, j, sim_matrix[i][j]
			if flag:
				break
			for k in item_set[j]:
				if sim_matrix[i][k] > threshold:
					item_set[j].append(i)
					flag = True
					break
		if flag == False:
			item_set.append([i])

	return item_set

def sim_between_two_set(seta, setb):
	seta_word = set([])
	for item in seta:
		words = item["title"].split()
		for w in words:
			seta_word.add(w)
	
	setb_word = set([])
	for item in setb:
		words = item["title"].split()
		for w in words:
			setb_word.add(w)

	return float(len(seta_word.intersection(setb_word))) / float(len(seta_word.union(setb_word)))

def get_words_information(structed_items):
	words = dict()
	i = 0
	for item in structed_items:
		tmp = item["title"].lower().split()
		for w in tmp:
			if words.has_key(w):
				words[w].append(i)
			else:
				words[w] = [i]
		i+=1
	
	maxi = 0
	for w in words.keys():
		if len(words[w]) > maxi:
			maxi = len(words[w])

	for w in words.keys():
		words[w].append(float(len(words[w])) / float(maxi))
		#words[w] = log(float(len(structed_items))/float(len(words[w])))
	return words

def top3(set_words):
	t1 = ""
	t2 = ""
	t3 = ""

	c1 = 0
	c2 = 0
	c3 = 0
	for w in set_words.keys():
		if c1 <= c2 and c1 <= c3 and set_words[w] > c1:
			c1 = set_words[w]
			t1 = w
		elif c2 <= c3 and c2 <= c1 and c2 < set_words[w]:
			c2 = set_words[w]
			t2 = w
		elif c3 <= c2 and c3 <= c1 and c3 < set_words[w]:
			c3 = set_words[w]
			t3 = w
		else:
			pass
	return t1,t2,t3

def set_process(item_set, set_name, structed_items):
	new_item_set = list()
	for j in range(0, len(item_set)):
		for i in range(0, len(item_set[j])):
			item_set[j][i] = structed_items[item_set[j][i]]
		one_set = dict()
		one_set["list"] = list(item_set[j])
		one_set["count"] = len(item_set[j])
		one_set["set_title"] = set_name[j]
		new_item_set.append(one_set)
	return new_item_set


def get_final_sets(item_set, words, structed_items):
	j = 0
	new_item_set = list()
	for j in range(0, len(item_set)):
		i = 0
		set_words = dict()
		for i in range(0, len(item_set[j])):
			item_set[j][i] = structed_items[item_set[j][i]]
			tmp = item_set[j][i]["title"].lower().split()
			for w in tmp:
				if set_words.has_key(w):
					set_words[w].add(i)
				else:
					set_words[w] = set([i])
		for w in set_words.keys():
			set_words[w] = ( float(len(set_words[w])) / float(len(item_set[j])) ) * words[w][-1]
		t1,t2,t3 = top3(set_words)
		one_set = dict()
		one_set["list"] = list(item_set[j])
		one_set["count"] = len(item_set[j])
		one_set["set_title"] = t1+' '+t2+' '+t3
		new_item_set.append(one_set)
	return new_item_set

def remove_nouse_items(structed_items, path):
	item_cnt = 0
	for item in structed_items:
		false = False
		true = True
		if item['itemid']+'.json' not in os.listdir(path):
			structed_items.pop(item_cnt)
		item_cnt+=1
	return structed_items
	  
def get_new_formed_attr(attribute_info, item_cnt):
	new_formed_attr = list(dict())
	for i in range(0, item_cnt):
		new_formed_attr.append({})
	for attr_name in attribute_info.keys():
		for attr_value in attribute_info[attr_name].keys():
			for i in attribute_info[attr_name][attr_value][:-1]:
				if not new_formed_attr[i].has_key(attr_name):
					new_formed_attr[i][attr_name] = attr_value
	return new_formed_attr

def get_set_name(structed_items, item_set, new_formed_attr, item_cnt):
	set_name = list(dict())
	for set_id in range(0, len(item_set)):
		set_name.append({})

	for set_id in range(0, len(item_set)):
		for i in item_set[set_id]:
			for attr_name in new_formed_attr[i].keys():
				attr_value = new_formed_attr[i][attr_name].lower()
				if attr_value.find(' / ') != -1:
					for v in attr_value.split('/'):
						v = v.strip()
						if set_name[set_id].has_key(v):
							set_name[set_id][v]+=1
						else:
							set_name[set_id][v] = 1
						if structed_items[i]["title"].lower().find(v) != -1:
							set_name[set_id][v]+=1.2
				else:
					if set_name[set_id].has_key(attr_value):
						set_name[set_id][attr_value]+=1
					else:
						set_name[set_id][attr_value] = 1

					if structed_items[i]["title"].lower().find(attr_value) != -1:
						set_name[set_id][attr_value]+=1.2
	for set_id in range(0, len(item_set)):
		name = ""
		for w in sorted(set_name[set_id].items(), key=lambda d: d[1], reverse=True)[:3]:
			name += w[0]+' '
		if name == "":
			set_name[set_id] = "Unkown"
		else:
			set_name[set_id] = name
	return set_name

def set_ranking(item_set, sim_matrix, item_cnt):
	for oneset in item_set:
		ave_sim = 0
		for i in range(0, len(oneset)):
			for j in range(i+1, len(oneset)):
				ave_sim += sim_matrix[oneset[i]][oneset[j]]
		ave_sim = float(ave_sim) / float(len(oneset))+float(len(oneset))/float(item_cnt)
		oneset.append(ave_sim)
	item_set.sort(key=lambda k:k[-1], reverse=True)
	for i in range(0,len(item_set)):
		item_set[i] = item_set[i][:-1]
	return item_set


def main():
#	path = "/var/www/html/sigirdemo/test_data_more/"
#	structed_items_more = get_structed_items_local('asdf', 2, path)  #the second page
#	attribute_info_more,item_cnt_more = get_attribute_info_local(structed_items_more, path)
#	sim_matrix, sim = cal_similarity(attribute_info_more, item_cnt_more)
#	item_set_more = entity_resolution(sim_matrix, item_cnt_more, sim)
	#print item_set_more
	structed_items = get_structed_items_local()
	#structed_items = remove_nouse_items(structed_items, '/var/www/html/sigirdemo/test_data/')

	attribute_info,item_cnt = get_attribute_info_local(structed_items)

	words = get_words_information(structed_items)
	
	sim_matrix, sim = cal_similarity(attribute_info, item_cnt, structed_items, words)
	item_set = entity_resolution(sim_matrix, item_cnt, sim)
	item_set = set_ranking(item_set, sim_matrix, item_cnt)
	print item_set

	new_formed_attr = get_new_formed_attr(attribute_info, item_cnt)

	set_name = get_set_name(structed_items, item_set, new_formed_attr, item_cnt)
	item_set = set_process(item_set, set_name, structed_items)
#	set_name = list(dict())
#	for set_id in range(0, len(item_set)):
#		set_name.append({})
#
#	for set_id in range(0, len(item_set)):
#		for i in item_set[set_id]:
#			for attr_name in new_formed_attr[i].keys():
#				attr_value = new_formed_attr[i][attr_name].lower()
#				if attr_value.find(' / ') != -1:
#					for v in attr_value.split('/'):
#						v = v.strip()
#						if set_name[set_id].has_key(v):
#							set_name[set_id][v]+=1
#						else:
#							set_name[set_id][v] = 1
#						if structed_items[i]["title"].lower().find(v) != -1:
#							set_name[set_id][v]+=1.2
#				else:
#					if set_name[set_id].has_key(attr_value):
#						set_name[set_id][attr_value]+=1
#					else:
#						set_name[set_id][attr_value] = 1
#
#					if structed_items[i]["title"].lower().find(attr_value) != -1:
#						set_name[set_id][attr_value]+=1.2
#	for set_id in range(0, len(item_set)):
#		name = ""
#		for w in sorted(set_name[set_id].items(), key=lambda d: d[1], reverse=True)[:3]:
#			name += w[0]+' '
#		set_name[set_id] = name
#		print set_name[set_id]
				#print set_id, attr_name, new_formed_attr[i][attr_name] 
#	item_set = get_final_sets(item_set, words, structed_items)

	#print item_set[1]

#	words = sorted(words.items(), key=lambda d: d[1]) 
#
#	for attr_name in attribute_info.keys():
#		for attr_value in attribute_info[attr_name].keys():
#			print attr_name, attr_value;
#	words = dict()
#	i = 0
#	for item in structed_items:
#		tmp = item["title"].lower().split()
#		for w in tmp:
#			if words.has_key(w):
#				words[w].add(i)
#			else:
#				words[w] = set([i])
#		i+=1
#	
#	for w in words.keys():
#		words[w] = log(float(item_cnt)/float(len(words[w])))
	#	print w, words[w]
#	for w in words.keys():
#		print w, len(words[w]), log(float(item_cnt)/float(len(words[w])))
#	print len(structed_items),item_cnt
#	j = 0
#	for j in range(0, len(item_set_more)):
#		i = 0
#		for i in range(0, len(item_set_more[j])):
#			item_set_more[j][i] = structed_items_more[item_set_more[j][i]]
	
#	j = 0
#	for j in range(0, len(item_set)):
#		i = 0
#		for i in range(0, len(item_set[j])):
#			item_set[j][i] = structed_items[item_set[j][i]]
			#print item_set[j][i]["url"]
#	return item_set
if __name__ == "__main__":
	main()
