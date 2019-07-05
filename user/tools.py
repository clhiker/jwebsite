from email.mime.text import MIMEText
import random
import time
import smtplib
import string


class Tools:
    def __init__(self):
        pass

    def getRandomPassword(self):
        src = string.ascii_letters + string.digits
        list_passwd_all = random.sample(src, 5)  # 从字母和数字中随机取5位
        list_passwd_all.extend(random.sample(string.digits, 1))  # 让密码中一定包含数字
        list_passwd_all.extend(random.sample(string.ascii_lowercase, 1))  # 让密码中一定包含小写字母
        list_passwd_all.extend(random.sample(string.ascii_uppercase, 1))  # 让密码中一定包含大写字母
        random.shuffle(list_passwd_all)  # 打乱列表顺序
        return ''.join(list_passwd_all)  # 将列表转化为字符串

    def sendEmail(self, info, mail_to):
        mail_body = info
        # 发信邮箱
        mail_from = 'clhiker@163.com'
        # 收信邮箱
        mail_to = [mail_to]
        # 定义正文
        msg = MIMEText(mail_body)
        # 定义标题
        msg['Subject'] = 'verification your register'
        # 定义发信人
        msg['From'] = mail_from
        msg['To'] = ';'.join(mail_to)
        # 定义发送时间（不定义的可能有的邮件客户端会不显示发送时间）
        msg['date'] = time.strftime('%a, %d %b %Y %H:%M:%S %z')
        smtp = smtplib.SMTP()
        # 连接SMTP服务器，此处用的126的SMTP服务器
        smtp.connect('smtp.163.com')
        # 用户名密码
        smtp.login('clhiker@163.com', 'cl7155293')
        smtp.sendmail(mail_from, mail_to, msg.as_string())
        smtp.quit()

    def getRandomVerificationCode(self):
        # 正文
        seeds = "1234567890"
        # 定义一个空列表，每次循环，将拿到的值，加入列表
        random_str = []
        # choice函数：每次从seeds拿一个值，加入列表
        for i in range(4):
            random_str.append(random.choice(seeds))
        # 将列表里的值，变成四位字符串
        return "".join(random_str)

