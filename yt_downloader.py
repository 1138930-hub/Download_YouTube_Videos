
"""
Um aplicativo simples com interface gráfica para baixar vídeos do YouTube.

Este programa usa:
- customtkinter: Para criar a interface gráfica moderna.
- pytubefix: Uma versão corrigida do 'pytube' para lidar com os downloads do YouTube.
- threading: Para garantir que a interface não congele durante o download.
"""

import customtkinter as ctk
from pytubefix import YouTube  # Usando a versão 'fix' que você incluiu
import threading

class App(ctk.CTk):
    """
    Define a classe principal do nosso aplicativo, que herda do CustomTkinter
    e controla todos os elementos da interface e a lógica.
    """
    def __init__(self):
        super().__init__()

        # --- 1. Configuração da Janela Principal ---
        self.title("Baixador de Vídeos do YouTube")
        self.geometry("720x300") # Aumentei um pouco a altura para as mensagens
        self.grid_columnconfigure(0, weight=1)

        # Aparência do aplicativo
        ctk.set_appearance_mode("system")
        
        # --- 2. Criação dos Componentes (Widgets) ---

        # Rótulo (Label) do Título
        self.rotulo_titulo = ctk.CTkLabel(self, text="Insira o Link do Vídeo do YouTube", font=ctk.CTkFont(size=20, weight="bold"))
        self.rotulo_titulo.pack(padx=10, pady=(20, 10))

        # Campo de Entrada (Entry) para a URL
        self.variavel_url = ctk.StringVar()
        self.campo_url = ctk.CTkEntry(self, textvariable=self.variavel_url, width=500, height=40, placeholder_text="Cole o link do YouTube aqui...")
        self.campo_url.pack(padx=20, pady=10)

        # Botão de Download
        self.botao_baixar = ctk.CTkButton(self, text="Baixar Vídeo", command=self.iniciar_thread_de_download, height=40)
        self.botao_baixar.pack(padx=20, pady=10)

        # Rótulo de Status (onde daremos feedback ao usuário)
        self.rotulo_status = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=14))
        self.rotulo_status.pack(padx=20, pady=5)

        # Barra de Progresso
        self.barra_progresso = ctk.CTkProgressBar(self, width=500, height=15)
        self.barra_progresso.set(0) # Inicia em 0%
        self.barra_progresso.pack(padx=20, pady=10)

    # --- 3. Funções de Lógica ---

    def iniciar_thread_de_download(self):
        """
        Esta função é chamada quando o botão "Baixar" é clicado.
        Ela inicia o download em uma "thread" (processo) separada
        para evitar que a interface gráfica congele.
        """
        url = self.variavel_url.get()
        if not url:
            self.atualizar_status("Opa! Parece que você esqueceu de colar o link.", "orange")
            return

        # Desabilita o botão para evitar cliques duplos
        self.botao_baixar.configure(state="disabled", text="Baixando...")
        self.barra_progresso.set(0)
        self.atualizar_status("Conectando ao YouTube...", "cyan")

        # Cria e inicia a thread. O 'daemon=True' garante que a thread
        # feche junto com o programa principal.
        thread_de_download = threading.Thread(target=self.processar_download, args=(url,), daemon=True)
        thread_de_download.start()

    def processar_download(self, url):
        """
        Esta é a função que realmente faz o trabalho pesado.
        Ela roda na thread separada.
        IMPORTANTE: Esta função NÃO PODE atualizar a interface diretamente.
        """
        try:
            # Cria o objeto YouTube e registra as funções de "callback"
            # (funções que são chamadas automaticamente pelo pytube)
            video = YouTube(url, 
                            on_progress_callback=self.ao_progredir, 
                            on_complete_callback=self.ao_completar)
            
            # Pega o stream (fluxo) de maior resolução que tenha áudio e vídeo juntos
            stream_escolhido = video.streams.get_highest_resolution()
            
            # Informa o título (de forma segura para a thread)
            # self.after(0, ...) agenda a atualização na thread principal da GUI
            self.after(0, lambda: self.atualizar_status(f"Baixando: {video.title}", "white"))
            
            # Inicia o download!
            stream_escolhido.download()

        except Exception as e:
            # Se algo der errado (vídeo indisponível, link errado, etc.)
            self.after(0, lambda: self.lidar_com_erro(str(e)))

    # --- 4. Callbacks (Funções chamadas pelo Pytube) ---

    def ao_progredir(self, stream, pedaco_dados, bytes_restantes):
        """
        Callback chamado continuamente pelo pytube durante o download.
        """
        tamanho_total = stream.filesize
        bytes_baixados = tamanho_total - bytes_restantes
        porcentagem = (bytes_baixados / tamanho_total)
        
        # Agenda a atualização da barra de progresso na thread principal
        self.after(0, lambda: self.atualizar_progresso_na_tela(porcentagem))

    def atualizar_progresso_na_tela(self, porcentagem):
        """
        Esta função ATUALIZA A GUI e, por isso, só pode ser chamada
        pela thread principal (através do self.after).
        """
        self.barra_progresso.set(porcentagem)
        self.rotulo_status.configure(text=f"Progresso: {int(porcentagem * 100)}%")

    def ao_completar(self, stream, caminho_arquivo):
        """
        Callback chamado pelo pytube quando o download termina com sucesso.
        """
        self.after(0, lambda: self.atualizar_status(f"Sucesso! Vídeo salvo em:\n{caminho_arquivo}", "green"))
        # Reabilita o botão e muda o texto
        self.after(0, lambda: self.botao_baixar.configure(state="normal", text="Baixar Outro Vídeo"))
        self.after(0, lambda: self.barra_progresso.set(0)) # Reseta a barra

    def lidar_com_erro(self, mensagem_erro):
        """
        Função chamada para tratar qualquer erro que ocorrer na thread de download.
        """
        self.atualizar_status(f"Deu ruim... Erro: {mensagem_erro}", "red")
        self.botao_baixar.configure(state="normal", text="Tentar Novamente")
        self.barra_progresso.set(0)

    def atualizar_status(self, mensagem, cor="white"):
        """
        Função "helper" (ajudante) para centralizar a atualização do
        rótulo de status e sua cor.
        """
        self.rotulo_status.configure(text=mensagem, text_color=cor)


# --- Ponto de Entrada Principal ---
if __name__ == "__main__":
    # Cria a instância da nossa classe de aplicativo
    janela_principal = App()
    # Inicia o loop principal da interface (mantém a janela aberta)
    janela_principal.mainloop()