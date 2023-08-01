import geojson,pandas
from typing import List
from model.networkElement import NetworkElement

class ConvertToGeoJSON:

    def convert(self, listItems,config):
        self._config = config
        feeder = list(filter(lambda e: e.table == config['Tables']['ALIMENTADOR'], listItems))
        print(feeder)
        for e in feeder:
            self.searchPac(e,listItems)
        ctmt_layer = list(map(self.createPointFeature,feeder))
        print(listItems.__str__())
        untrd = list(filter(lambda e: e.table == config['Tables']['TRAFO'], listItems))
        untrd_layer = list(map(self.createPointFeature,untrd))

        ssdmt = list(filter(lambda e: e.table == config['Tables']['SEGMENTO_MT'], listItems))
        ssdmt_layer = list(map(self.createLineFeature,ssdmt))

        ssdbt = list(filter(lambda e: e.table == config['Tables']['SEGMENTO_BT'], listItems))
        ssdbt_layer = list(map(self.createLineFeature, ssdbt))

        unsemt = list(filter(lambda e: e.table == config['Tables']['SECCIONADOR_MT'], listItems))
        unsemt_layer = list(map(self.createPointFeature,unsemt))

        reg = list(filter(lambda e: e.table == config['Tables']['REGULADOR'], listItems))
        reg_layer = list(map(self.createPointFeature,reg))

        unsebt = list(filter(lambda e: e.table == config['Tables']['SECCIONADOR_BT'], listItems))
        unsebt_layer = list(map(self.createPointFeature,unsebt))

        ucrbt = list(filter(lambda e: e.table == config['Tables']['UNIDADE_COMPENSADORA_BAIXA_TENSAO'], listItems))
        ucrbt_layer = list(map(self.createPointFeature,ucrbt))

        ucrmt = list(filter(lambda e: e.table == config['Tables']['UNIDADE_COMPENSADORA_MEDIA_TENSAO'], listItems))
        ucrmt_layer = list(map(self.createPointFeature,ucrmt))

        #Only disconecteds for consumers
        ucbt = list(filter(lambda e: e.order ==0 and e.table == config['Tables']['CARGA_BAIXA_TENSAO'], listItems))
        for e in ucbt:
            self.searchPac(e,listItems)
        ucbt_layer = list(map(self.createPointFeature,ucbt))

        ucmt = list(filter(lambda e:  e.order ==0 and  e.table == config['Tables']['CARGA_MEDIA_TENSAO'], listItems))
        for e in ucmt:
            self.searchPac(e,listItems)
        ucmt_layer = list(map(self.createPointFeature,ucmt))

        pip = list(filter(lambda e:  e.order ==0 and e.table == config['Tables']['CARGA_ILUMINACAO_PUBLICA'], listItems))
        for e in pip:
            self.searchPac(e,listItems)
        pip_layer = list(map(self.createPointFeature,pip))

        ramlig = list(filter(lambda e: e.order ==0 and  e.table == config['Tables']['RAMAL'], listItems))
        for e in ramlig:
            self.searchPac(e,listItems)
        ramlig_layer = list(map(self.createPointFeature,ramlig))

        geojson_data = {            
            "ctmt": {"type": "FeatureCollection", "features": ctmt_layer},
            "ssdmt": {"type": "FeatureCollection", "features": ssdmt_layer},
            "ssdbt": {"type": "FeatureCollection", "features": ssdbt_layer},
            "unsemt": {"type": "FeatureCollection", "features": unsemt_layer},
            "unsebt": {"type": "FeatureCollection", "features": unsebt_layer},
            "ucrmt": {"type": "FeatureCollection", "features": ucrmt_layer},
            "ucrbt": {"type": "FeatureCollection", "features": ucrbt_layer},
            "unsemt": {"type": "FeatureCollection", "features": unsemt_layer},
            "unsebt": {"type": "FeatureCollection", "features": unsebt_layer},
            "unremt": {"type": "FeatureCollection", "features": reg_layer},
            "untrd": {"type": "FeatureCollection", "features": untrd_layer},
            "ucbt": {"type": "FeatureCollection", "features": ucbt_layer},
            "ucmt": {"type": "FeatureCollection", "features": ucmt_layer},
            "pip": {"type": "FeatureCollection", "features": pip_layer},
            "ramlig": {"type": "FeatureCollection", "features": ramlig_layer}
        }        
        return geojson_data

    def searchPac(self,element, searchList:List[NetworkElement]):
        if self.is_terminal(element):
            firstConected = list(filter(lambda x:  x.code != element.code and x.x1 != 0 and x.y1 != 0 and x.order > 0 and ((x.flowDirection == "2->1" and x.pac1==element.pac1) or (x.flowDirection != "2->1" and x.pac2 == element.pac1)),searchList))
            if firstConected:
                element.x1 = firstConected[0].x1
                element.y1 = firstConected[0].y1
        else:
            firstConected = list(filter(lambda x:  x.code != element.code and x.x1 != 0 and x.y1 != 0 and x.order > 0 and ((x.flowDirection == "2->1" and x.pac2==element.pac1) or (x.flowDirection != "2->1" and x.pac1 == element.pac1)),searchList))
            if firstConected:
                element.x1 = firstConected[0].x1
                element.y1 = firstConected[0].y1

        

    def createLineFeature(self, element):
        feature = geojson.Feature(
            geometry=geojson.LineString([(element.x1,element.y1),(element.x2,element.y2)]), 
            properties=element.__dict__
        )
        return feature

    def createPointFeature(self, element):
        feature = geojson.Feature(
            geometry=geojson.Point((element.x1,element.y1)), 
            properties=element.__dict__
        )
        return feature
    
    def is_terminal(self,element):
        terminal_tables = [
            self._config['Tables']["CARGA_BAIXA_TENSAO"],
            self._config['Tables']["CARGA_MEDIA_TENSAO"],
            self._config['Tables']["CARGA_ILUMINACAO_PUBLICA"],
            self._config['Tables']["UNIDADE_COMPENSADORA_BAIXA_TENSAO"],
            self._config['Tables']["UNIDADE_COMPENSADORA_MEDIA_TENSAO"]
        ]
        return element.table in terminal_tables
