import src.exchange.gateio.Analyse.GateioAnalystMan as GateioAnalystMan
import src.exchange.lbank.analyse.LBankAnalystMan as LBankAnalystMan
import  src.Telegram.Telegram as Telegram

def searchInLBank():
    lbank=LBankAnalystMan.LBankAnalystMan()
    lbank.updatePairs()
    lbank.findTokenWithGap()
    lbank.countVolume(240,60,True)
def searchInGate():
    gateio=GateioAnalystMan.GateioAnalystMan()
    gateio.updatePairs()
    gateio.findTokenWithGap()
    gateio.countVolume(240,60,True)
    
if __name__=='__main__':
    print("To search in LBank tap 'l'")
    print("To search in GateIo tap 'g'")
    while True:
        answer=input('Tap your answer\n')
        if answer!='l' and answer!='g':
            print('False entry, retry please')
        else:
            break
    
    if answer == "l":
        searchInLBank()
    elif answer == "g":
        searchInGate()
    Telegram.Telegram('Database').send_file()
