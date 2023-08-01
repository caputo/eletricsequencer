from sequencer import NetworkSequencer
from repository.networkElementRepository import NetworkElementRepository
from dbSequenceExecutor import DBSequenceExecutor

if __name__ == "__main__":
    file_path = 'data.csv'
    collection_name = 'eletricalAsset'
    mongodb_uri = 'mongodb://localhost:27017/'
    database_name = 'sequencia'
    
    DBSequenceExecutor().executeMongoDB('BRBBB-FC');  

    

    