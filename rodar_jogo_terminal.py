# rodar_jogo_terminal.py

import os
from pypokerengine.api.game import setup_config, start_poker
from examples.players.fold_man import FoldMan  # Jogador oficial de exemplo
from meus_players.meu_agente import AgenteInteligente
from meus_players.agente_gpt_v2 import AgenteGPT_V2
from meus_players.agente_gpt_agressivo import AgenteAgressivo # O novo agente agressivo

# --- Verificação de Segurança ---
# Antes de rodar, verifica se a chave da API está configurada.
if not os.environ.get('OPENAI_API_KEY'):
    print("ERRO CRÍTICO: A variável de ambiente OPENAI_API_KEY não foi encontrada.")
    exit()
# -----------------------------


# 1. Configura as regras do jogo
# Reduzi para 2 rodadas para um teste mais rápido.
config = setup_config(max_round=10, initial_stack=10000, small_blind_amount=500)

# 2. Registra os jogadores
# <<< MUDANÇA AQUI: Registra o AgenteGPT em vez do AgenteInteligente
config.register_player(name="Agente GPT Balanceado", algorithm=AgenteGPT_V2())
config.register_player(name="Agente heuristico", algorithm=AgenteInteligente())
config.register_player(name="Agente GPT agressivo", algorithm=AgenteAgressivo())

# 3. Inicia o jogo com o modo verbose ativado
# verbose=1 mostra o fluxo do jogo (quem apostou, quanto, etc.)
print("Iniciando partida no terminal com o AgenteGPT...")
print("Atenção: Cada jogada do AgenteGPT pode levar alguns segundos devido à chamada da API.")
game_result = start_poker(config, verbose=1)

# 4. Mostra o resultado final
print("\n--- Fim de Jogo ---")
print(game_result)
