-- Resposta do Comando SQL item a)
DECLARE 
    V_NR_CLIENTE NUMBER;
BEGIN 
INSERT INTO MC_CLIENTE
(
    NM_CLIENTE,
    QT_ESTRELAS,
    VL_MEDIO_COMPRA,
    ST_CLIENTE,
    DS_EMAIL,
    NR_TELEFONE,
    NM_LOGIN,
    DS_SENHA
    )
    VALUES 
(
    'João Bastos Silva',
    4,
    20.50,
    'A',
    'joaobastos@gmail.com',
    '(11) 96437-4321',
    'jbastos',
    'abc1234'
    )
RETURNING NR_CLIENTE INTO V_NR_CLIENTE;

INSERT INTO MC_CLI_FISICA
(
    NR_CLIENTE,
    DT_NASCIMENTO,
    FL_SEXO_BIOLOGICO,
    DS_GENERO,
    NR_CPF 
    )
    VALUES
(
    V_NR_CLIENTE,
    TO_DATE('04/06/1990', 'DD/MM/YYYY'),
    'M',
    'Masculino',
    '314.563.457-00'
    ); 
END;
/

INSERT INTO MC_END_CLI (
NR_CLIENTE,
CD_LOGRADOURO_CLI,
NR_END,
DS_COMPLEMENTO_END,
DT_INICIO,
ST_END
)
VALUES (
1,
1,
487,
'Apartamento 288 torre B',
TO_DATE('21/09/2020', 'DD/MM/YYYY'),
'A'
);

DECLARE 
    V_NR_CLIENTE NUMBER;
BEGIN 
INSERT INTO MC_CLIENTE
(
    NM_CLIENTE,
    QT_ESTRELAS,
    VL_MEDIO_COMPRA,
    ST_CLIENTE,
    DS_EMAIL,
    NR_TELEFONE,
    NM_LOGIN,
    DS_SENHA
    )
    VALUES 
(
    'Lumos Solutions',
    3,
    60.45,
    'A',
    'lumosolutions@gmail.com',
    '(11) 97543-9988',
    'lsolutions',
    'jkl4433'
    ) 
RETURNING NR_CLIENTE INTO V_NR_CLIENTE;

INSERT INTO MC_CLI_JURIDICA
(
    NR_CLIENTE,
    DT_FUNDACAO,
    NR_CNPJ,
    NR_INSCR_EST
    )
    VALUES
(
    V_NR_CLIENTE,
    TO_DATE('07/10/2000', 'DD/MM/YYYY'),
    '56.321.784/0001-90',
    '99.123.784.988'
    ); 
END;
/

INSERT INTO MC_END_CLI (
NR_CLIENTE,
CD_LOGRADOURO_CLI,
NR_END,
DS_COMPLEMENTO_END,
DT_INICIO,
ST_END
)
VALUES (
2,
5,
1384,
'Torre Atrium, 5º andar',
TO_DATE('12/05/2023', 'DD/MM/YYYY'),
'A'
);

COMMIT;

-- Resposta do Comando SQL item b)
DECLARE 
    V_NR_CLIENTE NUMBER;
BEGIN 
INSERT INTO MC_CLIENTE
(
    NM_CLIENTE,
    QT_ESTRELAS,
    VL_MEDIO_COMPRA,
    ST_CLIENTE,
    DS_EMAIL,
    NR_TELEFONE,
    NM_LOGIN,
    DS_SENHA
    )
    VALUES 
(
    'Gabriel Dias',
    2,
    74.50,
    'A',
    'gabrieldias@gmail.com',
    '(11) 96422-1234',
    'jbastos',
    'udye893'
    )
RETURNING NR_CLIENTE INTO V_NR_CLIENTE;

INSERT INTO MC_CLI_FISICA
(
    NR_CLIENTE,
    DT_NASCIMENTO,
    FL_SEXO_BIOLOGICO,
    DS_GENERO,
    NR_CPF 
    )
    VALUES
(
    V_NR_CLIENTE,
    TO_DATE('10/04/1990', 'DD/MM/YYYY'),
    'M',
    'Masculino',
    '354.576.757-99'
    ); 
END;
/

COMMIT;

-- Resposta do Comando SQL item c)
UPDATE MC_FUNCIONARIO 
SET
    DS_CARGO = 'Vendedor(a) IV',
    VL_SALARIO = VL_SALARIO * 1.12
WHERE CD_FUNCIONARIO = 3;
COMMIT;

-- Resposta do Comando SQL item d)
UPDATE MC_END_CLI
SET
    ST_END = 'I',
    DT_TERMINO = TO_DATE('14/10/2025', 'DD/MM/YYYY')
WHERE NR_CLIENTE = 1;
COMMIT;

-- Resposta do Comando SQL item e)
DELETE FROM MC_ESTADO WHERE SG_ESTADO = 'SP';

-- Resposta do Comando SQL item f)
UPDATE MC_PRODUTO
SET
    ST_PRODUTO = 'X'
WHERE CD_PRODUTO = 1;

-- Resposta do Comando SQL item g)
COMMIT;