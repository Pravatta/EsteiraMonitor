import os
import subprocess
import re
import warnings

# Ignora avisos desnecessários
warnings.filterwarnings("ignore", category=UserWarning)

# Lista de esteiras para configurar
esteiras = [1, 2, 3, 4, 5, 6, 7, 8]

# Define o caminho do script; usa variável de ambiente para flexibilidade
script_path = os.getenv("SCRIPT_PATH", "controle_esteira.py")

def kill_process(port):
    """
    Encerra processos que usam a porta especificada.
    """
    try:
        result = subprocess.check_output(f"netstat -ano | findstr :{port}", shell=True).decode()
        if result:
            lines = result.strip().split('\n')
            for line in lines:
                parts = re.split(r'\s+', line)
                pid = parts[-1]
                if pid.isdigit() and pid != '0':
                    subprocess.check_call(f"taskkill /PID {pid} /F", shell=True)
                    print(f"Processo na porta {port} encerrado.")
    except subprocess.CalledProcessError as e:
        if "No matching processes" not in str(e):
            print(f"Erro ao encerrar processo na porta {port}: {e}")
    except Exception as e:
        print(f"Erro inesperado ao encerrar processo na porta {port}: {e}")

def run_streamlit(esteira):
    """
    Inicia o Streamlit em uma porta calculada para a esteira.
    """
    port = 8500 + esteira
    os.environ['STREAMLIT_SERVER_PORT'] = str(port)
    kill_process(port)
    command = f"streamlit run {script_path} --server.port {port}"
    subprocess.Popen(command, shell=True)

if __name__ == "__main__":
    for esteira in esteiras:
        run_streamlit(esteira)
