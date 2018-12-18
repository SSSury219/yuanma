# encoding: utf-8
import time, datetime
import pymysql
import math,re

class mysql_handler:
	def __init__(self):
		self.conn = None
		self.cursor = None
		try:
			self.conn = pymysql.connect(host='127.0.0.1', user="root", password="root", database="infosecurity", port=3306, charset='utf8', cursorclass=pymysql.cursors.DictCursor)
			self.cursor = self.conn.cursor()
		except pymysql.Error as e:
			print"Mysql connect Error:%s" % e
	'''update mysql database webpage table count as mysql service status '''

	def close(self):
		self.cursor.close()
		self.conn.close()

	def __select(self, sql):
		try:
			self.cursor.execute(sql)
			results = self.cursor.fetchall()
			return results
		except:
			print 'select error'
		return []

	#新增加对抓包的时间,src,dst,ptl四个字段的查询bySJT
	def select_now_data(self):
         pass

	def select_top10_web(self):
		#sql = 'SELECT webname,count(webname)  FROM detailinfo group by webname order by count(webname) desc;'
        # 选择网站名，采用求和
		sql = 'SELECT webname,SUM(size)  FROM detailinfo group by webname order by SUM(size) desc;'
		result = self.__select(sql)
		#print len(result)
		list  = []
		for k in range(len(result)):
			if result[k]['webname'] != 'other' and not judge_legal_ip(result[k]['webname']):
				try:
					list.append(result[k]['webname'])
				except:
					list.append("Name Error")
			if len(list) == 10 :
				break
		#list = ['lol','qq','youdaoyun','baidu','aqy','weibo','h1z1','CSDN','baiduwenxue','pandatv']
		if len(list)< 10:
			for i in range(len(list),10):
				list.append("Name Error")
		#print list
		return list

	'''SELECT destinationip,count(*)  FROM detailinfo  group by destinationip  order by COUNT(*) desc;'''
	def select_info(self,str_sql):
		sql = 'SELECT * FROM detailinfo where classify != 10 and %s;' % str_sql
		print sql
		#sql = 'SELECT * FROM detailinfo where classify != 10 and time>="2018-01-01 00:00:00" and time<="2018-01-08 00:00:00" and true ;'
		result = self.__select(sql)

		#print type(result)
		dict = []
		for i in range(len(result)):
			if result[i]['classify'] == 1:
				result[i]['classify'] = 'Music'
			elif result[i]['classify'] == 2:
				result[i]['classify'] = 'Video'
			elif result[i]['classify'] == 3:
				result[i]['classify'] = 'Shopping'
			elif result[i]['classify'] == 4:
				result[i]['classify'] = 'Games'
			elif result[i]['classify'] == 5:
				result[i]['classify'] = 'Learning'
			elif result[i]['classify'] == 6:
				result[i]['classify'] = 'News'
			dict.append(result[i])
		#print dict
		return dict

	def selsect_soudes_ip(self):
		sql_sou = 'SELECT COUNT(*),sourceip FROM `detailinfo` GROUP BY sourceip ORDER BY COUNT(*) desc;'
		sou_list = self.__select(sql_sou)
		if len(sou_list)<10:
			for i in range(len(sou_list),10):
				add_dict = {"COUNT(*)":0,"sourceip":"NULL"}
				sou_list.append(add_dict)
		sql_des = 'SELECT COUNT(*),destinationip FROM `detailinfo` GROUP BY destinationip ORDER BY COUNT(*) desc;'
		des_list = self.__select(sql_des)
		#print len(des_list[0:10])
		return sou_list, des_list[0:10]

	def select_website(self):
		sql = 'SELECT name,COUNT(*) FROM `weblist` GROUP BY `name`;'
		result_1 = self.__select(sql)
		result = []
		for i in range(0,len(result_1)):
			sql= 'SELECT * FROM weblist where name="%s";' % result_1[i]['name']
			result_2 = self.__select(sql)
			result.append(result_2[0])
		return result

	def insert_web(self,str_ip, classify, name):
		sql = ''
		pass
		return True

	def select_classify_6(self):
		sql = 'SELECT classify,count(*)  FROM detailinfo group by classify;'
		result = self.__select(sql)
		#print result 1是音乐，2是视频，3是购物，4是游戏，5是学习，6是新闻
		list  = [0,0,0,0,0,0]
		for i in range(len(result)):
			class_id = result[i]['classify']-1
			if class_id == 9:
				continue
			"数据经过处理"
			list[class_id] = int(math.log(result[i]['count(*)'])*10)
		#print list
		return list

	def select_classify_61(self,str_sql):
		sql = 'SELECT classify,count(*)  FROM detailinfo where %s group by classify;' % str_sql
		#print sql
		result = self.__select(sql)
		#print result 1是音乐，2是视频，3是购物，4是游戏，5是学习，6是新闻
		list  = [0,0,0,0,0,0]
		for i in range(len(result)):
			class_id = result[i]['classify']-1
			if class_id == 9:
				continue
			"数据经过处理"
			list[class_id] = int(math.log(result[i]['count(*)'])*10)
		#print list
		return list

	def select_day_times(self):
		# day_sql = "select DATE_FORMAT(time,'%Y-%c-%e:%H:00:00') weeks,count(size) count from detailinfo group by weeks;"
		day_sql = "select DATE_FORMAT(time,'%Y-%c-%e') weeks,count(size) count from detailinfo group by weeks; "
		result = self.__select(day_sql)
		dict = {}
		day_list = []
		for i in range(len(result)):
			dict[result[i]['weeks']] = i
			day_list.append(result[i]['weeks'])
		return_list = []
		for j in range(7):
			if j == 6:
				j = 9
			sql = "select DATE_FORMAT(time,'%%Y-%%c-%%e') weeks,count(size)count from detailinfo WHERE classify = %d group by weeks; " % (j+1)
			result_class = self.__select(sql)
			list_class = []
			for k in range(0,len(result)):
				list_class.append(0)
			for i in range(0,len(result_class)):
				if dict.has_key(result_class[i]['weeks']):
					tmp_i = dict[result_class[i]['weeks']]
					list_class[tmp_i] = result_class[i]['count']
			#print list_class
			return_list.append(lsit_class)
		#print dict
		return day_list,return_list

	def select_day_kb(self):
		# day_sql = "select DATE_FORMAT(time,'%Y-%c-%e:%H:00:00') weeks,count(size) count from detailinfo group by weeks;"
		day_sql = "select DATE_FORMAT(time,'%Y-%c-%e') weeks,sum(size)  from detailinfo group by weeks; "
		result = self.__select(day_sql)
		dict = {}
		day_list = []
		for i in range(len(result)):
			dict[result[i]['weeks']] = i
			day_list.append(result[i]['weeks'])
		print day_list
		return_list = []
		for j in range(7):
			if j == 6:
				j = 9
			sql = "select DATE_FORMAT(time,'%%Y-%%c-%%e') weeks,sum(size) from detailinfo WHERE classify = %d group by weeks; " % (j+1)
			result_class = self.__select(sql)
			list_class = []
			for k in range(0,len(result)):
				list_class.append(0)
			for i in range(0,len(result_class)):
				if dict.has_key(result_class[i]['weeks']):
					tmp_i = dict[result_class[i]['weeks']]
					list_class[tmp_i] = int(result_class[i]['sum(size)']/1024)
			print list_class
			return_list.append(list_class)
		#print dict
		return day_list,return_list

	def select_hour_class(self):
		sql = 'SELECT DATE_FORMAT(time,"%H") hour,count(*) as count FROM detailinfo GROUP BY HOUR;'
		result = self.__select(sql)
		#print result
		list = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,]
		for i in range(len(result)):
			hour = int(result[i]['hour'])
			list[hour] = result[i]['count']
		#print list
		return list

	def select_hour_class1(self,str_sql):
		sql = 'SELECT DATE_FORMAT(time,"%H") hour,count(*) as count FROM detailinfo WHERE '+str_sql + ' GROUP BY HOUR;'
		#print sql
		result = self.__select(sql)
		#print result
		list = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,]
		for i in range(len(result)):
			hour = int(result[i]['hour'])
			list[hour] = result[i]['count']
		#print list
		return list
	'''生成数据'''

	def __update(self,sql):
		try:
			self.cursor.execute(sql)
			self.conn.commit()
		except:
			self.conn.rollback()
			print 'update error'

	# def update_classif(self):
	# 	sql = 'SELECT destinationip,count(*)  FROM detailinfo group by destinationip;'
	# 	result = self.__select(sql)
	# 	list_ip = []
	# 	for i in range(len(result)):
	# 		list_ip.append(result[i]['destinationip'])
	# 		ip_test = result[i]['destinationip']
	# 		sql = 'update detailinfo set webname="%s" where destinationip="%s";' % (ip_test,ip_test)
	# 		print sql
	# 		self.__update(sql)


def judge_legal_ip(one_str):
	compile_ip = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
	if compile_ip.match(one_str):
		return True
	else:
		return False

#conn= mysql_handler()
#conn.select_day_kb()