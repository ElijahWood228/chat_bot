import streamlit as st
import requests

# URL FastAPI (обновите на ваш URL или оставьте заглушку)
API_URL = "https://fastapi-chatbot-0sfz.onrender.com"

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

# Интерфейс Streamlit
st.sidebar.title("Навигация")
page = st.sidebar.selectbox("Выберите страницу", ["Эхо-чат", "Профиль", "Регистрация", "Авторизация"])

# Страница регистрации
if page == "Регистрация":
    st.title("Регистрация")
    name = st.text_input("Имя")
    email = st.text_input("Email")
    password = st.text_input("Пароль", type="password")
    if st.button("Зарегистрироваться"):
        if name and email and password:
            response = register_user(name, email, password)
            if response.get("status") == 200:
                st.success("Регистрация успешна! Теперь авторизуйтесь.")
            else:
                st.error(response.get("detail", "Ошибка регистрации."))
        else:
            st.error("Все поля обязательны для заполнения.")

# Страница авторизации
elif page == "Авторизация":
    st.title("Авторизация")
    email = st.text_input("Email")
    password = st.text_input("Пароль", type="password")
    if st.button("Войти"):
        if email and password:
            response = login_user(email, password)
            if response.get("status") == 200:
                st.session_state["is_logged_in"] = True
                st.session_state["user_data"] = {
                    "name": response.get("name"),
                    "email": email
                }
                st.success("Вход выполнен успешно!")
                st.rerun()
            else:
                st.error(response.get("detail", "Ошибка авторизации."))
        else:
            st.error("Введите email и пароль.")

# Страница профиля
elif page == "Профиль":
    if st.session_state["is_logged_in"]:
        st.title("Профиль пользователя")
        st.write(f"**Имя:** {st.session_state['user_data']['name']}")
        st.write(f"**Email:** {st.session_state['user_data']['email']}")
    else:
        st.warning("Пожалуйста, авторизуйтесь, чтобы увидеть профиль.")

# Страница эхо-чата
elif page == "Эхо-чат":
    if st.session_state["is_logged_in"]:
        st.title("Эхо-чат")
        user_input = st.text_input("Введите сообщение:")
        if st.button("Отправить"):
            if user_input:
                # Эхо-бот: возвращаем тот же текст пользователю
                st.text_area("Ответ:", value=user_input, height=100)
            else:
                st.warning("Введите сообщение для отправки.")
    else:
        st.warning("Пожалуйста, авторизуйтесь, чтобы использовать чат.")
