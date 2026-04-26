import base64
import json
import streamlit as st

# ── Load question banks from Streamlit secrets ────────────────────────────────
def _load(key):
    return json.loads(base64.b64decode(st.secrets["questions"][key]).decode("utf-8"))

AI_ENGINEER_QUESTIONS  = _load("prompt_engineer")
DEVELOPER_QUESTIONS_A  = _load("developer_a")
DEVELOPER_QUESTIONS_B  = _load("developer_b")
DEVELOPER_QUESTIONS_C  = _load("developer_c")
QA_QUESTIONS           = _load("quality_assurance")
UIUX_QUESTIONS         = _load("ui_ux")
DEVOPS_QUESTIONS       = _load("devops")
PM_QUESTIONS           = _load("product_manager")

# ── QUIZ ASSIGNMENTS ──────────────────────────────────────────────────────────
QUIZ_ASSIGNMENTS = {
    "sharjeel@sideline.agency":     "prompt_engineer",
    "anas@sideline.agency":          "developer_a",
    "farzam@sideline.agency":        "product_manager",
    "hashim@sideline.agency":        "developer_b",
    "nudrat@sideline.agency":        "developer_c",
    "sardar@sideline.agency":        "developer_b",
    "faisal@sideline.agency":        "developer_a",
    "rahat@sideline.agency":         "developer_b",
    "abdulqadir@sideline.agency":    "prompt_engineer",
    "samaika@sideline.agency":       "quality_assurance",
    "arslan@sideline.agency":        "developer_c",
    "muzamil@sideline.agency":       "ui_ux",
    "arbaz@sideline.agency":         "product_manager",
    "bilal@sideline.agency":         "devops",
    "zeeshan@sideline.agency":       "developer_a",
    "tayyab@sideline.agency":        "devops",
    "mahnoor@sideline.agency":       "developer_b",
    "atsam@sideline.agency":         "prompt_engineer",
    "Gulsher@sideline.agency":       "developer_c",
    "danish@sideline.agency":        "developer_b",
    "kawish@sideline.agency":        "developer_a",
    "ahmad@sideline.agency":         "developer_a",
    "talharauf@sideline.agency":     "prompt_engineer",
    "rizwan@sideline.agency":        "devops",
    "maria@sideline.agency":         "ui_ux",
    "sardarkhurram@sideline.agency": "developer_c",
    "atif@sideline.agency":          "prompt_engineer",
    "imad@sideline.agency":          "developer_b",
    "rabia@sideline.agency":         "quality_assurance",
    "zainab@sideline.agency":        "product_manager",
    "ahsan@sideline.agency":         "developer_a",
    "kinza@sideline.agency":         "quality_assurance",
    "mohsin@sideline.agency":        "developer_c",
    "raheel@sideline.agency":        "developer_c",
    "hashimhussain@sideline.agency": "ui_ux",
    "sanum@sideline.agency":         "developer_b",
    "sana@sideline.agency":          "quality_assurance",
    "sajjad@sideline.agency":        "developer_c",
    "asma@sideline.agency":          "quality_assurance",
    "touseef@sideline.agency":       "developer_c",
    "meesum@sideline.agency":        "developer_a",
    "umair@sideline.agency":         "developer_a",
    "ramayabaidullah@gmail.com":     "prompt_engineer",
    "abaidullah@sideline.agency":    "developer_c",
}

# ── QUIZ CONFIGS ──────────────────────────────────────────────────────────────
QUIZ_CONFIGS = {
    "prompt_engineer": {
        "title": "Prompt Quiz — Prompt Engineers",
        "icon": "🧠",
        "color": "#818cf8",
        "topic": "Prompt Engineering",
        "tag_section": ("AI Ecosystem", "name every tool, model & framework you know"),
        "questions": AI_ENGINEER_QUESTIONS,
    },
    "developer_a": {
        "title": "Prompt Quiz — Developers",
        "icon": "💻",
        "color": "#34d399",
        "topic": "Prompt Engineering for Developers",
        "tag_section": ("Dev Ecosystem", "name every language, framework & AI tool you use"),
        "questions": DEVELOPER_QUESTIONS_A,
    },
    "developer_b": {
        "title": "Prompt Quiz — Developers",
        "icon": "💻",
        "color": "#34d399",
        "topic": "Prompt Engineering for Developers",
        "tag_section": ("Dev Ecosystem", "name every language, framework & AI tool you use"),
        "questions": DEVELOPER_QUESTIONS_B,
    },
    "developer_c": {
        "title": "Prompt Quiz — Developers",
        "icon": "💻",
        "color": "#34d399",
        "topic": "Prompt Engineering for Developers",
        "tag_section": ("Dev Ecosystem", "name every language, framework & AI tool you use"),
        "questions": DEVELOPER_QUESTIONS_C,
    },
    "quality_assurance": {
        "title": "Prompt Quiz — Quality Assurance",
        "icon": "🔍",
        "color": "#f59e0b",
        "topic": "Prompt Engineering for QA Engineers",
        "tag_section": ("QA Toolkit", "name every testing tool, framework & AI assistant you use"),
        "questions": QA_QUESTIONS,
    },
    "ui_ux": {
        "title": "Prompt Quiz — UI/UX",
        "icon": "🎨",
        "color": "#a78bfa",
        "topic": "Prompt Engineering for UI/UX Designers",
        "tag_section": ("Design Toolkit", "name every design, research & AI tool you use"),
        "questions": UIUX_QUESTIONS,
    },
    "devops": {
        "title": "Prompt Quiz — DevOps",
        "icon": "⚙️",
        "color": "#38bdf8",
        "topic": "Prompt Engineering for DevOps Engineers",
        "tag_section": ("DevOps Toolkit", "name every CI/CD, IaC, container & cloud tool you use"),
        "questions": DEVOPS_QUESTIONS,
    },
    "product_manager": {
        "title": "Prompt Quiz — Product Managers",
        "icon": "📦",
        "color": "#fb923c",
        "topic": "Prompt Engineering for Product Managers",
        "tag_section": ("PM Toolkit", "name every roadmap, analytics, research & AI tool you use"),
        "questions": PM_QUESTIONS,
    },
}
