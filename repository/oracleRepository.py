import cx_Oracle
import math
from repository.networkElementRepository import NetworkElementRepository

class OracleRepository:
    def __init__(self, connection_dns, user, password):
        self.connection_dns = connection_dns
        self.user = user 
        self.password = password

    def execute_query(self, query, params=None):
        with cx_Oracle.connect(self.connection_string) as connection:
            with connection.cursor() as cursor:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                result = cursor.fetchall()
        return result

    def execute_insert(self, query, params=None):
        with cx_Oracle.connect(self.connection_string) as connection:
            with connection.cursor() as cursor:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                connection.commit()

    
    def bulk_insert(self, table_name, data_list):
        if not data_list:
            return

        columns = data_list[0].keys()
        values = [tuple(item.values()) for item in data_list]

        placeholders = ', '.join([':' + str(i+1) for i in range(len(columns))])
        columns_str = ', '.join(columns)

        insert_query = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"

        with cx_Oracle.connect(user=self.user, password=self.password, dsn=self.connection_dns) as connection:
            with connection.cursor() as cursor:
                print(values)
                cursor.executemany(insert_query, values)
                connection.commit()



class mongoToOracle:

    def __init__(self):
        self.count = 0 

    def toElementoRedeComPac(self, ele):
        elementorede = {}
        self.count = self.count + 1 
        elementorede['CTMT'] = ele['feeder']
        elementorede['COD_ID'] = ele['code']
        elementorede['DIRECAOFLUXO'] = ele['flowDirection']
        elementorede['PARENT_COD_ID'] = ele['parentElement']
        elementorede['PARENT_TYPE'] = ele['parentType']
        elementorede['PARENT_PHASES'] = ele['parentPhases']
        elementorede['ID'] = self.count 
        elementorede['ORDEM'] = int(ele['order']) if ele['order'] is not None else 0
        elementorede['PAC_1'] = ele['pac1']
        elementorede['PAC_2'] = ele['pac2'] if ele['pac2'] is not None else ''
        
        elementorede['QTDADEELEMCONECTADOSJUSANTE'] = int(ele['qtdeElementsDownstream'])if ele['qtdeElementsDownstream'] is not None else 0
        elementorede['TABELA'] = ele['table']
        elementorede['TENSAO'] = str(ele['voltage']) if str(ele['voltage']) is not None and not math.isnan(ele['voltage']) else ""         
        elementorede['TIPOTENSAO'] = ele['voltageType']
        elementorede['TRANSFORMADOR'] = ele['transformer']
        elementorede['SECCIONADOR'] = ele['switcher']
        elementorede['TENSAOPAI'] = str(ele['parentVoltage'])
        elementorede['TENSAOFASE'] = str(ele['phaseVoltage'])
        elementorede['MALHA'] = int(ele['mesh']) if ele['mesh'] is not None else 0
        elementorede['TRAFORETICULADO'] = ele['reticulatedTransformer']
        elementorede['FASES'] = ele['_phases']
        elementorede['VERSION_ID'] = 1
        return elementorede   
    
    def execute(self):
        # Defina a sua string de conexão com o banco Oracle
        dsnStr = '(DESCRIPTION=(ADDRESS_LIST=(ADDRESS=(PROTOCOL=TCP)(HOST=192.213.102.69)(PORT=1521)))(CONNECT_DATA=(SID=SIS11GPER)))'
        connection_string = "gper_dev2/gper_dev2@192.213.102.69:1521/SIS11GPER"

        # Crie uma instância do repositório
        repository = OracleRepository(dsnStr,'gper_dev2','gper_dev2')

        mongodb_uri = 'mongodb://localhost:27017/'
        database_name = 'sequencia'

        networkElements = NetworkElementRepository(mongodb_uri,database_name).find_many({})

        elementos = list(map(self.toElementoRedeComPac,networkElements))

        repository.bulk_insert("ELEMENTOTESTE", elementos)

# Exemplo de uso
if __name__ == "__main__":
    mgOr = mongoToOracle()
    mgOr.execute()