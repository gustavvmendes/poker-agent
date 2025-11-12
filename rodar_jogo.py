# rodar_jogo.py (versão com a correção final no FoldPlayer)

from pypokerengine.api.game import setup_config, start_poker
from pypokerengine.players import BasePokerPlayer
from jogador_console import JogadorConsole
from meu_agente import AgenteSimples
from examples.players.fish_player import FishPlayer

# --- Jogador que sempre desiste (FoldPlayer) ---
# CORREÇÃO FINAL: Agora ele também retorna uma tupla (action, amount)
class FoldPlayer(BasePokerPlayer):
    def declare_action(self, valid_actions, hole_card, round_state):
        fold_action_info = valid_actions[0]
        action = fold_action_info["action"]
        amount = fold_action_info["amount"] # O valor para 'fold' é sempre 0
        return action, amount # RETORNANDO A TUPLA

    def receive_game_start_message(self, game_info): pass
    def receive_round_start_message(self, round_count, hole_card, seats): pass
    def receive_street_start_message(self, street, round_state): pass
    def receive_game_update_message(self, action, player): pass
    def receive_round_result_message(self, winners, hand_info, round_state): pass
# ---------------------------------------------------------h

# 1. Configura o jogo
config = setup_config(max_round=1, initial_stack=100, small_blind_amount=5)

# 2. Registra os jogadores
config.register_player(name="Jogador Humano", algorithm=AgenteSimples())
config.register_player(name="Inimigo 1", algorithm=FishPlayer())
config.register_player(name="Inimigo 2", algorithm=FoldPlayer())

# 3. Inicia o jogo
# verbose=0 para uma tela mais limpa, já que o JogadorConsole mostra tudo.
game_result = start_poker(config, verbose=1)

print("\n--- Fim de Jogo ---")
print(game_result)
