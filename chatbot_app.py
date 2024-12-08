import streamlit as st
import requests

# URL FastAPI (обновите на ваш URL с Render)
API_URL = "https://my-fastapi-app.onrender.com"

# Проверка авторизации пользователя
if "is_logged_in" not in st.session_state:
    st.session_state["is_logged_in"] = False
    st.session_state["user_data"] = None

# Регистрация пользователя
def register_user(name, email, password):
    response = requests.post(f"{API_URL}/register", json={
        "name": name,
        "email": email,
        "password": password
    })
    return response.json()

# Авторизация пользователя
def login_user(email, password):
    response = requests.post(f"{API_URL}/login", json={
        "email": email,
        "password": password
    })
    return response.json()

# Streamlit интерфейс
st.sidebar.title("Навигация")
page = st.sidebar.selectbox("Выберите страницу", ["Эхо-чат", "Профиль", "Регистрация", "Авторизация"])

if page == "Регистрация":
    st.title("Регистрация")
    name = st.text_input("Имя")
    email = st.text_input("Email")
    password = st.text_input("Пароль", type="password")
    if st.button("Зарегистрироваться"):
        response = register_user(name, email, password)
        if response.get("status") == 200:
            st.success("Регистрация успешна! Теперь авторизуйтесь.")
        else:
            st.error(response.get("detail", "Ошибка регистрации."))

elif page == "Авторизация":
    st.title("Авторизация")
    email = st.text_input("Email")
    password = st.text_input("Пароль", type="password")
    if st.button("Войти"):
        response = login_user(email, password)
        if response.get("status") == 200:
            st.session_state["is_logged_in"] = True
            st.session_state["user_data"] = response
            st.success("Вход выполнен успешно!")
            st.experimental_rerun()
        else:
            st.error(response.get("detail", "Ошибка авторизации."))

elif page == "Профиль":
    if st.session_state["is_logged_in"]:
        st.title("Профиль пользователя")
        st.write(f"**Имя:** {st.session_state['user_data']['name']}")
        st.write(f"**Email:** {st.session_state['user_data']['email']}")
    else:
        st.warning("Пожалуйста, авторизуйтесь.")

elif page == "Эхо-чат":
    if st.session_state["is_logged_in"]:
        st.title("Эхо-чат")
        user_input = st.text_input("Введите сообщение:")
        if st.button("Отправить"):
            st.text_area("Ответ:", value=f"Эхо: {user_input}")
    else:
        st.warning("Пожалуйста, авторизуйтесь.")
