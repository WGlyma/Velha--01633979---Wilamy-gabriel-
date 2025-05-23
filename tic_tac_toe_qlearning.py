import pygame
import random
import pickle
import numpy as np
import matplotlib.pyplot as plt  # NOVO

# Inicializando o pygame
pygame.init()

# CONFIGURAÇÕES DO JOGO
LARGURA, ALTURA = 300, 340
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Tic-Tac-Toe com Q-Learning")
FONTE = pygame.font.SysFont(None, 40)

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)

# AMBIENTE
class TicTacToe:
    def __init__(self):
        self.reset()

    def reset(self):
        self.board = [' ' for _ in range(9)]
        self.done = False
        self.winner = None
        return tuple(self.board)

    def available_actions(self):
        return [i for i, x in enumerate(self.board) if x == ' ']

    def make_move(self, pos, player):
        if self.board[pos] == ' ':
            self.board[pos] = player
            self.check_winner()
            return True
        return False

    def check_winner(self):
        combos = [(0,1,2), (3,4,5), (6,7,8),
                  (0,3,6), (1,4,7), (2,5,8),
                  (0,4,8), (2,4,6)]
        for (i,j,k) in combos:
            if self.board[i] == self.board[j] == self.board[k] != ' ':
                self.done = True
                self.winner = self.board[i]
                return
        if ' ' not in self.board:
            self.done = True
            self.winner = 'Empate'

    def render(self):
        TELA.fill(BRANCO)
        for i in range(1, 3):
            pygame.draw.line(TELA, PRETO, (0, i * 100), (300, i * 100), 2)
            pygame.draw.line(TELA, PRETO, (i * 100, 0), (i * 100, 300), 2)
        for i in range(9):
            x = (i % 3) * 100 + 40
            y = (i // 3) * 100 + 30
            if self.board[i] != ' ':
                texto = FONTE.render(self.board[i], True, VERMELHO if self.board[i] == 'X' else PRETO)
                TELA.blit(texto, (x, y))
        pygame.display.flip()

# AGENTE
class QAgent:
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=1.0, epsilon_decay=0.995, min_epsilon=0.1):
        self.q_table = {}
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.min_epsilon = min_epsilon

    def get_state_key(self, state):
        return str(state)

    def choose_action(self, state, actions):
        key = self.get_state_key(state)
        if random.random() < self.epsilon:
            return random.choice(actions)
        q_values = self.q_table.get(key, [0]*9)
        max_q = -float('inf')
        best_action = random.choice(actions)
        for a in actions:
            if q_values[a] > max_q:
                max_q = q_values[a]
                best_action = a
        return best_action

    def learn(self, state, action, reward, next_state):
        key = self.get_state_key(state)
        next_key = self.get_state_key(next_state)
        if key not in self.q_table:
            self.q_table[key] = [0] * 9
        if next_key not in self.q_table:
            self.q_table[next_key] = [0] * 9
        old_value = self.q_table[key][action]
        next_max = max(self.q_table[next_key])
        new_value = old_value + self.alpha * (reward + self.gamma * next_max - old_value)
        self.q_table[key][action] = new_value

    def update_epsilon(self):
        self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)

# TREINAMENTO 
def train_agent(agent, env, episodes=5000):
    history = {'episodios': [], 'vitorias': [], 'derrotas': [], 'empates': []}
    vit, der, emp = 0, 0, 0

    for ep in range(episodes):
        state = env.reset()
        done = False
        player_turn = 'X'

        while not done:
            if player_turn == 'X':
                actions = env.available_actions()
                action = agent.choose_action(state, actions)
                env.make_move(action, 'X')
                next_state = tuple(env.board)
                env.check_winner()
                done = env.done

                if done:
                    if env.winner == 'X':
                        reward = 1
                        vit += 1
                    elif env.winner == 'Empate':
                        reward = 0.5
                        emp += 1
                    else:
                        reward = -1
                        der += 1
                else:
                    reward = 0
                agent.learn(state, action, reward, next_state)
                state = next_state
                player_turn = 'O'

            else:
                actions = env.available_actions()
                if not actions:
                    break
                action = random.choice(actions)
                env.make_move(action, 'O')
                env.check_winner()
                done = env.done
                if done:
                    if env.winner == 'O':
                        reward = -1
                        der += 1
                        agent.learn(state, action, reward, state)
                    elif env.winner == 'Empate':
                        reward = 0.5
                        emp += 1
                        agent.learn(state, action, reward, state)
                player_turn = 'X'

        agent.update_epsilon()

        if (ep + 1) % 100 == 0:
            history['episodios'].append(ep + 1)
            history['vitorias'].append(vit)
            history['derrotas'].append(der)
            history['empates'].append(emp)
            print(f'Episódio {ep+1}: Vitórias={vit}, Derrotas={der}, Empates={emp}')
            vit, der, emp = 0, 0, 0

    #  RESULTADOS
    plt.figure(figsize=(10, 5))
    plt.plot(history['episodios'], history['vitorias'], label='Vitórias', color='green')
    plt.plot(history['episodios'], history['derrotas'], label='Derrotas', color='red')
    plt.plot(history['episodios'], history['empates'], label='Empates', color='blue')
    plt.xlabel('Episódios')
    plt.ylabel('Quantidade')
    plt.title('Desempenho do Agente durante o Treinamento')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("grafico_desempenho.png")  # ← SALVA A IMAGEM
    plt.show()

# GAMEPLAY COM PLACAR
def play_against_agent(agent, env):
    running = True
    clock = pygame.time.Clock()
    state = env.reset()
    player_turn = True
    placar = {'Jogador': 0, 'Agente': 0, 'Empates': 0}

    while running:
        env.render()
        texto_placar = FONTE.render(f"Jogador: {placar['Jogador']}  Agente: {placar['Agente']}  Empates: {placar['Empates']}", True, PRETO)
        pygame.draw.rect(TELA, BRANCO, (0, ALTURA - 40, LARGURA, 40))
        TELA.blit(texto_placar, (10, ALTURA - 35))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                return
            if player_turn and event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if y < 300:
                    col = x // 100
                    row = y // 100
                    pos = row * 3 + col
                    if pos in env.available_actions():
                        env.make_move(pos, 'O')
                        env.check_winner()
                        player_turn = False

        if not player_turn and not env.done:
            state = tuple(env.board)
            actions = env.available_actions()
            action = agent.choose_action(state, actions)
            env.make_move(action, 'X')
            env.check_winner()
            player_turn = True

        if env.done:
            env.render()
            pygame.time.wait(1000)
            if env.winner == 'O':
                placar['Jogador'] += 1
            elif env.winner == 'X':
                placar['Agente'] += 1
            else:
                placar['Empates'] += 1
            state = env.reset()
            player_turn = True
        clock.tick(30)

# MAIN
def main():
    env = TicTacToe()
    agent = QAgent()
    train_agent(agent, env, episodes=5000)
    play_against_agent(agent, env)

if __name__ == "__main__":
    main()
