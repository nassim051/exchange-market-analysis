import requests, zipfile, os
class Telegram:
    def __init__(self,channel):
        self.botUserName='1679040280'
        if channel=='LBank':
            self.token='6782346013:AAEGp1yyfrDOahxFrFxfGAtpz-xd_tQ9Jb4'
        elif channel=='gateio':
            self.token='6864729802:AAF44BBdieBlGdMprIKXkxdNV-51QBm7abc'
        elif channel=='Database':
            self.token="6703631441:AAEpw1kuglpXm2gHDVdIDFOul7IO4LbPpLg"            

    def send_message(self, text):
        url = f"https://api.telegram.org/bot{self.token}/sendMessage?chat_id={self.botUserName}&text={text}"
        requests.get(url).json() # this sends the message        
        return
    
    def send_file(self): ##it zips the file before sending it
        print("Sending file to telegram")
        text=zipfile.ZipFile("Nassim_searchResult","w",compression=zipfile.ZIP_DEFLATED)
        text.write('src/db/bot.db',arcname=os.path.basename('src/db/bot.db'),compress_type=zipfile.ZIP_DEFLATED)
        text.close()
        a =open('searchResult','rb')
        send_document = 'https://api.telegram.org/bot' + self.token +'/sendDocument?'
        data = {
        'chat_id': self.botUserName,
        'parse_mode':'HTML',
        'caption':'This is my file'
        }
        print("Response: ")
        r = requests.post(send_document, data=data, files={'document': a},stream=True)
        print(r.json())
        os.remove("testZip")
