"""КПЭ-аналитик · ГК «Меридиан» — стартовый шаблон (урок 7).

Вкладки «Дерево КПЭ», «Отклонения», «Методология», «Люди и процессы»
и «Записка правлению» заполняются на шагах 1–5 практики промптами в Replit Agent.
"""
import streamlit as st

import analytics  # noqa: F401  расчёты добавляются на шагах практики
from data_loader import UPLOAD_DIR, load_all
from llm import ask_gemini, key_is_set, model_name

st.set_page_config(page_title="КПЭ-аналитик · ГК «Меридиан»", page_icon="📊", layout="wide")

ORANGE = "#F58200"
st.markdown(
    f"""
    <style>
      .block-container {{padding-top: 1.6rem;}}
      h1, h2, h3 {{color: #58595B;}}
      .tag {{background:{ORANGE}; color:white; padding:4px 12px; border-radius:4px; font-weight:600;}}
      .placeholder {{background:#F4F4F4; border:1px dashed #C8C8C8; border-radius:8px; padding:24px; color:#58595B;}}
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data(show_spinner="Загружаю данные…")
def get_data(_version: int):
    return load_all()


if "data_version" not in st.session_state:
    st.session_state.data_version = 0
data = get_data(st.session_state.data_version)

# ---------------- Боковая панель ----------------
with st.sidebar:
    st.markdown('<span class="tag">КПЭ-аналитик</span>', unsafe_allow_html=True)
    st.caption("ГК «Меридиан» · учебный кейс, данные синтетические")

    st.subheader("Данные")
    st.write(f"Источник: **{'встроенный пакет' if data['source'] == 'data' else 'загруженные файлы'}**")
    st.write(f"Файлов загружено: **{len(data['files'])}**")
    uploaded = st.file_uploader(
        "Загрузить свои файлы (xlsx, docx)", type=["xlsx", "docx"], accept_multiple_files=True
    )
    if uploaded and st.button("Использовать загруженные файлы"):
        UPLOAD_DIR.mkdir(exist_ok=True)
        for f in uploaded:
            (UPLOAD_DIR / f.name).write_bytes(f.getbuffer())
        st.session_state.data_version += 1
        st.rerun()
    if UPLOAD_DIR.exists() and any(UPLOAD_DIR.iterdir()) and st.button("Вернуть встроенный пакет"):
        for p in UPLOAD_DIR.iterdir():
            p.unlink()
        st.session_state.data_version += 1
        st.rerun()

    st.subheader("Модель")
    st.write(f"Ключ Gemini: **{'найден ✅' if key_is_set() else 'не найден ❌'}**")
    st.caption(f"Модель: {model_name()}")
    if st.button("Проверить связь с моделью"):
        with st.spinner("Спрашиваю модель…"):
            answer = ask_gemini("Ответь одним словом по-русски: «Готово».")
        if answer.startswith("Ошибка"):
            st.error(answer)
        else:
            st.success(f"Модель отвечает: {answer.strip()}")

# ---------------- Основная часть ----------------
st.title("КПЭ-аналитик · ГК «Меридиан»")
st.caption("Отчёт по КПЭ: от черновика к регламенту. Цифры считает код, слова пишет модель, решение принимает человек.")

tabs = st.tabs(
    ["📂 Данные", "🌳 Дерево КПЭ", "📉 Отклонения", "🧪 Методология", "👥 Люди и процессы", "📝 Записка правлению"]
)


def placeholder(step: str, text: str):
    st.markdown(f'<div class="placeholder"><b>{step}</b><br>{text}</div>', unsafe_allow_html=True)


with tabs[0]:
    st.subheader("Исходные данные")
    tables = [
        ("Карта КПЭ: дерево и паспорта", "kpi"),
        ("Индивидуальные КПЭ", "ind_kpi"),
        ("Факт и план по кварталам", "fact_plan"),
        ("Внутригрупповые обороты", "interseg"),
        ("Сотрудники", "employees"),
        ("Карты КПЭ сотрудников", "cards"),
    ]
    for title, key in tables:
        if key in data:
            with st.expander(f"{title} · {len(data[key])} строк"):
                st.dataframe(data[key], width="stretch", hide_index=True)
    st.subheader("Документы")
    for name, text in data["docs"].items():
        with st.expander(name):
            st.text(text)

with tabs[1]:
    placeholder("Шаг 1", "Здесь появится дерево КПЭ: каскад Группа → Дивизион → Подразделение, паспорта КПЭ и разрывы каскада.")
with tabs[2]:
    placeholder("Шаг 2", "Здесь появятся отклонения факта от плана, светофор и автокомментарии в едином нарративе.")
with tabs[3]:
    placeholder("Шаг 3", "Здесь появится контроль методологии: проверки кодом и экспертиза модели.")
with tabs[4]:
    placeholder("Шаг 4", "Здесь появится анализ связи КПЭ сотрудников с результатами и процессами.")
with tabs[5]:
    placeholder("Шаг 5", "Здесь появится управленческая записка к заседанию Правления с выгрузкой в Word.")
