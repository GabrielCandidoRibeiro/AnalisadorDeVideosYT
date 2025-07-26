import os
from pytubefix import YouTube
import google.generativeai as genai 
from dotenv import load_dotenv 

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    print("Erro: A variável de ambiente GOOGLE_API_KEY não está configurada.")
    print("Por favor, defina-a no seu arquivo .env ou como uma variável de ambiente do sistema.")
    exit()

genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('models/gemini-1.5-flash')

def obter_info_video(url):
    try:
        yt = YouTube(url)

        captions = yt.captions.get('pt') or yt.captions.get('pt-BR') or yt.captions.get('a.pt')

        info = {
            "titulo": yt.title,
            "descricao": yt.description,
            "visualizacoes": yt.views,
            "duracao": yt.length,
            "autor": yt.author,
            "legendas": None
        }

        if captions:
            info['legendas'] = captions.generate_srt_captions()

        return info
    except Exception as e:
        print(f"Erro ao obter informações do vídeo: {e}")
        return None

def analisar_conteudo(info):
    if not info:
        return "❌ Não foi possível obter informações do vídeo."

    conteudo = f"🎬 Vídeo: {info['titulo']} ({info['visualizacoes']} visualizações)\n"

    if info.get('legendas'):
        conteudo += f"\n📝 Transcrição:\n{info['legendas']}"

    prompt = f"""
    Analise o seguinte conteúdo de um vídeo do YouTube em português e forneça um resumo detalhado:

    {conteudo}

    Por favor, inclua os seguintes elementos na sua análise:
    1. Resumo geral do conteúdo
    2. Principais tópicos ou pontos discutidos (com base no título, descrição e transcrição, se disponível)
    3. Insights ou informações importantes
    4. Conclusão ou mensagem final do vídeo (se aplicável)
    5. Popularidade do vídeo com base nas visualizações

    Responda em português.
    """

    try:
        response = model.generate_content(prompt)

        return response.text
    except Exception as e:
        return f"❌ Erro ao processar análise do conteúdo com Google Gemini: {e}"


if __name__ == "__main__":
    print("📽️  ANALISADOR DE VÍDEOS DO YOUTUBE\n")

    url = input("🔗 Insira a URL do vídeo do YouTube: ").strip()
    print("\n🔍 Buscando informações do vídeo...\n")

    info = obter_info_video(url)
    print("📄 Informações do vídeo:")
    print(f"📌 Título: {info.get('titulo', 'Desconhecido')}")
    print(f"👁️ Visualizações: {info.get('visualizacoes', 'N/A')}\n")

    print("🧠 Gerando análise completa com IA...\n")
    resultado = analisar_conteudo(info)

    print("📊 Resultado da Análise:\n")
    print(resultado)
