Nome do arquivo: 
 * Data de criação: 23/05/2025
 * Autor: Wilamy Gabriel
 * Matrícula: 01633979


❌ Jogo da Velha com Q-Learning


Projeto de aprendizado por reforço que treina um agente para jogar jogo da velha contra um oponente aleatório. O agente aprende estratégias para vencer, empatar e evitar derrotas, atualizando sua Q-Table dinamicamente.


📌 Objetivo



Treinar um agente capaz de jogar de forma inteligente, utilizando Q-Learning para maximizar vitórias e minimizar derrotas, aprendendo a partir das recompensas e penalidades.


🛠️ Tecnologias e Bibliotecas Utilizadas


Python 3.x

Pygame (interface gráfica)

Numpy (opcional para manipulação de dados)


📘 Algoritmo Utilizado


Q-Learning com estratégia ε-greedy para balancear exploração e exploração.

Fórmula de atualização:
Q[s][a] = Q[s][a] + α * (recompensa + γ * max(Q[s']) - Q[s][a])

α (alpha): taxa de aprendizado

γ (gamma): fator de desconto

ε (epsilon): taxa de exploração (decai ao longo do tempo)


🧪 Como Executar o Projeto


Clonar o repositório



Copiar
Editar
git clone <URL-do-seu-repo>
cd <pasta-do-repo>
Instalar dependências



nginx
Copiar
Editar
pip install pygame numpy
Executar o script principal



nginx
Copiar
Editar
python jogo_tictactoe.py



📊 Resultados Obtidos


Aprendizado progressivo do agente, aumentando o número de vitórias

Diminuição das derrotas e empates ao longo do treinamento

Visualização gráfica da partida em tempo real com placar atualizado


🧠 Dificuldades Encontradas

Ajuste da taxa de exploração para evitar que o agente fique preso em estratégias ruins

Definir recompensas e penalidades que guiem o aprendizado de forma eficiente

Balancear a velocidade do treinamento com a qualidade do aprendizado

✅ Comentários Finais

O projeto demonstra na prática os conceitos de aprendizado por reforço com Q-Learning, incluindo a exploração vs. exploração, atualização dinâmica da Q-Table e aprendizado com recompensas e penalidades.
