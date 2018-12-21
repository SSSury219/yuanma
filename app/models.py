#-*- coding=utf-8 -*-
from app import db
from mysql_init import mysql_handler
from threading import Thread
from sniff_data import start
from data_buffer import q
import Queue
import datetime,time
import json
flag=1
t_sniff = Thread(target=start,args=(1,)) # 创建一个待开启的嗅探进程
t_sniff.daemon = True
# 这个文件主要是从数据库获得数据
conn = mysql_handler()

# def start_sniff_thread():  # 开启sniff进程
#     t_sniff=threading.Thread(target=sniff)
#     t_sniff.start()
# def stop_sniff_thread()


def start_sniff():
    global flag
    print('嗅探进程已经开启')
    t_sniff.start()


def stop_sniff():
    print('嗅探进程已经关闭')
    global flag
    flag = 0


def monitor_data():  # 这里面一定要开始sniff
    serverdata = json.dumps(q.get())
    return serverdata


# 总览的数据,是从mysql数据库取出来
def overview_data():
	dict_info = {}
	dict_info['list_top10_info'] = conn.select_top10_web()
	dict_info['list_classify_6'] = conn.select_classify_6()
	dict_info['list_hour'] = conn.select_hour_class()
	#print dict_info['list_classify_6']
	return dict_info

def handel_analysis(sql_str):

	dict_info = {}
	dict_info['list_classify_6'] = conn.select_classify_61(sql_str)
	dict_info['list_hour'] = conn.select_hour_class1(sql_str)
	dict_info['dict_info'] = conn.select_info(sql_str)
	return dict_info

def website_show():
	links =[{
		"source": "网站",
		"target": "音乐"
	}, {
		"source": "网站",
		"target": "视频"
	}, {
		"source": "网站",
		"target": "购物"
	}, {
		"source": "网站",
		"target": "游戏"
	}, {
		"source": "网站",
		"target": "学习"
	}, {
		"source": "网站",
		"target": "新闻"
	}]


	size1 = 50
	yy = 200
	yy1 = 250
	data = []
	dict = {}
	dict['name'] = '网站'
	dict['x'] = 0
	dict['y'] = yy
	dict["symbolSize"]= 100
	dict["category"] = '网站'
	dict["draggable"]= "true"
	data.append(dict)
	dict = {}
	dict['name'] = '音乐'
	dict['x'] = 10
	dict['y'] = yy1
	dict["symbolSize"]= 80
	dict["category"] = '网站'
	dict["draggable"]= "true"
	data.append(dict)
	dict = {}
	dict['name'] = '视频'
	dict['x'] = 20
	dict['y'] = yy
	dict["symbolSize"]= 80
	dict["category"] = '网站'
	dict["draggable"]= "true"
	data.append(dict)
	dict = {}
	dict['name'] = '购物'
	dict['x'] = 30
	dict['y'] = yy1
	dict["symbolSize"]= 80
	dict["category"] = '网站'
	dict["draggable"]= "true"
	data.append(dict)
	dict = {}
	dict['name'] = '游戏'
	dict['x'] = 40
	dict['y'] = yy
	dict["symbolSize"]= 80
	dict["category"] = '网站'
	dict["draggable"]= "true"
	data.append(dict)
	dict = {}
	dict['name'] = '学习'
	dict['x'] = 50
	dict['y'] = yy1
	dict["symbolSize"]= 80
	dict["category"] = '网站'
	dict["draggable"]= "true"
	data.append(dict)
	dict = {}
	dict['name'] = '新闻'
	dict['x'] = 60
	dict['y'] = yy
	dict["symbolSize"]= 80
	dict["category"] = '网站'
	dict["draggable"]= "true"
	data.append(dict)
	list = conn.select_website()
	count_x = 70
	for i in range(0,len(list)):
		#print i
		dict_1 = {}
		dict['name'] = list[i]['name']
		dict['x'] = 80 + 10*i
		#print dict['x']
		#print 'x:' + str(dict["x"]) + ','
		if i%2 == 0:
			dict['y'] = yy1
		else:
			dict['y'] = yy
		#print 'y:' + str(dict["y"]) + '},'
		links_dict = {}
		if list[i]['classify'] == 1:
			dict["category"] = '音乐'
			links_dict["source"]= "音乐"
		elif list[i]['classify'] == 2:
			dict["category"] = '视频'
			links_dict["source"] = "视频"
		elif list[i]['classify'] == 3:
			dict["category"] = '购物'
			links_dict["source"] = "购物"
		elif list[i]['classify'] == 4:
			dict["category"] = '游戏'
			links_dict["source"] = "游戏"
		elif list[i]['classify'] == 5:
			dict["category"] = '学习'
			links_dict["source"] = "学习"
		elif list[i]['classify'] == 6:
			dict["category"] = '新闻'
			links_dict["source"] = "新闻"

		links_dict["target"] =dict['name']
		#print '{"source":"'+links_dict["source"]+ '",'
		#print '"target":"'+links_dict["target"]+'"},'

		#dict["category"] = u'网站'
		dict["symbolSize"] = 50
		dict["draggable"] = "true"
		#str = ''' {'category': '%','name': '%s','draggable': 'true', 'symbolSize': %d,'y': %d,'x': %d},''' % ( dict['name'], dict['symbolSize'], dict['x'], dict['y'])
		#str = "{'source':'"+str(links_dict["source"])+ "', 'target':'" +str(links_dict["target"])+ "'},"
		#print str

		print '{x:' + str(dict["x"]) + ','
		if i%2 == 0:
			dict['y'] = yy1
			print "y: yy1,"
		else:
			dict['y'] = yy
			print "y: yy,"
		print '"name":"' + dict["name"] + '",'

		# if i%2 == 0:
		# 	print '"symbolSize":' + str(dict["symbolSize"]) + ','
		#
		# else:
        #
		# 	print "y: yy,"
		print '"symbolSize":' + str(dict["symbolSize"]) + ','
		print '"category":"' + dict["category"] + '",'
		print '"draggable":"true"},'

		links.append(links_dict)
		data.append(dict)

	categories =[ {'name': '网站'
				}, {
					'name': '音乐'
				}, {
					'name': '购物'
				}, {
					'name': '视频'
				}, {
					'name': '游戏'
				}, {
					'name': '新闻'
				}, {
					'name': '学习'
			}]

	return data,links,categories

def sou_des_ip():
	sou_list, des_list = conn.selsect_soudes_ip()
	return sou_list, des_list

def insert_web(ip_1, classify, name):
 	if conn.insert_web(str_ip=ip_1, classify=classify, name=name):
		return True
	else:
		return False
#website_show()
#insert_web('1', 'classify', 'name')
# try:
# 	f = open('templates\\pdf.html','r')
# 	list = f.readlines()
# 	print list
# except:
# 	print 'path error'