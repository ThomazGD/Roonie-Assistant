import openai

# Substitua por sua chave da API quando tiver
openai.api_key = "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"

def conversa_leve(mensagem_usuario):
    try:
        resposta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é o Roonie, um assistente amigável e engraçado. Responda com bom humor e simpatia."},
                {"role": "user", "content": mensagem_usuario}
            ],
            temperature=0.8,
            max_tokens=100
        )
        return resposta.choices[0].message.content.strip()
    except Exception as e:
        return "Desculpe, tive um problema ao tentar conversar."
