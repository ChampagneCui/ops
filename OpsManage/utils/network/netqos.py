import sys
import time
import threading
import ConfigParser
import ssh_client
from LogFile import Logger
from LogFile import log_file


BASE_DIR=r'/opt/ops/OpsManage/utils/network/'
COUNTER_FILE=BASE_DIR+'counter.txt'
CMD_FILE=BASE_DIR+'cmd_list.txt'
CONFIG_FILE=BASE_DIR+'config'
SW_FILE=BASE_DIR+'sw_list.txt'
CMD_TEM_FILE=BASE_DIR+'cmd_template.txt'


""" Multi threading ssh function.
"""

def make_ip_rules(ip_group):
    SOURCE='rule  permit ip source '
    DESTINATION='rule  permit ip destination '
    ip_list=ip_group.split(',')
    result=[]
    for i in ip_list:
        add_s=SOURCE+i+' 0'
        add_d=DESTINATION+i+' 0'
        result.append(add_s)
        result.append(add_d)
    res_str='\n'.join(result)
    return res_str

def make_cmd_list(group,ip_group,width):
    width=int(width)
    width_min=width*1024
    width_max=width_min*2
    ip_rules=make_ip_rules(ip_group)
    result_all=[]
    number=counter()
    with open(CMD_TEM_FILE, "r") as f:
        for line in f:
            cmd = line.strip()
            cmd = cmd.replace('@GROUP',group)
            cmd = cmd.replace('@WIDTH_MIN',str(width_min))
            cmd = cmd.replace('@WIDTH_MAX',str(width_max))
            cmd = cmd.replace('@RULES',ip_rules)
            cmd = cmd.replace('@NUMBER',number)
            result_all.append(cmd)
        result_str='\n'.join(result_all)

    with open(CMD_FILE, "w") as ff:
        ff.write(result_str)

def counter():
    with open(COUNTER_FILE, "r") as f:
        number=f.readline().strip()
        next=int(number)+1
        #print(number,next)
        next_str=str(next)
    with open(COUNTER_FILE, "w") as f:
        f.write(next_str)
    return number

def threading_ssh(sw_each, sw_type, cmd_list):
    # config logging
    logger = log_file(sw_each)

    # print "Begin to ssh for switch: ", sw_each["sw_ip"], " in ", threading.current_thread()
    msg = "Begin to ssh for switch: ", sw_each["sw_ip"], " in ", threading.current_thread()
    logger.log(msg)

    ssh = ssh_client.ssh_connect(sw_each, logger)
    ssh_client.ssh_enable(ssh, sw_type, logger)
    #ssh_client.ssh_unpaging(ssh, sw_type, logger)
    ssh_client.ssh_exec_commands(ssh, cmd_list, logger)
    #ssh_client.ssh_paging(ssh, sw_type, logger)
    #ssh_client.ssh_disable(ssh, sw_each, sw_type)   #no need to change to user mode
    #ssh_client.ssh_save(ssh, sw_type, logger)
    ssh_client.ssh_disconnect(ssh, logger)
    #print "Success to exec commands for switch: ", sw_each["sw_ip"]
    msg = "All comands have been executed for switch: ", sw_each["sw_ip"], " in ", threading.current_thread()
    logger.log(msg)


def qos_exec(group,ip_group,width):
    make_cmd_list(group,ip_group,width)
    # config running parameters.
    sw_type = "huawei"
    sw_list_file = SW_FILE
    cmd_list_file = CMD_FILE
    thread_count = 2

    # sw_list stored all the switch data(ip,name,pwd)
    sw_list = []
    with open(sw_list_file, "r") as f:
        for line in f:
            sw_ip, sw_name, sw_pwd = line.strip().split("\t")
            sw_data = {"sw_ip": sw_ip, "sw_name": sw_name, "sw_pwd": sw_pwd}
            sw_list.append(sw_data)

    # cmd_list store all the cmd which will be exec
    cmd_list = []
    with open(cmd_list_file, "r") as f:
        for line in f:
            cmd = line.strip()
            cmd_list.append(cmd)

    threads = []
    # print "sw_list: ", sw_list
    #print "sw_list: ", sw_list
    #print "cmd_list: ", cmd_list
    for sw_each in sw_list:
        t = threading.Thread(target=threading_ssh, args=(sw_each, sw_type, cmd_list))
        t.setDaemon(True)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()


#if __name__ == "__main__":
    #main('cxb_1M','111.10.0.58,111.10.0.59','1')
