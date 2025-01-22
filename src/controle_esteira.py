from datetime import datetime
import time
import streamlit as st
import os
import pyodbc
import pandas as pd
import warnings


warnings.filterwarnings("ignore", category=UserWarning)
DB_CONFIG = {
    "server": os.getenv("DB_SERVER", "seu-servidor"),
    "database": os.getenv("DB_DATABASE", "sua-base-de-dados"),
    "username": os.getenv("DB_USERNAME", "usuario"),
    "password": os.getenv("DB_PASSWORD", "senha"),
    "driver": os.getenv("DB_DRIVER", "{ODBC Driver 17 for SQL Server}"),
}


def get_connection():
    try:
        conn_str = f'DRIVER={DB_CONFIG["driver"]};SERVER={DB_CONFIG["server"]};DATABASE={DB_CONFIG["database"]};UID={DB_CONFIG["username"]};PWD={DB_CONFIG["password"]}'
        return pyodbc.connect(conn_str)
    except Exception as e:
        st.error(f"Erro ao conectar ao banco de dados: {e}")
        raise

def formatted_table(df):
    df = df.reset_index(drop=True)
    styled_df = df.style.set_table_styles([
        {'selector': 'thead th', 'props': [('font-size', '20px'), ('color', 'white'), ('background-image', 'linear-gradient(to right, #4A90E2, #141E30)'), ('border-radius', '8px 8px 0 0'), ('padding', '10px'), ('text-align', 'center')]},
        {'selector': 'tbody td', 'props': [('font-size', '18px'), ('padding', '10px'), ('font-family', 'Arial, sans-serif'), ('border', '1px solid #dddddd'), ('text-align', 'center')]},
        {'selector': 'tbody td:nth-child(1)', 'props': [('background-color', '#f2f2f2')]},
        {'selector': 'tbody tr:nth-child(even) td', 'props': [('background-color', '#f7f7f7')]},
        {'selector': 'tbody tr:nth-child(odd) td', 'props': [('background-color', '#ffffff')]},
        {'selector': 'tbody tr:last-child td', 'props': [('border-radius', '0 0 8px 8px')]}
    ])
    return styled_df

def run_queryf(esteira):
    esteira = str(esteira)
    query = '''
            SELECT DISTINCT DT6_FROTA FROM DT6010 
            WHERE DT6_PEDCLI = '001CAB87' AND DT6_SORTER = ?
            '''
    with get_connection() as conn:
        df = pd.read_sql_query(query, conn, params=(esteira,))
    return df.values.tolist()

def run_query(esteira):
    esteira = esteira
    
    tmp = '''
            SELECT 
                CONVERT(varchar(8), DATEADD(minute, DATEDIFF(minute, MIN(data), MAX(data)), 0), 108) AS diferenca_tempo_hh_mm_ss
            FROM 
                Tcubagem
            WHERE 
                pedcli = '001CAB87' AND saida_env > 0;
            '''
    with get_connection() as conn:
        df1 = pd.read_sql_query(tmp, conn)
    tempo = df1.values.tolist()

    tot = '''
            SELECT 
                SUM(CASE 
                        WHEN saida_prog = ? THEN 1 
                        ELSE 0 
                    END) AS total,
                SUM(CASE 
                        WHEN saida_env = ? AND STATUS = 2 THEN 1 
                        ELSE 0 
                    END) AS saiu,
                SUM(CASE 
                        WHEN saida_prog = ? AND saida_env > 8 THEN 1 
                        ELSE 0 
                    END) AS rejeito,
                SUM(CASE 
                        WHEN saida_prog = ? AND saida_env < 1 THEN 1 
                        ELSE 0 
                    END) AS nao,
                SUM(CASE 
                        WHEN saida_env = ? AND STATUS = 888 THEN 1 
                        ELSE 0 
                    END) AS fora
            FROM 
                Tcubagem
            WHERE 
                pedcli = '001CAB87'
                AND (saida_prog = ? OR saida_env = ? OR saida_env > 8 OR saida_env < 1 OR STATUS = 888);
            '''
    with get_connection() as conn:
        df2 = pd.read_sql_query(tot, conn, params=(esteira, esteira, esteira, esteira, esteira, esteira, esteira))
    total = df2.values.tolist()
            
    query = '''
            SELECT DISTINCT
                D.DTC_ETIQUE AS Etiqueta,
                CONVERT(INT, D.DTC_QTDVOL) AS Total,
                SUBSTRING(D.DTC_DESTINATARIO, 1, 20) AS Cliente,
                CONVERT(INT, D.Caixas_Esteira) AS Passaram,
                CONVERT(INT, D.Caixas_Rejeito) AS Rejeitadas,
                (CONVERT(INT, D.DTC_QTDVOL) - CONVERT(INT, D.Caixas_Esteira) - CONVERT(INT, D.Caixas_Rejeito) - CONVERT(INT, D.Caixas_Bipada)) AS Faltantes,
                MAX(t.DATA) AS Data,
                T.Frota
            FROM DTC010 AS D
            LEFT JOIN TCUBAGEM AS T ON D.DTC_ETIQUE = SUBSTRING(T.ETIQUETA, 1, 9)
            WHERE D.DTC_PEDCLI = '001CAB87' AND SAIDA_PROG = ? AND DTC_QTDVOL <> D.Caixas_Esteira AND D.DTC_ETIQUE != ''
            GROUP BY D.DTC_ETIQUE, D.DTC_QTDVOL, D.DTC_DESTINATARIO, D.Caixas_Esteira, D.Caixas_Rejeito, D.Caixas_Bipada, T.Frota
            ORDER BY Data DESC;
            '''
    with get_connection() as conn:
        df = pd.read_sql_query(query, conn, params=(esteira,))
    df['Data'] = pd.to_datetime(df['Data']).dt.strftime('%d/%m/%Y %H:%M:%S')
    conn.close()
    return df, tempo, total

def inicializar():
    if 'conn' not in st.session_state:
        st.session_state.conn = get_connection()
    if 'dados' not in st.session_state:
        st.session_state.dados = None

def main():
    st.set_page_config(page_title="SQL Query Result", page_icon=":desktop_computer:", layout="wide")

    st.markdown("""
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        h1 {
            font-size: 24px;
        }
        table {
            font-size: 18px;
            width: 100%;
            margin-left: auto;
            margin-right: auto;
        }
        .stMarkdown div {
            display: flex;
            justify-content: space-between;
            font-size: 20px;
            width: 100%;
            margin-left: auto;
            margin-right: auto;
        }
        .title-container h1 {
            font-size: 32px; /* Font size for H1 style */
            font-weight: bold; /* Bold text for H1 style */
            margin: 0;
        }
        .title-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            width: 100%;
            margin-left: auto;
            margin-right: auto;
        }
        .align-right {
            margin-left: auto;
            font-size: 32px; /* Font size for H1 style */
            font-weight: bold; /* Bold text for H1 style */
            white-space: nowrap; /* Prevent line break */
        }
        .info-container {
            background-image: linear-gradient(to right, #4A90E2, #141E30); /* Lighter black */
            color: white;
            padding: 5px;
            border-radius: 8px;
            margin-bottom: 10px;
            display: flex;
            justify-content: space-between;
        }
        .stale-element {
            opacity: 1 !important; /* Ensure elements do not become opaque */
        }
        body {
            padding: 0; /* Remove default padding */
            margin: 0; /* Remove default margin */
        }
        .main .block-container {
            padding: 0 !important; /* Remove Streamlit's default padding */
        }
        </style>
    """, unsafe_allow_html=True)

    inicializar()

    port = os.getenv('STREAMLIT_SERVER_PORT')
    esteira = int(port) - 8500

    try:
        while True:
            frota = run_queryf(esteira)
            frotas = '-'.join(item[0] for item in frota)
            current_time = datetime.now().strftime('%H:%M:%S')
            st.markdown(f"""
                <div class="title-container">
                    <h1>Manifesto : 001CAB87</h1>
                    <h1>Esteira : {esteira}</h1>
                    <h1>Frota : {frotas}</h1>
                    <span class="align-right">Hora: {current_time}</span>
                </div>
            """, unsafe_allow_html=True)

            data, tmp, total = run_query(esteira)
            if tmp == []:
                tmp = [[0]]
            st.markdown(f"""
                <div class="info-container">
                    <span>Duração: {tmp[0][0]}</span>
                    <span>Total: {total[0][0]}</span>
                    <span>Passaram: {total[0][1]}</span>
                    <span>Rejeitadas: {total[0][2]}</span>
                    <span>Faltantes: {total[0][3]}</span>
                    <span>Lido Fora: {total[0][4]}</span>
                </div>
            """, unsafe_allow_html=True)
            if "Bipadas" in data.columns:
                data = data.drop(columns=["Bipadas"])
            styled_df = formatted_table(data)
            if not data.empty:
                st.write(styled_df.hide(axis='index').to_html(), unsafe_allow_html=True)
            else:
                st.write("No data available")
            time.sleep(5)
            st.rerun()
    except Exception as e:
        st.error(f"Erro fatal: {e}")

if __name__ == '__main__':
    main()
