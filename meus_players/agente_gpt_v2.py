# agente_gpt_v2.py

import os
import re
from openai import OpenAI
from pypokerengine.players import BasePokerPlayer

# --- 1. Configuração do Cliente OpenAI ---
try:
    client = OpenAI()
    API_CONFIGURADA = True
except Exception as e:
    print(f"ERRO: Não foi possível configurar a API da OpenAI. Detalhes: {e}")
    API_CONFIGURADA = False

# --- 2. Função para Consultar o GPT (Versão 2.0) ---
def consultar_gpt_para_acao_v2(prompt_detalhado):
    if not API_CONFIGURADA:
        return 'fold', 0

    try:
        completion = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "Você é um jogador de poker Texas Hold'em de classe mundial. Sua resposta DEVE estar no formato 'ação, valor'. A ação deve ser 'fold', 'call' ou 'raise'. O valor para fold e call deve ser 0. Para raise, especifique o valor. Exemplo: 'raise, 25' ou 'call, 0'."},
                {"role": "user", "content": prompt_detalhado}
            ],
            temperature=0.6,
            max_tokens=15
        )
        
        resposta_gpt = completion.choices[0].message.content.strip().lower()
        print(f"--- Resposta Bruta do GPT: '{resposta_gpt}' ---")
        
        match = re.search(r"(\w+),\s*(\d+)", resposta_gpt)
        
        if match:
            acao = match.group(1)
            valor = int(match.group(2))
            if acao in ['fold', 'call', 'raise']:
                print(f"--- GPT Decodificado: Ação={acao}, Valor={valor} ---")
                return acao, valor

        if 'fold' in resposta_gpt: return 'fold', 0
        if 'call' in resposta_gpt: return 'call', 0
        if 'raise' in resposta_gpt: return 'raise', 0

        print("AVISO: GPT retornou uma resposta em formato inesperado. Jogando de forma segura (fold).")
        return 'fold', 0

    except Exception as e:
        print(f"ERRO ao chamar a API do GPT: {e}. Jogando de forma segura (fold).")
        return 'fold', 0

# --- 3. Classe do Agente GPT (Versão 2.0) ---
class AgenteGPT_V2(BasePokerPlayer):

    def declare_action(self, valid_actions, hole_card, round_state):
        # AQUI ESTÁ A NOVA LINHA PARA VISUALIZAR A MÃO
        print(f"\n--- MÃO DO AGENTE GPT: {hole_card} ---")

        fold_action_info = valid_actions[0]
        call_action_info = valid_actions[1]
        raise_action_info = valid_actions[2]
        
        historia_legivel = []
        for acao in round_state['action_histories'][round_state['street']]:
            historia_legivel.append(f"- Jogador {acao['uuid'][-4:]} fez {acao['action']} de {acao.get('amount', 0)}")

        prompt = f"""
        **Cenário de Poker Texas Hold'em**

        **Minha Mão:** {hole_card}
        **Cartas na Mesa:** {round_state['community_card']}
        **Rodada (Street):** {round_state['street']}

        **Valores Importantes:**
        - Meu Stack: {self.stack}
        - Pote Atual: {round_state['pot']['main']['amount']}
        - Valor para Pagar (Call): {call_action_info['amount']}

        **Ações dos Oponentes nesta Rodada:**
        {"\n".join(historia_legivel) if historia_legivel else "Nenhuma ação ainda."}

        **Decisão Necessária:**
        Sua resposta DEVE estar no formato "ação, valor".
        - Para 'raise', o valor deve estar entre {raise_action_info['amount']['min']} e {raise_action_info['amount']['max']}.
        - Para 'call' e 'fold', o valor deve ser 0.

        Qual a sua jogada?
        """

        print(f"--- AGENTE GPT V2: Consultando o LLM... ---")
        acao_recomendada, valor_recomendado = consultar_gpt_para_acao_v2(prompt)

        if acao_recomendada == 'raise' and raise_action_info['amount']['min'] != -1:
            acao = raise_action_info['action']
            valor = max(raise_action_info['amount']['min'], valor_recomendado)
            valor = min(raise_action_info['amount']['max'], valor)
            print(f"AGENTE GPT V2: Decisão final -> {acao} {valor}")
            return acao, valor
        
        elif acao_recomendada == 'call':
            acao = call_action_info['action']
            valor = call_action_info['amount']
            print(f"AGENTE GPT V2: Decisão final -> {acao} {valor}")
            return acao, valor
        
        else:
            acao = fold_action_info['action']
            valor = fold_action_info['amount']
            print(f"AGENTE GPT V2: Decisão final -> {acao} {valor}")
            return acao, valor

    def receive_game_start_message(self, game_info):
        self.stack = [s['stack'] for s in game_info['seats'] if s['uuid'] == self.uuid][0]
    def receive_round_start_message(self, round_count, hole_card, seats): pass
    def receive_street_start_message(self, street, round_state): pass
    def receive_game_update_message(self, action, player): pass
    def receive_round_result_message(self, winners, hand_info, round_state): pass
