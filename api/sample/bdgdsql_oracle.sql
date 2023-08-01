select
    'CTMT' as "Table",
    A.cod_id as "Code",
    A.PAC_INI as "Pac1",
    Null as "Pac2",
    to_binary_double(A.TEN_NOM) as Voltage,
    to_char(Null) as "Phases",
    to_char(Null) as "SecPhases",
    'MT' as "VoltageType",
    A.COD_ID as "Feeder",
    '' as "TransformerType",
    0 as "X1",
    0 as "Y1",
    0 as "X2",
    0 as "Y2"
from
    CTMT A
where
    A.COD_ID = 'BRBBB-FC'
UNION
ALL
select
    'UCBT' as "Table",
    A.cod_id as "Code",
    A.PAC as "Pac1",
    Null as "Pac2",
    Null as Voltage,
    to_char(A.FAS_CON) as "Phases",
    to_char(Null) as "SecPhases",
    'BT' as "VoltageType",
    A.CTMT as "Feeder",
    '' as "TransformerType",
    sde.st_x(SHAPE) as "X1",
    sde.st_Y(SHAPE) as "Y1",
    0 as "X2",
    0 as "Y2"
from
    UCBT A
where
    A.CTMT = 'BRBBB-FC'
UNION
ALL
select
    'UCMT' as "Table",
    A.cod_id as "Code",
    A.PAC as "Pac1",
    Null as "Pac2",
    Null as Voltage,
    to_char(A.FAS_CON) as "Phases",
    to_char(Null) as "SecPhases",
    'MT' as "VoltageType",
    A.CTMT as "Feeder",
    '' as "TransformerType",
    sde.st_x(SHAPE) as "X1",
    sde.st_y(SHAPE) as "Y1",
    0 as "X2",
    0 as "Y2"
from
    UCMT A
where
    A.CTMT = 'BRBBB-FC'
UNION
ALL
select
    'PIP' as "Table",
    A.cod_id as "Code",
    A.PAC as "Pac1",
    Null as "Pac2",
    Null as Voltage,
    to_char(A.FAS_CON) as "Phases",
    to_char(Null) as "SecPhases",
    'BT' as "VoltageType",
    A.CTMT as "Feeder",
    '' as "TransformerType",
    0 as "X1",
    0 as "Y1",
    0 as "X2",
    0 as "Y2"
from
    PIP A
where
    A.CTMT = 'BRBBB-FC'
UNION
ALL
select
    'UNSEMT' as "Table",
    A.cod_id as "Code",
    A.PAC_1 as "Pac1",
    A.PAC_2 as "Pac2",
    Null as Voltage,
    to_char(A.FAS_CON) as "Phases",
    to_char(Null) as "SecPhases",
    'MT' as "VoltageType",
    A.CTMT as "Feeder",
    '' as "TransformerType",
    sde.st_x (SHAPE) AS X1,
    sde.st_y (SHAPE) AS Y1,
    0 AS X2,
    0 AS Y2
from
    UNSEMT A 
where
    A.CTMT = 'BRBBB-FC'
    AND A.P_N_OPE = 'F'
UNION
ALL
select
    'UNSEBT' as "Table",
    A.cod_id as "Code",
    A.PAC_1 as "Pac1",
    A.PAC_2 as "Pac2",
    Null as Voltage,
    to_char(A.FAS_CON) as "Phases",
    to_char(Null) as "SecPhases",
    'BT' as "VoltageType",
    A.CTMT as "Feeder",
    '' as "TransformerType",
    sde.st_x (SHAPE) AS X1,
    sde.st_y (SHAPE) AS Y1,
    0 AS X2,
    0 AS Y2
from
    UNSEBT A 
where
    A.CTMT = 'BRBBB-FC'
    AND A.P_N_OPE = 'F'
UNION
ALL
select
    'UNREMT' as "Table",
    A.cod_id as "Code",
    A.PAC_1 as "Pac1",
    A.PAC_2 as "Pac2",
    Null as Voltage,
    to_char(A.FAS_CON) as "Phases",
    to_char(Null) as "SecPhases",
    'MT' as "VoltageType",
    A.CTMT as "Feeder",
    '' as "TransformerType",
    sde.st_x (SHAPE) AS X1,
    sde.st_y (SHAPE) AS Y1,
    0 AS X2,
    0 AS Y2
from
    UNREMT A 
where
    A.CTMT = 'BRBBB-FC'
UNION
ALL
select
    'SSDMT' as "Table",
    A.cod_id as "Code",
    A.PAC_1 as "Pac1",
    A.PAC_2 as "Pac2",
    Null as Voltage,
    to_char(A.FAS_CON) as "Phases",
    to_char(Null) as "SecPhases",
    'MT' as "VoltageType",
    A.CTMT as "Feeder",
    '' as "TransformerType",
    sde.st_x (sde.st_startpoint(SHAPE)) AS X1,
    sde.st_y (sde.st_startpoint(SHAPE)) AS Y1,
    sde.st_x (sde.st_endpoint(SHAPE)) AS X2,
    sde.st_y (sde.st_endpoint(SHAPE)) AS Y2
from
    SSDMT A
where
    A.CTMT = 'BRBBB-FC'
UNION
ALL
select
    'SSDBT' as "Table",
    A.cod_id as "Code",
    A.PAC_1 as "Pac1",
    A.PAC_2 as "Pac2",
    Null as Voltage,
    to_char(A.FAS_CON) as "Phases",
    to_char(Null) as "SecPhases",
    'BT' as "VoltageType",
    A.CTMT as "Feeder",
    '' as "TransformerType",
    sde.st_x (sde.st_startpoint(SHAPE)) AS X1,
    sde.st_y (sde.st_startpoint(SHAPE)) AS Y1,
    sde.st_x (sde.st_endpoint(SHAPE)) AS X2,
    sde.st_y (sde.st_endpoint(SHAPE)) AS Y2
from
    SSDBT A
where
    A.CTMT = 'BRBBB-FC'
UNION
ALL
select
    'RAMLIG' as "Table",
    A.cod_id as "Code",
    A.PAC_1 as "Pac1",
    A.PAC_2 as "Pac2",
    Null as Voltage,
    to_char(A.FAS_CON) as "Phases",
    to_char(Null) as "SecPhases",
    'BT' as "VoltageType",
    A.CTMT as "Feeder",
    '' as "TransformerType",
    0 as "X1",
    0 as "Y1",
    0 as "X2",
    0 as "Y2"
from
    RAMLIG A
where
    A.CTMT = 'BRBBB-FC'
UNION
ALL
select
    'UNCRBT' as "Table",
    A.cod_id as "Code",
    A.PAC_1 as "Pac1",
    A.PAC_2 as "Pac2",
    Null as Voltage,
    to_char(A.FAS_CON) as "Phases",
    to_char(Null) as "SecPhases",
    'BT' as "VoltageType",
    A.CTMT as "Feeder",
    '' as "TransformerType",
    sde.st_x(A.SHAPE) as "X1",
    sde.st_y(A.SHAPE) as "Y1",
    0 as "X2",
    0 as "Y2"
from
    UNCRBT A 
where
    A.CTMT = 'BRBBB-FC'
UNION
ALL
select
    'UNCRMT' as "Table",
    A.cod_id as "Code",
    A.PAC_1 as "Pac1",
    A.PAC_2 as "Pac2",
    Null as Voltage,
    to_char(A.FAS_CON) as "Phases",
    to_char(Null) as "SecPhases",
    'MT' as "VoltageType",
    A.CTMT as "Feeder",
    '' as "TransformerType",
    sde.st_x(A.SHAPE) as "X1",
    sde.st_x(A.SHAPE) as "Y1",
    0 as "X2",
    0 as "Y2"
from
    UNCRMT A 
where
    A.CTMT = 'BRBBB-FC'
UNION
ALL
SELECT
    'UNTRD' AS "Table",
    A.COD_ID AS "Code",
    A.PAC_1 AS "Pac1",
    A.PAC_2 AS "Pac2",
    to_binary_double(ten_lin_se * 1000) AS "Voltage",
    to_char(FE.FAS_PRI) AS "Phases",
    to_char(FE.FAS_SEC) AS "SecPhases",
    'MT' AS "VoltageType",
    A.CTMT AS "Feeder",    
    A.TIP_TRAFO AS "TransformerType",
    sde.st_x(A.SHAPE) as "X1",
    sde.st_Y(A.SHAPE) as "Y1",
    0 as "X2",
    0 as "Y2"
FROM
    UNTRD_PVW A
    INNER JOIN (
        SELECT
            U.COD_ID,
            U.TIP_TRAFO,  
            LISTAGG(E.LIG_FAS_P, ',') WITHIN GROUP (ORDER BY U.COD_ID) AS FAS_PRI,
            LISTAGG(E.LIG_FAS_S || ',' || E.LIG_FAS_T, ',') WITHIN GROUP (ORDER BY U.COD_ID) AS FAS_SEC
        FROM
            UNTRD_PVW U
            JOIN EQTRD_PVW E ON U.COD_ID = E.UNI_TR_MT
        GROUP BY
            TIP_TRAFO,
            U.COD_ID
    ) FE ON FE.COD_ID = A.COD_ID
WHERE
    A.CTMT = 'BRBBB-FC'
