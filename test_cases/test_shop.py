import pytest
import os
from configs.config import NAME_PSW
from libs.login import Login
from libs.shop import Shop
from tools.excelControl import get_excel_data



# @pytest.mark.usefixtures('xt_shop2') #class
# @pytest.mark.usefixtures('xt_shop1') #类级别



class TestShop:
    #这个测试类里面，每一个接口都需要登陆的token,这个实例只需要操作一次
    def setup_class(self):
        #所有的实例只需要登陆一次,可以使用参数化--配置文件实现
        self.token = Login().login(NAME_PSW, getToken=True)

        self.shopObject = Shop(self.token) #创建店铺实例

    #1 列出店铺
    @pytest.mark.parametrize('inBody, expData',get_excel_data('我的商铺','listshopping'))
    def test_shop_list(self,inBody, expData):
        #调用业务模块代码
        res = self.shopObject.shop_list(inBody)

        #做断言：遇到不规范的断言
        #如果一个断言不能判断出，需要多个断言:assert后面就是一个布尔表达式
        if 'code' in res:
            assert res['code'] == expData['code']
        else:
            assert res['error'] == expData['error']

    
    # def test_001(self,update_shop_init):
    #     print('店铺id: ',update_shop_init[0])
    #     print('图片信息: ', update_shop_init[1])


    # 2 更新店铺
    #在执行店铺更新的接口，不仅需要登录操作，还有一些前置操作，获取id,获取图片
    #只有这个接口需要，其他接口不需要，不能放到setup_class---->setup_method 来完成前置操作，可以尝试下

    #pytest--fixture--环境初始化与清除操作,添加conftest文件
    # @pytest.mark.usefixtures('update_shop_init')#写入函数名字，调用conftest里面的初始化函数

    @pytest.mark.parametrize('inBody, expData',get_excel_data('我的商铺','updateshopping'))
    def test_shop_update(self,inBody, expData, update_shop_init):
        #调用业务模块代码
        res = self.shopObject.shop_update(inBody,update_shop_init[0],update_shop_init[1])

        #做断言：遇到不规范的断言
        #如果一个断言不能判断出，需要多个断言:assert后面就是一个布尔表达式
        if 'code' in res:
            assert res['code'] == expData['code']
        else:
            assert res['error'] == expData['error']


if __name__ == '__main__':
    pytest.main(['test_shop.py','-s','--alluredir','../report/tmp'])
    os.system('allure serve ../report/tmp')




    #2 更新店铺