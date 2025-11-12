# rodar_jogo_terminal.py

from pypokerengine.api.game import setup_config, start_poker
from examples.players.fold_man import FoldMan  # Jogador oficial de exemplo
from meu_agente import AgenteInteligente      # Nosso novo agente!

# 1. Configura as regras do jogo
config = setup_config(max_round=5, initial_stack=100, small_blind_amount=5)

# 2. Registra os jogadores
config.register_player(name="Agente Inteligente", algorithm=AgenteInteligente())
config.register_player(name="FoldMan 1", algorithm=FoldMan())
config.register_player(name="FoldMan 2", algorithm=FoldMan())

# 3. Inicia o jogo com o modo verbose ativado
# verbose=1 mostra o fluxo do jogo (quem apostou, quanto, etc.)
print("Iniciando partida no terminal...")
game_result = start_poker(config, verbose=1)

# 4. Mostra o resultado final
print("\n--- Fim de Jogo ---")
print(game_result)
