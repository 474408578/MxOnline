from random import Random
from django.core.mail import send_mail
from users.models import EmailVerifyRecord
# 导入settings
from django.conf import settings
# 生成随机字符串
def random_str(random_length=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(random_length):
        str += chars[random.randint(0, length)]
    return str


# 发送邮件
def send_register_email(email, send_type='register'):
    # 发送前先保存到数据库，到时候查询链接是否存在
    email_record = EmailVerifyRecord()
    code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    
    email_record.save()
    
    # 定义邮件
    email_title = ""
    email_body = ""
    
    if send_type == "register":
        email_title = "NOC注册激活链接"
        email_body = "请点击以下链接激活您的账号：http://127.0.0.1:8000/active/{0}".format(code)
        
        # 使用Django内置的函数发送邮件，四个参数：主题，邮件内容，发件人邮箱地址，收件人（是一个字符串列表）
        send_status = send_mail(email_title, email_body, settings.EMAIL_FROM, [email])
        
        if send_status:
            pass
        
    
    elif send_type == 'forget':
        email_title = 'NOC找回密码链接'
        email_body = '请点击以下链接找回您的密码：http://127.0.0.1:8000/reset/{0}'.format(code)
        send_status = send_mail(email_title, email_body, settings.EMAIL_FROM, [email])
        
        if send_status:
            pass