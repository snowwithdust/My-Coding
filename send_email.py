#coding:utf -8
 
import smtplib #smtp服务器
from email.mime.text import MIMEText #邮件文本
 
#邮件构建
 
subject = "滴滴答答"#邮件标题
sender = "13610603075@163.com"#发送方
content = "新年快乐！"
recver = "2542871002@qq.com"#接收方
password = 'FNTSRJFVKASVDRWQ'
message = MIMEText(content,"plain","utf-8")
#content 发送内容     "plain"文本格式   utf-8 编码格式
 
message['Subject'] = subject #邮件标题
message['To'] = recver #收件人
message['From'] = sender #发件人
 
smtp = smtplib.SMTP_SSL("smtp.163.com",465) #实例化smtp服务器
smtp.login(sender,password)#发件人登录
smtp.sendmail(sender,[recver],message.as_string()) #as_string 对 message 的消息进行了封装
smtp.close()
print("发送成功")
