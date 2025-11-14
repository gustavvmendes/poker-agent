# meu_agente.py

from pypokerengine.players import BasePokerPlayer
from pypokerengine.utils.card_utils import gen_cards, estimate_hole_card_win_rate

# --- Função Auxiliar para Avaliar a Mão ---
def avaliar_forca_mao_inicial(hole_card_str):
    """
    Avalia a força das duas cartas iniciais (hole cards).
    Retorna um valor de 0 (fraca) a 2 (forte).
    """
    # Converte as strings das cartas (ex: 'H5') para o formato interno da biblioteca
    ranks = "23456789TJQKA"
    rank1 = ranks.find(hole_card_str[0][1])
    rank2 = ranks.find(hole_card_str[1][1])
    
    # É um par?
    is_pair = (rank1 == rank2)
    # São do mesmo naipe?
    is_suited = (hole_card_str[0][0] == hole_card_str[1][0])
    
    # 1. Mãos fortes: Pares altos (TT+) ou Ás com Rei/Dama/Valete do mesmo naipe.
    if is_pair and rank1 >= ranks.find('T'): # Par de Dez ou maior
        return 2
    if is_suited and rank1 >= ranks.find('J') and rank2 >= ranks.find('J'): # AKs, AQs, AJs, KQs, KJs, QJs
        return 2

    # 2. Mãos médias: Pares médios, cartas altas, ou cartas do mesmo naipe.
    if is_pair: # Qualquer outro par
        return 1
    if rank1 >= ranks.find('T') and rank2 >= ranks.find('T'): # Duas cartas maiores que Dez
        return 1
    if is_suited: # Qualquer outra mão do mesmo naipe
        return 1

    # 3. Mãos fracas: Todo o resto.
    return 0

# --- Classe do Agente Inteligente ---
class AgenteInteligente(BasePokerPlayer):

    def declare_action(self, valid_actions, hole_card, round_state):
        # Pega informações sobre as ações possíveis
        fold_action_info = valid_actions[0]
        call_action_info = valid_actions[1]
        raise_action_info = valid_actions[2]

        # Analisa o estado do jogo
        street = round_state['street']
        valor_para_pagar = call_action_info['amount']

        # --- Lógica Pré-Flop ---
        if street == 'preflop':
            forca_mao = avaliar_forca_mao_inicial(hole_card)
            
            # Mão forte: Aumentar a aposta (raise) se possível
            if forca_mao == 2 and raise_action_info['amount']['min'] != -1:
                aumento = raise_action_info['amount']['min'] # Aumenta o mínimo possível
                print(f"AGENTE: Mão forte ({hole_card}), aumentando para {aumento}")
                return raise_action_info['action'], aumento

            # Mão média: Apenas pagar (call)
            if forca_mao == 1:
                print(f"AGENTE: Mão média ({hole_card}), pagando {valor_para_pagar}")
                return call_action_info['action'], valor_para_pagar

            # Mão fraca: Desistir se alguém já apostou. Se não, passar a vez.
            if forca_mao == 0:
                if valor_para_pagar > 0:
                    print(f"AGENTE: Mão fraca ({hole_card}), desistindo.")
                    return fold_action_info['action'], fold_action_info['amount']
                else:
                    print(f"AGENTE: Mão fraca ({hole_card}), passando a vez (check).")
                    return call_action_info['action'], call_action_info['amount']

        # --- Lógica Pós-Flop (por enquanto, simples) ---
        # Se chegou até aqui, é porque estamos no flop, turn ou river.
        # A lógica será a mesma do AgenteSimples: check ou call.
        print(f"AGENTE: Pós-flop, jogando seguro (check/call).")
        return call_action_info['action'], call_action_info['amount']


    # Métodos restantes não precisam de lógica por enquanto
    def receive_game_start_message(self, game_info): pass
    def receive_round_start_message(self, round_count, hole_card, seats): pass
    def receive_street_start_message(self, street, round_state): pass
    def receive_game_update_message(self, action, player): pass
    def receive_round_result_message(self, winners, hand_info, round_state): pass

