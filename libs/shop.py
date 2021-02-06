import requests
from configs.config import HOST
from libs.login import Login


class Shop:
    # 1- 需要操作商铺--需要token
    def __init__(self, inToken):
        self.header = {'Authorization': inToken}  # 请求头

    # 2- 列出商铺
    def shop_list(self, inData):
        payload = inData
        url = f'{HOST}/shopping/myShop'
        resp = requests.get(url, headers=self.header, params=payload)
        return resp.json()  # 响应数据

    #文件上传
    def file_upload(self, fileName,fileDir):
        url = f'{HOST}/file'
        #post请求的body
        #{'变量名1':(文件名：文件对象，文件类型)}
        #open rb 非文本文件（图片，音频）用rb打开，读2进制
        user_file = {'file':(fileName,open(fileDir,'rb'), 'image/png')}
        resp = requests.post(url, files=user_file, headers=self.header)
        return resp.json()['data']['realFileName']

    #店铺更新，需要两个前置：店铺id（列出接口获取）和图片的信息（upload接口）
    def shop_update(self, inData, shopID, imageInfo):
        url = f'{HOST}/shopping/updatemyshop'
        #1更新店铺的id
        inData['id'] = shopID
        #2 更新图片信息
        inData['image'] = f'{HOST}/file/getImgStream?fileName={imageInfo}'
        inData['image_path'] = imageInfo

        resp = requests.post(url, data=inData, headers=self.header)
        return resp.json()


if __name__ == '__main__':
    token = Login().login({'username': 'sq0777', 'password': 'xintian'}, getToken=True)
    print(token)

    # 列出店铺调用
    shop = Shop(token)
    shopID = shop.shop_list({'page':1,'limit':20})['data']['records'][0]['id']

    #图片上传接口
    image_info =shop.file_upload('123.png','../data/123.png')
    print(image_info)

    #更新店铺
    info = {
            "name": "星巴克新建店",
            "address": "上海市静安区秣陵路303号",
            "id": "3269",
            "Phone": "13176876632",
            "rating": "6.0",
            "recent_order_num":100,
            "category": "快餐便当/简餐",
            "description": "满30减5，满60减8",
            "image_path": "b8be9abc-a85f-4b5b-ab13-52f48538f96c.png",
            "image": "http://121.41.14.39:8082/file/getImgStream?fileName=b8be9abc-a85f-4b5b-ab13-52f48538f96c.png"
        }
    res = shop.shop_update(info, shopID,image_info)
    print(res)

