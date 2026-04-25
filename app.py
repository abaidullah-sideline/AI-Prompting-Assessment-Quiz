import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
from questions import QUIZ_CONFIGS, QUIZ_ASSIGNMENTS
from utils import get_llama_recommendation, send_result_email, get_level, score_scenario_with_llm

# ── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Sideline Technologies",
    page_icon="📋",
    layout="centered",
    initial_sidebar_state="collapsed"
)

QUIZ_DURATION_SECONDS = 1800  # 30 minutes

# ── CUSTOM CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }

[data-testid="stAppViewContainer"] { background: #0a0f1e; }
[data-testid="stHeader"]           { background: transparent; }
[data-testid="stSidebar"]          { display: none; }
[data-testid="stDecoration"]       { display: none; }
section[data-testid="stMain"]      { padding-top: 1.5rem; }

/* ── Question container left-border colours via :has() ── */
[data-testid="stVerticalBlockBorderWrapper"]:has([data-qtype="mcq"]) {
    border-left: 4px solid #3b82f6 !important;
    background: rgba(59,130,246,.03) !important;
}
[data-testid="stVerticalBlockBorderWrapper"]:has([data-qtype="scenario"]) {
    border-left: 4px solid #8b5cf6 !important;
    background: rgba(139,92,246,.03) !important;
}
[data-testid="stVerticalBlockBorderWrapper"]:has([data-qtype="tags"]) {
    border-left: 4px solid #10b981 !important;
    background: rgba(16,185,129,.03) !important;
}
[data-testid="stVerticalBlockBorderWrapper"]:has([data-qtype="text"]) {
    border-left: 4px solid #f59e0b !important;
    background: rgba(245,158,11,.03) !important;
}

/* ── Section divider ── */
.section-divider {
    background: linear-gradient(90deg, rgba(99,102,241,.12), transparent 80%);
    border-left: 3px solid #6366f1;
    padding: 0.55rem 1rem;
    border-radius: 0 8px 8px 0;
    margin: 2.5rem 0 1rem;
}
.section-divider h3 {
    color: #a5b4fc; font-size: 0.82rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.1em; margin: 0;
}

/* ── Tag chips ── */
.tags-wrap {
    display: flex; flex-wrap: wrap; gap: 6px; min-height: 44px;
    padding: 8px 12px; background: #0d1117; border: 1px solid #1e3a5f;
    border-radius: 8px; margin-bottom: 0.6rem; align-items: center;
}
.tag-chip {
    background: rgba(16,185,129,.15); color: #34d399;
    border: 1px solid rgba(16,185,129,.3); border-radius: 20px;
    padding: 3px 11px; font-size: 0.8rem; font-weight: 500;
}
.tag-empty { color: #334155; font-size: 0.82rem; }

/* ── Login ── */
.hero { text-align: center; padding: 2.5rem 0 1.5rem; }
.hero-icon { font-size: 4rem; line-height: 1; margin-bottom: 0.5rem; }
.hero-title {
    font-size: 2.4rem; font-weight: 800; margin: 0; letter-spacing: -0.02em;
    background: linear-gradient(135deg, #818cf8, #a78bfa, #38bdf8);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.hero-sub { color: #64748b; font-size: 1rem; margin-top: 0.5rem; }

/* ── Quiz header ── */
.quiz-header {
    border-radius: 16px; padding: 1.2rem 1.6rem; margin-bottom: 1.2rem;
    display: flex; justify-content: space-between; align-items: flex-start;
    border: 1px solid #1e3a5f;
}
.qh-title { font-size: 1.2rem; font-weight: 700; color: #f1f5f9; margin: 0; }
.qh-user  { font-size: 0.8rem; color: #64748b; margin: 3px 0 0; }

/* ── Submit banner ── */
.submit-banner {
    background: linear-gradient(135deg,rgba(99,102,241,.1),rgba(139,92,246,.1));
    border: 1px solid rgba(99,102,241,.2); border-radius: 16px;
    padding: 1.4rem; text-align: center; margin: 1.5rem 0 0.75rem;
}

/* ── Proctoring screens ── */
.screen-card {
    background: #1e293b; border-radius: 16px; padding: 3rem 2rem;
    text-align: center; border: 1px solid #334155; margin-top: 3rem;
}
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ─────────────────────────────────────────────────────────────
for k, v in {"authenticated": False, "current_user": None, "quiz_type": None,
              "start_time": None, "cheated": False, "time_up": False,
              "submitted": False, "final_score": "", "final_level": "",
              "email_sent": False, "email_error": ""}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── LOGIN ─────────────────────────────────────────────────────────────────────
if not st.session_state.authenticated:
    st.markdown("""
<div class="hero">
    <div class="hero-icon">📋</div>
    <h1 class="hero-title">Sideline AI Prompting Assessment</h1>
    <p class="hero-sub">Enter your credentials to begin your assigned quiz.</p>
</div>
""", unsafe_allow_html=True)

    _, col, _ = st.columns([1, 2.2, 1])
    with col:
        st.markdown(
            '<div style="display:flex;gap:8px;justify-content:center;flex-wrap:wrap;margin-bottom:1.5rem">'
            '<span style="background:rgba(99,102,241,.15);color:#818cf8;border:1px solid rgba(99,102,241,.3);border-radius:20px;padding:5px 14px;font-size:.8rem;font-weight:600">📋 20 Questions</span>'
            '<span style="background:rgba(16,185,129,.15);color:#34d399;border:1px solid rgba(16,185,129,.3);border-radius:20px;padding:5px 14px;font-size:.8rem;font-weight:600">⏱ 30 Minutes</span>'
            '<span style="background:rgba(245,158,11,.15);color:#fbbf24;border:1px solid rgba(245,158,11,.3);border-radius:20px;padding:5px 14px;font-size:.8rem;font-weight:600">🏆 100 Points</span>'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div style="background:rgba(239,68,68,.08);border:1px solid rgba(239,68,68,.2);'
            'border-radius:12px;padding:14px 18px;margin-bottom:1.4rem">'
            '<p style="margin:0 0 6px;font-size:.78rem;font-weight:700;color:#f87171;'
            'text-transform:uppercase;letter-spacing:.07em">⚠️ Important — Please Read</p>'
            '<ul style="margin:0;padding-left:1.2rem;color:#94a3b8;font-size:.82rem;line-height:1.9">'
            '<li>Switching tabs or minimising the window will <strong style="color:#fca5a5">immediately terminate</strong> your quiz.</li>'
            '<li>You have <strong style="color:#fca5a5">30 minutes</strong> — the timer starts the moment you click Begin Exam.</li>'
            '<li>If your quiz is terminated, you must <strong style="color:#fca5a5">contact the invigilator</strong> to restart.</li>'
            '</ul></div>',
            unsafe_allow_html=True
        )

        username    = st.text_input("Username / Candidate ID", placeholder="your@email.com")
        access_code = st.text_input("Access Code", type="password", placeholder="Enter your access code")

        if st.button("Begin Exam →", use_container_width=True, type="primary"):
            valid = any(
                u == username and p == access_code
                for u, p in st.secrets["credentials"].items()
            )
            if valid:
                # Clear any leftover question state from a previous session
                for qid in range(1, 21):
                    for key in [f"q{qid}_answer", f"q{qid}_tags", f"q{qid}_tag_input"]:
                        st.session_state.pop(key, None)

                st.session_state.authenticated = True
                st.session_state.current_user  = username
                st.session_state.quiz_type     = QUIZ_ASSIGNMENTS.get(username, "prompt_engineer")
                st.session_state.start_time    = datetime.now()
                st.rerun()
            else:
                st.error("Invalid credentials. Please check your username and access code.")

        st.markdown(
            '<p style="text-align:center;color:#334155;font-size:.78rem;margin-top:1.2rem;line-height:1.6">'
            'By starting this exam you agree to the proctoring terms.<br>'
            'Switching tabs or minimising the window will terminate your quiz.</p>',
            unsafe_allow_html=True
        )
    st.stop()

# ── SUBMISSION SUCCESS SCREEN (must come before time_up guard) ────────────────
if st.session_state.submitted:
    score_display = st.session_state.final_score
    level_display = st.session_state.final_level
    if st.session_state.email_sent:
        email_html = (
            '<p style="color:#34d399;font-size:.9rem;margin:.5rem 0">'
            '✅ Results emailed successfully.</p>'
        )
    else:
        err = st.session_state.email_error.replace("\n", "<br>")
        email_html = (
            f'<p style="color:#f59e0b;font-size:.9rem;margin:.5rem 0">'
            f'⚠️ Email could not be sent.</p>'
            f'<p style="color:#64748b;font-size:.78rem;white-space:pre-line;'
            f'background:#0f172a;border-radius:8px;padding:10px 14px;margin:.5rem 0;text-align:left">'
            f'{err}</p>'
        )
    st.markdown(f"""
<div class="screen-card">
    <div style="font-size:3.5rem;margin-bottom:1rem">🎉</div>
    <p style="font-size:1.4rem;font-weight:700;color:#f1f5f9;margin:.5rem 0">Quiz Submitted Successfully!</p>
    <div style="display:flex;gap:16px;justify-content:center;margin:1.2rem 0">
        <div style="background:#1e3a5f;border-radius:12px;padding:14px 28px;text-align:center;min-width:110px">
            <p style="margin:0;font-size:.72rem;color:#64748b;text-transform:uppercase;letter-spacing:.07em">Score</p>
            <p style="margin:6px 0 0;font-size:1.8rem;font-weight:800;color:#818cf8">{score_display}</p>
        </div>
        <div style="background:#1e3a5f;border-radius:12px;padding:14px 28px;text-align:center;min-width:110px">
            <p style="margin:0;font-size:.72rem;color:#64748b;text-transform:uppercase;letter-spacing:.07em">Level</p>
            <p style="margin:6px 0 0;font-size:1.8rem;font-weight:800;color:#a78bfa">{level_display}</p>
        </div>
    </div>
    {email_html}
    <p style="color:#334155;font-size:.8rem;margin-top:1.5rem">You may now close this window.</p>
</div>
""", unsafe_allow_html=True)
    st.stop()

# ── PROCTORING GUARDS ─────────────────────────────────────────────────────────
if st.session_state.cheated:
    st.markdown("""
<div class="screen-card">
    <div style="font-size:3.5rem;margin-bottom:1rem">🚨</div>
    <p style="font-size:1.4rem;font-weight:700;color:#f1f5f9;margin:.5rem 0">Quiz Terminated</p>
    <p style="color:#64748b">You switched tabs or minimised the browser window.<br>Your session has been locked and flagged.</p>
</div>
""", unsafe_allow_html=True)
    st.stop()

elapsed_s = (datetime.now() - st.session_state.start_time).total_seconds()
if st.session_state.time_up or elapsed_s > QUIZ_DURATION_SECONDS:
    st.markdown("""
<div class="screen-card">
    <div style="font-size:3.5rem;margin-bottom:1rem">⏳</div>
    <p style="font-size:1.4rem;font-weight:700;color:#f1f5f9;margin:.5rem 0">Time Is Up</p>
    <p style="color:#64748b">Your 30-minute window has expired.<br>The quiz has been locked.</p>
</div>
""", unsafe_allow_html=True)
    st.stop()

# ── LOAD QUIZ CONFIG ──────────────────────────────────────────────────────────
quiz_cfg  = QUIZ_CONFIGS[st.session_state.quiz_type]
QUESTIONS = quiz_cfg["questions"]
TOTAL_PTS = sum(q["points"] for q in QUESTIONS)  # always 100

# Init question session state (idempotent — setdefault only sets if missing)
for q in QUESTIONS:
    if q["type"] == "tags":
        st.session_state.setdefault(f"q{q['id']}_tags", [])
        st.session_state.setdefault(f"q{q['id']}_tag_input", "")
    else:
        st.session_state.setdefault(f"q{q['id']}_answer", None if q["type"] == "mcq" else "")

# ── HIDDEN ANTI-CHEAT BUTTONS ─────────────────────────────────────────────────
if st.button("HiddenCheatButton", key="hcb"):
    st.session_state.cheated = True
    st.rerun()
if st.button("HiddenTimeUpButton", key="htub"):
    st.session_state.time_up = True
    st.rerun()

# ── TIMER + ANTI-CHEAT JS ─────────────────────────────────────────────────────
remaining = max(0, QUIZ_DURATION_SECONDS - int(elapsed_s))

js = f"""
<script>
(function() {{
    var par  = window.parent;
    var pdoc = par.document;

    // Build fixed timer bar once; on reruns just update the clock text
    if (!pdoc.getElementById('qt-bar')) {{
        var bar = pdoc.createElement('div');
        bar.id = 'qt-bar';
        bar.style.cssText = (
            'position:fixed;top:0;left:0;right:0;z-index:99999;' +
            'background:#0a0f1e;border-bottom:1px solid #1e3a5f;' +
            'display:flex;align-items:center;justify-content:center;gap:10px;' +
            'padding:7px 20px;font-family:Inter,sans-serif;'
        );
        var lbl = pdoc.createElement('span');
        lbl.style.cssText = 'color:#475569;font-size:.82rem';
        lbl.innerText = '⏱ Time remaining:';
        var clk = pdoc.createElement('span');
        clk.id = 'qt';
        clk.style.cssText = (
            'font-size:1rem;font-weight:700;color:#34d399;' +
            'min-width:54px;font-variant-numeric:tabular-nums'
        );
        clk.innerText = '{remaining // 60}:{remaining % 60:02d}';
        bar.appendChild(lbl);
        bar.appendChild(clk);
        pdoc.body.appendChild(bar);
        var sty = pdoc.createElement('style');
        sty.id = 'qt-bar-style';
        sty.textContent = 'section[data-testid="stMain"] {{ padding-top: 2.8rem !important; }}';
        pdoc.head.appendChild(sty);
    }}

    var t  = {remaining};
    var el = pdoc.getElementById('qt');
    if (el) {{
        el.innerText  = Math.floor(t / 60) + ':' + String(t % 60).padStart(2, '0');
        el.style.color = t < 300 ? '#ef4444' : t < 600 ? '#f59e0b' : '#34d399';
    }}

    // textContent (not innerText) works even when the button's parent is display:none
    function findBtn(txt) {{
        return Array.from(pdoc.querySelectorAll('button'))
            .find(function(b) {{ return b.textContent.trim() === txt; }});
    }}

    setTimeout(function() {{
        ['HiddenCheatButton', 'HiddenTimeUpButton'].forEach(function(txt) {{
            var btn = findBtn(txt);
            if (btn) {{
                var node = btn;
                for (var i = 0; i < 5; i++) {{
                    node = node.parentElement;
                    if (!node) break;
                    if (node.getAttribute('data-testid') === 'column' ||
                        node.className.indexOf('stButton') !== -1) {{
                        node.style.cssText = 'display:none!important';
                        break;
                    }}
                }}
            }}
        }});
    }}, 800);

    // Clear any stale interval from the previous Streamlit rerun, then restart
    if (par._timerTick) clearInterval(par._timerTick);
    par._timerTick = setInterval(function() {{
        if (t <= 0) {{
            clearInterval(par._timerTick);
            var btn = findBtn('HiddenTimeUpButton');
            if (btn) btn.click();
            return;
        }}
        t--;
        var m = Math.floor(t / 60), s = t % 60;
        var e = pdoc.getElementById('qt');
        if (e) {{
            e.innerText   = m + ':' + String(s).padStart(2, '0');
            e.style.color = t < 300 ? '#ef4444' : t < 600 ? '#f59e0b' : '#34d399';
        }}
    }}, 1000);

    // Central cheat trigger — called by both listeners below
    function triggerCheat() {{
        var btn = findBtn('HiddenCheatButton');
        if (btn) btn.click();
    }}

    // Re-attach both listeners on every rerun so the closure is always fresh
    if (par._antiCheatListener) {{
        pdoc.removeEventListener('visibilitychange', par._antiCheatListener);
    }}
    if (par._antiCheatBlurListener) {{
        par.removeEventListener('blur', par._antiCheatBlurListener);
    }}

    // visibilitychange — catches tab switching
    par._antiCheatListener = function() {{
        if (pdoc.hidden) triggerCheat();
    }};
    pdoc.addEventListener('visibilitychange', par._antiCheatListener);

    // blur — catches window minimise, Alt+Tab, and switching to another app.
    // Delay before acting so transient browser UI (e.g. save-password popup)
    // that briefly steals focus and returns it doesn't falsely terminate the quiz.
    par._antiCheatBlurListener = function() {{
        setTimeout(function() {{
            if (!par.document.hasFocus()) {{
                triggerCheat();
            }}
        }}, 700);
    }};
    par.addEventListener('blur', par._antiCheatBlurListener);
}})();
</script>
"""
components.html(js, height=0)

# ── QUIZ HEADER ───────────────────────────────────────────────────────────────
qicon  = quiz_cfg["icon"]
qtitle = quiz_cfg["title"]
qcolor = quiz_cfg["color"]

st.markdown(
    f'<div class="quiz-header" style="background:linear-gradient(135deg,#1e293b,#0f172a)">'
    f'<div>'
    f'<p class="qh-title">{qicon} {qtitle}</p>'
    f'<p class="qh-user">Logged in as <strong style="color:#94a3b8">{st.session_state.current_user}</strong></p>'
    f'</div>'
    f'<div style="text-align:right">'
    f'<p style="font-size:.7rem;color:#334155;text-transform:uppercase;letter-spacing:.06em;margin:0">Total</p>'
    f'<p style="font-size:1.2rem;font-weight:800;color:{qcolor};margin:2px 0 0">100 pts</p>'
    f'</div>'
    f'</div>',
    unsafe_allow_html=True
)

# ── PROGRESS BAR ──────────────────────────────────────────────────────────────
answered = sum(
    1 for q in QUESTIONS
    if (q["type"] == "tags" and st.session_state.get(f"q{q['id']}_tags"))
    or (q["type"] != "tags" and st.session_state.get(f"q{q['id']}_answer") not in (None, ""))
)
st.markdown(
    f'<div style="display:flex;justify-content:space-between;margin-bottom:.35rem">'
    f'<span style="font-size:.78rem;color:#475569">Your progress</span>'
    f'<span style="font-size:.78rem;font-weight:600;color:#64748b">{answered}/{len(QUESTIONS)} answered</span>'
    f'</div>',
    unsafe_allow_html=True
)
st.progress(answered / len(QUESTIONS))

# ── HELPERS ───────────────────────────────────────────────────────────────────
BADGE_STYLES = {
    "mcq":      ("rgba(59,130,246,.2)",   "#60a5fa",  "MCQ"),
    "scenario": ("rgba(139,92,246,.2)",   "#a78bfa",  "Scenario"),
    "tags":     ("rgba(16,185,129,.2)",   "#34d399",  "AI Tools"),
    "text":     ("rgba(245,158,11,.2)",   "#fbbf24",  "Open Ended"),
}

# Section headers — Q18 label comes from the quiz config
tag_sec_title, tag_sec_sub = quiz_cfg["tag_section"]
SECTIONS = {
    1:  ("Multiple Choice Questions",  "12 questions · theory & concepts"),
    13: ("Practical Scenarios",         "5 questions · write real prompts"),
    18: (tag_sec_title,                 tag_sec_sub),
    19: ("Deep-Dive Open Questions",    "2 questions · show your thinking"),
}

def make_add_cb(q_id):
    def _cb():
        tag = st.session_state[f"q{q_id}_tag_input"].strip()
        if tag and tag not in st.session_state[f"q{q_id}_tags"]:
            st.session_state[f"q{q_id}_tags"].append(tag)
        st.session_state[f"q{q_id}_tag_input"] = ""
    return _cb

def make_clear_cb(q_id):
    def _cb():
        st.session_state[f"q{q_id}_tags"] = []
    return _cb

# ── RENDER QUESTIONS ──────────────────────────────────────────────────────────
for q in QUESTIONS:
    qid = q["id"]

    if qid in SECTIONS:
        sec_title, sec_sub = SECTIONS[qid]
        st.markdown(
            f'<div class="section-divider"><h3>{sec_title} '
            f'<span style="font-weight:400;color:#475569;text-transform:none;letter-spacing:0">— {sec_sub}</span></h3></div>',
            unsafe_allow_html=True
        )

    bg, color, label = BADGE_STYLES[q["type"]]

    with st.container(border=True):
        # Hidden zero-height marker for CSS :has() targeting
        st.markdown(
            f'<div data-qtype="{q["type"]}" style="height:0;overflow:hidden;margin:0;padding:0"></div>',
            unsafe_allow_html=True
        )

        col_badge, col_meta = st.columns([7, 3])
        with col_badge:
            st.markdown(
                f'<span style="background:{bg};color:{color};border-radius:20px;'
                f'padding:2px 10px;font-size:.7rem;font-weight:700;'
                f'text-transform:uppercase;letter-spacing:.06em">{label}</span>',
                unsafe_allow_html=True
            )
        with col_meta:
            st.caption(f"Q{qid} of {len(QUESTIONS)}  ·  {q['points']} pts")

        if q["type"] == "scenario":
            st.write(q["text"])
            if q.get("code"):
                lang = "python" if any(x in q["code"] for x in ["Traceback", "TypeError", "File", "def ", "import"]) else "javascript"
                st.code(q["code"], language=lang)
            st.markdown(f"**{q['prompt_label']}**")
        else:
            st.markdown(f"**{q['text']}**")
            if q.get("description"):
                st.caption(q["description"])

        # ── Widget ─────────────────────────────────────────────────────────
        if q["type"] == "mcq":
            st.radio(
                "answer", q["options"],
                key=f"q{qid}_answer", index=None,
                label_visibility="collapsed",
            )

        elif q["type"] == "scenario":
            st.text_area(
                "prompt", key=f"q{qid}_answer",
                height=120, placeholder="Write your prompt here…",
                label_visibility="collapsed",
            )

        elif q["type"] == "tags":
            tags = st.session_state[f"q{qid}_tags"]
            chips = (
                "".join(f'<span class="tag-chip">✦ {t}</span>' for t in tags)
                if tags else '<span class="tag-empty">No tools added yet…</span>'
            )
            st.markdown(f'<div class="tags-wrap">{chips}</div>', unsafe_allow_html=True)

            c_inp, c_add, c_clr = st.columns([5, 1.3, 1.3])
            with c_inp:
                st.text_input("tool", key=f"q{qid}_tag_input",
                              placeholder="Type a tool name and click Add…",
                              label_visibility="collapsed")
            with c_add:
                st.button("Add →", key=f"add_{qid}",
                          on_click=make_add_cb(qid), use_container_width=True)
            with c_clr:
                st.button("Clear", key=f"clr_{qid}",
                          on_click=make_clear_cb(qid), use_container_width=True)
            if tags:
                st.caption(f"{len(tags)} tool(s) added · {min(len(tags), q['points'])}/{q['points']} pts")

        elif q["type"] == "text":
            st.text_area(
                "answer", key=f"q{qid}_answer",
                height=150, placeholder=q.get("placeholder", "Write your answer here…"),
                label_visibility="collapsed",
            )

# ── SUBMIT ────────────────────────────────────────────────────────────────────
unanswered = len(QUESTIONS) - answered
warn = (f" · <span style='color:#f59e0b'>{unanswered} unanswered</span>"
        if unanswered else " ✅")
st.markdown(
    f'<div class="submit-banner">'
    f'<p style="color:#94a3b8;font-size:.9rem;margin:0"><strong style="color:{qcolor}">'
    f'{answered}/20 answered</strong>{warn}</p>'
    f'<p style="color:#475569;font-size:.78rem;margin:.3rem 0 0">'
    f'Once submitted the quiz will be locked and results emailed to you.</p>'
    f'</div>',
    unsafe_allow_html=True
)

if st.button("🚀  Submit Quiz", use_container_width=True, type="primary"):
    score = 0
    with st.spinner("Grading and generating AI feedback…"):
        for q in QUESTIONS:
            qid = q["id"]
            if q["type"] == "mcq":
                if st.session_state.get(f"q{qid}_answer") == q["answer"]:
                    score += q["points"]
            elif q["type"] == "scenario":
                answer = (st.session_state.get(f"q{qid}_answer") or "").strip()
                if answer:
                    score += score_scenario_with_llm(
                        q["text"], answer, q["expected_answer"], q["points"]
                    )
            elif q["type"] == "tags":
                score += min(len(st.session_state.get(f"q{qid}_tags", [])), q["points"])
            elif q["type"] == "text":
                answer = (st.session_state.get(f"q{qid}_answer") or "").strip()
                if answer:
                    score += score_scenario_with_llm(
                        q["text"], answer, q["expected_answer"], q["points"]
                    )

        final_score = f"{score}/{TOTAL_PTS}"
        level_label, level_name, next_label, next_name = get_level(score)
        level_str = f"{level_label} {level_name}"
        next_str  = f"{next_label} {next_name}"
        ai_feedback = get_llama_recommendation(
            st.session_state.current_user, final_score,
            quiz_cfg["topic"], level_str, next_str
        )
        email_sent, email_error = send_result_email(
            st.session_state.current_user, final_score, level_str, ai_feedback
        )

    st.session_state.submitted   = True
    st.session_state.final_score = final_score
    st.session_state.final_level = level_str
    st.session_state.email_sent  = email_sent
    st.session_state.email_error = email_error
    st.rerun()
