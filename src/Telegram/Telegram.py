import requests, zipfile, os
class Telegram:
    def __init__(self,channel):
        self.botUserName='6595500268'
        if channel=='lbank':
            #self.token='6782346013:AAEGp1yyfrDOahxFrFxfGAtpz-xd_tQ9Jb4'
            self.token='6918649252:AAEsR16dA6NUFcT73DKUICTOqaKsrlvDJ54'

        elif channel=='gateio':
            #self.token='6864729802:AAF44BBdieBlGdMprIKXkxdNV-51QBm7abc'
            self.token='6789159808:AAE6w5XsWoJdhpbU26M9-eUIAs4DcmdORSM'

        elif channel=='mexc':
            #self.token='6680399656:AAEG_eVUqtBEcre2V9mpv-8nH79WB3vbCO8'
            self.token='6761479251:AAG-PU2TyWpCpgfYLaDbCzbv_9R7JZqGYkM'

        elif channel=='Database':
            self.botUserName='1679040280'
            self.token="6747769758:AAF9Df4rd3okLXE_RjLPds8zb25nG4o5jjM"    
                

    def send_message(self, text):
        url = f"https://api.telegram.org/bot{self.token}/sendMessage?chat_id={self.botUserName}&text={text}"
        requests.get(url).json() # this sends the message        
        return
    
    def send_file(self): ##it zips the file before sending it
        print("Sending file to telegram")
        text=zipfile.ZipFile("searchResult","w",compression=zipfile.ZIP_DEFLATED)
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
