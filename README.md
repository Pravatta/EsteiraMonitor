
# Exibição e Controle Logístico em Esteiras Industriais

Este sistema exibe em tempo real informações detalhadas sobre os produtos na esteira de transporte, auxiliando a equipe a monitorar o fluxo de caixas, seus status e atualizações instantâneas.

![image](https://github.com/user-attachments/assets/fa1881c4-87a8-45a1-ae8e-d1a9b96d592d)

---
🔍 Ponto Importante

O sistema é totalmente dependente dos dados provenientes do Sorter, que está integrado ao banco de dados. Todas as informações que aparecem no sistema, como caixas processadas, rejeitadas e faltantes, são registradas automaticamente no banco assim que passam pelo Sorter. A lógica do script utiliza essas informações em tempo real para exibir os dados atualizados nas telas. Portanto, é fundamental que o banco de dados esteja configurado corretamente e sincronizado com o Sorter para o sistema funcionar adequadamente.

## 📋 **Funcionalidades**

- **Exibição do Manifesto:**
  - Número do manifesto.
  - Esteira em operação.
  - Frota associada ao manifesto.
  - Hora atual do processamento.
  - Duração da execução.
  - Totais: quantidade de produtos, caixas que passaram, rejeitadas e faltantes.
  - Informações sobre caixas lidas fora do contexto.

- **Atualização do Manifesto:**
  - Permite trocar e atualizar os dados para refletir o manifesto mais recente.

- **Gerenciamento de Exibição:**
  - Controle eficiente de janelas de exibição para várias esteiras em computadores conectados.

- **Visibilidade do Fluxo:**
  - Informações claras e em tempo real para gestão logística eficiente.

---

## 🛠️ **Tecnologias Utilizadas**

- **Python**: Automação e backend do sistema.
- **Streamlit**: Criação de interface web para exibição em tempo real.
- **Tkinter**: Interface gráfica para atualização do manifesto.
- **MySQL Connector**: Conexão com o banco de dados.
- **ODBC**: Integração com SQL Server.
- **Pandas**: Manipulação de dados.
- **PyODBC**: Consultas ao banco de dados SQL.

---

## 🚀 **Como Executar**

### 1️⃣ **Pré-requisitos**
- Instale o Python 3.8 ou superior ([Clique aqui para baixar](https://www.python.org/)).
- Configure o banco de dados com as tabelas e informações necessárias.

### 2️⃣ **Clone o Repositório**
Abra o terminal e execute os comandos abaixo:
```bash
mkdir ExibicaoManifesto
cd ExibicaoManifesto
git clone https://github.com/seu-usuario/seu-repositorio.git
```

### 3️⃣ **Instale as Dependências**
Ainda no terminal, navegue até a pasta do repositório clonado e instale as bibliotecas necessárias:
```bash
pip install streamlit mysql-connector-python pandas pyodbc
```

### 4️⃣ **Configure o Banco de Dados**
No arquivo `controle_esteira.py`, edite a variável `DB_CONFIG` com as credenciais do seu banco de dados SQL Server:
```python
DB_CONFIG = {
    "server": "seu-servidor",
    "database": "sua-base-de-dados",
    "username": "seu-usuario",
    "password": "sua-senha",
    "driver": "{ODBC Driver 17 for SQL Server}",
}
```
Certifique-se de que as tabelas e colunas no banco de dados estejam conforme as consultas SQL definidas no código.

### 5️⃣ **Atualize o Manifesto**
Execute o script `atualizar_manifesto.py` para alterar o manifesto atual. No terminal, digite:
```bash
python atualizar_manifesto.py
```
- Uma janela será exibida solicitando o código do novo manifesto (8 caracteres).
- Após inserir o código e confirmar, o manifesto será atualizado no sistema e refletirá nos monitores em tempo real.

**Importante:**
- Existe uma versão `.exe` do `atualizar_manifesto.py`, utilizada pela equipe de logística. Essa versão permite a atualização fácil do manifesto por meio de um arquivo compartilhado (`ultimo_manifesto.txt`), garantindo sincronização imediata com os monitores.

### 6️⃣ **Inicie as Janelas de Exibição**
Para abrir as janelas de exibição e monitorar os dados das esteiras, execute:
```bash
streamlit run abrir_janelas_esteira.py
```
- As janelas serão exibidas automaticamente em portas diferentes para cada esteira configurada.
- Utilize múltiplos monitores, se disponíveis, para melhorar a visualização dos dados.
- **Deixe este script rodando continuamente para manter o sistema ativo, idealmente operando 24 horas por dia.**

### 7️⃣ **Controle de Esteira**
O script `controle_esteira.py` é o núcleo do sistema e não deve ser alterado diretamente. Ele é responsável por gerenciar toda a lógica de exibição e conexão com o banco de dados.

## 🗄️ **Configuração do Banco de Dados**

O sistema utiliza o **SQL Server** para armazenar e processar as informações das esteiras e dos manifestos. A seguir, explicamos como configurar o banco de dados para utilizar o sistema com os seus próprios dados.

---

## 📂 **Arquivos Importantes**

- `controle_esteira.py`: **Script principal para exibição de dados. Não deve ser modificado diretamente.**
- `abrir_janelas_esteira.py`: Abre janelas para diferentes esteiras e deve ser mantido rodando continuamente.
- `atualizar_manifesto.py`: Atualiza o manifesto exibido no sistema, com versão `.exe` para uso pela logística.
- `ultimo_manifesto.txt`: Armazena o último manifesto processado e é atualizado automaticamente.
- `.gitignore`: Ignora arquivos desnecessários no repositório.

---

## ⚠️ **Observações Importantes**

1. Certifique-se de que os drivers do ODBC para SQL Server estão instalados no sistema.
2. Caso encontre erros ao executar os scripts, reinstale as bibliotecas necessárias:
   ```bash
   pip install --force-reinstall nome-da-biblioteca
   ```
3. Para melhor desempenho, utilize um computador com múltiplos monitores e boa conectividade de rede.
4. A atualização do manifesto por meio do `.exe` é essencial para operações em tempo real e sincronização com os monitores.

---

## 🔑 **Configuração do Banco de Dados**

### Estrutura Necessária

#### **Tabela: DT6010**

Armazena informações sobre as frotas e as esteiras.

```sql
CREATE TABLE DT6010 (
    DT6_FROTA VARCHAR(50),       -- Identificador da frota
    DT6_PEDCLI VARCHAR(50),      -- Código do pedido ou manifesto
    DT6_SORTER INT               -- Número da esteira
);
```

#### **Tabela: Tcubagem**

Registra detalhes sobre o fluxo de caixas processadas e seus respectivos status.

```sql
CREATE TABLE Tcubagem (
    data DATETIME,               -- Data e hora do processamento
    saida_prog INT,              -- Esteira programada para a saída
    saida_env INT,               -- Esteira que realmente processou a caixa
    STATUS INT,                  -- Status da caixa (ex.: 2 = sucesso, 888 = lido fora de contexto)
    pedcli VARCHAR(50)           -- Código do pedido ou manifesto
);
```

#### **Tabela: DTC010**

Contém informações detalhadas de cada caixa, incluindo status de processamento.

```sql
CREATE TABLE DTC010 (
    DTC_ETIQUE VARCHAR(50),      -- Etiqueta única identificadora da caixa
    DTC_QTDVOL INT,              -- Quantidade de volumes associados à etiqueta
    DTC_DESTINATARIO VARCHAR(50),-- Nome do cliente ou destinatário
    Caixas_Esteira INT,          -- Quantidade de caixas que passaram pela esteira
    Caixas_Rejeito INT,          -- Quantidade de caixas rejeitadas
    Caixas_Bipada INT            -- Quantidade de caixas bipadas (escaneadas)
);
```

---

### Populando o Banco de Dados

Após criar as tabelas, insira alguns dados iniciais para testar o sistema. Aqui estão exemplos de inserção:

#### Inserindo dados na tabela `DT6010`:

```sql
INSERT INTO DT6010 (DT6_FROTA, DT6_PEDCLI, DT6_SORTER)
VALUES 
('Frota01', '001CAB87', 1),
('Frota02', '001CAB88', 2);
```

#### Inserindo dados na tabela `Tcubagem`:

```sql
INSERT INTO Tcubagem (data, saida_prog, saida_env, STATUS, pedcli)
VALUES
(GETDATE(), 1, 1, 2, '001CAB87'),
(GETDATE(), 2, 2, 888, '001CAB88');
```

#### Inserindo dados na tabela `DTC010`:

```sql
INSERT INTO DTC010 (DTC_ETIQUE, DTC_QTDVOL, DTC_DESTINATARIO, Caixas_Esteira, Caixas_Rejeito, Caixas_Bipada)
VALUES
('ETQ001', 10, 'Cliente A', 8, 1, 1),
('ETQ002', 15, 'Cliente B', 10, 2, 3);
```

---

### Configurando o Sistema

Edite o arquivo `controle_esteira.py` para configurar as credenciais do banco de dados na variável `DB_CONFIG`:

```python
DB_CONFIG = {
    "server": "SEU_SERVIDOR",               # Exemplo: "localhost" ou "192.168.1.100"
    "database": "NOME_DO_BANCO_DE_DADOS",   # Exemplo: "ExibicaoManifesto"
    "username": "SEU_USUARIO",              # Exemplo: "sa"
    "password": "SUA_SENHA",                # Exemplo: "senha123"
    "driver": "{ODBC Driver 17 for SQL Server}"  # Driver ODBC instalado no sistema
}
```

Certifique-se de que o servidor de banco de dados esteja acessível e que o usuário tenha permissões para acessar as tabelas.

---

### Ajustando o Código para o Seu Banco

Se você utilizar nomes diferentes para tabelas ou colunas, ajuste as consultas SQL no código para refletir essas alterações.

#### Exemplo:

Na função `run_queryf`, o código utiliza a seguinte consulta:

```sql
SELECT DISTINCT DT6_FROTA 
FROM DT6010 
WHERE DT6_PEDCLI = '001CAB87' AND DT6_SORTER = ?
```

Se o identificador `'001CAB87'` variar, configure-o como uma variável:

```python
PEDCLI = os.getenv("PEDCLI", "001CAB87")  # Configurável por ambiente
```

E altere a consulta para:

```sql
SELECT DISTINCT DT6_FROTA 
FROM DT6010 
WHERE DT6_PEDCLI = ? AND DT6_SORTER = ?
```

Passe os parâmetros dinamicamente no código:

```python
params=(PEDCLI, esteira)
```

---

### Dependências Necessárias

Certifique-se de instalar os drivers e bibliotecas necessárias:

- **Drivers ODBC**: [Baixe o ODBC Driver 17 para SQL Server](https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server).
- **Bibliotecas Python**:
  ```bash
  pip install streamlit mysql-connector-python pandas pyodbc
  ```

---

### Testando a Conexão

Para garantir que o sistema consegue se conectar ao banco de dados, execute este script no Python:

```python
import pyodbc

conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=SEU_SERVIDOR;"
    "DATABASE=NOME_DO_BANCO_DE_DADOS;"
    "UID=SEU_USUARIO;"
    "PWD=SUA_SENHA;"
)
print("Conexão bem-sucedida!")
conn.close()
```

Se a mensagem **"Conexão bem-sucedida!"** aparecer, o banco está configurado corretamente.


---

### ✅ **Lista de Verificação Final**

- [ ] **Banco de Dados Configurado:**  
  - As tabelas `DT6010`, `Tcubagem` e `DTC010` foram criadas.
  - Dados de teste foram inseridos nas tabelas.
  - O servidor de banco de dados está acessível.

- [ ] **Dependências Instaladas:**  
  - Python 3.8 ou superior instalado.
  - Bibliotecas necessárias (`streamlit`, `mysql-connector-python`, `pandas`, `pyodbc`) instaladas via `pip`.
  - Driver ODBC para SQL Server configurado no sistema operacional.

- [ ] **Credenciais Configuradas:**  
  - O arquivo `controle_esteira.py` foi editado para incluir as credenciais corretas do banco de dados na variável `DB_CONFIG`.

- [ ] **Configuração do Código SQL:**  
  - Todas as consultas SQL foram ajustadas para refletir as tabelas e colunas usadas no banco de dados do sistema.

- [ ] **Testes de Conexão Realizados:**  
  - Testou a conexão com o banco de dados usando o script de exemplo fornecido.

- [ ] **Scripts Operacionais:**  
  - `controle_esteira.py` está pronto e configurado corretamente.
  - `atualizar_manifesto.py` foi testado e está funcionando para atualizar o manifesto.
  - `abrir_janelas_esteira.py` está rodando continuamente para exibição nas telas.

- [ ] **Ambiente Configurado:**  
  - Servidor com boa conectividade de rede para manter o sistema estável.
  - Computadores com múltiplos monitores para visualização eficiente.

---

Com essas etapas, qualquer pessoa conseguirá configurar o banco de dados e usar o sistema sem dificuldades. 🚀


![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![License](https://img.shields.io/badge/license-MIT-blue)
