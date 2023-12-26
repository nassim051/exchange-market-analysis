import pytest, os, sys
import src.Telegram.Telegram as Telegram
import zipfile, os, requests
bot_token = "6782346013:AAEGp1yyfrDOahxFrFxfGAtpz-xd_tQ9Jb4"
bot_chatId = "1679040280"



#@pytest.mark.skip
def test_sendingMessage():
    telegram=Telegram.Telegram(channel='gateio')
    telegram.send_message(text='hello brooooooooooooooaaaaaaahhhhh')

@pytest.mark.skip
def test_zipAndUnzip():
    os.remove("testZip")
    return
    #text=zipfile.ZipFile("testZip","w",compression=zipfile.ZIP_DEFLATED)
    #text.write('src/db/bot.db',arcname=os.path.basename('src/db/bot.db'),compress_type=zipfile.ZIP_DEFLATED)
    #text.close()
    zipfile.ZipFile("testZip","r").extractall()
    a =open('testZip','rb')
    send_document = 'https://api.telegram.org/bot' + bot_token +'/sendDocument?'
    data = {
    'chat_id': bot_chatId,
    'parse_mode':'HTML',
    'caption':'This is my file'
    }

    r = requests.post(send_document, data=data, files={'document': a},stream=True)
    print(r.json())

