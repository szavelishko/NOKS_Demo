"""Загрузка исходных данных кейса «КПЭ-аналитик».

load_all() возвращает словарь:
  kpi        — DataFrame, лист «Дерево и паспорта» (02_Карта_КПЭ.xlsx)
  ind_kpi    — DataFrame, лист «Индивидуальные КПЭ» (02_Карта_КПЭ.xlsx)
  fact_plan  — DataFrame, лист «Факт_план» (03_Факт_план.xlsx)
  interseg   — DataFrame, лист «Внутригрупповые обороты» (03_Факт_план.xlsx)
  employees  — DataFrame, лист «Сотрудники» (08_Сотрудники_и_карты_КПЭ.xlsx)
  cards      — DataFrame, лист «Карты КПЭ» (08_Сотрудники_и_карты_КПЭ.xlsx)
  docs       — dict {имя файла: полный текст} для всех .docx
  files      — список имён загруженных файлов
"""
from pathlib import Path

import pandas as pd
from docx import Document

DATA_DIR = Path(__file__).parent / "data"
UPLOAD_DIR = Path(__file__).parent / "uploads"

EXCEL_SHEETS = {
    "02_Карта_КПЭ.xlsx": {"kpi": "Дерево и паспорта", "ind_kpi": "Индивидуальные КПЭ"},
    "03_Факт_план.xlsx": {"fact_plan": "Факт_план", "interseg": "Внутригрупповые обороты"},
    "08_Сотрудники_и_карты_КПЭ.xlsx": {"employees": "Сотрудники", "cards": "Карты КПЭ"},
}


def docx_to_text(path: Path) -> str:
    """Текст документа Word: абзацы и таблицы, с сохранением нумерации пунктов."""
    doc = Document(path)
    parts = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    for table in doc.tables:
        for row in table.rows:
            parts.append(" | ".join(c.text.strip() for c in row.cells))
    return "\n".join(parts)


def _source_dir() -> Path:
    """Если пользователь загрузил свои файлы, используем их, иначе встроенный пакет."""
    if UPLOAD_DIR.exists() and any(UPLOAD_DIR.iterdir()):
        return UPLOAD_DIR
    return DATA_DIR


def load_all() -> dict:
    src = _source_dir()
    data: dict = {"docs": {}, "files": [], "source": str(src.name)}
    for fname, sheets in EXCEL_SHEETS.items():
        path = src / fname
        if not path.exists():
            continue
        data["files"].append(fname)
        for key, sheet in sheets.items():
            data[key] = pd.read_excel(path, sheet_name=sheet)
    for path in sorted(src.glob("*.docx")):
        data["docs"][path.name] = docx_to_text(path)
        data["files"].append(path.name)
    return data
