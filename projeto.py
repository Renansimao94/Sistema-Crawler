import tkinter as tk
from tkinter import ttk, scrolledtext
import requests
from bs4 import BeautifulSoup
import json

# Função para fazer o crawling e exibir os resultados
def fetch_url():
    url = entry_url.get()
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Parseia o HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            text_html.delete('1.0', tk.END)
            text_html.insert(tk.END, soup.prettify())
            
            # Extrai os links
            links = [a['href'] for a in soup.find_all('a', href=True)]
            text_links.delete('1.0', tk.END)
            text_links.insert(tk.END, '\n'.join(links))
            
            # Tenta converter o HTML para JSON
            try:
                data_json = soup.get_text()
                json_object = json.loads(data_json)
                text_json.delete('1.0', tk.END)
                text_json.insert(tk.END, json.dumps(json_object, indent=4))
            except json.JSONDecodeError:
                text_json.delete('1.0', tk.END)
                text_json.insert(tk.END, "Não foi possível converter o HTML para JSON.")
        else:
            text_html.delete('1.0', tk.END)
            text_html.insert(tk.END, f'Erro: Status Code {response.status_code}')
            text_json.delete('1.0', tk.END)
            text_links.delete('1.0', tk.END)
    except requests.exceptions.RequestException as e:
        text_html.delete('1.0', tk.END)
        text_html.insert(tk.END, str(e))
        text_json.delete('1.0', tk.END)
        text_links.delete('1.0', tk.END)

# Configuração da janela principal
root = tk.Tk()
root.title("Crawler de Site com Tkinter")

# Campo de entrada para a URL
entry_url = ttk.Entry(root, width=50)
entry_url.pack(pady=10)

# Botão para iniciar o crawling
fetch_button = ttk.Button(root, text="Buscar", command=fetch_url)
fetch_button.pack(pady=5)

# Área de texto para exibir o HTML
label_html = ttk.Label(root, text="HTML:")
label_html.pack()
text_html = scrolledtext.ScrolledText(root, height=10)
text_html.pack()

# Área de texto para exibir o JSON
label_json = ttk.Label(root, text="JSON:")
label_json.pack()
text_json = scrolledtext.ScrolledText(root, height=10)
text_json.pack()

# Área de texto para exibir os links
label_links = ttk.Label(root, text="Links:")
label_links.pack()
text_links = scrolledtext.ScrolledText(root, height=10)
text_links.pack()

# Executa a aplicação
root.mainloop()
