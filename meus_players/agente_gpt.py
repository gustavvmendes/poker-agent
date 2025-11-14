# agente_gpt.py

import os
from openai import OpenAI
from pypokerengine.players import BasePokerPlayer

# --- 1. Configuração do Cliente OpenAI ---
# O cliente irá automaticamente procurar a variável de ambiente OPENAI_API_KEY.
try:
    client = OpenAI()
    API_CONFIGURADA = True
except Exception as e:
    print(f"ERRO: Não foi possível configurar a API da OpenAI. Verifique sua chave de API. Detalhes: {e}")
    API_CONFIGURADA = False

# --- 2. Função para Consultar o GPT ---
def consultar_gpt_para_acao(prompt_detalhado):
    """
    Envia o estado do jogo para o GPT e pede uma recomendação de ação.
    Retorna a ação ('fold', 'call', 'raise') e o valor.
    """
    if not API_CONFIGURADA:
        # Se a API não estiver configurada, joga de forma segura (check/fold)
        return 'fold', 0

    try:
        completion = client.chat.completions.create(
            model="gpt-4.1-mini",  # Um modelo rápido e inteligente, ótimo para essa tarefa.
            messages=[
                {"role": "system", "content": "Você é um jogador de poker profissional de Texas Hold'em. Sua resposta deve ser apenas uma palavra em minúsculo: 'fold', 'call', ou 'raise'. Não adicione nenhuma outra palavra ou explicação."},
                {"role": "user", "content": prompt_detalhado}
            ],
            temperature=0.5, # Um pouco de criatividade, mas sem exageros.
            max_tokens=5     # A resposta é muito curta, então 5 tokens são suficientes.
        )
        
        resposta_gpt = completion.choices[0].message.content.strip().lower()
        print(f"--- Resposta do GPT: '{resposta_gpt}' ---")
        
        # Valida se a resposta é uma das ações esperadas
        if resposta_gpt in ['fold', 'call', 'raise']:
            return resposta_gpt
        else:
            # Se o GPT responder algo inesperado, joga de forma segura.
            print("AVISO: GPT retornou uma resposta inválida. Jogando de forma segura (fold).")
            return 'fold'

    except Exception as e:
        print(f"ERRO ao chamar a API do GPT: {e}. Jogando de forma segura (fold).")
        return 'fold'

# --- 3. Classe do Agente GPT ---
class AgenteGPT(BasePokerPlayer):

    def declare_action(self, valid_actions, hole_card, round_state):
        # --- Formata o Prompt para o GPT ---
        # Pega informações sobre as ações possíveis
        fold_action_info = valid_actions[0]
        call_action_info = valid_actions[1]
        raise_action_info = valid_actions[2]
        
        # Constrói o prompt com todas as informações relevantes
        prompt = f"""
        Estou em uma mão de poker Texas Hold'em. Preciso da sua recomendação.

        **Minha Mão (Hole Cards):** {hole_card}

        **Cartas na Mesa (Community Cards):** {round_state['community_card']}

        **Estado do Jogo:**
        - Rodada (Street): {round_state['street']}
        - Meu stack de fichas: {self.stack}
        - Pote principal: {round_state['pot']['main']['amount']}
        - Jogadores na mão: {[p['name'] for p in round_state['seats'] if p['state'] == 'participating']}

        **Ações Possíveis:**
        - Desistir (fold)
        - Pagar (call): {call_action_info['amount']} fichas
        - Aumentar (raise): entre {raise_action_info['amount']['min']} e {raise_action_info['amount']['max']} fichas

        **Histórico de Ações nesta Rodada:**
        {round_state['action_histories'][round_state['street']]}

        Com base em tudo isso, qual ação você recomenda? Responda apenas com uma palavra: 'fold', 'call', ou 'raise'.
        """

        print(f"\n--- AGENTE GPT: Consultando o LLM para a jogada... ---")
        acao_recomendada = consultar_gpt_para_acao(prompt)

        # --- Processa a Resposta do GPT ---
        if acao_recomendada == 'raise' and raise_action_info['amount']['min'] != -1:
            # Se o GPT recomendar 'raise', aumenta o mínimo possível.
            acao = raise_action_info['action']
            valor = raise_action_info['amount']['min']
            print(f"AGENTE GPT: Decisão final -> {acao} {valor}")
            return acao, valor
        
        elif acao_recomendada == 'call':
            acao = call_action_info['action']
            valor = call_action_info['amount']
            print(f"AGENTE GPT: Decisão final -> {acao} {valor}")
            return acao, valor
        
        else: # 'fold' ou qualquer outra resposta
            acao = fold_action_info['action']
            valor = fold_action_info['amount']
            print(f"AGENTE GPT: Decisão final -> {acao} {valor}")
            return acao, valor

    # Métodos restantes não precisam de lógica por enquanto
    def receive_game_start_message(self, game_info):
        self.stack = [s['stack'] for s in game_info['seats'] if s['uuid'] == self.uuid][0]
    def receive_round_start_message(self, round_count, hole_card, seats): pass
    def receive_street_start_message(self, street, round_state): pass
    def receive_game_update_message(self, action, player): pass
    def receive_round_result_message(self, winners, hand_info, round_state): pass
