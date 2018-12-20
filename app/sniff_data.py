#-*- coding=utf-8 -*-
from scapy.all import *
from test import q

# dpkt = sniff(filter='host 10.10.4.164',prn=lambda x:x.summary())
list = []
last_pkt_time = 0  # 每一次存储的时间
data_plan = {}  # 数据流量的存储：时间(str)与数据大小(int/B),主要是拿来做一秒钟的流量统计
# data_plan_list = []  # 数据流量的列表，采用列表主要是为了方便给前端返回下一个时间点与数据长度统计值
# 每一秒的数据包的解析


def get_last_pkt(last_pkt_time):
    print('每一秒的数据开始存储到data_plan_list')
    global data_plan
    each_pkt_dict = {}  # 存储每个包的临时字典变量
    each_pkt_dict['time']=last_pkt_time
    each_pkt_dict['length'] = data_plan[last_pkt_time]
    print(each_pkt_dict)
    q.put(each_pkt_dict)
    # data_plan_list.append(each_pkt_dict)
    print('队列大小:', q.qsize())



# def show_last_pkt(last_pkt_time):
#     print(last_pkt_time, '的数据大小是：',data_plan[last_pkt_time])

# 每一个数据包的统计
def get_data_plan(pkt_time, pkt_len):
    global last_pkt_time
    global data_plan
    if not (pkt_time==last_pkt_time):
        data_plan[pkt_time] = pkt_len  # 如果没有这个时间点的数据长度，那么就直接创建
        if last_pkt_time:
            get_last_pkt(last_pkt_time)  # 第一个是不展示数据的，然后我没有展示最后一秒的数据包，因为我不知道怎么判定这是最后一个包
        last_pkt_time = pkt_time
    else:
        data_plan[pkt_time] = data_plan[pkt_time] + pkt_len  # 如果已经存在这个时间点的数据包，那么就叠加数据长度。并且把上一秒的流量给展示出来
          # 如果是下一个时间点的话，就把上一个时间点的数据给打印出来


def packet_parse(pkt):  # 解析每一个包
    dic = {}
    now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 得到当前时间戳，但是数据格式不对，需要转换成str类型
    pkt_lenth = pkt.__len__()
    dic['time']=now_time  # 把包暂时存入字典里
    data_plan['time']= now_time  # 每到一个包拿去统计+实时显示
    data_plan['len']= now_time  # 每到一个包的大小拿去统计
    get_data_plan(now_time, pkt_lenth)

    if pkt.haslayer(IP):  # 先过滤到IP，后面再过滤到TCP和UDP
        dic['src'] = pkt[IP].src  # 获得源地址
        dic['dst'] = pkt[IP].dst  # 获得目的地址
        dic['len'] = pkt_lenth # 获得包的大小，单位是byte，字节，不是bit
        if pkt.haslayer(TCP):
            dic['ptl'] = 'TCP'  # 获得TCP协议
        else:
            dic['ptl'] = 'UDP'  # 获得UDP协议
        return list.append(dic)  # 返回一个解析出来的包

def start(signal):
    if signal == 1:
        print('sniff函数已经开启')
        sniff(filter='host 10.16.68.150', prn=packet_parse)  # prn传入一个函数名，然后sniff会调用这个函数传入捕获的一个包


# class Capture:
#     def __init__(self):
#         self.list = {}  # 拿来存储每个包的列表
#
#     def print_data(self):
#         print(self.list)  # 打印数据
#
#     def set_data(self,data):
#         self.list = data
#
#     def get_data(self,):
#         return self.list  # 获得解析后数据，以列表存储，但是每个元素却是字典

# a=Capture()
# a.set_data(list)
# a.print_data()

# wrpcap("demo.pcap", dpkt)
