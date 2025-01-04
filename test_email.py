import smtplib

email = input("enter email - ")
server = smtplib.SMTP('smtp.gmail.com',587)
server.starttls()
server.login('sp.info.creation@gmail.com','ojfy tjcz sdzm evzn')
server.sendmail('sp.info.creation@gmail.com','{}'.format(email),'Hi well come to sp_creation company')
print("mail send")