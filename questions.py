import base64
import json
import streamlit as st

# ── Load question banks from Streamlit secrets ────────────────────────────────
def _load(key):
    return json.loads(base64.b64decode(st.secrets["questions"][key]).decode("utf-8"))

AI_ENGINEER_QUESTIONS      = _load("prompt_engineer")
FRONTEND_VUE_QUESTIONS     = _load("frontend_engineer_vue")
FRONTEND_REACT_QUESTIONS   = _load("frontend_engineer_react")
BACKEND_RUBY_QUESTIONS     = _load("backend_engineer_ruby")
BACKEND_DOTNET_QUESTIONS   = _load("backend_engineer_dotnet")
ANDROID_QUESTIONS       = _load("android_developer")
IOS_QUESTIONS           = _load("ios_developer")
QA_QUESTIONS            = _load("quality_assurance")
UIUX_QUESTIONS          = _load("ui_ux")
DEVOPS_QUESTIONS        = _load("devops")
PM_QUESTIONS            = _load("product_manager")

# ── QUIZ ASSIGNMENTS ──────────────────────────────────────────────────────────
QUIZ_ASSIGNMENTS = {
    "sharjeel@sideline.agency":      "prompt_engineer",
    "anas@sideline.agency":          "backend_engineer_ruby",
    "farzam@sideline.agency":        "product_manager",
    "hashim@sideline.agency":        "backend_engineer_ruby",
    "nudrat@sideline.agency":        "ios_developer",
    "sardar@sideline.agency":        "android_developer",
    "faisal@sideline.agency":        "backend_engineer_dotnet",
    "rahat@sideline.agency":         "frontend_engineer_vue",
    "abdulqadir@sideline.agency":    "prompt_engineer",
    "samaika@sideline.agency":       "quality_assurance",
    "arslan@sideline.agency":        "backend_engineer_dotnet",
    "muzamil@sideline.agency":       "ui_ux",
    "arbaz@sideline.agency":         "product_manager",
    "bilal@sideline.agency":         "devops",
    "zeeshan@sideline.agency":       "backend_engineer_dotnet",
    "tayyab@sideline.agency":        "devops",
    "mahnoor@sideline.agency":       "android_developer",
    "atsam@sideline.agency":         "prompt_engineer",
    "Gulsher@sideline.agency":       "ios_developer",
    "danish@sideline.agency":        "backend_engineer_dotnet",
    "kawish@sideline.agency":        "frontend_engineer_react",
    "ahmad@sideline.agency":         "ios_developer",
    "talharauf@sideline.agency":     "prompt_engineer",
    "rizwan@sideline.agency":        "devops",
    "maria@sideline.agency":         "ui_ux",
    "sardarkhurram@sideline.agency": "android_developer",
    "atif@sideline.agency":          "prompt_engineer",
    "imad@sideline.agency":          "android_developer",
    "rabia@sideline.agency":         "quality_assurance",
    "zainab@sideline.agency":        "product_manager",
    "ahsan@sideline.agency":         "frontend_engineer_vue",
    "kinza@sideline.agency":         "quality_assurance",
    "mohsin@sideline.agency":        "frontend_engineer_vue",
    "raheel@sideline.agency":        "android_developer",
    "hashimhussain@sideline.agency": "ui_ux",
    "sanum@sideline.agency":         "ios_developer",
    "sana@sideline.agency":          "quality_assurance",
    "sajjad@sideline.agency":        "backend_engineer_dotnet",
    "asma@sideline.agency":          "quality_assurance",
    "touseef@sideline.agency":       "backend_engineer_dotnet",
    "meesum@sideline.agency":        "ios_developer",
    "umair@sideline.agency":         "backend_engineer_dotnet",
    "ramayabaidullah@gmail.com":     "prompt_engineer",
    "abaidullah@sideline.agency":    "backend_engineer_dotnet",
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
    "frontend_engineer_vue": {
        "title": "Prompt Quiz — Frontend Engineers (Vue)",
        "icon": "🖥️",
        "color": "#34d399",
        "topic": "Prompt Engineering for Frontend Engineers (Vue.js)",
        "tag_section": ("Frontend Ecosystem", "name every framework, library, tool & AI assistant you use"),
        "questions": FRONTEND_VUE_QUESTIONS,
    },
    "frontend_engineer_react": {
        "title": "Prompt Quiz — Frontend Engineers (React)",
        "icon": "🖥️",
        "color": "#61dafb",
        "topic": "Prompt Engineering for Frontend Engineers (React)",
        "tag_section": ("Frontend Ecosystem", "name every framework, library, tool & AI assistant you use"),
        "questions": FRONTEND_REACT_QUESTIONS,
    },
    "backend_engineer_ruby": {
        "title": "Prompt Quiz — Backend Engineers (Ruby on Rails)",
        "icon": "⚡",
        "color": "#ef4444",
        "topic": "Prompt Engineering for Backend Engineers (Ruby on Rails)",
        "tag_section": ("Backend Ecosystem", "name every gem, framework, database, cloud service & AI tool you use"),
        "questions": BACKEND_RUBY_QUESTIONS,
    },
    "backend_engineer_dotnet": {
        "title": "Prompt Quiz — Backend Engineers (.NET)",
        "icon": "⚡",
        "color": "#60a5fa",
        "topic": "Prompt Engineering for Backend Engineers (.NET)",
        "tag_section": ("Backend Ecosystem", "name every NuGet package, framework, database, cloud service & AI tool you use"),
        "questions": BACKEND_DOTNET_QUESTIONS,
    },
    "android_developer": {
        "title": "Prompt Quiz — Android Developers",
        "icon": "📱",
        "color": "#4ade80",
        "topic": "Prompt Engineering for Android Developers",
        "tag_section": ("Android Ecosystem", "name every library, Jetpack component, tool & AI assistant you use"),
        "questions": ANDROID_QUESTIONS,
    },
    "ios_developer": {
        "title": "Prompt Quiz — iOS Developers",
        "icon": "🍎",
        "color": "#f472b6",
        "topic": "Prompt Engineering for iOS Developers",
        "tag_section": ("iOS Ecosystem", "name every framework, library, tool & AI assistant you use"),
        "questions": IOS_QUESTIONS,
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
