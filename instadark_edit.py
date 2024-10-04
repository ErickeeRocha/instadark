import os
import tkinter as tk
from tkinter import filedialog, messagebox
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip

def selecionar_pasta_videos():
    pasta_videos = filedialog.askdirectory(title="Selecione a pasta com os vídeos")
    entry_pasta_videos.delete(0, tk.END)
    entry_pasta_videos.insert(0, pasta_videos)

def selecionar_logomarca():
    logomarca_path = filedialog.askopenfilename(title="Selecione a Logomarca", filetypes=[("Arquivos PNG", "*.png"), ("Todos os Arquivos", "*.*")])
    entry_logomarca.delete(0, tk.END)
    entry_logomarca.insert(0, logomarca_path)

def adicionar_logomarca():
    pasta_videos = entry_pasta_videos.get()
    logomarca_path = entry_logomarca.get()
    
    if not os.path.exists(pasta_videos) or not os.path.exists(logomarca_path):
        messagebox.showerror("Erro", "Caminho da pasta ou logomarca inválidos. Verifique e tente novamente.")
        return

    # Criar pasta para vídeos editados
    pasta_editados = os.path.join(pasta_videos, "videos_editados")
    os.makedirs(pasta_editados, exist_ok=True)

    # Processar todos os arquivos de vídeo na pasta
    for arquivo in os.listdir(pasta_videos):
        if arquivo.endswith(".mp4"):
            video_path = os.path.join(pasta_videos, arquivo)
            video = VideoFileClip(video_path)

            # Criar a logomarca
            logomarca = ImageClip(logomarca_path).set_duration(video.duration).resize(height=300)  # Aumenta a altura da logomarca
            logomarca = logomarca.set_opacity(0.3).set_position(("center", "center"))

            # Reduzir o volume do áudio
            video = video.volumex(0.995)  # Reduz o volume em 0,5%

            # Criar o vídeo com logomarca
            video_com_logomarca = CompositeVideoClip([video, logomarca])

            # Salvar o vídeo editado sem o áudio separado
            video_saida = os.path.join(pasta_editados, f"edited_{arquivo}")
            video_com_logomarca.write_videofile(video_saida, codec='libx264', audio_codec='aac')

    messagebox.showinfo("Sucesso", "Edição concluída! Vídeos salvos na pasta 'videos_editados'.")

# Interface Tkinter
root = tk.Tk()
root.title("Edição de Vídeos")
root.geometry("500x300")
root.configure(bg='#1f1f1f')

# Estilos
fonte_padrao = ("Helvetica", 12)
fonte_titulo = ("Helvetica", 14, "bold")
cor_fundo = '#1f1f1f'
cor_fonte = '#ffffff'
cor_botao = '#4caf50'
cor_botao_claro = '#00bfa5'

# Título
titulo = tk.Label(root, text="Ferramenta de Edição de Vídeos", font=fonte_titulo, bg=cor_fundo, fg=cor_fonte)
titulo.pack(pady=10)

# Campo para selecionar pasta de vídeos
tk.Label(root, text="Pasta de Vídeos:", bg=cor_fundo, fg=cor_fonte, font=fonte_padrao).pack(pady=5)
entry_pasta_videos = tk.Entry(root, width=50, font=fonte_padrao)
entry_pasta_videos.pack(pady=5)
btn_selecionar_pasta = tk.Button(root, text="Selecionar Pasta", command=selecionar_pasta_videos, bg=cor_botao_claro, fg=cor_fonte, font=fonte_padrao)
btn_selecionar_pasta.pack(pady=5)

# Campo para selecionar logomarca
tk.Label(root, text="Logomarca:", bg=cor_fundo, fg=cor_fonte, font=fonte_padrao).pack(pady=5)
entry_logomarca = tk.Entry(root, width=50, font=fonte_padrao)
entry_logomarca.pack(pady=5)
btn_selecionar_logomarca = tk.Button(root, text="Selecionar Logomarca", command=selecionar_logomarca, bg=cor_botao_claro, fg=cor_fonte, font=fonte_padrao)
btn_selecionar_logomarca.pack(pady=5)

# Botão para adicionar logomarca e editar vídeos
btn_confirmar_edicao = tk.Button(root, text="Confirmar e Editar Vídeos", command=adicionar_logomarca, bg=cor_botao, fg=cor_fonte, font=fonte_padrao)
btn_confirmar_edicao.pack(pady=20)

# Rodapé com o texto "CRIADO POR: @japablackhat"
rodape = tk.Label(root, text="CRIADO POR: @japablackhat", font=("Helvetica", 10), bg=cor_fundo, fg=cor_fonte)
rodape.pack(pady=10)

root.mainloop()