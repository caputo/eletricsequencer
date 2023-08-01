from model.networkElement import NetworkElement
class ConvertToModel:
    def NetworkElementToDict(list):
        return map(lambda e: e.__dict__,list)
    
    def DictToListNetworkElement(dict):
        return list(map(ConvertToModel.RowToNetworkElement,dict))   

    def NetworkElementoToDictList(list):
        return list(map(lambda e: e.__dict__),list)

    def RowToNetworkElement(row):            
        return NetworkElement(
            row['TABLE'],
            row['CODE'],
            row['PAC1'],
            row['PAC2'],
            row['VOLTAGE'],
            row['PHASES'],
            row['SEC_PHASES'],
            row['VOLTAGE_TYPE'],
            row['FEEDER'],
            row['TRANSFORMER_TYPE']
            #row['X1'],
            #row['Y1'],
            #row['X2'],
            #row['Y2']
        )
    def DicToElement(element):
        e = NetworkElement()
        for key, value in element.items():
            setattr(e, key, value)
        return e
    
    def DictionaryListToListElement(listItems):
        return list(map(ConvertToModel.DicToElement,listItems))        
    
