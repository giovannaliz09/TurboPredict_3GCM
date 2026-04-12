-- Gerado por Oracle SQL Developer Data Modeler 24.3.1.351.0831
--   em:        2025-09-14 18:41:21 BRT
--   site:      Oracle Database 11g
--   tipo:      Oracle Database 11g



DROP TABLE MC_BAIRRO CASCADE CONSTRAINTS 
;

DROP TABLE MC_CIDADE CASCADE CONSTRAINTS 
;

DROP TABLE MC_CLIENTE CASCADE CONSTRAINTS 
;

DROP TABLE MC_DEPTO CASCADE CONSTRAINTS 
;

DROP TABLE MC_END_CLI CASCADE CONSTRAINTS 
;

DROP TABLE MC_END_FUNC CASCADE CONSTRAINTS 
;

DROP TABLE MC_ESTADO CASCADE CONSTRAINTS 
;

DROP TABLE MC_FUNCIONARIO CASCADE CONSTRAINTS 
;

DROP TABLE MC_LOGRADOURO CASCADE CONSTRAINTS 
;

DROP TABLE MC_SGV_SAC CASCADE CONSTRAINTS 
;

DROP TABLE MC_SGV_VIDEO_PROD CASCADE CONSTRAINTS 
;

DROP TABLE SGV_CAT_PROD CASCADE CONSTRAINTS 
;

DROP TABLE SGV_CAT_VIDEO CASCADE CONSTRAINTS 
;

DROP TABLE SGV_MC_CATEGORIA CASCADE CONSTRAINTS 
;

DROP TABLE SGV_PRODUTO CASCADE CONSTRAINTS 
;

DROP TABLE SGV_VISUALI_VIDEO CASCADE CONSTRAINTS 
;

-- predefined type, no DDL - MDSYS.SDO_GEOMETRY

-- predefined type, no DDL - XMLTYPE

CREATE TABLE MC_BAIRRO 
    ( 
     CD_BAIRRO      NUMBER (8)  NOT NULL , 
     CD_CIDADE      NUMBER (8)  NOT NULL , 
     NM_BAIRRO      VARCHAR2 (45)  NOT NULL , 
     NM_ZONA_BAIRRO VARCHAR2 (20) 
    ) 
;

COMMENT ON COLUMN MC_BAIRRO.CD_BAIRRO IS 'Esta coluna irá receber o codigo do bairro e seu conteúdo é obrigatório.' 
;

COMMENT ON COLUMN MC_BAIRRO.CD_CIDADE IS 'Esta coluna irá receber o codigo da cidade e seu conteúdo é obrigatório.' 
;

COMMENT ON COLUMN MC_BAIRRO.NM_BAIRRO IS 'Esta coluna ira receber o nome do Bairro. Esse conteúdo é obrigatório.' 
;

COMMENT ON COLUMN MC_BAIRRO.NM_ZONA_BAIRRO IS 'Esta coluna irá receber a localização da zona onde se encontra o bairro. Alguns exemplos: Zona Norte, Zona Sul, Zona Leste, Zona Oeste, Centro.' 
;

ALTER TABLE MC_BAIRRO 
    ADD CONSTRAINT PK_MC_BAIRRO PRIMARY KEY ( CD_BAIRRO ) ;

CREATE TABLE MC_CIDADE 
    ( 
     CD_CIDADE NUMBER (8)  NOT NULL , 
     SG_ESTADO CHAR (2)  NOT NULL , 
     NM_CIDADE VARCHAR2 (60)  NOT NULL , 
     CD_IBGE   NUMBER (8) , 
     NR_DDD    NUMBER (3) 
    ) 
;

COMMENT ON COLUMN MC_CIDADE.CD_CIDADE IS 'Esta coluna irá receber o codigo da cidade e seu conteúdo é obrigatório.' 
;

COMMENT ON COLUMN MC_CIDADE.SG_ESTADO IS 'Esta coluna ira receber a siga do Estado. Esse conteúdo é obrigatório.' 
;

COMMENT ON COLUMN MC_CIDADE.NM_CIDADE IS 'Esta coluna ira receber o nome da Cidade. Esse conteúdo é obrigatório.' 
;

COMMENT ON COLUMN MC_CIDADE.CD_IBGE IS 'Esta coluna irá receber o código do IBGE que fornece informações para geração da NFe.' 
;

COMMENT ON COLUMN MC_CIDADE.NR_DDD IS 'Esta coluna irá receber o número do DDD da cidade para ser utilizado no contato telefônico. Seu conteudo é opcional.' 
;

ALTER TABLE MC_CIDADE 
    ADD CONSTRAINT PK_MC_CIDADE PRIMARY KEY ( CD_CIDADE ) ;

CREATE TABLE MC_CLIENTE 
    ( 
     NR_CLIENTE      NUMBER (10)  NOT NULL , 
     NM_CLIENTE      VARCHAR2 (160)  NOT NULL , 
     QT_ESTRELAS     NUMBER (1)  NOT NULL , 
     VL_MEDIO_COMPRA NUMBER (10,2)  NOT NULL , 
     ST_CLIENTE      CHAR (1)  NOT NULL , 
     DS_EMAIL        VARCHAR2 (100)  NOT NULL , 
     NR_TELEFONE     VARCHAR2 (20) , 
     NM_LOGIN        VARCHAR2 (50)  NOT NULL , 
     DS_SENHA        VARCHAR2 (50)  NOT NULL , 
     NR_CPF          VARCHAR2 (14) , 
     NR_CNPJ         VARCHAR2 (19) , 
     DT_NASCIMENTO   DATE , 
     TP_CLIENTE      CHAR (2)  NOT NULL 
    ) 
;

COMMENT ON COLUMN MC_CLIENTE.NR_CLIENTE IS 'Essa coluna irá armazenar o código único do cliente na plataforma ecommerce da Melhores Compras.Seu conteúdo deve ser obrigatório, único e preenhcido a  parrtir da chamada de sequence  SQ_MC_CLIENTE, a qual terá sempre o número disponivel para uso.' 
;

COMMENT ON COLUMN MC_CLIENTE.NM_CLIENTE IS 'Essa coluna irá armazenar o nome do cliente na plataforma ecommerce da Melhores Compras.Seu conteúdo deve ser obrigatório.' 
;

COMMENT ON COLUMN MC_CLIENTE.QT_ESTRELAS IS 'Essa coluna irá armazenar a quantiade de estrelas do cliente na plataforma ecommerce da Melhores Compras.Seu conteúdo deve ser obrigatório e ser possível de estar entre 1 e 5 estrelas.' 
;

COMMENT ON COLUMN MC_CLIENTE.VL_MEDIO_COMPRA IS 'Essa coluna irá armazenar o valor  médio de gastos f eito pelo cliente na plataforma ecommerce da Melhores Compras.Seu conteúdo deve ser obrigatório e deve ser calculado diariamente.' 
;

COMMENT ON COLUMN MC_CLIENTE.ST_CLIENTE IS 'Essa coluna irá armazenar o stauts do cliente da Melhorees Compras. Os valores permitidos aqui são: A(tivo) e I(nativo).' 
;

COMMENT ON COLUMN MC_CLIENTE.DS_EMAIL IS 'Essa coluna irá armazenar o email  do cliente da Melhorees Compras. No minimo é esperado um email contendo o caractere (@) em seu conteúdo.' 
;

COMMENT ON COLUMN MC_CLIENTE.NR_TELEFONE IS 'Essa coluna irá armazenar o número do cliente da Melhorees Compras. A mascara de armazenamento deve ser: (<nr_ddd>) 99999-9999 e  deve ser utilizada pré definida.' 
;

COMMENT ON COLUMN MC_CLIENTE.NM_LOGIN IS 'Essa coluna irá armazenar o login de cada cliente na plataforma ecommerce da Melhores Compras. Seu conteúdo deve ser obrigatório e  único para cada cliente.' 
;

COMMENT ON COLUMN MC_CLIENTE.DS_SENHA IS 'Essa coluna irá armazenar a senha de cada cliente na plataforma ecommerce da Melhores Compras.Seu conteúdo deve ser obrigatório.' 
;

COMMENT ON COLUMN MC_CLIENTE.NR_CPF IS 'Este atributo irá receber o número do CPF já com a sua respectiva máscara. Exemplo: 09.08.554-09. Seu conteúdo é opcional pois o cliente por ser pessoa física ou juridica.' 
;

COMMENT ON COLUMN MC_CLIENTE.NR_CNPJ IS 'Este atributo irá receber o número do CNPJ  já com a sua respectiva máscara. Exemplo: 02.248.678/0001-12. Seu conteúdo é opcional pois o cliente por ser pessoa física ou juridica.' 
;

COMMENT ON COLUMN MC_CLIENTE.DT_NASCIMENTO IS 'Este atributo irá receber a data de nascimento ou data de fundação do cliente e seu conteúdo é opcional.' 
;

COMMENT ON COLUMN MC_CLIENTE.TP_CLIENTE IS 'Este atirbuto irá receber o tipo do cliente, que poderá ser PF (para pessao física) ou PJ (para pessoa jurídica).' 
;

ALTER TABLE MC_CLIENTE 
    ADD CONSTRAINT PK_MC_CLIENTE PRIMARY KEY ( NR_CLIENTE ) ;

ALTER TABLE MC_CLIENTE 
    ADD CONSTRAINT UN_MC_CLIENTE_CPF_CNPJ UNIQUE ( NR_CPF , NR_CNPJ ) ;

ALTER TABLE MC_CLIENTE 
    ADD CONSTRAINT UN_MC_CLIENTE_EMAIL UNIQUE ( DS_EMAIL ) ;

CREATE TABLE MC_DEPTO 
    ( 
     CD_DEPTO NUMBER (3)  NOT NULL , 
     NM_DEPTO VARCHAR2 (100)  NOT NULL , 
     ST_DEPTO CHAR (1)  NOT NULL 
    ) 
;

COMMENT ON COLUMN MC_DEPTO.CD_DEPTO IS 'Esta coluna irá receber o codigo do departamento  e seu conteúdo é obrigatório.' 
;

COMMENT ON COLUMN MC_DEPTO.NM_DEPTO IS 'Esta coluna irá receber o nome do  departamento  e seu conteúdo é obrigatório.' 
;

COMMENT ON COLUMN MC_DEPTO.ST_DEPTO IS 'Esta coluna irá receber o status do  departamento  e seu conteúdo é obrigatório. Os valores possíveis são: (A)tivo e (I)nativo.' 
;

ALTER TABLE MC_DEPTO 
    ADD CONSTRAINT PK_MC_DEPTO PRIMARY KEY ( CD_DEPTO ) ;

CREATE TABLE MC_END_CLI 
    ( 
     NR_CLIENTE         NUMBER (10)  NOT NULL , 
     CD_LOGRADOURO      NUMBER (10)  NOT NULL , 
     NR_END             NUMBER (8)  NOT NULL , 
     DS_COMPLEMENTO_END VARCHAR2 (80) , 
     DT_INICIO          DATE , 
     DT_TERMINO         DATE , 
     ST_END             CHAR (1) 
    ) 
;

COMMENT ON COLUMN MC_END_CLI.NR_CLIENTE IS 'Essa coluna irá armazenar o código único do cliente na plataforma ecommerce da Melhores Compras.Seu conteúdo deve ser obrigatório, único e preenhcido a  parrtir da chamada de sequence  SQ_MC_CLIENTE, a qual terá sempre o número disponivel para uso.' 
;

COMMENT ON COLUMN MC_END_CLI.CD_LOGRADOURO IS 'Esta coluna irá receber o código do logradouro e seu conteúdo é obrigatório.' 
;

COMMENT ON COLUMN MC_END_CLI.NR_END IS 'Número do Endereço do Cliente. O número da Rua/Localidade onde o cliente está associado.' 
;

COMMENT ON COLUMN MC_END_CLI.DS_COMPLEMENTO_END IS 'Esta coluna irá receber o complemento do endereço do cliente e seu conteúdo pode ser opcional.' 
;

COMMENT ON COLUMN MC_END_CLI.DT_INICIO IS 'Data de início do endereço associado ao cliente.' 
;

COMMENT ON COLUMN MC_END_CLI.DT_TERMINO IS 'Data de término do endereço associado ao cliente.' 
;

COMMENT ON COLUMN MC_END_CLI.ST_END IS 'Status do endereço. (A)itvo ou (I)nativo.' 
;

ALTER TABLE MC_END_CLI 
    ADD CONSTRAINT PK_MC_END_CLI PRIMARY KEY ( CD_LOGRADOURO, NR_CLIENTE ) ;

CREATE TABLE MC_END_FUNC 
    ( 
     CD_FUNCIONARIO     NUMBER (10)  NOT NULL , 
     CD_LOGRADOURO      NUMBER (10)  NOT NULL , 
     NR_END             NUMBER (8)  NOT NULL , 
     DS_COMPLEMENTO_END VARCHAR2 (80) , 
     DT_INICIO          DATE  NOT NULL , 
     DT_TERMINO         DATE , 
     ST_END             CHAR (1)  NOT NULL 
    ) 
;

COMMENT ON COLUMN MC_END_FUNC.CD_FUNCIONARIO IS 'Esta coluna irá receber o codigo do funcionário e seu conteúdo é obrigatório.' 
;

COMMENT ON COLUMN MC_END_FUNC.CD_LOGRADOURO IS 'Esta coluna irá receber o código do logradouro e seu conteúdo é obrigatório.' 
;

COMMENT ON COLUMN MC_END_FUNC.NR_END IS 'Número do Endereço do Cliente. O número da Rua/Localidade onde o cliente está associado.' 
;

COMMENT ON COLUMN MC_END_FUNC.DT_INICIO IS 'Data de início do endereço associado ao cliente.' 
;

COMMENT ON COLUMN MC_END_FUNC.DT_TERMINO IS 'Data de término do endereço associado ao cliente.' 
;

ALTER TABLE MC_END_FUNC 
    ADD CONSTRAINT PK_MC_END_FUNC PRIMARY KEY ( CD_LOGRADOURO, CD_FUNCIONARIO ) ;

CREATE TABLE MC_ESTADO 
    ( 
     SG_ESTADO CHAR (2)  NOT NULL , 
     NM_ESTADO VARCHAR2 (30)  NOT NULL 
    ) 
;

COMMENT ON COLUMN MC_ESTADO.SG_ESTADO IS 'Esta coluna ira receber a siga do Estado. Esse conteúdo é obrigatório.' 
;

COMMENT ON COLUMN MC_ESTADO.NM_ESTADO IS 'Esta coluna irá receber o nome do estado' 
;

ALTER TABLE MC_ESTADO 
    ADD CONSTRAINT PK_MC_ESTADO PRIMARY KEY ( SG_ESTADO ) ;

CREATE TABLE MC_FUNCIONARIO 
    ( 
     CD_FUNCIONARIO    NUMBER (10)  NOT NULL , 
     CD_DEPTO          NUMBER (3)  NOT NULL , 
     CD_GERENTE        NUMBER (10) , 
     NM_FUNCIONARIO    VARCHAR2 (160)  NOT NULL , 
     DT_NASCIMENTO     DATE  NOT NULL , 
     FL_SEXO_BIOLOGICO CHAR (1)  NOT NULL , 
     DS_GENERO         VARCHAR2 (100) , 
     DS_CARGO          VARCHAR2 (80)  NOT NULL , 
     VL_SALARIO        NUMBER (10,2) , 
     DS_EMAIL          VARCHAR2 (80) , 
     ST_FUNC           CHAR (1) , 
     DT_CADASTRAMENTO  DATE , 
     DT_DESLIGAMENTO   DATE 
    ) 
;

COMMENT ON COLUMN MC_FUNCIONARIO.CD_FUNCIONARIO IS 'Esta coluna irá receber o codigo do funcionário e seu conteúdo é obrigatório.' 
;

COMMENT ON COLUMN MC_FUNCIONARIO.CD_DEPTO IS 'Esta coluna irá receber o codigo do departamento  e seu conteúdo é obrigatório.' 
;

COMMENT ON COLUMN MC_FUNCIONARIO.CD_GERENTE IS 'Esta coluna faz referência ao código do gerente.' 
;

COMMENT ON COLUMN MC_FUNCIONARIO.NM_FUNCIONARIO IS 'Esta coluna irá receber o nome do funcionário e seu conteúdo é obrigatório.' 
;

COMMENT ON COLUMN MC_FUNCIONARIO.DT_NASCIMENTO IS 'Esta coluna irá receber a data de nascimento  do funcionário e seu conteúdo é obrigatório.' 
;

COMMENT ON COLUMN MC_FUNCIONARIO.FL_SEXO_BIOLOGICO IS 'Esta coluna irá receber o sexo biológico do funcionário e seu conteúdo é obrigatório.Os valores permitidos aqui seriam: (F)eminino; (M)asculino ou (Hermafrodita)' 
;

COMMENT ON COLUMN MC_FUNCIONARIO.DS_GENERO IS 'Esta coluna irá receber o genero atribuido ao funcionário e seu conteúdo é opcional.' 
;

COMMENT ON COLUMN MC_FUNCIONARIO.DS_CARGO IS 'Esta coluna irá receber o cargo do funcionário e seu conteúdo é opcional.' 
;

COMMENT ON COLUMN MC_FUNCIONARIO.VL_SALARIO IS 'Esta coluna irá receber o valor do salário do funcionário e seu conteúdo é opcional.' 
;

COMMENT ON COLUMN MC_FUNCIONARIO.DS_EMAIL IS 'Esta coluna irá receber o email do funcionário e seu conteúdo é opcional.' 
;

COMMENT ON COLUMN MC_FUNCIONARIO.ST_FUNC IS 'Essa coluna irá armazenar o stauts do funcionário da Melhorees Compras. Os valores permitidos aqui são: A(tivo) e I(nativo).' 
;

COMMENT ON COLUMN MC_FUNCIONARIO.DT_CADASTRAMENTO IS 'Data de cadastramento do Funcionario' 
;

COMMENT ON COLUMN MC_FUNCIONARIO.DT_DESLIGAMENTO IS 'Data de desligamento  do Funcionario. Seu conteúdo é opcional.' 
;

ALTER TABLE MC_FUNCIONARIO 
    ADD CONSTRAINT PK_MC_FUNCIONARIO PRIMARY KEY ( CD_FUNCIONARIO ) ;

ALTER TABLE MC_FUNCIONARIO 
    ADD CONSTRAINT UN_MC_FUNCIONARIO_EMAIL UNIQUE ( DS_EMAIL ) ;

CREATE TABLE MC_LOGRADOURO 
    ( 
     CD_LOGRADOURO NUMBER (10)  NOT NULL , 
     CD_BAIRRO     NUMBER (8)  NOT NULL , 
     NM_LOGRADOURO VARCHAR2 (160)  NOT NULL , 
     NR_CEP        NUMBER (8) 
    ) 
;

COMMENT ON COLUMN MC_LOGRADOURO.CD_LOGRADOURO IS 'Esta coluna irá receber o código do logradouro e seu conteúdo é obrigatório.' 
;

COMMENT ON COLUMN MC_LOGRADOURO.CD_BAIRRO IS 'Esta coluna irá receber o codigo do bairro e seu conteúdo é obrigatório.' 
;

COMMENT ON COLUMN MC_LOGRADOURO.NM_LOGRADOURO IS 'Esta coluna irá receber o nome do logradouro e seu conteúdo é obrigatório.' 
;

COMMENT ON COLUMN MC_LOGRADOURO.NR_CEP IS 'Esta coluna irá receber o numero do CEP do Logradouro e seu conteúdo é obrigatório.' 
;

ALTER TABLE MC_LOGRADOURO 
    ADD CONSTRAINT PK_MC_LOGRADOURO PRIMARY KEY ( CD_LOGRADOURO ) ;

CREATE TABLE MC_SGV_SAC 
    ( 
     NR_SAC                   NUMBER (10)  NOT NULL , 
     NR_CLIENTE               NUMBER (10)  NOT NULL , 
     CD_FUNCIONARIO           NUMBER (10) , 
     CD_PRODUTO               NUMBER (10)  NOT NULL , 
     ST_SAC                   CHAR (1)  NOT NULL , 
     DS_DETALHADA_SAC         VARCHAR2 (4000 CHAR)  NOT NULL , 
     DT_ABERTURA_SAC          DATE  NOT NULL , 
     HR_ABERTURA_SAC          TIMESTAMP  NOT NULL , 
     DT_ATENDIMENTO_SAC       DATE , 
     HR_ATENDIMENTO_SAC       NUMBER (2) , 
     NR_TEMPO_TOTAL_SAC       NUMBER (10) , 
     DS_DETALHADA_RETORNO_SAC VARCHAR2 (4000) , 
     TP_SAC                   CHAR (1)  NOT NULL , 
     NR_INDICE_SATISFACAO     NUMBER (2) 
    ) 
;



ALTER TABLE MC_SGV_SAC 
    ADD CONSTRAINT CK_MC_SGV_TP_SAC
    CHECK (TP_SAC IN ('1', '2')) 
;

COMMENT ON COLUMN MC_SGV_SAC.NR_SAC IS 'Essa coluna irá armazenar a chave primária da tabela de SAC de vídeo da Melhores Compras. A cada SAC cadastrado pelo cliente será acionada a Sequence  SQ_MC_SGV_SAC que se encarregará de gerar o próximo número único do chamado SAC feito pelo Cliente.' 
;

COMMENT ON COLUMN MC_SGV_SAC.NR_CLIENTE IS 'Essa coluna irá armazenar o código único do cliente na plataforma ecommerce da Melhores Compras.Seu conteúdo deve ser obrigatório, único e preenhcido a  parrtir da chamada de sequence  SQ_MC_CLIENTE, a qual terá sempre o número disponivel para uso.' 
;

COMMENT ON COLUMN MC_SGV_SAC.CD_FUNCIONARIO IS 'Esta coluna irá receber o codigo do funcionário e seu conteúdo é obrigatório.' 
;

COMMENT ON COLUMN MC_SGV_SAC.CD_PRODUTO IS 'Codigo de identificação do produto.' 
;

COMMENT ON COLUMN MC_SGV_SAC.ST_SAC IS 'Essa coluna  irá  receber o STATUS  do chamado SAC aberto pelo cliente.  Seu conteúdo deve ser obrigatório e os possíveis valores são: (A)berto, o primeiro status criado no início; (E)m Atendimento; (C)ancelado; (F)echado ou (X)Fechado com Insatisfação do cliente.' 
;

COMMENT ON COLUMN MC_SGV_SAC.DS_DETALHADA_SAC IS 'Essa coluna irá receber a descrição completa do SAC aberto pelo cliente. Seu conteudo deve ser obrigatório.' 
;

COMMENT ON COLUMN MC_SGV_SAC.DT_ABERTURA_SAC IS 'Essa coluna  irá  receber a data e horário do SAC aberto pelo cliente. Seu conteudo deve ser obrigatório.' 
;

COMMENT ON COLUMN MC_SGV_SAC.HR_ABERTURA_SAC IS 'Essa coluna  irá  receber a hora do SAC aberto pelo cliente. Seu conteudo deve ser obrigatório.' 
;

COMMENT ON COLUMN MC_SGV_SAC.DT_ATENDIMENTO_SAC IS 'Essa coluna  irá  receber a data e horário do atendmiento SAC feita pelo funcionário da Melhores Compras. Seu conteudo deve ser opcional.' 
;

COMMENT ON COLUMN MC_SGV_SAC.HR_ATENDIMENTO_SAC IS 'Essa coluna  irá  receber a hora do SAC do atendimento  feito  pelo funcionario da Melhores Compras. Seu conteudo deve ser opcional.' 
;

COMMENT ON COLUMN MC_SGV_SAC.NR_TEMPO_TOTAL_SAC IS 'Essa coluna  irá  receber o tempo total em horas  (HH24) computado desde a abertura até a conclusão dele. A unidade de medida é horas, ou seja, em quantas horas o chamado foi concluído desde a sua abertura. Seu conteudo deve ser opcional.' 
;

COMMENT ON COLUMN MC_SGV_SAC.DS_DETALHADA_RETORNO_SAC IS 'Essa coluna  irá  receber a descrição detalhada do retorno feito pelo funcionário a partir da solicitação do cliente. Seu conteúdo deve ser opcional e preenchido pelo funcionário.' 
;

COMMENT ON COLUMN MC_SGV_SAC.TP_SAC IS 'Essa coluna  irá  receber o TIPO do chamado SAC aberto pelo cliente.  Seu conteúdo deve ser obrigatório e os possíveis valores são: (1) Sugestão; (2) Reclamação.' 
;

COMMENT ON COLUMN MC_SGV_SAC.NR_INDICE_SATISFACAO IS 'Essa coluna  irá  receber o índice de satisfação, , computado como um valor simples de 1 a 10, onde 1 refere-se ao cliente menos satisfeito e 10 o cliente mais satisfeito. Esse índice de satisfação é opcional e informado pelo cliente ao final do atendimento.' 
;

ALTER TABLE MC_SGV_SAC 
    ADD CONSTRAINT CK_MC_SGV_SAC_STATUS 
    CHECK (ST_SAC IN ('A','E','C','F','X'))
;




ALTER TABLE MC_SGV_SAC 
    ADD CONSTRAINT CK_MC_SGV_SAC_SATISF 
    CHECK (NR_INDICE_SATISFACAO BETWEEN 1 AND 10)
;
ALTER TABLE MC_SGV_SAC 
    ADD CONSTRAINT PK_MC_SGV_SAC PRIMARY KEY ( NR_SAC ) ;

CREATE TABLE MC_SGV_VIDEO_PROD 
    ( 
     COD_VIDEO        NUMBER (10)  NOT NULL , 
     CD_PRODUTO       NUMBER (10)  NOT NULL , 
     CD_CATEGORIA     NUMBER (10)  NOT NULL , 
     ST_VIDEO         CHAR (1)  NOT NULL , 
     DT_INICIO_VIDEO  DATE  NOT NULL , 
     DT_TERMINO_VIDEO DATE , 
     DESCRICAO_VIDEO  VARCHAR2 (100)  NOT NULL 
    ) 
;

COMMENT ON COLUMN MC_SGV_VIDEO_PROD.COD_VIDEO IS 'Essa coluna irá armazenar a chave primária da tabela de vídeo de produtos da Melhores Compras. A cada vídeo de produto cadastrado será acionada a Sequence SQ_MC_COD_VIDEO que se encarregará de gerar o próximo número único do vídeo de produto.' 
;

COMMENT ON COLUMN MC_SGV_VIDEO_PROD.CD_PRODUTO IS 'codigo de produto referente a entidade mc_produto' 
;

COMMENT ON COLUMN MC_SGV_VIDEO_PROD.CD_CATEGORIA IS 'Categoria de video referente a entidade sgv_cat_video' 
;

COMMENT ON COLUMN MC_SGV_VIDEO_PROD.ST_VIDEO IS 'Essa coluna irá armazenar o status do vídeo de produto. Os valores permitidos aqui são: A(tivo) e I(nativo). ' 
;

COMMENT ON COLUMN MC_SGV_VIDEO_PROD.DT_INICIO_VIDEO IS 'Essa coluna irá armazenar a data de início do vídeo de produto. Seu conteúdo deve ser obrigatório.' 
;

COMMENT ON COLUMN MC_SGV_VIDEO_PROD.DT_TERMINO_VIDEO IS 'Essa coluna irá armazenar a data de término do vídeo de produto. Seu conteúdo deve ser opcional.' 
;

COMMENT ON COLUMN MC_SGV_VIDEO_PROD.DESCRICAO_VIDEO IS 'Essa coluna irá armazenar uma breve descrição do vídeo de produto. Seu conteúdo deve ser obrigatório.' 
;

ALTER TABLE MC_SGV_VIDEO_PROD 
    ADD CONSTRAINT CK_MC_SGV_VIDEO_STATUS 
    CHECK (ST_VIDEO IN ('A','I'))
;
ALTER TABLE MC_SGV_VIDEO_PROD 
    ADD CONSTRAINT MC_SGV_VIDEO_PROD_PK PRIMARY KEY ( COD_VIDEO ) ;

CREATE TABLE SGV_CAT_PROD 
    ( 
     CD_CATEGORIA NUMBER (10)  NOT NULL 
    ) 
;

COMMENT ON COLUMN SGV_CAT_PROD.CD_CATEGORIA IS 'Chave primaria e estrangeira refente a entidade pai sgv_mc_categoria' 
;

ALTER TABLE SGV_CAT_PROD 
    ADD CONSTRAINT CAT_PROD_PK PRIMARY KEY ( CD_CATEGORIA ) ;

CREATE TABLE SGV_CAT_VIDEO 
    ( 
     CD_CATEGORIA NUMBER (10)  NOT NULL 
    ) 
;

COMMENT ON COLUMN SGV_CAT_VIDEO.CD_CATEGORIA IS 'Chave primaria e estrangeira refente a entidade pai sgv_mc_categoria' 
;

ALTER TABLE SGV_CAT_VIDEO 
    ADD CONSTRAINT CAT_VIDEO_PK PRIMARY KEY ( CD_CATEGORIA ) ;

CREATE TABLE SGV_MC_CATEGORIA 
    ( 
     CD_CATEGORIA         NUMBER (10)  NOT NULL , 
     TP_CATEGORIA         VARCHAR2 (1)  NOT NULL , 
     NM_CATEGORIA         VARCHAR2 (80) , 
     SG_CATEGORIA         VARCHAR2 (6) , 
     DESCRICAO_CATEGORIA  VARCHAR2 (80)  NOT NULL , 
     ST_CATEGORIA         CHAR (1)  NOT NULL , 
     DT_INICIO_CATEGORIA  DATE  NOT NULL , 
     DT_TERMINO_CATEGORIA DATE 
    ) 
;

COMMENT ON COLUMN SGV_MC_CATEGORIA.CD_CATEGORIA IS 'Essa coluna irá armazenar a chave primária da tabela de categorias da Melhores Compras. A cada categoria cadastrada será acionada a Sequence SQ_MC_CD_CATEGORIA que se encarregará de gerar o próximo número único da categoria.' 
;

COMMENT ON COLUMN SGV_MC_CATEGORIA.TP_CATEGORIA IS 'Essa coluna irá armazenar otipo da categoria. Os valores permitidos aqui são: P(roduto) e V(ídeo). Seu conteúdo deve ser obrigatório.' 
;

COMMENT ON COLUMN SGV_MC_CATEGORIA.NM_CATEGORIA IS 'Essa coluna irá armazenar o nome da categoria de produto. Seu conteúdo deve ser opcional.' 
;

COMMENT ON COLUMN SGV_MC_CATEGORIA.SG_CATEGORIA IS 'Essa coluna irá armazenar a sigla da categoria de produto. Seu conteúdo deve ser opcional.' 
;

COMMENT ON COLUMN SGV_MC_CATEGORIA.DESCRICAO_CATEGORIA IS 'Essa coluna irá armazenar a descrição da categoria de produto. Seu conteúdo deve ser obrigatório.' 
;

COMMENT ON COLUMN SGV_MC_CATEGORIA.ST_CATEGORIA IS 'Essa coluna irá armazenar o status da categoria de produto. Os valores permitidos aqui são: A(tivo) e I(nativo). Seu conteúdo deve ser obrigatório.' 
;

COMMENT ON COLUMN SGV_MC_CATEGORIA.DT_INICIO_CATEGORIA IS 'Essa coluna irá armazenar a data de início da categoria de produto. Seu conteúdo deve ser obrigatório.' 
;

COMMENT ON COLUMN SGV_MC_CATEGORIA.DT_TERMINO_CATEGORIA IS 'Essa coluna irá armazenar a data de término da categoria de produto. Seu conteúdo deve ser opcional.' 
;

ALTER TABLE SGV_MC_CATEGORIA 
    ADD CONSTRAINT CK_SGV_ST_CATEG 
    CHECK (ST_CATEGORIA IN ('A','I'))
;


ALTER TABLE SGV_MC_CATEGORIA 
    ADD CONSTRAINT CK_SGV_TP_CATEG 
    CHECK (TP_CATEGORIA IN ('P', 'V'))
;
ALTER TABLE SGV_MC_CATEGORIA 
    ADD CONSTRAINT MC_CAT_PROD_PK PRIMARY KEY ( CD_CATEGORIA ) ;

ALTER TABLE SGV_MC_CATEGORIA 
    ADD CONSTRAINT UN_SGV_MC_CATEGORIA_SG UNIQUE ( SG_CATEGORIA ) ;

CREATE TABLE SGV_PRODUTO 
    ( 
     CD_PRODUTO            NUMBER (10)  NOT NULL , 
     CD_CATEGORIA          NUMBER (10)  NOT NULL , 
     ST_PRODUTO            CHAR (1)  NOT NULL , 
     NR_CD_BARRAS_PROD     VARCHAR2 (13) , 
     DS_PRODUTO            VARCHAR2 (80)  NOT NULL , 
     VL_PRECO_UNITARIO     NUMBER (8,2)  NOT NULL , 
     TP_EMBALAGEM          VARCHAR2 (15) , 
     VL_PERC_LUCRO         NUMBER (8,2) , 
     DS_COMPLETA_PROD      VARCHAR2 (4000)  NOT NULL , 
     VL_TOTAL_IMPOSTO_PAGO NUMBER (10,2)  NOT NULL , 
     DT_INICIO_PRODUTO     DATE  NOT NULL , 
     DT_TERMINO_PRODUTO    DATE 
    ) 
;

ALTER TABLE SGV_PRODUTO 
    ADD CONSTRAINT CK_SGV_PRODUTO_STATUS
    CHECK (ST_PRODUTO IN ('A', 'I', 'P')) 
;

COMMENT ON COLUMN SGV_PRODUTO.CD_PRODUTO IS 'Essa coluna irá armazenar a chave primária da tabela de produtos da Melhorees Compras. A cada produto cadastrado será acionada a Sequence  SQ_MC_PRODUTO que se encarregará de gerar o próximo número único do produto.' 
;

COMMENT ON COLUMN SGV_PRODUTO.CD_CATEGORIA IS 'Categoria de video referente a entidade sgv_cat_prod' 
;

COMMENT ON COLUMN SGV_PRODUTO.ST_PRODUTO IS 'Essa coluna irá armazenar o stauts do produto da Melhorees Compras. Os valores permitidos aqui são: A(tivo), I(nativo) e P(rospecção).' 
;

COMMENT ON COLUMN SGV_PRODUTO.NR_CD_BARRAS_PROD IS 'Essa coluna irá armazenar o número do codigo de barras  do produto. Seu conteúdo deve ser opcional.' 
;

COMMENT ON COLUMN SGV_PRODUTO.DS_PRODUTO IS 'Essa coluna irá armazenar a descrição principal do produto. Seu conteúdo deve ser  obrigatorio.' 
;

COMMENT ON COLUMN SGV_PRODUTO.VL_PRECO_UNITARIO IS 'Essa coluna irá armazenar o valor unitário do produto. Seu conteúdo deve ser > 0 ' 
;

COMMENT ON COLUMN SGV_PRODUTO.TP_EMBALAGEM IS 'Essa coluna irá armazenar o tipo de embalagem do produto. Seu conteúdo pode ser opcional.' 
;

COMMENT ON COLUMN SGV_PRODUTO.VL_PERC_LUCRO IS 'Essa coluna irá armazenar o percentual  do lucro médio para cada produto. Seu conteúdo deve ser opcional.' 
;

COMMENT ON COLUMN SGV_PRODUTO.DS_COMPLETA_PROD IS 'Essa coluna irá armazenar a descrição completa do produto. Seu conteúdo deve ser  obrigatorio.' 
;

COMMENT ON COLUMN SGV_PRODUTO.VL_TOTAL_IMPOSTO_PAGO IS 'Essa coluna irá armazenar o valor total do imposto pago para comercializar o produto. Seu conteúdo deve ser obrigatório.' 
;

COMMENT ON COLUMN SGV_PRODUTO.DT_INICIO_PRODUTO IS 'Essa coluna irá armazenar a data de início do produto no formato dd/mm/aaaa hh24:mi:ss, que informa a abertura de acesso a ele. Seu conteúdo deve ser obrigatorio.' 
;

COMMENT ON COLUMN SGV_PRODUTO.DT_TERMINO_PRODUTO IS 'Essa coluna irá armazenar a data de término do produto no formato dd/mm/aaaa hh24:mi:ss. Seu conteúdo deve ser opcional.' 
;

ALTER TABLE SGV_PRODUTO 
    ADD CONSTRAINT CK_SGV_PROD_VL_UN 
    CHECK (VL_PRECO_UNITARIO > 0)
;


ALTER TABLE SGV_PRODUTO 
    ADD CONSTRAINT CK_SGV_PROD_EAN13 
    CHECK (NR_CD_BARRAS_PROD IS NULL OR REGEXP_LIKE(NR_CD_BARRAS_PROD,'^[0-9]{13}$'))
;


ALTER TABLE SGV_PRODUTO 
    ADD CONSTRAINT PK_MC_PRODUTO PRIMARY KEY ( CD_PRODUTO ) ;

ALTER TABLE SGV_PRODUTO 
    ADD CONSTRAINT UN_SGV_DS_PRODUTO_ UNIQUE ( DS_PRODUTO ) ;

CREATE TABLE SGV_VISUALI_VIDEO 
    ( 
     ID_VISUALIZACAO NUMBER (12)  NOT NULL , 
     COD_VIDEO       NUMBER (10)  NOT NULL , 
     NR_CLIENTE      NUMBER (10) , 
     DATA_VISITA     DATE  NOT NULL , 
     NM_LOGIN        VARCHAR2 (50) 
    ) 
;

COMMENT ON COLUMN SGV_VISUALI_VIDEO.ID_VISUALIZACAO IS 'É a chave primaria da entidade id_visualização. Ele serve para identificar de forma única cada registro de visualização no banco de dados, garantindo que não haja duplicidade e permitindo relacionamentos com outras entidades..' 
;

COMMENT ON COLUMN SGV_VISUALI_VIDEO.NR_CLIENTE IS 'Codigo de cliente que visualiza o video logado na conta cliente' 
;

COMMENT ON COLUMN SGV_VISUALI_VIDEO.DATA_VISITA IS 'Essa coluna irá armazenar a data e hora da visita feita pelo usuário. Seu conteúdo deve ser obrigatório.' 
;

COMMENT ON COLUMN SGV_VISUALI_VIDEO.NM_LOGIN IS 'Essa coluna irá armazenar o login do usuário que visualizou o vídeo. Seu conteúdo deve ser opcional.' 
;

ALTER TABLE SGV_VISUALI_VIDEO 
    ADD CONSTRAINT MC_SGV_VISUALI_VIDEO_PK PRIMARY KEY ( ID_VISUALIZACAO ) ;

ALTER TABLE SGV_CAT_PROD 
    ADD CONSTRAINT CLASSIFICAR_PRODUTO FOREIGN KEY 
    ( 
     CD_CATEGORIA
    ) 
    REFERENCES SGV_MC_CATEGORIA 
    ( 
     CD_CATEGORIA
    ) 
;

ALTER TABLE SGV_CAT_VIDEO 
    ADD CONSTRAINT CLASSIFICAR_VIDEO FOREIGN KEY 
    ( 
     CD_CATEGORIA
    ) 
    REFERENCES SGV_MC_CATEGORIA 
    ( 
     CD_CATEGORIA
    ) 
;

ALTER TABLE SGV_VISUALI_VIDEO 
    ADD CONSTRAINT cliente_realiza_visualizacao FOREIGN KEY 
    ( 
     NR_CLIENTE
    ) 
    REFERENCES MC_CLIENTE 
    ( 
     NR_CLIENTE
    ) 
;

ALTER TABLE MC_LOGRADOURO 
    ADD CONSTRAINT FK_MC_BAIRROLOGRADOURO FOREIGN KEY 
    ( 
     CD_BAIRRO
    ) 
    REFERENCES MC_BAIRRO 
    ( 
     CD_BAIRRO
    ) 
;

ALTER TABLE MC_BAIRRO 
    ADD CONSTRAINT FK_MC_CIDADE_BAIRRO FOREIGN KEY 
    ( 
     CD_CIDADE
    ) 
    REFERENCES MC_CIDADE 
    ( 
     CD_CIDADE
    ) 
;

ALTER TABLE MC_END_CLI 
    ADD CONSTRAINT FK_MC_CLIENTE_END_CLI FOREIGN KEY 
    ( 
     NR_CLIENTE
    ) 
    REFERENCES MC_CLIENTE 
    ( 
     NR_CLIENTE
    ) 
;

ALTER TABLE MC_SGV_SAC 
    ADD CONSTRAINT FK_MC_CLIENTE_SGV_SAC FOREIGN KEY 
    ( 
     NR_CLIENTE
    ) 
    REFERENCES MC_CLIENTE 
    ( 
     NR_CLIENTE
    ) 
;

ALTER TABLE MC_FUNCIONARIO 
    ADD CONSTRAINT FK_MC_DEPTO_FUNCIONARIO FOREIGN KEY 
    ( 
     CD_DEPTO
    ) 
    REFERENCES MC_DEPTO 
    ( 
     CD_DEPTO
    ) 
;

ALTER TABLE MC_END_FUNC 
    ADD CONSTRAINT FK_MC_END_FUNC_LOGRADOURO FOREIGN KEY 
    ( 
     CD_LOGRADOURO
    ) 
    REFERENCES MC_LOGRADOURO 
    ( 
     CD_LOGRADOURO
    ) 
;

ALTER TABLE MC_CIDADE 
    ADD CONSTRAINT FK_MC_ESTADO_CIDADE FOREIGN KEY 
    ( 
     SG_ESTADO
    ) 
    REFERENCES MC_ESTADO 
    ( 
     SG_ESTADO
    ) 
;

ALTER TABLE MC_END_FUNC 
    ADD CONSTRAINT FK_MC_FUNC_END FOREIGN KEY 
    ( 
     CD_FUNCIONARIO
    ) 
    REFERENCES MC_FUNCIONARIO 
    ( 
     CD_FUNCIONARIO
    ) 
;

ALTER TABLE MC_SGV_SAC 
    ADD CONSTRAINT FK_MC_FUNC_SGV_SAC FOREIGN KEY 
    ( 
     CD_FUNCIONARIO
    ) 
    REFERENCES MC_FUNCIONARIO 
    ( 
     CD_FUNCIONARIO
    ) 
;

ALTER TABLE MC_FUNCIONARIO 
    ADD CONSTRAINT FK_MC_FUNC_SUPERIOR FOREIGN KEY 
    ( 
     CD_GERENTE
    ) 
    REFERENCES MC_FUNCIONARIO 
    ( 
     CD_FUNCIONARIO
    ) 
;

ALTER TABLE MC_END_CLI 
    ADD CONSTRAINT FK_MC_LOGRAD_END_CLI FOREIGN KEY 
    ( 
     CD_LOGRADOURO
    ) 
    REFERENCES MC_LOGRADOURO 
    ( 
     CD_LOGRADOURO
    ) 
;

ALTER TABLE MC_SGV_SAC 
    ADD CONSTRAINT produto_gera_sac FOREIGN KEY 
    ( 
     CD_PRODUTO
    ) 
    REFERENCES SGV_PRODUTO 
    ( 
     CD_PRODUTO
    ) 
;

ALTER TABLE SGV_PRODUTO 
    ADD CONSTRAINT produto_tem_categoria FOREIGN KEY 
    ( 
     CD_CATEGORIA
    ) 
    REFERENCES SGV_CAT_PROD 
    ( 
     CD_CATEGORIA
    ) 
;

ALTER TABLE MC_SGV_VIDEO_PROD 
    ADD CONSTRAINT produto_tem_video FOREIGN KEY 
    ( 
     CD_PRODUTO
    ) 
    REFERENCES SGV_PRODUTO 
    ( 
     CD_PRODUTO
    ) 
;

ALTER TABLE SGV_VISUALI_VIDEO 
    ADD CONSTRAINT video_recebe_visualizacao FOREIGN KEY 
    ( 
     COD_VIDEO
    ) 
    REFERENCES MC_SGV_VIDEO_PROD 
    ( 
     COD_VIDEO
    ) 
;

ALTER TABLE MC_SGV_VIDEO_PROD 
    ADD CONSTRAINT video_tem_categoria FOREIGN KEY 
    ( 
     CD_CATEGORIA
    ) 
    REFERENCES SGV_CAT_VIDEO 
    ( 
     CD_CATEGORIA
    ) 
;

CREATE OR REPLACE TRIGGER ARC_Arc_1_SGV_CAT_PROD 
BEFORE INSERT OR UPDATE OF CD_CATEGORIA 
ON SGV_CAT_PROD 
FOR EACH ROW 
DECLARE 
    d VARCHAR2 (1); 
BEGIN 
    SELECT A.TP_CATEGORIA INTO d 
    FROM SGV_MC_CATEGORIA A 
    WHERE A.CD_CATEGORIA = :new.CD_CATEGORIA; 
    IF (d IS NULL OR d <> 'P') THEN 
        raise_application_error(-20223,'FK CLASSIFICAR_PRODUTO in Table SGV_CAT_PROD violates Arc constraint on Table SGV_MC_CATEGORIA - discriminator column TP_CATEGORIA doesn''t have value ''P'''); 
    END IF; 
    EXCEPTION 
    WHEN NO_DATA_FOUND THEN 
        NULL; 
    WHEN OTHERS THEN 
        RAISE; 
END; 
/

CREATE OR REPLACE TRIGGER ARC_Arc_1_SGV_CAT_VIDEO 
BEFORE INSERT OR UPDATE OF CD_CATEGORIA 
ON SGV_CAT_VIDEO 
FOR EACH ROW 
DECLARE 
    d VARCHAR2 (1); 
BEGIN 
    SELECT A.TP_CATEGORIA INTO d 
    FROM SGV_MC_CATEGORIA A 
    WHERE A.CD_CATEGORIA = :new.CD_CATEGORIA; 
    IF (d IS NULL OR d <> 'V') THEN 
        raise_application_error(-20223,'FK CLASSIFICAR_VIDEO in Table SGV_CAT_VIDEO violates Arc constraint on Table SGV_MC_CATEGORIA - discriminator column TP_CATEGORIA doesn''t have value ''V'''); 
    END IF; 
    EXCEPTION 
    WHEN NO_DATA_FOUND THEN 
        NULL; 
    WHEN OTHERS THEN 
        RAISE; 
END; 
/

CREATE SEQUENCE SQ_MC_CLIENTE 
START WITH 1 
    NOCACHE 
    ORDER ;

CREATE OR REPLACE TRIGGER SQ_MC_CLIENTE 
BEFORE INSERT ON MC_CLIENTE 
FOR EACH ROW 
BEGIN 
    :NEW.NR_CLIENTE := SQ_MC_CLIENTE.NEXTVAL; 
END;
/

CREATE SEQUENCE SQ_SGV_PRODUTO 
START WITH 1 
    NOCACHE 
    ORDER ;

CREATE OR REPLACE TRIGGER SQ_SGV_PRODUTO 
BEFORE INSERT ON SGV_PRODUTO 
FOR EACH ROW 
BEGIN 
    :NEW.CD_PRODUTO := SQ_SGV_PRODUTO.NEXTVAL; 
END;
/

CREATE SEQUENCE SQ_MC_SGV_SAC 
START WITH 1 
    NOCACHE 
    ORDER ;

CREATE OR REPLACE TRIGGER SQ_MC_SGV_SAC 
BEFORE INSERT ON MC_SGV_SAC 
FOR EACH ROW 
BEGIN 
    :NEW.NR_SAC := SQ_MC_SGV_SAC.NEXTVAL; 
END;
/

CREATE SEQUENCE SQ_MC_COD_VIDEO 
START WITH 1 
    NOCACHE 
    ORDER ;

CREATE OR REPLACE TRIGGER SQ_MC_COD_VIDEO 
BEFORE INSERT ON MC_SGV_VIDEO_PROD 
FOR EACH ROW 
BEGIN 
    :NEW.COD_VIDEO := SQ_MC_COD_VIDEO.NEXTVAL; 
END;
/

CREATE SEQUENCE SQ_MC_CD_CATEGORIA 
START WITH 1 
    NOCACHE 
    ORDER ;

CREATE OR REPLACE TRIGGER SQ_MC_CD_CATEGORIA 
BEFORE INSERT ON SGV_MC_CATEGORIA 
FOR EACH ROW 
BEGIN 
    :NEW.CD_CATEGORIA := SQ_MC_CD_CATEGORIA.NEXTVAL; 
END;
/



-- Relatório do Resumo do Oracle SQL Developer Data Modeler: 
-- 
-- CREATE TABLE                            16
-- CREATE INDEX                             0
-- ALTER TABLE                             54
-- CREATE VIEW                              0
-- ALTER VIEW                               0
-- CREATE PACKAGE                           0
-- CREATE PACKAGE BODY                      0
-- CREATE PROCEDURE                         0
-- CREATE FUNCTION                          0
-- CREATE TRIGGER                           5
-- ALTER TRIGGER                            0
-- CREATE COLLECTION TYPE                   0
-- CREATE STRUCTURED TYPE                   0
-- CREATE STRUCTURED TYPE BODY              0
-- CREATE CLUSTER                           0
-- CREATE CONTEXT                           0
-- CREATE DATABASE                          0
-- CREATE DIMENSION                         0
-- CREATE DIRECTORY                         0
-- CREATE DISK GROUP                        0
-- CREATE ROLE                              0
-- CREATE ROLLBACK SEGMENT                  0
-- CREATE SEQUENCE                          3
-- CREATE MATERIALIZED VIEW                 0
-- CREATE MATERIALIZED VIEW LOG             0
-- CREATE SYNONYM                           0
-- CREATE TABLESPACE                        0
-- CREATE USER                              0
-- 
-- DROP TABLESPACE                          0
-- DROP DATABASE                            0
-- 
-- REDACTION POLICY                         0
-- 
-- ORDS DROP SCHEMA                         0
-- ORDS ENABLE SCHEMA                       0
-- ORDS ENABLE OBJECT                       0
-- 
-- ERRORS                                   0
-- WARNINGS                                 0
