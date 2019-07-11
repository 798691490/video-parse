import pymysql
import json
import time
import urllib
import urllib.request
import hashlib
import random

MYSQL_HOST = "118.24.241.115"
MYSQL_PORT = 3306
MYSQL_USER = "root"
MYSQL_PASSWD = "123456"
MYSQL_DB = "save_YZM"
MYSQL_DB1 = "USER_VERIFY"

def md5(str):
    import hashlib
    m = hashlib.md5()
    m.update(str.encode("utf8"))
    return m.hexdigest()

def send_YZM(phone):
    j = 4
    statusStr = {
        '0': '短信发送成功',
        '-1': '参数不全',
        '-2': '服务器空间不支持,请确认支持curl或者fsocket,联系您的空间商解决或者更换空间',
        '30': '密码错误',
        '40': '账号不存在',
        '41': '余额不足',
        '42': '账户已过期',
        '43': 'IP地址限制',
        '50': '内容含有敏感词'
    }

    smsapi = "http://api.smsbao.com/"
    user = '13453276222'
    password = md5('qweasdzxc.')
    random_num = ''.join(str(i) for i in random.sample(range(0,9),j))
    print(random_num)
    content = '【短视频解析助手】 您的验证码是：{}，请在30分钟内使用。'.format(random_num)
    data = urllib.parse.urlencode({'u': user, 'p': password, 'm': phone, 'c': content})
    send_url = smsapi + 'sms?' + data
    response = urllib.request.urlopen(send_url)
    the_page = response.read().decode('utf-8')
    print(statusStr[the_page])
    if statusStr[the_page] == '短信发送成功':
        return random_num
    if statusStr[the_page] == '余额不足':
        return '余额不足'


# 不存在上传
def Upload_the_infoid(MD5, YZM):
    try:
        with pymysql.connect(host=MYSQL_HOST, port=MYSQL_PORT, database=MYSQL_DB,user=MYSQL_USER,password=MYSQL_PASSWD, charset='utf8')as cursor:
            sql = "INSERT INTO YZM(MD5_KEY, YZM) VALUES('%s','%s')" % (MD5, YZM)
            cursor.execute(sql)
        return True
    except:
        import traceback
        traceback.print_exc()
        return False

# 检查密钥
def duplicate_checking_key(MD5, YZM):
    try:
        with pymysql.connect(host=MYSQL_HOST, port=MYSQL_PORT, database=MYSQL_DB,
                               user=MYSQL_USER,
                               password=MYSQL_PASSWD, charset='utf8', cursorclass=pymysql.cursors.DictCursor)as cursor:
            cursor.execute(
                "SELECT YZM from YZM where MD5_KEY ='%s'" % (MD5))

            data = cursor.fetchone()["YZM"]
            print(data)
            if int(data) == int(YZM):
                return True
            else:
                return False
    except:
        return False

# 不存在上传
def Upload_the_info(USERNAME, MD5, DDH_NUM, PHONE_NUM,BEIZHU, VX_NUM, QQ_NUM):
    time_ = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
    try:
        state = '1'
        with pymysql.connect(host=MYSQL_HOST, port=MYSQL_PORT, database=MYSQL_DB,user=MYSQL_USER,password=MYSQL_PASSWD, charset='utf8')as cursor:
            sql = "INSERT INTO Dingdan_info(USERNAME, MD5, DDH_NUM, PHONE_NUM,BEIZHU, VX_NUM, QQ_NUM, state, UPTIME) VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (str(USERNAME), str(MD5), str(DDH_NUM), str(PHONE_NUM),str(BEIZHU), str(VX_NUM), str(QQ_NUM), state, str(time_))
            cursor.execute(sql)
        return True
    except Exception as e:
        import traceback
        traceback.print_exc()
        return False

# duplicate_checking_key('a0deb4d124159da796c0e935ac8fbaa1','3611')

def send_TZ(phone):
    j = 4
    statusStr = {
        '0': '短信发送成功',
        '-1': '参数不全',
        '-2': '服务器空间不支持,请确认支持curl或者fsocket,联系您的空间商解决或者更换空间',
        '30': '密码错误',
        '40': '账号不存在',
        '41': '余额不足',
        '42': '账户已过期',
        '43': 'IP地址限制',
        '50': '内容含有敏感词'
    }

    smsapi = "http://api.smsbao.com/"
    user = '13453276222'
    password = md5('qweasdzxc.')
    random_num = ''.join(str(i) for i in random.sample(range(0,9),j))
    content = '【短视频解析助手】 您的验证码是：{}，请在30分钟内使用。'.format(random_num)
    data = urllib.parse.urlencode({'u': user, 'p': password, 'm': phone, 'c': content})
    send_url = smsapi + 'sms?' + data
    response = urllib.request.urlopen(send_url)
    the_page = response.read().decode('utf-8')
    print(statusStr[the_page])
    if statusStr[the_page] == '短信发送成功':
        return random_num
    if statusStr[the_page] == '余额不足':
        return '余额不足'

# 不存在上传
def Upload_the_YZM(PHONE, YZM):
    time_ = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
    state = '0'
    try:
        with pymysql.connect(host=MYSQL_HOST, port=MYSQL_PORT, database=MYSQL_DB,user=MYSQL_USER,password=MYSQL_PASSWD, charset='utf8')as cursor:
            sql = "INSERT INTO YZM_1(UPTIME, YZM, PHONE, state) VALUES('%s','%s','%s','%s')" % (str(time_), str(YZM), str(PHONE), state)
            cursor.execute(sql)
        return True
    except:
        import traceback
        traceback.print_exc()
        return False

# 检查密钥
def duplicate_checking_key11(PHONE, YZM):
    try:
        with pymysql.connect(host=MYSQL_HOST, port=MYSQL_PORT, database=MYSQL_DB,
                               user=MYSQL_USER,
                               password=MYSQL_PASSWD, charset='utf8', cursorclass=pymysql.cursors.DictCursor)as cursor:
            cursor.execute(
                "SELECT * from YZM_1 where PHONE ='%s' order by UPTIME desc;" % (PHONE))

            data = cursor.fetchall()[0]
            print(data,'111')
            if data["state"] != '1':
                print(111,YZM)
                if int(data["YZM"]) == int(YZM):
                    return True
                else:
                    return False
            else:
                return False
    except:
        return False


def Get_dingdan_info(PHONE):
    try:
        with pymysql.connect(host=MYSQL_HOST, port=MYSQL_PORT, database=MYSQL_DB,
                               user=MYSQL_USER,
                               password=MYSQL_PASSWD, charset='utf8', cursorclass=pymysql.cursors.DictCursor)as cursor:
            cursor.execute(
                "SELECT * from Dingdan_info where PHONE_NUM ='%s' order by UPTIME desc;" % (PHONE))

            data = cursor.fetchall()
            print(data)
            data_list = []
            for i in data:
                dict = {}
                dict["id"] = i["DDH_NUM"]
                dict["phone"] = i["PHONE_NUM"]
                dict["name"] = i["USERNAME"]
                if i["state"] == '1' or i["USERNAME"] == 1:
                    dict["j1ob"] = '待发货！'
                    dict["j2ob"] = ''
                elif i["state"] == '2' or i["USERNAME"] == 2:
                    dict["j1ob"] = '订单完成！'
                    dict["j2ob"] = i["KEY"]

                else:
                    dict["j1ob"] = '订单异常！'
                    dict["j2ob"] = ''

                data_list.append(dict)
            print(data_list)
            return data_list
    except Exception as e:
        print(e)
        return None

Get_dingdan_info('17603414639')


def Update_Download_state(YZM,PHONE):
    try:
        with pymysql.connect(host=MYSQL_HOST, port=MYSQL_PORT, database=MYSQL_DB,
                             user=MYSQL_USER,
                             password=MYSQL_PASSWD, charset='utf8')as cursor:
            state = '1'
            sql = "update YZM_1 set state='%s' where YZM='%s' AND PHONE='%s'" % (state,YZM,PHONE)
            cursor.execute(sql)
        return True
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(e)
        return False

def Upload_the_keyy(Secret_key, valid_time, whether_to_activate):
    try:
        with pymysql.connect(host=MYSQL_HOST, port=MYSQL_PORT, database=MYSQL_DB1,user=MYSQL_USER,password=MYSQL_PASSWD, charset='utf8')as cursor:
            sql = "INSERT INTO Secret_key_List(Secret_key, valid_time, whether_to_activate) VALUES('%s','%s','%s')" % (Secret_key, valid_time, whether_to_activate)
            cursor.execute(sql)
        return True
    except:
        import traceback
        traceback.print_exc()
        return False

def DDH_cunzai(DDH_NUM):
    with pymysql.connect(host=MYSQL_HOST, port=MYSQL_PORT, database=MYSQL_DB,
                         user=MYSQL_USER,
                         password=MYSQL_PASSWD, charset='utf8')as cursor:
        sql = "SELECT * FROM Dingdan_info where DDH_NUM='%s';" % (DDH_NUM)
        cursor.execute(sql)
        data = cursor.fetchone()
    if data == None:
        return False
    else:
        return True

def Upload_the_shiyong_user(users_phone):
    try:
        with pymysql.connect(host=MYSQL_HOST, port=MYSQL_PORT, database=MYSQL_DB,user=MYSQL_USER,password=MYSQL_PASSWD, charset='utf8')as cursor:
            sql = "INSERT INTO The_trial_users(users_phone) VALUES('%s')" % (users_phone)
            cursor.execute(sql)
        return True
    except:
        import traceback
        traceback.print_exc()
        return False

def shiyong_user_cunzai(users_phone):
    with pymysql.connect(host=MYSQL_HOST, port=MYSQL_PORT, database=MYSQL_DB,
                         user=MYSQL_USER,
                         password=MYSQL_PASSWD, charset='utf8')as cursor:
        sql = "SELECT * FROM The_trial_users where users_phone='%s';" % (users_phone)
        cursor.execute(sql)
        data = cursor.fetchone()
    if data == None:
        return False
    else:
        return True
