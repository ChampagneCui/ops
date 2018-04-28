#!/opt/env27/bin/python
#encoding=utf-8
from netlib.conn_type import SSH
import LogFile


def ssh_connect(sw_each, logger):
    """ connect to switch
    sw_each:    one switch data(ip, name, pwd)
    Returns:
    sshclient:  SSH shell object.
    """
    sw_ip = sw_each["sw_ip"]
    sw_name = sw_each["sw_name"]
    sw_pwd = sw_each["sw_pwd"]
    ssh = SSH(sw_ip, sw_name, sw_pwd)
    res = ssh.connect()
    # print res
    msg = res
    logger.log(msg)

    return ssh


def ssh_exec_commands(ssh, cmd_list, logger):
    """ Execute all the commands in cmd_list.
    ssh:            SSH connection.
    cmd_list:    command list will be executed.
    """
    for cmd in cmd_list:
        res = ssh.command(cmd.strip())
        # print res
        msg = res
        logger.log(msg)


def ssh_enable(ssh, sw_type, logger):
    """ Enter to the switch enable mode.
    ssh:            SSH connection.
    sw_type:     Switch type=["cisco", "ruijie", "huawei"].
    """
    if sw_type == "cisco" or sw_type == "ruijie":
        res = ssh.set_enable(sw_pwd)
        # print res
    elif sw_type == "huawei":
        res = ssh.command("sys")
        # print res
    msg = res
    logger.log(msg)



def ssh_unpaging(ssh, sw_type, logger):
    """ Diable the switch pageing func: show all info in one page.
    ssh:            SSH connection.
    sw_type:    Switch type=["cisco", "ruijie", "huawei"].
    """
    if sw_type == "cisco" or sw_type == "ruijie":
        res = ssh.disable_paging()
    elif sw_type == "huawei":
        res = ssh.command("user-interface vty 0 4")
        res = ssh.command("screen-length 0")
        res = ssh.command("q")


def ssh_disable(ssh, sw_type, logger):
    """ Return to user-view mode of switch: exit from enable mode.
    ssh:            SSH connection.
    sw_type:     Switch type=["cisco", "ruijie", "huawei"].
    """
    if sw_type == "cisco" or sw_type == "ruijie":
        res = ssh.command("end")
        res = ssh.command("exit")
        # print res
    elif sw_type == "huawei":
        res = ssh.command("return")
        # print res
    msg = res
    logger.log(msg)


def ssh_paging(ssh, sw_type, logger):
    """ Enable switch paging views: info displays in serval pages.
    ssh:            SSH connection.
    sw_type:     Switch type=["cisco", "ruijie", "huawei"].
    """
    if sw_type == "cisco" or sw_type == "ruijie":
        res = ssh.command("end")
        res = ssh.command("terminal len 62")
    elif sw_type == "huawei":
        res = ssh.command("user-interface vty 0 4")
        res = ssh.command("undo screen-length")
        res = ssh.command("q")


def ssh_save(ssh, sw_type, logger):
    """ save switch config
    ssh:            SSH connection.
    sw_type:    one switch data(ip, name, pwd)
    """
    import re
    if sw_type == "cisco" or sw_type == "ruijie":
        res = ssh.command("end")
        res = ssh.command("write")
        # print res
        msg = res
        logger.log(msg)
    elif sw_type == "huawei":
        res = ssh.command("return")
        res = ssh.command("save")
        # print res
        msg = res
        logger.log(msg)
        if re.search("continue", res):
            res = ssh.command("Y\n")
            # return res
            msg = res
            logger.log(msg)
        else:
            print "Fail to save config for huawei switch."


def ssh_disconnect(ssh, logger):
    """ Disconnect the ssh link
    ssh:            SSH connection.
    """
    ssh.close()


""" Multi threading ssh function.
"""
def threading_ssh(sw_each, logger):
    ssh = ssh_client.ssh_connect(sw_each)
    ssh_client.ssh_enable(ssh,  sw_type)
    ssh_client.ssh_unpaging(ssh, sw_type)
    ssh_client.ssh_exec_commands(ssh, cmd_list)
    ssh_client.ssh_paging(ssh, sw_type)
    # ssh_client.ssh_disable(ssh, sw_each, sw_type)   #no need to change to user mode
    ssh_client.ssh_save(ssh, sw_type)
    ssh_client.ssh_disconnect(ssh)
    # print "All comands have been executed for switch: ", sw_each["sw_ip"]
    msg = "All comands have been executed for switch: ", sw_each["sw_ip"]
    logger.log(msg)
