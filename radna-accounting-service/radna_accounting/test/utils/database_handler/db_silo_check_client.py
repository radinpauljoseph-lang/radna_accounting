from abc import ABC, abstractmethod

class DbSiloCheckClient(ABC):

    def __init__(self, creds: dict = None):
        self.credentials = creds
        self.engine = None
        self.command = None
        self.data = None
        self.result = None

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def setCommand(self):
        pass

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def store(self):
        pass

    @abstractmethod
    def getData(self):
        pass

