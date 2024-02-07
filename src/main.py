import src.exchange.gateio.Analyse.GateioAnalystMan as GateioAnalystMan
import src.exchange.lbank.analyse.LBankAnalystMan as LBankAnalystMan
import src.exchange.mexc.Analyse.MexcAnalystMan as MexcAnalystMan
import  src.Telegram.Telegram as Telegram
import sys
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
def searchInMexc():
    mexc=MexcAnalystMan.MexcAnalystMan()
    mexc.updatePairs()
    mexc.findTokenWithGap()
    mexc.countVolume(240,60,True)    
    
if __name__=='__main__':
    Telegram.Telegram('Database').send_file()

    print("To search in LBank tap 'l'")
    print("To search in GateIo tap 'g'")
    print("To search in GateIo tap 'm'")

    while True:
        answer=input('Tap your answer\n')
        if answer!='l' and answer!='g' and answer!='m':
            print('False entry, retry please')
        else:
            break
    
    if answer == "l":
        searchInLBank()
    elif answer == "g":
        searchInGate()
    elif answer == "m":
        searchInMexc()

    Telegram.Telegram('Database').send_file()
