from abc import ABC, abstractmethod

class IMarketMan(ABC):
    @abstractmethod
    def getTicker(self, **d):
        pass

    @abstractmethod 
    def getDepth(self, **d):
        pass
    @abstractmethod
    def getIncrDepth(self, **d):
        pass

    @abstractmethod
    def getTrades(self, **d):
        pass

    @abstractmethod
    def getKline(self, **d):
        pass

