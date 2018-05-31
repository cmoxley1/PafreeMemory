import smtplib
import time
import paramiko
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re
import logging
import csv
import arrow
from configparser import ConfigParser

def email_send(alert1,alert2):	
    from_addr = ''
    to_addr = ['','','']
    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = ", ".join(to_addr)
    msg['Subject'] = fw
    body = "%s    %s" %(alert1,alert2)
    msg.attach(MIMEText(body, 'plain'))
    text55 = msg.as_string()
    server = smtplib.SMTP('smtp.stuff.com', 25)
    server.sendmail("auto@stuff.com",to_addr, text55 )
    server.quit()
    logging.info('Email Sent for ' + fw1 +" "+result1) #Logging

LOG_FILENAME = ''
logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO,format='%(asctime)s %(levelname)-8s %(message)s')
if __name__ == '__main__':
    logging.info('**************Script started****************')#Logging
port = "22"
config = ConfigParser()
config.read('.\config.ini')
username = config.get('auth','username')
password = config.get('auth', 'password')
cmd = "debug dataplane pool statistics | match chunks"
exit = "exit"
firewalls = ['','']
nv = arrow.now()
date = nv.format('MM-DD-YYYY HH:mm:ss')
    #SSH connection
for fw in firewalls:
        logging.info('**************For Statement started****************') #Logging
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(fw ,port,username= username,password=password)
        logging.info('SSH connection started on ' + fw) #Logging
        remotecon = ssh.invoke_shell()
        logging.info('Shell opened on ' + fw) #Logging
        remotecon.send(""+cmd+"\n")
        logging.info('debug cmd ran')#Logging
        time.sleep(2)
        resp = remotecon.recv(1500)
        test1 = str(resp)
        remotecon.send(exit+"\n")
        time.sleep(4)
        ssh.close()
        time.sleep(2)
        logging.info('SSH connection closed on ' + fw)#Logging
        #REGEX begins
        test2 = re.search(r'(free\schunks\s\d+)', test1)
        logL = test2.group()
        logging.info('Current level on ' + fw +" "+logL)  #Logging

        if fw == '':
            fw1 = ''
            logging.info('Running If statement on ' + fw1) #Logging 
            result1 = test2.group()
            edit1 = result1.replace('free chunks ',"")
            output = [ date,edit1]
            logging.info('Write to CSV')#Logging
            with open('', 'a', newline='') as csv1:
                writer = csv.writer(csv1,delimiter=',')
                writer.writerow(output)
                csv1.close
                logging.info('Closing CSV')#Logging                 
            if int(edit1) <= 50:
                logging.info('Compare Values ending ' + fw1) #Logging 
                alert1 = ("Alert! " + fw1 + " is below 300")
                alert2 = ("Currently at " + edit1)
                #Send email with results
                email_send(alert1,alert2)
        else:
            fw2= ''
            logging.info('Running Else statement on ' + fw2) #Logging
            result2 = test2.group()
            edit2 = result2.replace('free chunks ',"")
            output = [ date,edit2]
            logging.info('Write to CSV')#Logging
            with open('', 'a', newline='') as csv2:
                writer = csv.writer(csv2,delimiter=',')
                writer.writerow(output)
                csv2.close
                logging.info('Closing CSV')#Logging
            if int(edit2) <= 50:
                logging.info('Compare Values ending ' + fw2) #Logging
                alert1 = ("Alert! " + fw2 + " is below 300")
                alert2 = ("Currently at " + edit2)
                #Send email with results
                email_send(alert1,alert2)
logging.info('End of Script') #Logging                  
