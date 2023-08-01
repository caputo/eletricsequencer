import math
import concurrent.futures
from utils.logger import Logger
import json


class NetworkSequencer:
    directFlow = "1->2"
    reverseFlow = "2->1"
    ThreeSquareRoot = math.sqrt(3)    
    pac1Elements={}
    pac2Elements={}

    def __init__(self, logger):        
        self.elements = None
        self.LoggerHandler = logger
        self.elementsPrimaryNetwork = None
        self.elementsSecondaryNetwork = None
        self.elementsOriginal = None
        with open('config.json', 'r') as arquivo:            
            self._config = json.load(arquivo)      

    def execute(self, feeder, elements, removeNeutral=False, articulated=False, voltage=""):        

        self.loadElements(feeder, elements, removeNeutral)

        self.LoggerHandler.info(f"Total elements: {len(self.elements)}")
        self.LoggerHandler.info(f"Primary network: {len(self.elementsPrimaryNetwork)}")
        self.LoggerHandler.info(f"Secundary network: {len(self.elementsSecondaryNetwork)}")

        if not voltage:
            if articulated:
                self.execPrimaryNetwork(self.elementsPrimaryNetwork)                
                joinedElements = self.elementsSecondaryNetwork + list(filter(lambda e: e.Table.lower() == self._config['Tables']["TRAFO"].lower(), self.elementsPrimaryNetwork))
                self.execSecondaryNetwork(joinedElements)
            else:                
                self.execPrimaryNetwork(self.elementsPrimaryNetwork + self.elementsSecondaryNetwork)
        elif voltage.upper() == "MT":
            self.execPrimaryNetwork(self.elementsPrimaryNetwork)
        elif voltage.upper() == "BT":
            self.execPrimaryNetwork(self.elementsSecondaryNetwork)       
        
        self.LoggerHandler.info(f"Process finished. Conected: {len([e for e in self.elements if e.conected()])} - Disconecteds: {len([e for e in self.elements if not e.conected()])}")        
        return self.elements    
   

    def execSecondaryNetwork(self, elements):
        transformerUpstream = True
        self.LoggerHandler.info("Executing secondary network")
        self.elements = elements
        self.loadPacDict()
        for transformer in sorted(filter(lambda e: e.Table.lower() == self._config['Tables']["TRAFO"].lower() and e.conected(), self.elementsPrimaryNetwork), key=lambda s: s.order):
            secondPac = transformer.Pac1 if transformer.ReverseFlow() else transformer.Pac2

            conectedElements = self.sequenceNetwork(transformer, secondPac, transformer.Order, transformerUpstream, False) + \
                self.sequenceNetwork(transformer, secondPac, transformer.Ordem, transformerUpstream, True)

            while conectedElements:                
                conetedDownstream = []
                conetedDownstream += self.pacSequence(conectedElements, transformerUpstream, False)
                conetedDownstream += self.pacSequence(conectedElements, transformerUpstream, True)
                conectedElements = conetedDownstream

    def execPrimaryNetwork(self, elements):
        self.LoggerHandler.info("Executing primary network")
        feeder = next((e for e in self.elements if e.table.lower() == self._config['Tables']["ALIMENTADOR"].lower()), None)
        feeder.order = 1
        feeder.flowDirection = self.directFlow
        feeder.parentVoltage = feeder.voltage
        feeder.phaseVoltage = round(feeder.parentVoltage / self.ThreeSquareRoot, 5)
        
        self.elements = elements
        self.loadPacDict()
        conectedElements = self.sequenceNetwork(feeder, feeder.pac1, 1, False, False) + \
            self.sequenceNetwork(feeder, feeder.pac1, 1, False, True)

        while conectedElements:
            conectedDown = []
            conectedDown += self.pacSequence(conectedElements, True, False)
            conectedDown += self.pacSequence(conectedElements, True, True)
            conectedElements = conectedDown

    def pacSequence(self, conectedElements, upTransformer, isReverse):
        concConected = []
        for element in conectedElements:
            pacJusante = element.pac2 if element.flowDirection == self.directFlow else element.pac1
            if pacJusante:
                concConected += self.sequenceNetwork(element, pacJusante, element.order, upTransformer, isReverse)

        return concConected
    
    def loadPacDict(self):
        self.pac1Elements = {} 
        self.pac2Elements = {}  
        self.pacsConnected = {}      
        for ele in self.elements:
            self.pac1Elements.setdefault(ele.pac1,[]).append(ele)
            if ele.pac2:
                self.pac2Elements.setdefault(ele.pac2,[]).append(ele)

    def loadElements(self,feeder,elements, removeNeutral):                
        self.elements = [e for e in elements if e.feeder == feeder and (removeNeutral and e.phases != 'N')]
        self.elementsOriginal = self.elements        
        transformersList = self.getTransformers()
        self.transformers = {}
        for t in transformersList:
            self.transformers[t.code] = t            


    def calculateElementPhaseVoltage(self, voltagePai, tipoTrafo, tipovoltage):
        phaseVoltage = round(voltagePai / self.ThreeSquareRoot, 5)

        if tipovoltage == "BT":
            if tipoTrafo == "M":
                phaseVoltage = round(voltagePai, 5)
            if tipoTrafo in ["MT", "DA", "DF"]:
                phaseVoltage = round(voltagePai / 2, 5)

        return phaseVoltage

    def calculatePhaseVoltage(self, element):
        try:
            if element.conected():
                if self.has_value(element.transformer):
                    transformer = self.transformers[element.transformer]
                    if transformer is not None:                    
                        element.phaseVoltage = self.calculateElementPhaseVoltage(element.parentVoltage, transformer.transformerType, element.voltageType)
                        return
                
                element.phaseVoltage = round(element.parentVoltage / self.ThreeSquareRoot, 5)                                        
        except Exception as ex:
            self.LoggerHandler.Error(ex)
            raise

    def getTransformers(self):
        return [e for e in self.elementsOriginal if e.table == self._config['Tables']['TRAFO']]

    def sequenceDownstream(self, downstreamElement:list, order, flowDirection, parentCode, parentVoltage, parentType, parentPhases, upTransformer, upSwitcher, isUpTransformer=False):        
        if len(downstreamElement) > 0:
            with concurrent.futures.ThreadPoolExecutor(max_workers=len(downstreamElement)) as executor:                        
                results = executor.map(lambda e: self.markElement(e,order, flowDirection, parentCode, parentVoltage, parentType, parentPhases, upTransformer, upSwitcher), downstreamElement)
            return list(filter(None, results))
        return []
    
    def markElement(self,downElement,order, flowDirection, parentCode, parentVoltage, parentType, parentPhases, upTransformer, upSwitcher):
        downElement.setParent({"order":order, "flowDirection":flowDirection, "code":parentCode,"table":parentType,"voltage":parentVoltage, "phases":parentPhases, "transformer":upTransformer,"switcher":upSwitcher})
        pacJusante = downElement.pac2 if downElement.flowDirection == self.directFlow else downElement.pac1
        self.calculatePhaseVoltage(downElement)
        return downElement if self.has_value(pacJusante) else None

    def sequenceNetwork(self, currentElement, pac, order, isUpTransformer=False, isReverse=False):
        if self.is_terminal(currentElement) or pac is None or str(pac).strip() == "0":
            return []               

        currentElementSwitcher = currentElement.switcher        
        if currentElement.table == self._config['Tables']["SECCIONADOR_MT"] or currentElement.table == self._config['Tables']["SECCIONADOR_BT"]:
            if currentElement.switcher != currentElement.code:
                currentElementSwitcher = currentElement.code

        if isUpTransformer and currentElement.table == self._config['Tables']["TRAFO"]:
            currentElement.transformer = currentElement.code

        elementsInPac = []        
        elementsInPac = self.pac2Elements.get(pac,[]) if isReverse else self.pac1Elements.get(pac,[])

        conectedsAlready = [e for e in elementsInPac if e.conected() and not (e.table == self._config['Tables']["TRAFO"] and currentElement.table == self._config['Tables']["TRAFO"]) and e.code != currentElement.transformer]
        
        conectedPac = [e for e in elementsInPac if (not e.conected()) and (self.is_terminal(e) or ((not self.is_terminal(e)) and self.has_value(e.pac1) and self.has_value(e.pac2)))]        

        currentElement.qtdeElementsDownstream = len(conectedPac)               

        # ** TRACE BACKS (LOOPS) **
        if len(conectedsAlready) > 1:            
            if any(e.pac1 != currentElement.pac1 and e.pac2 != currentElement.pac2 for e in conectedsAlready):
                currentElement.MarkAsALoop()
            
            conectedTransformers = [e for e in conectedsAlready if e.table == self._config['Tables']["TRAFO"]]
            for trafo in conectedTransformers:
                trafo.reticulatedTransformer = currentElement.transformer
        markedElements = self.sequenceDownstream(conectedPac, order, self.reverseFlow if isReverse else self.directFlow, currentElement.code, currentElement.voltage if currentElement.voltage > 0 else currentElement.parentVoltage, currentElement.table, currentElement.secPhases if self.has_value(currentElement.secPhases) else currentElement.phases, currentElement.transformer, currentElementSwitcher, isUpTransformer)
        return markedElements
    
    def has_value(self, value):
        if value is None:
            return False

        if isinstance(value,(int,float)) and math.isnan(value):
            return False
        
        if isinstance(value,(str)) and (value == "" or len(value) ==0):
            return False
        
        return True
    
    def is_terminal(self, element):
        terminal_tables = [
            self._config['Tables']["CARGA_BAIXA_TENSAO"],
            self._config['Tables']["CARGA_MEDIA_TENSAO"],
            self._config['Tables']["CARGA_ILUMINACAO_PUBLICA"],
            self._config['Tables']["UNIDADE_COMPENSADORA_BAIXA_TENSAO"],
            self._config['Tables']["UNIDADE_COMPENSADORA_MEDIA_TENSAO"]
        ]
        return element.table in terminal_tables
