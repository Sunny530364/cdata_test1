#!/usr/bin/python
# -*- coding: UTF-8 -*-

#author:ZHOGNQI
from telnetlib import Telnet
import time
import logging

class TelnetClient():
    def __init__(self):
        self.tn = Telnet()
        # self.tn.set_debuglevel(2)

    def login_host(self,host_ip,username,password):
        '''
            # 此函数实现telnet登录主机
        :param host_ip:
        :param username:
        :param password:
        :return:
        '''
        try:
            # self.tn = telnetlib.Telnet(host_ip,port=23)
            self.tn.open(host_ip)
        except:
            print('%s 设备连接失败'%host_ip)
            return False
        # 等待login出现后输入用户名，最多等待10秒
        self.tn.read_until(b'>>User name: ',timeout=10)
        self.tn.write(username.encode('ascii') + b'\n')
        # 等待Password出现后输入用户名，最多等待10秒
        self.tn.read_until(b'>>User password: ',timeout=10)
        self.tn.write(password.encode('ascii') + b'\n')
        # 延时两秒再收取返回结果，给服务端足够响应时间
        time.sleep(2)
        # 获取登录结果
        # read_very_eager()获取到的是的是上次获取之后本次获取之前的所有输出
        command_result = self.tn.read_very_eager().decode('utf-8')
        if 'Login-Time'  in command_result:
            print('%s 登录成功'%host_ip)
            return True
        else:
            print('%s 登录失败，用户名或密码错误'%host_ip)
            return False

    def execute_some_command(self):
        '''
        # 此函数实现执行传过来的命令，并输出其执行结果
        :return:
        '''
        # 执行命令
        while True:
            command = input("请输入要执行的命令: ")
            if command == "logout":
                break
            self.tn.write(command.encode()+b'\n')
            time.sleep(1)
            # 获取命令结果
            command_result = self.tn.read_very_eager().decode('utf-8')
            print('命令执行结果：%s' % command_result)

    def backup_config(self,serverip,filename='config1.txt'):
        '''
        备份配置
        :param serverip: 服务器ip
        :param filename: 备份的文件名
        :return: 布尔值
        '''
        self.tn.read_until(b'OLT>', timeout=10)
        self.tn.write('enable'.encode() + b'\n')
        # self.tn.read_until(b'OLT# ', timeout=10)
        self.tn.write('config'.encode() + b'\n')
        self.tn.read_until(b'OLT(config)# ', timeout=10)
        self.tn.write((('backup configuration format txt tftp {0} {1}'.format(serverip,filename)).encode() + b'\n'))
        time.sleep(10)
        backupresult = self.tn.read_very_eager().decode('utf-8')
        if ' backup is successful' in backupresult:
            print('backup configure success')
            return True
        else:
            print('backup configure fail')
            return False

    def update(self,serverip,filename):
        '''
        更新olt的软件版本
        :param serverip: 服务器ip地址
        :param filename: 需要更新的软件版本
        :return: 布尔值
        '''
        self.tn.read_until(b'OLT>', timeout=10)
        self.tn.write('enable'.encode()+b'\n')
        self.tn.read_until(b'OLT# ', timeout=10)
        self.tn.write('config'.encode() + b'\n')
        self.tn.read_until(b'OLT(config)# ', timeout=10)
        self.tn.write(('load packetfile tftp {0} {1}'.format(serverip, filename)).encode()+b'\n')
        #olt升级时间大概在4分钟左右，延时200秒显示结果
        time.sleep(240)
        updateresult = self.tn.read_very_eager().decode('utf-8')
        # print(updateresult)
        if 'upgrade is successful' in updateresult:
            print('update image success')
            return True
        else:
            print('update image fail')
            return False



    def logout_host(self):
        '''
        # 退出telnet
        :return:
        '''
        self.tn.write(b"logout\n")


if __name__ == '__main__':
    host_ip = '192.168.5.98'
    username = 'zq@22'
    password = '1'
    serverip = '192.168.5.33'
    filename = 'FD1616GS_Image_V1.0.6_191204.img'
    telnet_client = TelnetClient()
    # commands=['enable','config','load packetfile tftp {0} {1})+b" \r\n"']
    # 如果登录结果返加True，则执行命令，然后退出
    if telnet_client.login_host(host_ip,username,password):
        # telnet_client.execute_some_command()
        # telnet_client.update(serverip,filename)
        # telnet_client.backup_config(serverip=serverip)
        telnet_client.logout_host()
