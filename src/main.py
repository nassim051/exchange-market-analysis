import src.exchange.gateio.Analyse.GateioAnalystMan as GateioAnalystMan
import src.exchange.lbank.analyse.LBankAnalystMan as LBankAnalystMan
import  multiprocessing, time

def searchInLBank():
    lbank=LBankAnalystMan.LBankAnalystMan()

    lbank.findTokenWithGap()
    lbank.countVolume(240,60,True)
def searchInGate():
    gateio=GateioAnalystMan.GateioAnalystMan()
    gateio.countVolume(240,60,True)
def searchVolume():
    #lbank=LBankAnalystMan.LBankAnalystMan()
    #lbank.updatePairs()
    #lbank.findTokenWithGap()
    #gateio=GateioAnalystMan.GateioAnalystMan()
    #gateio.updatePairs()
    #gateio.findTokenWithGap()
    processes=[]
    process=multiprocessing.Process(target=searchInLBank, args=())
    processes.append(process)
    process.start()
    time.sleep(1)
    process=multiprocessing.Process(target=searchInGate, args=())
    processes.append(process)
    process.start()
    for process in processes:
        process.join()
if __name__=='__main__':
    searchInLBank()
    #gateio.countVolume(240,60,True)
