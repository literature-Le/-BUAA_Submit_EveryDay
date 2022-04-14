"""
2021-12-6 初始版本成功
2021-12-7 增加Try 语句 ，并添加未到填报时间
2022-3-10 17点13分 过段时间 得更新一下 chromedriver.exe 来保持驱动的一致才行  http://npm.taobao.org/mirrors/chromedriver/ 更新chromedriver.exe
2022-3-14 16点24分 尝试进行地理位置的模拟，因为自动签到时，一直将我的位置识别为香港，导致我不能使用  成功！！！！
"""
from selenium import webdriver
import time
import WeChat_XiaTuiShaSend


Sno = "ZY2X07XXX"           # 学号信息
Spassword = "xxxxxx"     # 学号密码

# 北航的地理位置
latitude = 39.991538
longitude = 116.358428
accuracy = 100

Dictionary = {Sno:Spassword} # 这里可以配置多个学生的信息 进行多学生的自动签到


def Submit(tempSno,tempSpwd):
    try:
        #可以增加 Try Except
        Target_Website_Url = "https://app.buaa.edu.cn/uc/wap/login?redirect=https%3A%2F%2Fapp.buaa.edu.cn%2Fsite%2FbuaaStudentNcov%2Findex"
        option = webdriver.ChromeOptions()
        # option.add_argument('headless')  # 设置option    网页显示 取消注释后，就可以再后台执行
        browser = webdriver.Chrome(options=option)
        #定位 北京市海淀区  沙河校区的可以查找经纬度 替换到上面即可
        browser.execute_cdp_cmd("Emulation.setGeolocationOverride", {
            "latitude": latitude,
            "longitude": longitude,
            "accuracy": accuracy
        })
        browser.get(Target_Website_Url)
        browser.find_element_by_xpath("/html/body/div[1]/div[2]/div[1]/input").send_keys(tempSno)  # 学号输入
        browser.find_element_by_xpath("/html/body/div[1]/div[2]/div[2]/input").send_keys(tempSpwd)  # 密码输入
        browser.find_element_by_xpath("/html/body/div[1]/div[3]").click()  # 点击登录
        # 获取是否签到成功的提示信息
        time.sleep(8)
        IS_SubmitText = browser.find_element_by_xpath(" /html/body/div[1]/div[1]/div/div[6]/a").text
        print('提示信息是：', IS_SubmitText)
        if(IS_SubmitText == "您已提交过信息"):
            return "已提交"
        if IS_SubmitText == "未到填报时间":
            return "未到填报时间"
        else:
            # 点击获取 当前位置
            time.sleep(2)
            browser.find_element_by_xpath(
                "/html/body/div[1]/div[1]/div/div[5]/div/div[2]/div[2]/div[2]/input").click()  # 点击当前位置
            # 点击签到
            time.sleep(5)
            browser.find_element_by_xpath("/html/body/div[1]/div[1]/div/div[6]/a").click()
            # 确定的确定
            time.sleep(1)
            browser.find_element_by_xpath("/html/body/div[5]/div/div[2]/div[2]").click()
            # 成功的信息
            InfromationText = browser.find_element_by_xpath("/html/body/div[1]/div[3]/div/p/span").text
            print(InfromationText)
            return "提交成功"
    except:
        return "提交失败"


print("开始执行")

str = ""
for student in Dictionary:
    str += student +":"
    str += (Submit(student,Dictionary[student]))
    str += ','

print('  ',str)
# WeChat_XiaTuiShaSend.Send_email('BUAA每日签到ok',str)
WeChat_XiaTuiShaSend.Send_email(str,str)


