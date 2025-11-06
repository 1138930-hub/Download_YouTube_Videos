# 🚀 Downloader de Vídeos do YouTube
Este é um aplicativo de desktop simples que criei para baixar vídeos do YouTube diretamente para o computador. A ideia era construir uma ferramenta prática e, ao mesmo tempo, aprimorar minhas habilidades em Python e desenvolvimento de interfaces gráficas 
# ✨ Funcionalidades Principais
Interface Limpa e Moderna: Utiliza CustomTkinter para um visual agradável e responsivo. Busca de Opções: Cole um link e clique em "Baixar"; Uma barra de progresso e um rótulo de status informam exatamente o que está acontecendo (conectando, baixando, concluído ou se deu erro). Operação Segura: O download é feito em um processo separado (threading) para garantir que a interface do usuário nunca "congele".
# 🛠️ Tecnologias Utilizadas
Este projeto foi construído com as seguintes tecnologias:
Python 3: A linguagem de programação principal.
CustomTkinter: Uma biblioteca moderna baseada no Tkinter para criar a interface gráfica.
Pytube: Usada para buscar as informações e fazer o download dos vídeos e áudios do YouTube.
Threading: Módulo nativo do Python usado para executar o download em segundo plano.
# 💡 Como Foi Feito
Eu decidi criar este projeto como um desafio pessoal. O núcleo do projeto foi descobrir como "conversar" com o YouTube. Para isso, usei a biblioteca pytube, que faz todo o trabalho pesado de encontrar os streams (fluxos) de vídeo e áudio. O segundo grande desafio foi criar uma interface gráfica que não "congelasse" no momento em que o download começasse. Aprendi da maneira mais difícil que qualquer tarefa longa (como baixar um arquivo) trava a interface se for executada no mesmo processo.A solução foi usar o módulo threading do Python. Com ele, eu consigo iniciar o download em um "processo paralelo". Isso deixa a interface principal livre para continuar respondendo ao usuário, enquanto o download acontece em segundo plano. A parte mais legal foi integrar os callbacks do pytube com o CustomTkinter. Usei o método .after() para "agendar" atualizações na interface de forma segura, diretamente de dentro da thread de download. Foi assim que consegui fazer a barra de progresso e as mensagens de status funcionarem em tempo real!
# 🏃‍♂️ Como Rodar o ProjetoVocê pode rodar este projeto facilmente na sua máquina local.
1. Pré-requisitosVocê precisa ter o Python 3 instalado no seu computador.
2. InstalaçãoPrimeiro, clone este repositório (ou apenas baixe o arquivo .py). 
3. Agora, instale as bibliotecas necessárias:pip install customtkinter pytubefix.
4. ExecuçãoCom tudo instalado, basta rodar o script:python nome_do_seu_arquivo.py
# 📋 Como Usar o AplicativoAbra o aplicativo.
Copie um link de um vídeo do YouTube, cole o link no campo de entrada. 
Clique no botão "Baixar". 
Acompanhe o progresso na barra e nas mensagens de status.
O arquivo será salvo na mesma pasta onde o script .py está localizado.

'Este projeto é totalmente meu para fins de aprendizado e portfólio. Sinta-se à vontade para usar e modificar.'
