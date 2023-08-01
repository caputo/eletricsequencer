class EletricalAsset:
    def __init__(self,table,code,pac1,pac2,voltage,phases,sec_phases,voltagetype,feeder,transformerType):
        self.table = table
        self.code = code
        self.pac1 = pac1
        self.pac2 = pac2
        self.voltage = voltage
        self.phases = phases
        self.sec_phases = sec_phases
        self.voltagetype = voltagetype
        self.feeder = feeder
        self.transformerType = transformerType