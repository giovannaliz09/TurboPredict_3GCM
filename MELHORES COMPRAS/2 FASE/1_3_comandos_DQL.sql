--Resposta Comandos SQL item a)
SELECT
    c.CD_CATEGORIA AS "Código da Categoria",
    c.DS_CATEGORIA AS "Nome da Categoria",
    p.CD_PRODUTO AS "Código do Produto",
    p.DS_PRODUTO AS "Descrição do Produto",
    p.VL_UNITARIO AS "Valor Unitário",
    p.TP_EMBALAGEM AS "Tipo de Embalagem",
    p.VL_PERC_LUCRO AS "Percentual do Lucro de cada Produto"
FROM
    MC_CATEGORIA_PROD c LEFT OUTER JOIN MC_PRODUTO p 
        ON ( c.CD_CATEGORIA = p.CD_CATEGORIA )
ORDER BY
    c.DS_CATEGORIA ASC,
    p.DS_PRODUTO ASC;
    
--Resposta Comandos SQL item b)
SELECT
    c.NR_CLIENTE AS "Código do Cliente",
    c.NM_CLIENTE AS "Nome do Cliente",
    c.DS_EMAIL AS "E-mail",
    c.NR_TELEFONE AS "Telefone",
    c.NM_LOGIN AS "Login",
    TO_CHAR(f.DT_NASCIMENTO, 'DD-MM-YYYY') AS "Data de Nascimento",
    TO_CHAR(f.DT_NASCIMENTO,'DY') AS "Dia da Semana da Data de Nascimento",
    TRUNC(MONTHS_BETWEEN(SYSDATE, f.DT_NASCIMENTO) / 12) AS "Anos de vida",
    f.FL_SEXO_BIOLOGICO AS "Sexo Biológico",
    f.NR_CPF AS "CPF"
FROM MC_CLIENTE c INNER JOIN MC_CLI_FISICA f
    ON (c.NR_CLIENTE = f.NR_CLIENTE );

--Resposta Comandos SQL item c)
SELECT
    p.CD_PRODUTO AS "Código do Produto",
    p.DS_PRODUTO AS "Nome do Produto",
    v.DT_VISUALIZACAO AS "Data de Visualização do Produto",
    v.NR_HORA_VISUALIZACAO AS "Hora de Visualização do Produto"
FROM MC_PRODUTO p INNER JOIN MC_SGV_VISUALIZACAO_VIDEO v
    ON ( p.CD_PRODUTO = v.CD_PRODUTO )
ORDER BY
    v.DT_VISUALIZACAO DESC,
    v.NR_HORA_VISUALIZACAO DESC;