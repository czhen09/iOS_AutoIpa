# -*- coding: utf-8 -*-
import os
import sys
import time
import hashlib
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib


#项目名称
project_name = "###工程名"
# 项目根目录
project_path = "/Users/zx/Desktop/trunk/" + project_name
# 编译成功后.archive所在目录
app_path = "/Users/zx/Desktop/脚本打包输出"+"/build/archive"
# 打包后ipa存储目录
targerIPA_parth = "/Users/zx/Desktop/脚本打包输出/ipa输出"

exportOptionsPlistPath = "/Users/zx/Desktop/ZX/ios/autoipa-master/exportOptionsPlist.plist"

# firm的api token
fir_api_token = "##############"

#个人qq邮箱
from_addr = "######@qq.com"
smtp_server = "smtp.qq.com"
password = "################"
port = 587
#qq企业邮箱---failure
#from_addr = "####@##.com"
#password = "################"
#smtp_server = "smtp.exmail.qq.com"
#port = 465


to_addr = "287617713@qq.com"


#判断是否上传，上传之后才发送邮件；
isUploadSuccess=False


# 清理项目 创建build目录
def clean_project_mkdir_build():
    os.system('cd %s;xcodebuild clean' % project_path) # clean 项目
    os.system('cd %s;mkdir build' % project_path)

def build_project():
    print("build release start")
    os.system ('xcodebuild -list')
#    os.system ('cd %s;xcodebuild -workspace FoodSecurityB.xcworkspace  -scheme FoodSecurityB -configuration release -derivedDataPath %s ONLY_ACTIVE_ARCH=NO || exit' % (project_path,build_path))
    os.system ('cd %s;xcodebuild archive -workspace %s.xcworkspace -scheme %s -configuration release -archivePath %s' % (project_path,project_name,project_name,app_path))


# CONFIGURATION_BUILD_DIR=./build/Release-iphoneos

# 打包ipa 并且保存在桌面
def build_ipa():
    global ipa_filename
    ipa_timename = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))
    ipa_filename = '%s_%s.ipa'%(project_name,ipa_timename)
#    os.system ('xcrun -sdk iphoneos PackageApplication -v %s -o %s/%s'%(app_path,targerIPA_parth,ipa_filename))

    os.system ('xcodebuild -exportArchive -archivePath %s.xcarchive -exportPath %s/%s -exportOptionsPlist %s'%(app_path,targerIPA_parth,ipa_filename,exportOptionsPlistPath))



#上传
def upload_fir():
    #需要修改全局变量的时候需要 用global 引入
    global isUploadSuccess
    if os.path.exists("%s/%s" % (targerIPA_parth,ipa_filename)):
        print('watting...')
        # 直接使用fir 有问题 这里使用了绝对地址 在终端通过 which fir 获得
        ret = os.system("/usr/local/bin/fir p '%s/%s/%s.ipa' -T '%s'" % (targerIPA_parth,ipa_filename,project_name,fir_api_token))
        isUploadSuccess=True
    else:
        print("没有找到ipa文件")

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

# 发邮件
def send_mail():
    msg = MIMEText('### iOS测试项目已经打包完毕，请前往 	http://fir.im/###### 下载测试！', 'plain', 'utf-8')
    msg['From'] = _format_addr('iOS开发-### <%s>' % from_addr)
    msg['To'] = _format_addr('###等测试人员 <%s>' % to_addr)
    msg['Subject'] = Header('食智监-基础版 iOS客户端打包程序', 'utf-8').encode()
    server = smtplib.SMTP(smtp_server, port)
    server.set_debuglevel(1)
    server.starttls()
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()


def main():
    # 清理并创建build目录
    clean_project_mkdir_build()
    # 编译coocaPods项目文件并 执行编译目录
    build_project()
    # 打包ipa 并制定到桌面
    build_ipa()
    # 上传fir
    upload_fir()
    # 发邮件
    if isUploadSuccess==True:
        print("即将发送邮件")
        send_mail()
    else:
        print("没有上传成功,暂不发送邮件")
# 执行
main()










