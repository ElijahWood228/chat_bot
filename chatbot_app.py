import streamlit as st
import requests

# Функции для проверки и управления пользователем
users = {}  # Хранилище для зарегистрированных пользователей {email: {"name": ..., "password": ...}}

# Функция для проверки email через BulkEmailVerifier API
def verify_email(email):
    # Ваш API-ключ, полученный на EmailListVerify
    api_key = "your_api_key"  # Замените на свой API-ключ
    
    url = "https://api.email-list-verify.com/v1/verify"
    
    params = {
        "email": email,
        "api_key": api_key
    }
    
    try:
        # Отправка запроса на проверку email
        response = requests.get(url, params=params)
        response.raise_for_status()  # Пытаемся получить успешный ответ от API (код 2xx)
        
        # Получение результата в формате JSON
        result = response.json()
        
        # Возвращаем результат, например, статус email
        return result
        
    except requests.exceptions.RequestException as e:
        print(f"Ошибка соединения: {e}")
        return None


def registration():
    # Ввод данных пользователем
    name = st.text_input("Введите имя")
    email = st.text_input("Введите email")
    password = st.text_input("Введите пароль", type="password")
    
    if st.button("Зарегистрироваться"):
        # Проверка email на валидность через API
        result = verify_email(email)
        
        if result and result.get('status') == 'valid':
            # Если email валиден
            st.session_state["name"] = name
            st.session_state["email"] = email
            st.session_state["password"] = password
            st.success("Регистрация успешна! Проверьте свой email.")
        else:
            # Если email невалиден
            st.error("Введённый email не является действительным.")


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
            success, message = registration(name, email, password)
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
