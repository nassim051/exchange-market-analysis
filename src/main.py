import src.exchange.gateio.Analyse.GateioAnalystMan as GateioAnalystMan
import src.exchange.lbank.analyse.LBankAnalystMan as LBankAnalystMan
import src.exchange.mexc.Analyse.MexcAnalystMan as MexcAnalystMan
from src.exchange.binance.Analyse import VolumeChangeAlert_AllPairs,VolumeChangeAlert_OnePair,WebSocketVolumeChangeAlert
import src.exchange.lbank.analyse.LBankWaveAnalyzer as LBankWaveAnalyzer
import src.exchange.gateio.Analyse.GateioWaveAnalyzer as GateioWaveAnalyzer
import src.exchange.mexc.Analyse.MexcWaveAnalyzer as MexcWaveAnalyzer
import src.exchange.binance.Analyse.BinanceWaveAnalyzer as BinanceWaveAnalyzer
import src.exchange.bitmart.Analyse.BitMartAnalystMan as BitMartAnalystMan
import src.exchange.bitmart.Analyse.BitMartWaveAnalyzer as BitMartWaveAnalyzer
import  src.Telegram.Telegram as Telegram
import src.db.DbManager as DbManager
import src.exchange.Xt.Analyse.XtAnalystMan as XtAnalystMan
import src.exchange.Xt.Analyse.XtWaveAnalyzer as XtWaveAnalyzer

import sys
TIME_FRAMES = [
    'minute5', 'minute15', 'minute30', 'hour1', 'hour4', 'hour8', 'hour12', 'day1', 'week1', 'month1'
]

def getWaveMinimumAmplitude():
    while True:
        answer = input('Enter the minimum wave amplitude (minimum to maximum amp): ')
        try:
            answer = float(answer)
            return answer
        except ValueError:
            print("Please enter a number")

def getPeriode():
    while True:
        answer = input('Enter the period of moving average (must be an integer): ')
        try:
            answer = int(answer)
            return answer
        except ValueError:
            print("Please enter an integer number")

def getTimeFrame():
    while True:
        answer = input("Choose a time frame: ('minute5', 'minute15', 'minute30', 'hour1', 'hour4', 'hour8', 'hour12', 'day1', 'week1', 'month1'): ")
        if answer not in TIME_FRAMES:
            print('Enter the correct timeframe.')
            continue
        else:
            break
    return answer

def getNbProcess():
    while True:
        answer = input('Enter the number of processes (must be equal to or lower than your processor cores): ')
        try:
            answer = int(answer)
            return answer
        except ValueError:
            print("Please enter an integer number")

def getNbThreads():
    while True:
        answer = input('Enter the number of threads: ')
        try:
            answer = int(answer)
            return answer
        except ValueError:
            print("Please enter an integer number")

def showOptions():
    while True:
        print("Count volume (v)")
        print("Count waves (w)")
        answer = input('Enter your choice (v/w): ')
        if answer not in {'v', 'w'}:
            print('Invalid entry, please retry.')
            continue
        return answer
def renitialiseVolumeTables():
        dbManager=DbManager.DbManager()
        dbManager.renitialise("pair")
        dbManager.renitialise("pairWithLiquidity")
        dbManager.renitialise("volume4h")
def newResearch():
    while True:
            print("New research (n)")
            print("Pursue curlrent research (p)")
            answer = input('Enter your choice (n/p)')
            if answer not in {'p', 'n'}:
                print('Invalid entry, please retry.')
            else:
                break
    if answer=='n':
        return True
    else:
        return False
def searchInXt():
    option = showOptions()
    if option == 'v':
        nbProcess = getNbProcess()
        xt = XtAnalystMan.XtAnalystMan(nbProcess=nbProcess)
        lunchNewResearch = newResearch()
        if lunchNewResearch:
            renitialiseVolumeTables()
            xt.updatePairs()
            xt.findTokenWithGap()
        xt.countVolume(240, 60, True)
        Telegram.Telegram('Database').send_file()

    elif option == 'w':
        nbProcess = getNbProcess()
        nbThreads = getNbThreads()
        waveAmplitude = getWaveMinimumAmplitude()
        timeFrame = getTimeFrame()
        nbHours = getNbHours()
        period = getPeriode()
        XtWaveAnalyzer.XtWaveAnalyzer(
            nbHour=nbHours,
            period=period,
            numProcess=nbProcess,
            numOfThreads=nbThreads,
            waveVolatility=waveAmplitude,
            timeFrame=timeFrame
        ).run()

def searchInBitMart():
    option = showOptions()
    if option == 'v':
        nbProcess = getNbProcess()
        bitmart = BitMartAnalystMan.BitMartAnalystMan(nbProcess=nbProcess)
        lunchNewResearch = newResearch()
        if lunchNewResearch:
            renitialiseVolumeTables()
            bitmart.updatePairs()
            bitmart.findTokenWithGap()
        bitmart.countVolume(240, 60, True)
        Telegram.Telegram('Database').send_file()

    elif option == 'w':
        nbProcess = getNbProcess()
        nbThreads = getNbThreads()
        waveAmplitude = getWaveMinimumAmplitude()
        timeFrame = getTimeFrame()
        nbHours = getNbHours()
        period = getPeriode()
        BitMartWaveAnalyzer.BitMartWaveAnalyzer(
            nbHour=nbHours,
            period=period,
            numProcess=nbProcess,
            numOfThreads=nbThreads,
            waveVolatility=waveAmplitude,
            timeFrame=timeFrame
        ).run()


def searchInLBank():
    option=showOptions()
    if option=='v':
        nbProcess=getNbProcess()
        lbank=LBankAnalystMan.LBankAnalystMan(nbProcess=nbProcess)
        lunchNewResearch=newResearch()
        if lunchNewResearch:
            renitialiseVolumeTables()
            lbank.updatePairs()
            lbank.findTokenWithGap()
        lbank.countVolume(240,60,True)
        Telegram.Telegram('Database').send_file()
    elif option=='w':
        nbProcess=getNbProcess()
        nbThreads=getNbThreads()
        waveAmplitude=getWaveMinimumAmplitude()
        timeFrame=getTimeFrame()
        nbHours=getNbHours()
        period=getPeriode()
        LBankWaveAnalyzer.LBankWaveAnalyzer(nbHour=nbHours,period=period,numProcess=nbProcess,numOfThreads=nbThreads,waveVolatility=waveAmplitude,timeFrame=timeFrame).run()

def searchInGate():
    option=showOptions()
    if option=='v':
        nbProcess=getNbProcess()
        gateio=GateioAnalystMan.GateioAnalystMan(nbProcess=nbProcess)
        lunchNewResearch=newResearch()
        if lunchNewResearch:
            renitialiseVolumeTables()
            gateio.updatePairs()
            gateio.findTokenWithGap()
        gateio.countVolume(240,60,True)
        Telegram.Telegram('Database').send_file()
    elif option=='w':
            nbProcess=getNbProcess()
            nbThreads=getNbThreads()
            waveAmplitude=getWaveMinimumAmplitude()
            timeFrame=getTimeFrame()
            nbHours=getNbHours()
            period=getPeriode()
            GateioWaveAnalyzer.GateioWaveAnalyzer(nbHour=nbHours,period=period,numProcess=nbProcess,numOfThreads=nbThreads,waveVolatility=waveAmplitude,timeFrame=timeFrame).run()

def searchInMexc():
    option=showOptions()
    if option=='v':
        nbProcess=getNbProcess()
        mexc=MexcAnalystMan.MexcAnalystMan(nbProcess=nbProcess)
        lunchNewResearch=newResearch()
        if lunchNewResearch:
            renitialiseVolumeTables()
            mexc.updatePairs()
            mexc.findTokenWithGap()
        mexc.countVolume(240,60,True)    
        Telegram.Telegram('Database').send_file()
    elif option=='w':
            nbProcess=getNbProcess()
            nbThreads=getNbThreads()
            waveAmplitude=getWaveMinimumAmplitude()
            timeFrame=getTimeFrame()
            nbHours=getNbHours()
            period=getPeriode()
            MexcWaveAnalyzer.MexcWaveAnalyzer(nbHour=nbHours,period=period,numProcess=nbProcess,numOfThreads=nbThreads,waveVolatility=waveAmplitude,timeFrame=timeFrame).run()

def showBinanceOptions():
    while True:
        print("Search for liquidity (l)")
        print("Count waves (w)")
        answer = input('Enter your choice (l/w): ')
        if answer not in {'l', 'w'}:
            print('Invalid entry, please retry.')
            continue
        return answer

def searchInBinance():
    option=showBinanceOptions()
    if option=='l':
        while True:
            print("Search in all pairs (a)")
            print("Search in a specific pair (s)")
            answer = input('Enter your choice (a/s): ')
            if answer not in {'a', 's'}:
                print('Invalid entry, please retry.')
                continue
            else:
                break
        if answer == 'a':
            nbprocess=getNbProcess()
            nbThreads=getNbThreads()
            alerts = VolumeChangeAlert_AllPairs.VolumeChangeAlert_AllPairs(interval=20000,numOfThreads=nbThreads,numProcess=nbprocess)
            nbHours = getNbHours()
            alerts.run(nbHours=nbHours)
        elif answer == 's':
            searchInBinance_onePair()
    elif option=='w':
            nbProcess=getNbProcess()
            nbThreads=getNbThreads()
            waveAmplitude=getWaveMinimumAmplitude()
            timeFrame=getTimeFrame()
            nbHours=getNbHours()
            period=getPeriode()
            BinanceWaveAnalyzer.BinanceWaveAnalyzer(nbHour=nbHours,period=period,numProcess=nbProcess,numOfThreads=nbThreads,waveVolatility=waveAmplitude,timeFrame=timeFrame).run()
    
def searchInBinance_onePair():
    while True:
        print("Dynamic search with websocket (w)")
        print("Search in past data (p)")
        answer = input('Enter your choice (w/p): ')
        if answer not in {'w', 'p'}:
            print('Invalid entry, please retry.')
            continue
        else:
            break        
    
    if answer == 'p':
        alert = VolumeChangeAlert_OnePair.VolumeChangeAlert_OnePair(interval=20000)
        nbHours = getNbHours()
        symbol = getSymbol()
        alert.run(nbHours=nbHours, symbol=symbol)
    elif answer == 'w':
        symbol = getSymbol()
        alert = WebSocketVolumeChangeAlert.WebSocketVolumeChangeAlert(symbol=symbol, interval=20000)
        alert.run()
        
def getSymbol():
    while True:
        symbol = input("Enter the symbol: ")
        if isinstance(symbol, str):
            return symbol
        else: 
            print("Please enter a string")
     
def getNbHours():
    while True:
        nbHours = input("Please enter the number of candle back from the current time to start analyzing data: ")
        try:
            nbHours = int(nbHours)
            return nbHours
        except ValueError:
            print("Please enter an integer number")
if __name__=='__main__':

    while True:
        print("Search in LBank tap (l)")
        print("Search in GateIo tap (g)")
        print("Search in MEXC tap (m)")
        print("Search in Binance tap (b)")
        print("Search in BitMart tap (bm)")
        print("Search in XT.com tap (xt)")

        answer = input('Tap your answer\n')
        if answer not in {'l', 'g', 'm', 'b', 'bm','xt'}:
            print('Invalid entry, please retry.')
            continue
        else:
            break

    if answer == "l":
        searchInLBank()
    elif answer == "g":
        searchInGate()
    elif answer == "m":
        searchInMexc()
    elif answer == "b":
        searchInBinance()
    elif answer == "bm":
        searchInBitMart()
    elif answer == "xt":
        searchInXt()

