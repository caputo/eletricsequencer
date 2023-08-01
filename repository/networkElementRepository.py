from repository.repository import Repository 
from repository.eletricalAssetRepository import EletricalAssetRepository

class NetworkElementRepository(Repository):
    def __init__(self,db_url, db_name):
        super().__init__(db_url, db_name, 'networkElements')   
        self.assetRepo = EletricalAssetRepository(db_url, db_name)
    
    def getAssets(self, feeder, disregardNeutral): 
        return self.assetRepo.loadAsNetworkElement(feeder)
    
    def deleteFeeder(self, feeder):
        super().delete_many({"feeder":feeder})
    
    def save(self, elements):
        super().bulk_insert(list(map(lambda e: e.__dict__, elements)))
