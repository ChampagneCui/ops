import time
import threading
import ConfigParser
import ssh_client
from LogFile import Logger
from LogFile import log_file

""" Multi threading ssh function.
"""
def threading_ssh(sw_each, sw_type, cmd_list):
    # config logging
    logger = log_file(sw_each)

    # print "Begin to ssh for switch: ", sw_each["sw_ip"], " in ", threading.current_thread()
    msg = "Begin to ssh for switch: ", sw_each["sw_ip"], " in ", threading.current_thread()
    logger.log(msg)

    ssh = ssh_client.ssh_connect(sw_each, logger)
    ssh_client.ssh_enable(ssh,  sw_type, logger)
    ssh_client.ssh_unpaging(ssh, sw_type, logger)
    ssh_client.ssh_exec_commands(ssh, cmd_list, logger)
    ssh_client.ssh_paging(ssh, sw_type, logger)
    # ssh_client.ssh_disable(ssh, sw_each, sw_type)   #no need to change to user mode
    ssh_client.ssh_save(ssh, sw_type, logger)
    ssh_client.ssh_disconnect(ssh, logger)
    print "Success to exec commands for switch: ", sw_each["sw_ip"]
    msg = "All comands have been executed for switch: ", sw_each["sw_ip"], " in ", threading.current_thread()
    logger.log(msg)

def main():
    # config running parameters.
    conf = ConfigParser.ConfigParser()
    sw_type = "huawei"
    sw_list_file = "sw_list"
    cmd_list_file = "cmd_list"
    thread_count = 1
    with open("config", "r") as f:
        conf.readfp(f)
        sw_type = conf.get("Config", "sw_type")
        sw_list_file = conf.get("Config", "sw_list_file")
        # print "sw_list_file:", sw_list_file
        cmd_list_file = conf.get("Config", "cmd_list_file")
        thread_count = conf.get("Config", "thread_count")

    # sw_list stored all the switch data(ip,name,pwd)
    sw_list = []
    with open(sw_list_file, "r") as f:
        for line in f:
            sw_ip, sw_name, sw_pwd = line.strip().split("\t")
            sw_data = {"sw_ip":sw_ip, "sw_name":sw_name, "sw_pwd":sw_pwd}
            sw_list.append(sw_data)

    # cmd_list store all the cmd which will be exec
    cmd_list = []
    with open(cmd_list_file, "r") as f:
        cmd = f.readline().strip()
        cmd_list.append(cmd)
    
    threads = []
    # print "sw_list: ", sw_list
    for sw_each in sw_list:
        t = threading.Thread(target=threading_ssh, args=(sw_each, sw_type, cmd_list))
        t.setDaemon(True)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()


if __name__ == "__main__":
    main()
