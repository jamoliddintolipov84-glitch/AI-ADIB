import streamlit as st
import google.generativeai as genai

# Sahifa sozlamalari
st.set_page_config(page_title="AI-ADIB PRO", page_icon="📚", layout="wide")

# Saytning vizual qismi (Interfeys)
st.title("AI-ADIB: Intellektual Adabiyot Mentori")
st.subheader("Google Gemini API asosidagi ta'limiy platforma")

# API ulanishini tekshirish
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    api_key = st.sidebar.text_input("API Keyni kiriting:", type="password")
    if api_key:
        genai.configure(api_key=api_key)
    else:
        st.warning("Davom etish uchun API kalit zarur.")
        st.stop()

# AI Studio'dan olingan tizimli ko'rsatma (System Instruction)
# Bu yerga o'zingizning promtingizni yozing
system_message = "Siz professional adabiyotshunos va tanqidchisiz. Savollarga ilmiy va aniq javob bering."

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    system_instruction=system_message
)

# Chat xotirasi (Session State)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Chat interfeysi
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Adabiy tahlil yoki kitob tavsiyasi uchun yozing..."):
    # Foydalanuvchi xabari
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI javobi
    with st.chat_message("assistant"):
        response = model.generate_content(prompt)
        st.markdown(response.text)
        st.session_state.chat_history.append({"role": "assistant", "content": response.text})
