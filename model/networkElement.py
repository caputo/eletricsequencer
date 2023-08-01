import math
class NetworkElement():     
    def __init__(self,table="",code="",pac1="",pac2="",voltage="",phases:str="",sec_phases="",voltageType="",feeder="", transformerType="",x1=0,y1=0,x2=0,y2=0):        
        self.feeder = feeder
        self.code = code
        self.flowDirection = ""
        self.parentElement = ""
        self.parentType = ""
        self.parentPhases = ""
        self.id = 0
        self.order = 0
        self.pac1 = pac1
        self.pac2 = pac2
        self.qtdeElementsDownstream = 0
        self.table = table
        self.voltage = voltage
        self.voltageType = voltageType
        self.transformer = ""
        self.switcher = ""
        self.parentVoltage = 0
        self.phaseVoltage = ""
        self.mesh = 0
        self.reticulatedTransformer = ""
        self.transformerType = transformerType
        self.hasPhaseError = False
        self._phases = phases
        self._secPhases = sec_phases
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
    

    @property
    def phases(self):
        return self._phases

    @phases.setter
    def phases(self, value):
        try:
            self._phases = str(value).upper().replace("X", "N")
            self._phases = self.getJoinedPhases(self._phases.split(','))
        except:
            print(value)
            raise

    @property
    def secPhases(self):
        return self._secPhases

    @secPhases.setter
    def secPhases(self, value):
        try:
            self._secPhases = str(value).upper().replace("X", "N")
            self._secPhases = self.getJoinedPhases(self._secPhases.split(','))
        except:
            print(value)
            raise


    def getJoinedPhases(self, fases):
        if not fases:
            return ""
        fases = [f for f in fases if f.replace("\0", "").replace("0", "").strip()]       
        

        has_neutro = any("N" in s for s in fases)
        distinct_phases = sorted(set("".join(s.replace("N", "").replace("\0", "").replace("0", "") for s in fases)))

        if len(distinct_phases) > 1 and distinct_phases[0] == "A" and distinct_phases[1] == "C":
            return "CA" + ("N" if has_neutro else "")
        else:
            return "".join(distinct_phases) + ("N" if has_neutro else "")
 

    def primaryNetElement(self):
        return self.voltageType == "MT"

    def conected(self):        
        return self.order > 0

    def reverseFlow(self):
        return self.flowDirection == "2->1"

    def MarkAsALoop(self):
        self.mesh = True

    def IsLoopedElement(self):
        return self.mesh
    
    def setParent(self,parent):
        self.order = parent["order"] + 1
        self.flowDirection = parent["flowDirection"]
        self.parentElement = parent["code"]
        self.parentType = parent["table"]
        self.parentVoltage = parent["voltage"]
        self.parentPhases = parent["phases"]
        self.transformer = parent["transformer"]
        self.switcher = parent["switcher"]
        self.checkPhaseError()
    
    def checkPhaseError(self):
        self.hasPhaseError = "A" in str(self._phases).replace('N','') and not "A" in str(self.parentPhases).replace('N','') or \
                             "B" in str(self._phases).replace('N','') and not "B" in str(self.parentPhases).replace('N','') or \
                             "C" in str(self._phases).replace('N','') and not "C" in str(self.parentPhases).replace('N','')
    
