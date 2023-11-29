from abc import ABC, abstractmethod

class IBasicDataMan(ABC):
    @abstractmethod
    def getcurrencyPairs(self):
        pass

    @abstractmethod
    def getAccuracyInfo(self):
        pass

    @abstractmethod
    def getRatio(self, **d):
        pass

    @abstractmethod
    def getWithdrawConf(self, **d):
        pass

    @abstractmethod
    def getTimestamp(self):
        pass

