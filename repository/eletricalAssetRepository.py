from repository.repository import Repository 
from model.eletricalAsset import EletricalAsset
from utils.convertToModel import ConvertToModel
from model.networkElement import NetworkElement

class EletricalAssetRepository(Repository):
    def __init__(self,db_url, db_name):
        super().__init__(db_url, db_name, 'eletricalAsset')   

    def loadAsNetworkElement(self, feeder):
        elements = super().find_many({"FEEDER": feeder})                
        return  ConvertToModel.DictToListNetworkElement(elements)    

if __name__ == "__main__":
    mongodb_uri = 'mongodb://localhost:27017/'
    database_name = 'sequencia'
    rep = EletricalAssetRepository(mongodb_uri,database_name)
    eles = rep.loadAsNetworkElement('JCK01X5')
    print(len(eles))