#-*- coding=utf-8 -*-
import re
from app import app
from models import *
from flask import render_template, request, flash, url_for

#from flask_weasyprint import HTML, render_pdf

#主页（相当于总览）
@app.route('/')
def index():
    info_dict = overview_data()
    return render_template('overview.html', info_dict=info_dict)

@app.route('/monitor',methods=['GET','POST'])  # 实时监控静态页面，此时并没有开始和停止
def monitor():
        return render_template('monitor.html')

@app.route('/monitor/start',methods=['POST'])
def start():
    if request.method=='POST':  # Ajax请求：只要浏览器端发出了一个ajax的post请求，那么就立马返回下一个我这边的流量数据
        server_data = monitor_data()
    pass

@app.route('/monitor/stop',methods=['POST'])
def stop():
    return render_template('monitor.html')

#总览
@app.route('/overview')
def overview():
    info_dict = overview_data()
    return render_template('overview.html', info_dict=info_dict)

#分析功能
@app.route('/analysis')
def analysis():
    sou_list, des_list = sou_des_ip()
    return render_template('analysis.html',sou=sou_list,des=des_list)

#站点管理功能
@app.route('/website')
def website():
    data,links,categories = website_show()

    return render_template('website.html',a=data, b = links, c = 'categories')

@app.route('/website/add',methods=['POST'])
def add_site():
    form = request.form
    str_ip = form.get('ip')
    web_name = form.get('web_name')
    classify = form.get('classify')
    if not str_ip or not web_name or not classify:
        flash(u'请输入全部信息')
        return render_template('website.html')
    if not judge_legal_ip(str_ip):
        flash(u'请输入正确格式IP')
        return render_template('website.html')
    else:
        if insert_web(ip_1=str_ip, classify=classify, name=web_name):
            flash(u'添加成功')
            return render_template('website.html')
    return render_template('website.html')

@app.route('/throughput')
def throughput():
    return render_template('throughput.html')

@app.route('/createpdf')
def createpdf():
    return render_template('cretepdf.html')

@app.route('/createpdf/result.pdf',methods=['POST'])
def pdf():
    form = request.form
    since_date = form.get('since_date')
    until_date = form.get('until_date')
    sql = ''
    if since_date:
        since_date = datetime.datetime.strptime(since_date, '%a %b %d %Y')
        since_date = datetime.datetime.strftime(since_date, '%Y-%m-%d')
        sql_since_date = 'time>="%s" and ' % since_date
        sql = sql + sql_since_date
        pass
    if until_date:
        until_date = datetime.datetime.strptime(until_date, '%a %b %d %Y')
        until_date = datetime.datetime.strftime(until_date, '%Y-%m-%d')
        sql_until_date = 'time<="%s" and ' % until_date
        sql =sql + sql_until_date
        pass
    str_1 = u" %s to %s" % (since_date,until_date)
    #pdfkit.from_file('templates\\pdf.html', 'out.pdf')
    info_dict = overview_data()
    html =  render_template('pdf2.html',str_1 = str_1, info_dict=info_dict)
    return render_pdf(HTML(string=html))
    # return render_pdf(url_for('pdf.html',str_1=str_1, info_dict=info_dict))

@app.route('/createpdf/result1.pdf')
def hello_pdf(name):
    # Make a PDF straight from HTML in a string.
    html = render_template('app\\templates\\pdf.html', )
    return render_pdf(HTML(string=html))

@app.route('/analysis/search', methods=['POST'])
def analysis_search():
    form = request.form
    #handel_analysis_from(form=form)
    source_ip = form.get('source_ip')
    destination_ip = form.get('destination_ip')
    protocal = form.get('protocal')
    since_date = form.get('since_date')
    until_date = form.get('until_date')

    if not source_ip and not destination_ip and not protocal and not since_date and not until_date:
        flash(u'请输入一些查询条件')
        return analysis()
        #return render_template('analysis.html')

    sql = ''
    '处理source ip'
    if source_ip:
        if not judge_legal_ip(source_ip):
            flash(u'请输入正确格式的源IP地址')
            return analysis()

        else:
            sql_source_ip = 'sourceip="%s" and ' % source_ip
            sql = sql + sql_source_ip
    '处理destination ip'
    if destination_ip:
        if not judge_legal_ip(destination_ip):
            flash(u'请输入正确格式的目的IP地址')
            return analysis()
            #error_flash(str)
        else:
            sql_destination_ip = 'destinationip="%s" and ' % destination_ip
            sql = sql+ sql_destination_ip
    #sql = sql + ' true'

    '处理destination ip'
    if protocal :
        if protocal =='UDP':
            sql_protocal = 'protocol="UDP" and '
            sql = sql + sql_protocal
        elif protocal =='TCP':
            sql_protocal = 'protocol="TCP" and '
            sql = sql + sql_protocal
    if since_date:
        since_date = datetime.datetime.strptime(since_date, '%a %b %d %Y')
        sql_since_date = ' time>="%s" and ' % since_date
        sql = sql + sql_since_date
    if until_date:
        until_date = datetime.datetime.strptime(until_date, '%a %b %d %Y')
        sql_until_date = ' time<="%s" and ' % until_date
        sql =sql + sql_until_date
    sql =sql + ' true'
    print sql
    info_dict = handel_analysis(sql_str=sql)
    return render_template('analysis_result.html',info_dict=info_dict)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html')


def error_flash(ste):
    flash(str)
    return analysis()

def judge_legal_ip(one_str):
    compile_ip=re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    if compile_ip.match(one_str):
        return True
    else:
        return False