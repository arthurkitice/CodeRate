import json
from google import genai
from google.genai import types
from services.settings_service import SettingsService

class AIService:
    def __init__(self):
        self.settings_service = SettingsService()
        api_key = self.settings_service.get_api_key()
        
        if not api_key:
            raise ValueError("Chave da API do Gemini não configurada. Vá em Configurações e insira uma chave válida.")
            
        # O novo SDK usa inicialização de Client
        self.client = genai.Client(api_key=api_key)

    def evaluate_code(self, criteria_name: str, criteria_description: str, file_name: str, code_content: str) -> dict:
        prompt = f"""
        Você é um professor universitário de programação avaliando o código de um aluno.
        Sua avaliação deve ser justa, direta e estritamente baseada no critério fornecido abaixo.

        [CRITÉRIO DE AVALIAÇÃO]
        Nome do Critério: {criteria_name}
        Descrição / Regras: {criteria_description}

        [ARQUIVO DO ALUNO]
        Nome do Arquivo: {file_name}
        Código Fonte:
        {code_content}

        [INSTRUÇÕES DE SAÍDA]
        Responda EXCLUSIVAMENTE com um objeto JSON. Não inclua texto fora do JSON.
        O JSON deve seguir a estrutura exata:
        {{
            "score": <nota de 0.0 a 10.0, baseada no cumprimento do critério>,
            "feedback": "<Sua justificativa técnica e direta da nota. Aponte erros ou acertos.>"
        }}
        """

        try:
            # O novo formato de chamada do SDK 2.0+
            response = self.client.models.generate_content(
                model='gemini-2.5-flash', # Recomendado usar a versão mais recente e rápida
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                ),
            )
            
            result = json.loads(response.text)
            result["score"] = float(result.get("score", 0.0))
            return result
            
        except Exception as e:
            print(f"Erro na API do Gemini: {str(e)}")
            return {
                "score": 0.0,
                "feedback": f"Erro interno ao processar avaliação: {str(e)}"
            }