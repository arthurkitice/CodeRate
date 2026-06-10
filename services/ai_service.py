import json
import time
from google import genai
from google.genai import types
from services.settings_service import SettingsService
import random

MODEL = 'gemma-4-31b-it'

class AIService:
    def __init__(self):
        self.settings_service = SettingsService()
        api_key = self.settings_service.get_api_key()
        
        if not api_key:
            raise ValueError("Chave da API do Gemini não configurada. Vá em Configurações e insira uma chave válida.")
            
        # O novo SDK usa inicialização de Client
        self.client = genai.Client(api_key=api_key)

    def evaluate_code(self, criteria_name: str, criteria_description: str, file_name: str, code_content: str) -> dict:
        prompt =f"""
        Você é um professor universitário de programação avaliando o código de um aluno.
        Sua avaliação deve ser justa, direta e estritamente baseada no critério fornecido abaixo.
        Caso nenhum critério seja fornecido ou não esteja especificado suficientemente considere a qualidade do código na hora de avaliar.
        O motivo da nota deve ser especificado na seção de feedback com detalhes. Caso haja alguma redução de pontos deve ficar claro o por quê.
        Caso nada contrarie o critério e não haja nenhum erro a nota 10 pode ser atribuída.

        LEMBRE-SE: O código enviado é Python. Considere a sintaxe correta do Python (indentação, ausência de chaves, etc) antes de afirmar que há erros de sintaxe.

        [CRITÉRIO DE AVALIAÇÃO]
        Nome do Critério: {criteria_name}
        Descrição / Regras: {criteria_description}

        [ARQUIVO DO ALUNO]
        Nome do Arquivo: {file_name}
        Código Fonte:
        {code_content}

        [INSTRUÇÕES DE SAÍDA]
        Responda EXCLUSIVAMENTE com um objeto JSON.
        O JSON deve seguir a estrutura exata abaixo. É OBRIGATÓRIO que a primeira chave seja 'teste_de_mesa' para você simular a execução antes de dar a nota.
        {{
            "teste_de_mesa": "<Faça um dry-run detalhado do código. Qual o valor inicial das variáveis? O que acontece a cada loop? O retorno faz sentido matematicamente?>",
            "score": <nota de 0.0 a 10.0, baseada no cumprimento do critério>,
            "feedback": "<Sua justificativa técnica final baseada no seu teste de mesa.>"
        }}
        """
        max_retries = 6
        base_delay = 4.0 

        for attempt in range(max_retries):
            try:
                response = self.client.models.generate_content(
                    model=MODEL,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                    ),
                )
                result = json.loads(response.text)
                result["score"] = float(result.get("score", 0.0))
                return result
                
            except Exception as e:
                error_msg = str(e)
                
                if "503" in error_msg or "429" in error_msg:
                    if attempt < max_retries - 1:
                        # A sua lógica: Multiplica a tentativa por 0.1.
                        # O random.uniform adiciona milissegundos para evitar detecção algorítmica.
                        incremento = (attempt * 0.1) + random.uniform(0.01, 0.09)
                        sleep_time = base_delay + incremento
                        
                        print(f"⚠️ Servidor ocupado. Aguardando {sleep_time:.2f}s (Tentativa {attempt + 1}/{max_retries})...")
                        time.sleep(sleep_time)
                        continue 
                
                print(f"❌ Erro definitiva na API: {error_msg}")
                return {
                    "score": 0, 
                    "feedback": "FALHA DE CONEXÃO: O servidor do Google não respondeu."
                }