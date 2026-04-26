import base64
import json
import streamlit as st

# ── Load question banks from Streamlit secrets ────────────────────────────────
def _load(key):
    return json.loads(base64.b64decode(st.secrets["questions"][key]).decode("utf-8"))

AI_ENGINEER_QUESTIONS = _load("prompt_engineer")
DEVELOPER_QUESTIONS   = _load("developer")
QA_QUESTIONS          = _load("quality_assurance")
UIUX_QUESTIONS        = _load("ui_ux")
DEVOPS_QUESTIONS      = _load("devops")
PM_QUESTIONS          = _load("product_manager")

# ── QUIZ ASSIGNMENTS ──────────────────────────────────────────────────────────
QUIZ_ASSIGNMENTS = {
    "sharjeel@sideline.agency":     "prompt_engineer",
    "anas@sideline.agency":         "developer",
    "farzam@sideline.agency":       "product_manager",
    "hashim@sideline.agency":       "developer",
    "nudrat@sideline.agency":       "developer",
    "sardar@sideline.agency":       "developer",
    "faisal@sideline.agency":       "developer",
    "rahat@sideline.agency":        "developer",
    "abdulqadir@sideline.agency":   "prompt_engineer",
    "samaika@sideline.agency":      "quality_assurance",
    "arslan@sideline.agency":       "developer",
    "muzamil@sideline.agency":      "ui_ux",
    "arbaz@sideline.agency":        "product_manager",
    "bilal@sideline.agency":        "devops",
    "zeeshan@sideline.agency":      "developer",
    "tayyab@sideline.agency":       "devops",
    "mahnoor@sideline.agency":      "developer",
    "atsam@sideline.agency":        "prompt_engineer",
    "Gulsher@sideline.agency":      "developer",
    "danish@sideline.agency":       "developer",
    "kawish@sideline.agency":       "developer",
    "ahmad@sideline.agency":        "developer",
    "talharauf@sideline.agency":    "prompt_engineer",
    "rizwan@sideline.agency":       "devops",
    "maria@sideline.agency":        "ui_ux",
    "sardarkhurram@sideline.agency": "developer",
    "atif@sideline.agency":         "prompt_engineer",
    "imad@sideline.agency":         "developer",
    "rabia@sideline.agency":        "quality_assurance",
    "zainab@sideline.agency":       "product_manager",
    "ahsan@sideline.agency":        "developer",
    "kinza@sideline.agency":        "quality_assurance",
    "mohsin@sideline.agency":       "developer",
    "raheel@sideline.agency":       "developer",
    "hashimhussain@sideline.agency": "ui_ux",
    "sanum@sideline.agency":        "developer",
    "sana@sideline.agency":         "quality_assurance",
    "sajjad@sideline.agency":       "developer",
    "asma@sideline.agency":         "quality_assurance",
    "touseef@sideline.agency":      "developer",
    "meesum@sideline.agency":       "developer",
    "umair@sideline.agency":        "developer",
    "ramayabaidullah@gmail.com":    "prompt_engineer",
    "abaidullah@sideline.agency":   "developer",
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
    "developer": {
        "title": "Prompt Quiz — Developers",
        "icon": "💻",
        "color": "#34d399",
        "topic": "Prompt Engineering for Developers",
        "tag_section": ("Dev Ecosystem", "name every language, framework & AI tool you use"),
        "questions": DEVELOPER_QUESTIONS,
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
