import requests
class Telegram:
    def __init__(self,exchange):
        self.botUserName:Final='1679040280'
        if exchange=='LBank':
            self.token: Final='6782346013:AAEGp1yyfrDOahxFrFxfGAtpz-xd_tQ9Jb4'
        elif exchange=='gateio':
            self.token: Final='6864729802:AAF44BBdieBlGdMprIKXkxdNV-51QBm7abc'            

    def send_message(self, text):
        url = f"https://api.telegram.org/bot{self.token}/sendMessage?chat_id={self.botUserName}&text={text}"
        requests.get(url).json() # this sends the message        
        return
    
