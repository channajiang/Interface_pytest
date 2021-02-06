
# 1 获取excel对应的数据

from libs.login import Login

import pytest
import os
#

#4-封装测试类
from tools.excelControl import get_excel_data


class TestLogin():
    @pytest.mark.parametrize('inBody, expData', get_excel_data('登录模块', 'Login')) #[(a,b),()]
    def test_login(self, inBody, expData): #封装测试方法

        #调用登录接口代码

        res = Login().login(inBody)

        # 做断言
        assert res['msg'] == expData['msg']






if __name__ == '__main__':
    #需要删除上一次运行的文件，
    try:
        for one in os.listdir('../report/tmp'):
            if 'json' in one or 'txt' in one:
                os.remove(f'../report/tmp/{one}')
    except:
        print('first time run')

    pytest.main(['test_login.py','-s','--alluredir','../report/tmp']) #显示打印信息， -q 简化信息
    #2 -显示测试报告：步骤：1-先pytest --alluredir生成报告所需要的文件
                        # 2- 使用allure 生成可视化报告
    os.system('allure serve ../report/tmp')
    #1 启动allure 服务，不能关闭pycharm
    #2 自动打开浏览器--注意，使用谷歌，火狐

    '''
    . 用例执行成功
    F 断言失败
    E 语法错误
    '''
    #如果在命令行执行测试用例的话，
    # cd 到测试用例路径，直接pytest就可以执行目录下的所有用例






