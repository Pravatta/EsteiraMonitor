import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO

# Caminho do arquivo de configuração, agora usando variável de ambiente
CONFIG_FILE = os.getenv("CONFIG_FILE", "ultimo_manifesto.txt")

def load_last_manifesto():
    """
    Carrega o último manifesto salvo no arquivo de configuração.
    Retorna um código padrão se o arquivo não existir.
    """
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return f.read().strip()
    return "001CAB87"

def save_last_manifesto(manifesto):
    """
    Salva o novo manifesto no arquivo de configuração.
    """
    with open(CONFIG_FILE, 'w') as f:
        f.write(manifesto)

def atualizar_manifesto(novo_manifesto):
    """
    Atualiza o manifesto no arquivo e em outras referências.
    """
    print(f"Atualizando manifesto para: {novo_manifesto}")
    save_last_manifesto(novo_manifesto)

def on_submit():
    """
    Valida e salva o novo manifesto inserido pelo usuário.
    """
    novo_manifesto = entry.get().strip().upper()
    if len(novo_manifesto) == 8:
        atualizar_manifesto(novo_manifesto)
        messagebox.showinfo("Sucesso", f"Manifesto atualizado para {novo_manifesto}")
        root.quit()
    else:
        messagebox.showwarning("Erro", "O manifesto deve ter exatamente 8 caracteres.")

def to_uppercase(*args):
    """
    Força que o texto digitado seja convertido para maiúsculas.
    """
    entry_var.set(entry_var.get().upper())

# Interface gráfica
root = tk.Tk()
root.title("Atualizar Manifesto")
root.geometry("600x450")
root.configure(bg='#F5F5F5')

# Centraliza a janela
window_width = 600
window_height = 450
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
position_right = int(screen_width/2 - window_width/2)
position_down = int(screen_height/2 - window_height/2) - 50
root.geometry(f"{window_width}x{window_height}+{position_right}+{position_down}")

# Carrega o último manifesto
ultimo_manifesto = load_last_manifesto()

# Elementos da interface
title_label = tk.Label(root, text="Atualizar Código do Manifesto", font=("Arial", 20, "bold"), bg='#F5F5F5')
title_label.pack(pady=20)

entry_label = tk.Label(root, text="Insira o novo código do manifesto (8 caracteres):", font=("Arial", 14), bg='#F5F5F5')
entry_label.pack()

entry_var = tk.StringVar()
entry_var.trace("w", to_uppercase)

entry = tk.Entry(root, textvariable=entry_var, font=("Arial", 14), width=30)
entry.pack(pady=10)

submit_button = tk.Button(root, text="Atualizar", font=("Arial", 14, "bold"), bg='#1E90FF', fg='white', command=on_submit)
submit_button.pack(pady=20)

last_manifesto_label = tk.Label(root, text=f"Último Manifesto: {ultimo_manifesto}", font=("Arial", 12), bg='#F5F5F5')
last_manifesto_label.pack(pady=10)

root.mainloop()
