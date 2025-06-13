import json
import gradio as gr
from textblob import TextBlob
from deep_translator import GoogleTranslator

def sentiment_analysis(text: str) -> str:
    """
    Türkçe metni İngilizce'ye çevirip, İngilizce metin üzerinden duygu analizi yapar.
    """
    try:
        eng_text = GoogleTranslator(source='tr', target='en').translate(text)
    except Exception as e:
        return json.dumps({"hata": f"Çeviri hatası: {str(e)}"})

    blob = TextBlob(eng_text)
    sentiment = blob.sentiment

    # Değerleri Türkçeleştir
    if sentiment.polarity > 0:
        assessment = "pozitif"
    elif sentiment.polarity < 0:
        assessment = "negatif"
    else:
        assessment = "nötr"

    sonuc = {
        "duygu_puani": round(sentiment.polarity, 2),  # -1 (negatif) ile 1 (pozitif) arası
        "öznelik": round(sentiment.subjectivity, 2),   # 0 (nesnel) ile 1 (öznel) arası
        "degerlendirme": assessment
    }

    return json.dumps(sonuc, ensure_ascii=False)

# Create the Gradio interface
demo = gr.Interface(
    fn=sentiment_analysis,
    inputs=gr.Textbox(placeholder="Türkçe metin girin..."),
    outputs=gr.Textbox(),
    title="Türkçe Metin Duygu Analizi",
    description="Türkçe metinlerde duygu analizi. MCP ile Cursor, VSCode gibi ortamlarda kullanılabilir."
)

# Launch the interface and MCP server
if __name__ == "__main__":
    demo.launch(mcp_server=True)