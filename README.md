## Sobre

Este projeto tem como objetivo criar um Data Warehouse (utilizando modelagem tradicional Star Schema) no BigQuery com dados de transferência de jogadores de alguns campeonatos do futebol Europeu desde a temporada 1992/1993, a patir de um dataset do [Kaggle](https://www.kaggle.com/datasets/mexwell/football-player-transfers). 

Esse Dataset contém dados dos campeonatos:

- English Premier League (premier-league.csv)
- English Championship (championship.csv)
- French Ligue 1 (ligue-1.csv)
- German 1.Bundesliga (1-bundesliga.csv)
- Italian Serie A (serie-a.csv)
- Spanish La Liga (primera-division.csv)
- Portugese Liga NOS (liga-nos.csv)
- Dutch Eredivisie (eredivisie.csv)
- Russian Premier Liga (premier-liga.csv)

Neste projeto:

- Os dados de origem foram carregados manualmente no Google Cloud Storage como arquivos `.csv`; 

- O DW foi criado manualmente no BigQuery;

- Para o processamento e carga dos dados nas *dimensões* e *fato* foi utilizado o Google Dataproc com o PySpark;

- Para a criação do **Dataproc Cluster** e envio do **PySpark Job** foi utilizado o `gcloud` via Shell Script.

## Fases do desenvolvimento

- [x] Script para criar 


## Arquitetura

### Data Pipeline

![Image](data-pipeline.png)

### Data Warehouse

![Image](dw_schema.png)

## Estrutura do Projeto

### GCP

1. project-id criado para este projeto: `project-dev`;
2. Bucket criado para dados de origem: `bucket-football-transfer`;
3. Caminho para os arquivos csv: `bucket-football-transfer/csv-files/`;
4. Dataset criado no BigQuery: `dw-football-transfer`;
3. Dataproc Cluster: `football-transfer`.

### Cluster e Pyspark Job

O arquivo `sh/main.sh` é responsável por criar o cluster do dataproc e enviar o pyspark job. Para isso ele é auxiliado pelos arquivos `create_cluster.sh` e `submit_pyspark.sh`. O primeiro contém as configurações do cluster (região, tipo das máquinas virtuais, tipo de imagem, tempo máximo de inatividade e etc). O segundo arquivo contém informações do job e o do cluster que será utilizado, além de plugins necessários para algumas execuções.

### Arquivo de configuração

Os nomes de buckets, folders, tabelas, campos e demais informações necessárias sobre os arquivos de origem e tabelas de destino foram organizados no arquivo **json**: `configs/etl_football_transfer_config.json`.

### ETL

A fase de processamento e carga dos dados no DW encontra-se no arquivo `etl_football_transfer.py`, auxiliado pelos módulos: 
    - `utils`: Contém funções necessárias ao projeto como Criação de uma Sessão do Spark, funções para leitura e escrita de arquivos do GCS e BigQuery e etc. 
    - `etl_transform`: Contém funções de manipulação dos Spark DataFrames criados no projeto.

## Utilização

### Pré-configuração (OPCIONAL)

Deve-se realizar essas configurações apenas se a estrutura do projeto no GCP (project-id, dataset, bucket e etc) for diferente da apresentada anteriormente.

1. Altear `PROJECT_ID` e `CLUSTER_NAME`:

    No arquivo `sh/main.sh` deve-se substituir o nome do `PROJECT_ID` (`"project-dev"`) e do `CLUSTER_NAME` (`"football-transfer"`) pelo nome do projeto que será utilizado e o nome do cluster que desja criar.

    - **Opcional:** Pode-se ajustar o tempo máximo de inatividade do cluster antes de ser deletado automaticamente através do `--max-idle`. Padrão: 1200s.

2. Alterar informações no `configs/etl_football_transfer_config.json`:

    - source:
        - bucket: Trocar `"bucket-football-transfer"` pelo nome do bucket criado para os arquivos de origem;
        - folder: Trocar `"csv-files/"` pelo nome do folder onde os arquivos csv de origem estarão.

    - target:
        - project_id: Trocar `"project-dev"` pelo nome do projeto onde estará a tabela do BigQuery (O mesmo `project-id` definido no arquivo `main.sh`);
        - dataset: Trocar `"dw-football-transfer"` pelo nome do dataset onde estará a tabela do BigQuery;
        - temporary_bucket: Trocar `"bucket-temp/folder-temp"` pelo nome do bucket e folder criados para serem usados como caminho temporário (Necessário para a escrita de dados em uma tabela do BigQuery via Python).

3. Atualizar o `project-id` e o `dataset` do script `create_dw.sql` conforme definido no arquivo de configuração.

### Execução

- Rodar o script `create_dw.sql` diretamente no BigQuery;

Os demais passos podem ser executados no Google Cloud Shell ou [localmente](https://cloud.google.com/sdk/docs/install?hl=pt-br):


- Instalação (se já não tiver instalado) do [build](https://pypa-build.readthedocs.io/en/latest/):
        
    ```Shell
    python -m pip install build
    ```
    
- Criação do build:

    ```Shell
    python -m build
    ```

    Essa etapa vai criar o arquivo `/dist/etl_football_transfer-0.0.1-py3-none-any.whl`. Isso é necessário para que a estrutura do projeto (diretórios e módulos) seja mantida ao enviar o Pyspark Job.

- Rodar o arquivo `main.sh`:

    Na raíz do projeto, executar:

    ```Shell
    ./sh/main.sh
    ```