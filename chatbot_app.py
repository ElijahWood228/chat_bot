import streamlit as st
import requests

# Функции для проверки и управления пользователем
users = {}  # Хранилище для зарегистрированных пользователей {email: {"name": ..., "password": ...}}

# Функция для проверки email через BulkEmailVerifier API
def is_valid_email_bulkverifier(email):
    api_key = "kTaX3A0jJmJpbvEDrwfNj"  # Замените на ваш API-ключ
    url = "https://api.bulkemailverifier.com/v1/verify"  # URL для запроса

    # Параметры запроса
    params = {
        'api_key': api_key,
        'email': email
    }

    try:
        # Отправляем GET-запрос к BulkEmailVerifier API
        response = requests.get(url, params=params)
        response_data = response.json()

        # Проверяем статус ответа
        if response.status_code == 200:
            result = response_data.get("result")
            if result == "valid":
                return True, "Email валиден!"
            elif result == "invalid":
                return False, "Email недействителен."
            elif result == "unknown":
                return False, "Неизвестный статус email."
            else:
                return False, "Ошибка при проверке email."
        else:
            return False, f"Ошибка API: {response_data.get('message', 'Неизвестная ошибка')}"
    except Exception as e:
        return False, f"Ошибка соединения: {str(e)}"


def register_user(name, email, password):
    # Проверка email через BulkEmailVerifier
    is_valid, message = is_valid_email_bulkverifier(email)
    if not is_valid:
        return False, message
    
    # Проверка уникальности email
    if email in users:
        return False, "Email уже зарегистрирован."
    
    # Сохранение данных пользователя
    users[email] = {"name": name, "password": password}
    return True, "Регистрация успешна."


def authenticate_user(email, password):
    if email in users and users[email]["password"] == password:
        return True, users[email]["name"]
    return False, None

def is_authenticated():
    return st.session_state.get("authenticated", False)

def login(email, name):
    try:
        st.session_state["authenticated"] = True
        st.session_state["email"] = email
        st.session_state["name"] = name
    except Exception as e:
        st.error(f"Ошибка при сохранении данных: {str(e)}")

def logout():
    st.session_state["authenticated"] = False
    st.session_state["email"] = None
    st.session_state["name"] = None
    
    

def echo_api(input_text):
    return f"Ответ на '{input_text}': Это пример ответа."

# Инициализация приложения
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
    st.session_state["email"] = None
    st.session_state["name"] = None

# Навигация в боковом меню
st.sidebar.title("Навигация")
menu = st.sidebar.selectbox("Перейти к странице", ["Эхо-чат", "Регистрация", "Авторизация", "Профиль"])

if menu == "Регистрация":
    st.title("Регистрация")
    with st.form("registration_form"):
        name = st.text_input("Имя")
        email = st.text_input("Email")
        password = st.text_input("Пароль", type="password")
        submitted = st.form_submit_button("Зарегистрироваться")
        if submitted:
            success, message = register_user(name, email, password)
            st.success(message) if success else st.error(message)

elif menu == "Авторизация":
    st.title("Авторизация")
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Пароль", type="password")
        submitted = st.form_submit_button("Войти")
        if submitted:
            authenticated, name = authenticate_user(email, password)
            if authenticated:
                login(email, name)
                st.success("Успешный вход.")
            else:
                st.error("Неверные email или пароль.")


elif menu == "Профиль":
    if is_authenticated():
        st.title("Профиль")
        st.write(f"**Имя:** {st.session_state['name']}")
        st.write(f"**Email:** {st.session_state['email']}")
        if st.button("Выйти"):
            logout()
            st.success("Вы вышли из системы.")
    else:
        st.error("Вы должны войти в систему, чтобы просмотреть эту страницу.")

elif menu == "Эхо-чат":
    if is_authenticated():
        st.title("Эхо-чат")
        with st.form("chat_form"):
            user_input = st.text_input("Введите текст для бота")
            submitted = st.form_submit_button("Отправить")
            if submitted:
                response = echo_api(user_input)
                st.write(response)
    else:
        st.error("Вы должны войти в систему, чтобы воспользоваться чатом.")
