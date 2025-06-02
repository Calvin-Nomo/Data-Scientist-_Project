#python -m streamlit run  app.py   
import streamlit as st
from googletrans import Translator
from PyPDF2 import PdfReader
from fpdf import FPDF
import time
import os

# Set Streamlit title
st.title("📘 PDF Translator")
st.write("Upload a PDF and translate it to another language.")

# File upload
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

# Language selection
lang_dict = {
    "Afrikaans": "af",
    "Albanian": "sq",
    "Amharic": "am",
    "Arabic": "ar",
    "Armenian": "hy",
    "Azerbaijani": "az",
    "Basque": "eu",
    "Belarusian": "be",
    "Bengali": "bn",
    "Bosnian": "bs",
    "Bulgarian": "bg",
    "Catalan": "ca",
    "Cebuano": "ceb",
    "Chinese (Simplified)": "zh-cn",
    "Chinese (Traditional)": "zh-tw",
    "Corsican": "co",
    "Croatian": "hr",
    "Czech": "cs",
    "Danish": "da",
    "Dutch": "nl",
    "English": "en",
    "Esperanto": "eo",
    "Estonian": "et",
    "Finnish": "fi",
    "French": "fr",
    "Frisian": "fy",
    "Galician": "gl",
    "Georgian": "ka",
    "German": "de",
    "Greek": "el",
    "Gujarati": "gu",
    "Haitian Creole": "ht",
    "Hausa": "ha",
    "Hawaiian": "haw",
    "Hebrew": "he",
    "Hindi": "hi",
    "Hmong": "hmn",
    "Hungarian": "hu",
    "Icelandic": "is",
    "Igbo": "ig",
    "Indonesian": "id",
    "Irish": "ga",
    "Italian": "it",
    "Japanese": "ja",
    "Javanese": "jw",
    "Kannada": "kn",
    "Kazakh": "kk",
    "Khmer": "km",
    "Kinyarwanda": "rw",
    "Korean": "ko",
    "Kurdish": "ku",
    "Kyrgyz": "ky",
    "Lao": "lo",
    "Latin": "la",
    "Latvian": "lv",
    "Lithuanian": "lt",
    "Luxembourgish": "lb",
    "Macedonian": "mk",
    "Malagasy": "mg",
    "Malay": "ms",
    "Malayalam": "ml",
    "Maltese": "mt",
    "Maori": "mi",
    "Marathi": "mr",
    "Mongolian": "mn",
    "Myanmar (Burmese)": "my",
    "Nepali": "ne",
    "Norwegian": "no",
    "Nyanja (Chichewa)": "ny",
    "Odia (Oriya)": "or",
    "Pashto": "ps",
    "Persian": "fa",
    "Polish": "pl",
    "Portuguese": "pt",
    "Punjabi": "pa",
    "Romanian": "ro",
    "Russian": "ru",
    "Samoan": "sm",
    "Scots Gaelic": "gd",
    "Serbian": "sr",
    "Sesotho": "st",
    "Shona": "sn",
    "Sindhi": "sd",
    "Sinhala (Sinhalese)": "si",
    "Slovak": "sk",
    "Slovenian": "sl",
    "Somali": "so",
    "Spanish": "es",
    "Sundanese": "su",
    "Swahili": "sw",
    "Swedish": "sv",
    "Tagalog (Filipino)": "tl",
    "Tajik": "tg",
    "Tamil": "ta",
    "Tatar": "tt",
    "Telugu": "te",
    "Thai": "th",
    "Turkish": "tr",
    "Turkmen": "tk",
    "Ukrainian": "uk",
    "Urdu": "ur",
    "Uyghur": "ug",
    "Uzbek": "uz",
    "Vietnamese": "vi",
    "Welsh": "cy",
    "Xhosa": "xh",
    "Yiddish": "yi",
    "Yoruba": "yo",
    "Zulu": "zu"
}
# Language selection dropdown
target_lang = st.selectbox("Select language", list(lang_dict.keys()))

# Button to start translation
if uploaded_file and st.button("Translate"):
    # Save uploaded file temporarily
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.read())

    st.info("Translating, please wait...")

    translator = Translator()
    pdf_writer = FPDF()
    pdf_writer.set_auto_page_break(auto=True, margin=15)
    pdf_writer.add_font("DejaVu", "", "dejavu-fonts-ttf-2.37/ttf/DejaVuSans.ttf", uni=True)
    pdf_writer.set_font("DejaVu", size=12)

    reader = PdfReader("temp.pdf")

    for i, page in enumerate(reader.pages):
        try:
            text = page.extract_text()
            if text:
                translated = translator.translate(text, dest=lang_dict[target_lang]).text
                pdf_writer.add_page()
                pdf_writer.multi_cell(0, 10, f"Page {i + 1}:\n{translated}")
                time.sleep(1)
        except Exception as e:
            st.warning(f"Error on page {i+1}: {e}")
    output_filename=st.write(' What is The Tanslated Pdf  file name ?'+'.pdf')
 
    # output_filename = f"translated_{target_lang}.pdf"
    pdf_writer.output(output_filename)

    # Download link
    with open(output_filename, "rb") as f:
        st.download_button(" Download Translated PDF", f, file_name=output_filename)

    # Cleanup
    os.remove("temp.pdf")
    os.remove(output_filename)