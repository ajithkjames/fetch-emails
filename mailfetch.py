import imaplib
import email
import os
import io

imaplib.IMAP4.debug = imaplib.IMAP4_SSL.debug = 1
 
username,passwd = ('d9605408050@gmail.com','password')
 
con = imaplib.IMAP4_SSL('imap.gmail.com',993)
con.login(username, passwd)
con.select('INBOX')
typ, data = con.search(None, '(UNSEEN)')
c1 = 0
data_list = []
unread_msg_nums = data[0].split()
for num in unread_msg_nums:
    data_dict = {}
    typ, data = con.fetch(num, '(BODY.PEEK[])')
    c1 +=1
    text = data[0][1]
    msg = email.message_from_string(text)
    data_dict['mail_to'] = msg['To']
    data_dict['mail_subject'] = msg['Subject']
    data_dict['mail_from'] = email.utils.parseaddr(msg['From'])
    data_dict['body'] = msg.get_payload()
    data_list.append(data_dict)
    
    for part in msg.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        filename = part.get_filename()
        data = part.get_payload(decode=True)
        if not data or not filename:
            continue
        # print filename
        with io.FileIO(filename, "w") as file:
            file.write(data)
    msg_uid = con.fetch(num, 'UID')[1][0].split()[2].strip('()')
    con.uid('store', msg_uid, '+FLAGS', '(\\Seen)')
print(data_list)
con.close()
con.logout()