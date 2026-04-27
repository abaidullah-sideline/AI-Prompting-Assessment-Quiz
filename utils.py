import smtplib
import ssl
import streamlit as st
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from groq import Groq

# ── Skill level ladder ────────────────────────────────────────────────────────
_LEVELS = [
    (0,  12,  "L1", "Novice"),
    (13, 25,  "L2", "Beginner"),
    (26, 38,  "L3", "Developing"),
    (39, 50,  "L4", "Competent"),
    (51, 63,  "L5", "Proficient"),
    (64, 75,  "L6", "Advanced"),
    (76, 88,  "L7", "Expert"),
    (89, 100, "L8", "Master"),
]

def get_level(score_int):
    """
    Returns (label, name, next_label, next_name) for a given integer score.
    At L8 Master, next_label/next_name equal the current level.
    """
    for i, (lo, hi, label, name) in enumerate(_LEVELS):
        if lo <= score_int <= hi:
            if i + 1 < len(_LEVELS):
                next_label, next_name = _LEVELS[i + 1][2], _LEVELS[i + 1][3]
            else:
                next_label, next_name = label, name
            return label, name, next_label, next_name
    return "L1", "Novice", "L2", "Beginner"


def score_scenario_with_llm(question, student_answer, expected_answer, max_points):
    """
    Uses LLM to score a scenario (prompt-writing) answer against the rubric.
    Returns an integer 0–max_points.
    """
    client = Groq(api_key=st.secrets["api_keys"]["groq_api_key"])

    prompt = f"""You are an expert prompt engineering assessor. Score the student's answer.

TASK QUESTION:
{question}

GRADING RUBRIC (criteria a strong answer must address):
{expected_answer}

STUDENT'S ANSWER:
{student_answer}

Score the answer from 0 to {max_points} using this scale:
{max_points} — Addresses all rubric criteria, specific and actionable
{max_points - 1} — Addresses most criteria, mostly specific
{round(max_points * 0.6)} — Addresses some criteria, missing key elements
{round(max_points * 0.4)} — Shows partial understanding, too vague
1 — Minimal understanding, very incomplete
0 — Off-topic, empty, or fewer than 10 meaningful words

Reply with ONLY a single integer between 0 and {max_points}. No explanation."""

    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
            temperature=0,
            max_tokens=5,
        )
        score = int(response.choices[0].message.content.strip())
        return max(0, min(max_points, score))
    except Exception:
        return max_points // 2 if len(student_answer.strip()) >= 30 else 0


def get_llama_recommendation(username, score, topic, level, next_level):
    client = Groq(api_key=st.secrets["api_keys"]["groq_api_key"])

    at_top = level == next_level
    if at_top:
        improvement = "maintain and deepen their mastery at the highest level"
    else:
        improvement = f"advance from {level} to {next_level}"

    prompt = f"""
    You are an expert AI and Prompt Engineering tutor. A student named {username} just completed
    a 20-question quiz on {topic} and scored {score} out of 100.
    Their current skill level is {level} and their goal is to {improvement}.
    The quiz covered: zero-shot/few-shot/chain-of-thought prompting, hallucination, RAG,
    prompt injection, role prompting, context windows, practical prompt writing, and real-world
    prompt engineering use cases.
    In 3 concise, encouraging sentences: acknowledge their score and current level ({level}),
    identify the specific skill gap they must close to reach {next_level},
    and recommend one concrete next step (a resource, practice exercise, or concept to master).
    Be direct, warm, and actionable.
    """

    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            max_tokens=160,
        )
        return chat_completion.choices[0].message.content
    except Exception:
        return "Keep up the good work and continue reviewing the core concepts!"


def _build_answer_sheet_html(username, score, level, answer_log):
    """Builds the admin-only answer sheet HTML section."""
    rows = ""
    for a in answer_log:
        q_label = f"Q{a['id']} ({a['type'].upper()})"
        pts     = f"{a['earned']}/{a['points']}"

        if a["type"] == "mcq":
            icon   = "✅" if a["correct"] else "❌"
            detail = (
                f"<b>Answer:</b> {a['user_answer']}<br>"
                f"<b>Correct:</b> {a['correct_answer']}"
            )
            row_bg = "#f0fdf4" if a["correct"] else "#fff1f2"
        else:
            icon   = ""
            detail = f"<b>Answer:</b> {a['user_answer']}"
            row_bg = "#f8fafc"

        rows += f"""
        <tr style="background:{row_bg}">
          <td style="padding:8px 10px;font-size:.78rem;color:#64748b;white-space:nowrap;vertical-align:top">{q_label}</td>
          <td style="padding:8px 10px;font-size:.82rem;color:#1e293b;vertical-align:top">{a['text']}</td>
          <td style="padding:8px 10px;font-size:.82rem;color:#1e293b;vertical-align:top">{detail}</td>
          <td style="padding:8px 10px;font-size:.82rem;font-weight:700;color:#6366f1;white-space:nowrap;vertical-align:top;text-align:center">{icon} {pts}</td>
        </tr>"""

    return f"""
  <hr style="border:none;border-top:2px solid #6366f1;margin:28px 0">
  <h3 style="color:#6366f1;font-size:1rem;margin-bottom:4px">Answer Sheet — {username}</h3>
  <p style="color:#64748b;font-size:.8rem;margin:0 0 12px">Score: {score} &nbsp;|&nbsp; Level: {level}</p>
  <table style="width:100%;border-collapse:collapse;font-family:Arial,Helvetica,sans-serif">
    <thead>
      <tr style="background:#e0e7ff">
        <th style="padding:8px 10px;text-align:left;font-size:.75rem;color:#4338ca">Q#</th>
        <th style="padding:8px 10px;text-align:left;font-size:.75rem;color:#4338ca">Question</th>
        <th style="padding:8px 10px;text-align:left;font-size:.75rem;color:#4338ca">User Answer</th>
        <th style="padding:8px 10px;text-align:left;font-size:.75rem;color:#4338ca">Pts</th>
      </tr>
    </thead>
    <tbody>{rows}
    </tbody>
  </table>"""


def send_result_email(username, score, level, recommendation, answer_log=None):
    """
    Sends the quiz result email via Gmail SMTP (port 465, SSL).
    User receives a clean result email; sender receives a separate
    admin email that includes the full answer sheet.
    Returns (success: bool, error_message: str).
    """
    sender_email    = st.secrets["email_config"]["sender_email"]
    sender_password = st.secrets["email_config"]["sender_password"].replace(" ", "")

    recipient_email = next(
        (v for k, v in st.secrets["candidate_emails"].items() if k == username),
        username,
    )

    # ── User email (clean result — no answer sheet) ───────────────────────────
    user_msg = MIMEMultipart("alternative")
    user_msg["Subject"] = f"Your Quiz Results — {score} · {level}"
    user_msg["From"]    = sender_email
    user_msg["To"]      = recipient_email

    plain = (
        f"Hello {username},\n\n"
        f"Your quiz was submitted successfully.\n"
        f"Final Score : {score}\n"
        f"Skill Level : {level}\n\n"
        f"How to improve:\n{recommendation}\n\n"
        f"Thank you for participating!\n"
    )

    html = f"""<html>
<body style="font-family:Arial,Helvetica,sans-serif;max-width:580px;margin:0 auto;padding:24px;color:#1e293b">
  <h2 style="color:#6366f1;margin-bottom:4px">Quiz Submitted Successfully</h2>
  <p style="color:#64748b;margin-top:0">Secure Exam Portal</p>
  <hr style="border:none;border-top:1px solid #e2e8f0;margin:16px 0">
  <p>Hello <strong>{username}</strong>,</p>
  <p>Your quiz has been graded and your results are below.</p>

  <div style="display:flex;gap:12px;margin:20px 0">
    <div style="flex:1;background:#f1f5f9;border-radius:10px;padding:16px;text-align:center">
      <p style="margin:0;font-size:.75rem;color:#64748b;text-transform:uppercase;letter-spacing:.06em">Final Score</p>
      <p style="margin:6px 0 0;font-size:1.9rem;font-weight:800;color:#6366f1">{score}</p>
    </div>
    <div style="flex:1;background:#f1f5f9;border-radius:10px;padding:16px;text-align:center">
      <p style="margin:0;font-size:.75rem;color:#64748b;text-transform:uppercase;letter-spacing:.06em">Skill Level</p>
      <p style="margin:6px 0 0;font-size:1.9rem;font-weight:800;color:#8b5cf6">{level}</p>
    </div>
  </div>

  <h3 style="color:#334155;font-size:1rem;margin-bottom:8px">How to Improve</h3>
  <p style="color:#475569;line-height:1.6;background:#f8fafc;border-left:3px solid #6366f1;
     padding:12px 16px;border-radius:0 8px 8px 0;margin:0">{recommendation}</p>

  <hr style="border:none;border-top:1px solid #e2e8f0;margin:24px 0">
  <p style="color:#94a3b8;font-size:.8rem;margin:0">Secure Exam Portal — automated result notification</p>
</body>
</html>"""

    user_msg.attach(MIMEText(plain, "plain"))
    user_msg.attach(MIMEText(html,  "html"))

    # ── Admin email (result + full answer sheet) ──────────────────────────────
    admin_msg = MIMEMultipart("alternative")
    admin_msg["Subject"] = f"[Admin] {username} — {score} · {level}"
    admin_msg["From"]    = sender_email
    admin_msg["To"]      = sender_email

    admin_plain = (
        f"ADMIN COPY — {username}\n"
        f"Score : {score}\nLevel : {level}\n\n"
        f"Recommendation:\n{recommendation}\n\n"
        f"--- ANSWERS ---\n"
    )
    if answer_log:
        for a in answer_log:
            admin_plain += f"\nQ{a['id']} ({a['type']}) [{a['earned']}/{a['points']}]\n"
            admin_plain += f"  {a['text']}\n"
            admin_plain += f"  Answer: {a['user_answer']}\n"
            if a["type"] == "mcq":
                admin_plain += f"  Correct: {a['correct_answer']}\n"

    answer_sheet_html = _build_answer_sheet_html(username, score, level, answer_log or [])
    admin_html = f"""<html>
<body style="font-family:Arial,Helvetica,sans-serif;max-width:760px;margin:0 auto;padding:24px;color:#1e293b">
  <h2 style="color:#6366f1;margin-bottom:4px">Admin Copy — Quiz Submission</h2>
  <p style="color:#64748b;margin-top:0">Secure Exam Portal</p>
  <hr style="border:none;border-top:1px solid #e2e8f0;margin:16px 0">
  <p><strong>{username}</strong> has submitted their quiz.</p>

  <div style="display:flex;gap:12px;margin:20px 0">
    <div style="flex:1;background:#f1f5f9;border-radius:10px;padding:16px;text-align:center">
      <p style="margin:0;font-size:.75rem;color:#64748b;text-transform:uppercase;letter-spacing:.06em">Final Score</p>
      <p style="margin:6px 0 0;font-size:1.9rem;font-weight:800;color:#6366f1">{score}</p>
    </div>
    <div style="flex:1;background:#f1f5f9;border-radius:10px;padding:16px;text-align:center">
      <p style="margin:0;font-size:.75rem;color:#64748b;text-transform:uppercase;letter-spacing:.06em">Skill Level</p>
      <p style="margin:6px 0 0;font-size:1.9rem;font-weight:800;color:#8b5cf6">{level}</p>
    </div>
  </div>

  <h3 style="color:#334155;font-size:1rem;margin-bottom:8px">AI Recommendation</h3>
  <p style="color:#475569;line-height:1.6;background:#f8fafc;border-left:3px solid #6366f1;
     padding:12px 16px;border-radius:0 8px 8px 0;margin:0">{recommendation}</p>
  {answer_sheet_html}
  <hr style="border:none;border-top:1px solid #e2e8f0;margin:24px 0">
  <p style="color:#94a3b8;font-size:.8rem;margin:0">Secure Exam Portal — admin notification</p>
</body>
</html>"""

    admin_msg.attach(MIMEText(admin_plain, "plain"))
    admin_msg.attach(MIMEText(admin_html,  "html"))

    # ── Send both emails via port 465 (SSL) ───────────────────────────────────
    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, [recipient_email], user_msg.as_string())
            if sender_email != recipient_email:
                server.sendmail(sender_email, [sender_email], admin_msg.as_string())
        return True, ""
    except smtplib.SMTPAuthenticationError:
        return False, (
            "Authentication failed. Make sure:\n"
            "1. 2-Step Verification is ON for the sender Google account.\n"
            "2. You generated an App Password (Google Account → Security → App Passwords).\n"
            "3. The App Password is saved in secrets.toml under sender_password."
        )
    except smtplib.SMTPRecipientsRefused as e:
        return False, f"Recipient address rejected: {e}"
    except smtplib.SMTPException as e:
        return False, f"SMTP error: {e}"
    except OSError as e:
        return False, f"Connection error (check internet/firewall): {e}"
