#!/opt/env27/bin/python
import logging

LogDir=r'/opt/ops/OpsManage/utils/network/logs/'

class Logger(object):
    """Logger class for writing log to files"""
    def __init__(self, fname):
        super(Logger, self).__init__()
        self.file = open(fname, "w")
        self.file_name = fname

    def log(self, msg):
        msg = str(msg)
        self.file.write(msg)
        self.file.flush()

    def log_end(self):
        msg = "End logging for switch: ", self.file_name
        self.file.write(msg)
        self.file.close()

def log_file(sw_each):
    sw_ip = sw_each["sw_ip"]
    sw_name = sw_each["sw_name"]
    sw_pwd = sw_each["sw_pwd"]
    sw_ip_path=LogDir+sw_ip
    log = Logger(sw_ip_path)
    return log
