import streamlit as st
import requests
from PIL import Image
import io
from io import BytesIO

# Конфигурация API
API_URL = "http://api-service:5000/detect/"

# Настройки страницы
st.set_page_config(page_title="License Plate Blur", page_icon="📷")

# Инициализация состояния
if 'processed_image' not in st.session_state:
    st.session_state.processed_image = None

# Стили
st.markdown("""
    <style>
        .title {
            font-size: 36px;
            font-weight: bold;
            color: #2e7d32;
            text-align: center;
            margin-bottom: 20px;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
        }
        .stButton > button {
            background-color: #4CAF50;
            color: white;
            border-radius: 8px;
            padding: 10px 20px;
        }
        .stButton > button:hover {
            background-color: #45a049;
        }
        .stButton > button {
            background: linear-gradient(45deg, #4CAF50, #81C784);
        }
    </style>
""", unsafe_allow_html=True)

# Заголовок
st.markdown('<div class="title">Blur License Plates</div>', unsafe_allow_html=True)
st.markdown("Загрузите изображение с автомобильным номером — мы его размоем!")

# Загрузка файла
uploaded_file = st.file_uploader("Выберите изображение...", type=["jpg", "jpeg", "png"])

col1, col2 = st.columns(2)

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    with col1:
        st.image(image, caption='Оригинал', use_container_width=True)

    if st.button("Обработать"):
        with st.spinner("Обработка... Подождите"):
            # Читаем байты файла напрямую
            image_bytes = uploaded_file.getvalue()

            # Отправляем как multipart/form-data
            files = {
                "file": (uploaded_file.name, image_bytes, uploaded_file.type)
            }

            try:
                response = requests.post(API_URL, files=files)

                if response.status_code == 200:
                    processed_image = Image.open(BytesIO(response.content))
                    st.session_state.processed_image = processed_image
                else:
                    st.error(f"❌ Ошибка сервера: {response.status_code}")
                    st.code(response.text[:500])
            except Exception as e:
                st.error(f"Не удалось подключиться к API: {e}")

    # Показываем изображение и кнопку скачивания, если есть результат
    if st.session_state.processed_image is not None:
        with col2:
            st.image(st.session_state.processed_image, caption="Результат", use_container_width=True)

            buf = io.BytesIO()
            st.session_state.processed_image.save(buf, format="PNG")
            byte_im = buf.getvalue()

            st.download_button(
                label="⬇️ Скачать результат",
                data=byte_im,
                file_name="blurred_image.png",
                mime="image/png"
            )

else:
    with col1:
        st.info("Ожидается загрузка изображения...")
    with col2:
        st.info("Результат появится здесь")

# Футер
st.markdown("---")
st.markdown("<center>© 2025 License Plate Blur Service</center>", unsafe_allow_html=True)