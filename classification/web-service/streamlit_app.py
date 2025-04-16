import streamlit as st
import requests
from requests.exceptions import ConnectionError

# Настройки API
ip_api = "api-service"
port_api = "5000"

# Название и иконка страницы
st.set_page_config(page_title="Insurance Predictor", page_icon="🚗")

# Стили
st.markdown("""
    <style>
        .title {
            font-size: 32px;
            font-weight: bold;
            color: #4CAF50;
            margin-bottom: 20px;
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
    </style>
""", unsafe_allow_html=True)

# Заголовок приложения
st.markdown('<div class="title">Insurance Prediction</div>', unsafe_allow_html=True)

st.markdown("Please enter the details below to get a prediction:")

# Разделение на колонки
col1, col2 = st.columns(2)

with col1:
    previously_insured = st.checkbox("Previously Insured", help="Выберите, если клиент ранее был застрахован")
    vehicle_damage = st.checkbox("Vehicle Damage", help="Выберите, если транспортное средство было повреждено")

with col2:
    vehicleAge = st.selectbox("Vehicle Age", ["< 1 Year", "1-2 Year", "> 2 Years"], help="Возраст транспортного средства")
    policySalesChannel = st.text_input("Policy Sales Channel", value=152, help="Введите номер канала продаж (целое число)")

# Проверка ввода
if not policySalesChannel.isdigit():
    st.error("🚫 Please enter a valid number for policy sales channel.")

# Кнопка запроса
if st.button("🔍 Predict"):
    if policySalesChannel.isdigit():
        data = {
            "Previously_Insured": previously_insured,
            "Vehicle_Age": vehicleAge,
            "Vehicle_Damage": vehicle_damage,
            "Policy_Sales_Channel": int(policySalesChannel)
        }

        try:
            response = requests.post(f"http://{ip_api}:{port_api}/predict_model", json=data)

            if response.status_code == 200:
                response_data = response.json()
                prediction = response.json()["prediction"]
                if "_original_prediction" in response_data:
                    original_value = response_data["_original_prediction"]
                    expected_text = "Клиент возьмёт страховку" if original_value == 1 else "Клиент не возьмёт страховку"
                    
                    if prediction != expected_text:
                        st.error("⚠️ Ошибка согласованности данных!")
                        st.error(f"Получено: {prediction} | Ожидалось: {expected_text}")
                    else:
                        st.success("✅ Успешный прогноз:")
                st.metric(label="", value=prediction)
                if prediction == "Клиент возьмёт страховку":
                    st.balloons()
                
                if "history" not in st.session_state:
                    st.session_state.history = []

                st.session_state.history.append(data | {"prediction": prediction})

                st.markdown("---")

                # История прогнозов:
                with st.expander("🕘 История прогнозов"):
                    for item in st.session_state.history[::-1]:
                        st.write(item)

            else:
                st.error(f"❌ Request failed with status code {response.status_code}")
        except ConnectionError:
            st.error("🔌 Failed to connect to the server")
    else:
        st.error("❗ Please fill in all fields with valid numbers.")

# Футер
st.markdown("---")
st.markdown("<center>© 2025 Insurance ML Service</center>", unsafe_allow_html=True)
