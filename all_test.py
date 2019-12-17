#!/usr/bin/python
# -*- coding: UTF-8 -*-

#author:ZHOGNQI
#!/usr/bin/python
# -*- coding: UTF-8 -*-

#author:ZHOGNQI
#
# import sys,os
# sys.path.append(os.path.realpath(os.path.dirname(__file__)+ "/ .."))

import telnetlib
import unittest
import time
import os
from HTMLTestRunner import HTMLTestRunner

from device  import TelnetClient
from service import *


#连接测试仪的变量
port_location = ['//192.168.0.180/1/1', '//192.168.0.180/1/2']
multicaststream_header = ('ethernetII_1.destMacAdd=01:00:5e:02:02:02 ipv4_1.destination=239.2.2.2')
multicastgroupip = '239.2.2.2'
duration = 60
unicaststream_header = ('ethernetII_1.sourceMacAdd=00:00:00:11:11:11 ethernetII_1.destMacAdd=00:00:00:22:22:22',
                        'ethernetII_1.sourceMacAdd=00:00:00:22:22:22 ethernetII_1.destMacAdd=00:00:00:11:11:11')


#登录设备的变量
host_ip = '192.168.5.119'
username = 'root'
password = 'admin'
serverip = '192.168.5.33'
filename = 'FD1616GS_Image_V1.0.6_191216.img'



class OltTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # 实例化登录设备的类
        cls.telnet_client = TelnetClient()
        # 登录设备
        assert cls.telnet_client.login_host(host_ip, username, password)==True

    @classmethod
    def tearDownClass(cls):
        # 断开设备连接
        if cls.telnet_client.logout_host():
            print('设备成功断开连接')

    # '''olt配置测试'''
    # def test_001(self):
    #     '''设备升级测试:'''
    #     assert  self.telnet_client.update(serverip, filename)== True

    '''olt业务测试'''
    def test_002(self):
        '''olt业务测试：单播业务测试:'''
        reset_rom_cmd = ResetROMCommand()
        reset_rom_cmd.execute()
        assert unicast_test(port_location=port_location)=='PASS'
        # 删除测试仪的所有对象

    def test_003(self):
        '''olt业务测试：组播业务测试'''
        reset_rom_cmd = ResetROMCommand()
        reset_rom_cmd.execute()
        assert multicast_test(port_location=port_location)=='PASS'
        #删除测试仪的所有对象

    @staticmethod
    def suite(self):
        # 将测试套件分离出来
        suite = unittest.TestSuite(unittest.makeSuite(OltTest))
        return suite


def get_now_time():
    return time.strftime('%Y-%m-%d %H_%M_%S',time.localtime(time.time()))


# 加载测试类
if __name__ == '__main__':
    fp = os.path.join(os.path.dirname(__file__),'report',get_now_time()+'testReport.html')
    suite = unittest.TestLoader().loadTestsFromTestCase(OltTest)
    runner = HTMLTestRunner(stream=open(fp,'wb'),title='olt_test测试报告',description='olt升级，单播组播流量测试报告')
    runner.run(suite)



