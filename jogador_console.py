# jogador_console.py (adaptado para Python 3)

import pypokerengine.utils.visualize_utils as U
from pypokerengine.players import BasePokerPlayer

class JogadorConsole(BasePokerPlayer):

    def __init__(self, input_receiver=None):
        # Em Python 3, raw_input foi renomeado para input
        self.input_receiver = input_receiver if input_receiver else input

    def declare_action(self, valid_actions, hole_card, round_state):
        print(U.visualize_declare_action(valid_actions, hole_card, round_state, self.uuid))
        action, amount = self.__receive_action_from_console(valid_actions)
        return action, amount

    def receive_game_start_message(self, game_info):
        print(U.visualize_game_start(game_info, self.uuid))
        self.__wait_until_input()

    def receive_round_start_message(self, round_count, hole_card, seats):
        print(U.visualize_round_start(round_count, hole_card, seats, self.uuid))
        self.__wait_until_input()

    def receive_street_start_message(self, street, round_state):
        print(U.visualize_street_start(street, round_state, self.uuid))
        self.__wait_until_input()

    def receive_game_update_message(self, new_action, round_state):
        # O nome do argumento mudou em versões mais recentes
        print(U.visualize_game_update(new_action, round_state, self.uuid))
        self.__wait_until_input()

    def receive_round_result_message(self, winners, hand_info, round_state):
        print(U.visualize_round_result(winners, hand_info, round_state, self.uuid))
        self.__wait_until_input()

    def __wait_until_input(self):
        # Em Python 3, print é uma função
        input("Pressione Enter para continuar...")

    def __receive_action_from_console(self, valid_actions):
        flg = self.input_receiver('Digite f(fold), c(call), r(raise).\n >> ')
        if flg in self.__gen_valid_flg(valid_actions):
            if flg == 'f':
                return valid_actions[0]['action'], valid_actions[0]['amount']
            elif flg == 'c':
                return valid_actions[1]['action'], valid_actions[1]['amount']
            elif flg == 'r':
                valid_amounts = valid_actions[2]['amount']
                raise_amount = self.__receive_raise_amount_from_console(valid_amounts['min'], valid_amounts['max'])
                return valid_actions[2]['action'], raise_amount
        else:
            return self.__receive_action_from_console(valid_actions)

    def __gen_valid_flg(self, valid_actions):
        flgs = ['f', 'c']
        is_raise_possible = valid_actions[2]['amount']['min'] != -1
        if is_raise_possible:
            flgs.append('r')
        return flgs

    def __receive_raise_amount_from_console(self, min_amount, max_amount):
        raw_amount = self.input_receiver(f"Aumento válido entre [{min_amount}, {max_amount}]: ")
        try:
            amount = int(raw_amount)
            if min_amount <= amount and amount <= max_amount:
                return amount
            else:
                print(f"Valor de aumento inválido {amount}. Tente novamente.")
                return self.__receive_raise_amount_from_console(min_amount, max_amount)
        except:
            print("Entrada inválida. Tente novamente.")
            return self.__receive_raise_amount_from_console(min_amount, max_amount)

