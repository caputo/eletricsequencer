from repository.networkElementRepository import NetworkElementRepository
from sequencer import NetworkSequencer
from utils.logger import Logger

class DBSequenceExecutor:
    
    def __init__(self):
        self.mongodb_uri = 'mongodb://localhost:27017/'
        self.database_name = 'sequencia'
        self.LoggerHandler = Logger()
    
    def executeMongoDB(self,feeder):
        self.LoggerHandler.info("Started sequence through mongo DB ")
        repository = NetworkElementRepository(self.mongodb_uri, self.database_name)
        sequencer = NetworkSequencer(self.LoggerHandler)
        elements =  repository.getAssets(feeder,True)
        sequencer.execute(feeder, elements, True, False)
        self.LoggerHandler.info("Saving results.... ")
        repository.save(elements)
        self.LoggerHandler.info("End saving ")     