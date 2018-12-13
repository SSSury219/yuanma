'''from app import db
''''''
import datetime, time

tweet = db.tweet.find()
i = 0
for datajson in tweet:
	a = datajson['created_at']
	time_tuple = datetime.datetime.strptime(a, '%a %b %d %H:%M:%S +0000 %Y')
	t = time.mktime(time_tuple.timetuple())
	t = int(t)
	db.tweet.update({'id':datajson['id']}, {'$set': {'timestamp_ms': t}})
	print i
	i = i + 1'''

import pdfkit

pdfkit.from_url('http://baidu.com', 'out.pdf')

#pdfkit.from_file('test.html', 'out.pdf')

pdfkit.from_string('Hello!', 'out.pdf')

