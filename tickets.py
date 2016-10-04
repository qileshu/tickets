# coding: gbk

"""Train tickets query via command-line.

Usage:
	ticktes [-gdtkz] <from> <to> <date>

Options:
	-h,--help		显示帮助菜单
	-g				高铁
	-d				动车
	-t				特快
	-k				快速
	-z				直达

Examples:
	tickets 南京 北京 2016-9-23
	tickets -dg 南京 北京 2016-9-23

"""
import requests
import sys
from stations import stations
from docopt import docopt
from prettytable import PrettyTable
from colorama import Fore, init, AnsiToWin32

def cli():
    """command-line interface"""
    arguments = docopt(__doc__)
    from_station = stations.get(arguments['<from>'])
    to_station = stations.get(arguments['<to>'])
    date = arguments['<date>']
    
    #构建url
    #在chrome开发者工具Network找到的Name，右键copy link address
    #把queryDate、from_station和to_station换成{}占位符
    url = 'https://kyfw.12306.cn/otn/lcxxcx/query?purpose_codes=ADULT&queryDate={}&from_station={}&to_station={}'.format(date, from_station, to_station)

    #添加verify=False参数，不验证证书
    r = requests.get(url, verify = False)
    rows = r.json()['data']['datas']
    
    #格式化显示数据
    headers = '车次 车站 时间 历时 商务 一等 二等 软卧 硬卧 软座 硬座 无座'.split()
    pt = PrettyTable()
    pt._set_field_names(headers)
    for row in rows:
        #从row中根据headers过滤信息，然后调用pt.add_row()添加到表中
        pt.add_row([row["station_train_code"],row["start_station_name"],row["start_time"],row["lishi"],row["swz_num"],row["zy_num"],row["ze_num"],row["rw_num"],row["yw_num"],row["rz_num"],row["yz_num"],row["wz_num"]])
        pt.add_row(["",row["end_station_name"],row["arrive_time"],"","","","","","","","",""])
    print(pt)
    
if __name__ == '__main__':
    cli()





