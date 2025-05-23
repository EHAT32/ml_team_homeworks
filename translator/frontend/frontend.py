import streamlit as st
import requests
import constants

st.set_page_config(
    page_title="LLM Переводчик",
    layout="wide"
)

st.title("Переводчик с LLM API")

if 'source_lang' not in st.session_state:
    st.session_state.source_lang = list(constants.LANGUAGES)[1]
if 'target_lang' not in st.session_state:
    st.session_state.target_lang = list(constants.LANGUAGES)[0]
if 'translated_text' not in st.session_state:
    st.session_state.translated_text = ""

def translate_text(text, source_lang, target_lang):
    payload = {
        "text": text,
        "source_language": source_lang,
        "target_language": target_lang
    }
    try:
        response = requests.post(constants.API_URL, json=payload, timeout=10)
        if response.status_code == 200:
            return response.json().get("translated_text", "")
        st.error(f"Ошибка API: {response.text}")
        return ""
    except Exception as e:
        st.error(f"Ошибка соединения: {str(e)}")
        return ""

col1, col2 = st.columns(2)

with col1:
    st.subheader("Исходный текст")
    source_lang = st.selectbox(
        "Исходный язык",
        options=list(constants.LANGUAGES),
        key="source_lang"
    )
    source_text = st.text_area(
        "Введите текст для перевода",
        height=200,
        key="source_text"
    )

with col2:
    st.subheader("Перевод")
    target_lang = st.selectbox(
        "Целевой язык",
        options=list(constants.LANGUAGES),
        key="target_lang"
    )

    translation_display = st.text_area(
        "Результат перевода",
        value=st.session_state.translated_text,
        height=200,
        key="translation_display"
    )

if st.button("Перевести", type="primary"):
    if source_text.strip():
        with st.spinner("Идет перевод..."):
            translated = translate_text(
                source_text,
                source_lang,
                target_lang
            )
            if translated:
                st.session_state.translated_text = translated
                st.rerun()
    else:
        st.warning("Пожалуйста, введите текст для перевода")