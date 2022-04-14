#Python3通过虾推啥的API接口让你的消息推送到你的微信。
#encoding:utf-8

import requests
SendKey = 'HLxxxxxy3998IxxxxxxPEmNEs' #"在虾推啥获得的SCKEY值" 登录之后获取即可 http://www.xtuis.cn/



def Send_email(Your_Send_Title,Your_Send_Text):          #发微信消息
    api = '	http://wx.xtuis.cn/' + SendKey + '.send'
    if(Your_Send_Title != ""):
        title = Your_Send_Title  #最大长度为 32
    else:
        title = "默认通知标题"
    if(Your_Send_Text != ""):
        content = Your_Send_Text
    else:
        content = "默认的文本内容"
    #发送的数据如下：
    data = { "text": title,  "desp": content }
    req = requests.post(api, data=data)
    # print(req) #200表示返回成功

if __name__ =='__main__':
    Send_email('这是一个测试用的信息的标题','测试的内容')
