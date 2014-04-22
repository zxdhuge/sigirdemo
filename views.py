from django.template import Template, Context
from django.template.loader import get_template
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect

from get_information import *
from entity_resolute import *
from info_process import *
import os

def slide(request):
	f = open('/var/tmp/sim.tmp')
	r = float('%.2f' % float(f.read()))
	f.close()
	os.system('rm /var/tmp/sim.tmp')
	return render_to_response('slide.html', {'sim':r})

def search(request):
	return render_to_response('smartphone.html')

def clicked(request):
	return HttpResponseRedirect(request.GET['url'])

def index(request):
	if 'key' in request.GET:
		keywords = request.GET['key']
		
		keywords = keywords.replace(' ', '')
		path = local_download(keywords, '0')#default: the first page

		structed_items = get_structed_items_local(keywords, 1, path)
		attribute_info,desc,item_cnt = get_attribute_info_local(structed_items, path)
		words = get_words_information(structed_items)
		sim_matrix, sim = cal_similarity(attribute_info, item_cnt, structed_items, words)

		if 'threshold' in request.GET:
			sim = float(request.GET['threshold'])
			#item_set = entity_resolution(sim_matrix, item_cnt, float(request.GET['threshold']))
		#else:
		item_set = entity_resolution(sim_matrix, item_cnt, sim)
		item_set = set_ranking(item_set, sim_matrix, item_cnt)
		new_formed_attr = get_new_formed_attr(attribute_info, item_cnt)
		set_name = get_set_name(structed_items, item_set, new_formed_attr, item_cnt)
		item_set = set_process(item_set, set_name, structed_items)

		f = open("/tmp/tmp.iteminfo", "w")
		f.write(str(item_set))
		f.close()
		
		f = open("/tmp/tmp.attribute_info", "w")
		f.write(str(attribute_info))
		f.close()

		f = open("/var/tmp/sim.tmp", "w")
		f.write(str(sim))
		f.close()
		return render_to_response('result.html', {'sets':item_set, 'key':keywords})
	else:
		return render_to_response('index.html')

def more(request):
	keywords = request.GET['key']

	keywords = keywords.replace(' ', '')
	path = local_download(keywords, '1')#1: the second page

	setid = int(request.GET['setid'])-1

	f = open('/tmp/tmp.iteminfo')
	c = f.read()
	f.close()

	item_set = eval(c)

	#f = open("/tmp/tmp.attribute_info")
	#c = f.read()
	#f.close()

	#attribute_info = eval(c)
	#path = "/var/www/html/sigirdemo/test_data_more/"
	structed_items_more = get_structed_items_local(keywords, 2, path)  #the second page
	attribute_info_more, desc_mote, item_cnt_more = get_attribute_info_local(structed_items_more, path)
	sim_matrix, sim = cal_similarity(attribute_info_more, item_cnt_more)
	item_set_more = entity_resolution(sim_matrix, item_cnt_more, sim)
	words = get_words_information(structed_items_more)
	item_set_more = get_final_sets(item_set_more, words, structed_items_more)
	
	#this code is error after this line
	j = 0
	max_sim = 0
	max_sim_id = 0
	for j in range(0, len(item_set_more)):
		i = 0
		for i in range(0, len(item_set_more[j])):
			item_set_more[j][i] = structed_items_more[item_set_more[j][i]]
		tmp_sim = sim_between_two_set(item_set[setid], item_set_more[j])
		if tmp_sim > max_sim:
			max_sim = tmp_sim
			max_sim_id = j
	result_set = item_set[setid]+item_set_more[max_sim_id]

	return render_to_response("index.html", {'sets':[result_set], 'key':keywords})

def ajax_get_one_blog(request,template_name="more.html"):  

	keywords = request.GET['key']
	setid = int(request.GET['id'])-1
	set_count = int(request.GET['set_count'])

	color_flag = 'a'
	if set_count % 2 == 0:
		color_flag = 'b'
	

	keywords = keywords.replace(' ', '')
	path = local_download(keywords, '1')

	f = open('/tmp/tmp.iteminfo')
	c = f.read()
	f.close()

	item_set = eval(c)

	#f = open("/tmp/tmp.attribute_info")
	#c = f.read()
	#f.close()

	#attribute_info = eval(c)
	#path = "/var/www/html/sigirdemo/test_data_more/"
	structed_items_more = get_structed_items_local(keywords, 2, path)  #the second page
	attribute_info_more, desc_more, item_cnt_more = get_attribute_info_local(structed_items_more, path)
	words = get_words_information(structed_items_more)
	sim_matrix, sim = cal_similarity(attribute_info_more, item_cnt_more, structed_items_more, words)
	item_set_more = entity_resolution(sim_matrix, item_cnt_more, sim)
	item_set_more = get_final_sets(item_set_more, words, structed_items_more)
	
	j = 0
	max_sim = 0
	max_sim_id = 0
	for j in range(0, len(item_set_more)):
		i = 0
		#for i in range(0, len(item_set_more[j])):
			#item_set_more[j][i] = structed_items_more[item_set_more[j][i]]
		tmp_sim = sim_between_two_set(item_set[setid]["list"], item_set_more[j]["list"])
		if tmp_sim > max_sim:
			max_sim = tmp_sim
			max_sim_id = j
	result_set = item_set_more[max_sim_id]

	return render_to_response("more.html", {'sets':result_set["list"], 'set_count':set_count, 'color_flag':color_flag})
	#ctx=dict()  
	#id=request.GET.get("id")
	#blog={"id":"123123", "title":"ajax,hahaha!"}
	#ctx["obj"]=blog
	#return render_to_response('more.html', {"id":"123123", "title":"ajax,hahaha!"})

def test(request):
	return render_to_response("smartphone.html")
