select
    'CTMT' as "Table",
    A.cod_id as "Code",
    A.PAC_INI as "Pac1",
    Null as "Pac2",
    TO_CHAR(A.TEN_NOM) as Voltage,
    to_char(Null) as "Phases",
    to_char(Null) as "SecPhases",
    'MT' as "VoltageType",
    A.COD_ID as "Feeder"
from
    CTMT A
where
    A.COD_ID = 'JCK01X5'
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
    A.CTMT as "Feeder"
from
    UCBT A
where
    A.CTMT = 'JCK01X5'
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
    A.CTMT as "Feeder"
from
    UCMT A
where
    A.CTMT = 'JCK01X5'
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
    A.CTMT as "Feeder"
from
    PIP A
where
    A.CTMT = 'JCK01X5'
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
    A.CTMT as "Feeder"
from
    UNSEMT A
where
    A.CTMT = 'JCK01X5'
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
    A.CTMT as "Feeder"
from
    UNSEBT A
where
    A.CTMT = 'JCK01X5'
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
    A.CTMT as "Feeder"
from
    UNREMT A
where
    A.CTMT = 'JCK01X5'
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
    A.CTMT as "Feeder"
from
    SSDMT A
where
    A.CTMT = 'JCK01X5'
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
    A.CTMT as "Feeder"
from
    SSDBT A
where
    A.CTMT = 'JCK01X5'
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
    A.CTMT as "Feeder"
from
    RAMLIG A
where
    A.CTMT = 'JCK01X5'
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
    A.CTMT as "Feeder"
from
    UNCRBT A
where
    A.CTMT = 'JCK01X5'
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
    A.CTMT as "Feeder"
from
    UNCRMT A
where
    A.CTMT = 'JCK01X5'
UNION
ALL
SELECT
    'UNTRMT' AS TABELA,
    A.COD_ID AS CODIGO,
    A.PAC_1 AS PAC1,
    A.PAC_2 AS PAC2,
    (TEN_LIN_SE * 1000) as Voltage,
    (FE.FAS_PRI) AS FASES,
    (FE.FAS_SEC) AS FASESSEC,
    'MT' AS TIPOTENSAO,
    A.CTMT AS ALIMENTADOR
FROM
    UNTRMT A
    INNER JOIN (
        SELECT
            U.COD_ID,
            STRING_AGG(
                E.LIG_FAS_P,
                ','
                ORDER BY
                    U.COD_ID
            ) AS FAS_PRI,
            STRING_AGG(
                E.LIG_FAS_S || ',' || LIG_FAS_T,
                ','
                ORDER BY
                    U.COD_ID
            ) AS FAS_SEC
        FROM
            UNTRMT U
            JOIN EQTRMT E ON U.COD_ID = E.UNI_TR_MT
        GROUP BY
            TIP_TRAFO,
            U.COD_ID
    ) FE ON FE.COD_ID = A.COD_ID
WHERE
    A.CTMT = 'JCK01X5'