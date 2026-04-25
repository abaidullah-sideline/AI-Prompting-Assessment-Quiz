"""
Run this directly to diagnose SMTP issues:
  python test_email.py
"""
import smtplib
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

try:
    import toml
    with open(".streamlit/secrets.toml") as f:
        secrets = toml.load(f)
except Exception as e:
    sys.exit(f"Could not read secrets.toml: {e}")

sender_email    = secrets["email_config"]["sender_email"]
sender_password = secrets["email_config"]["sender_password"].replace(" ", "")
# Send test to the sender itself so you can verify receipt
test_recipient  = sender_email

print("=" * 55)
print("SMTP Diagnostic Test")
print("=" * 55)
print(f"Sender    : {sender_email}")
print(f"Recipient : {test_recipient}")
print(f"Password  : {'*' * len(sender_password)} ({len(sender_password)} chars)")
print()

msg = MIMEMultipart("alternative")
msg["From"]    = sender_email
msg["To"]      = test_recipient
msg["Subject"] = "SMTP Test — Secure Exam Portal"
msg.attach(MIMEText("SMTP is working correctly. This is a test from your exam portal.", "plain"))

# ── Try port 587 (STARTTLS) ──────────────────────────────────────────────────
def try_587():
    print("Attempt 1: smtp.gmail.com:587 (STARTTLS)")
    with smtplib.SMTP("smtp.gmail.com", 587, timeout=30) as srv:
        srv.ehlo()
        srv.starttls()
        srv.ehlo()
        srv.login(sender_email, sender_password)
        srv.sendmail(sender_email, test_recipient, msg.as_string())
    print(f"  ✅ Sent via port 587. Check {test_recipient} (and Spam folder).")
    return True

# ── Try port 465 (SSL) ───────────────────────────────────────────────────────
def try_465():
    print("Attempt 2: smtp.gmail.com:465 (SSL)")
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=30) as srv:
        srv.ehlo()
        srv.login(sender_email, sender_password)
        srv.sendmail(sender_email, test_recipient, msg.as_string())
    print(f"  ✅ Sent via port 465. Check {test_recipient} (and Spam folder).")
    return True

for attempt in (try_587, try_465):
    try:
        attempt()
        print()
        print("Email sent! If it doesn't arrive within 2 minutes, check Spam.")
        sys.exit(0)
    except smtplib.SMTPAuthenticationError as e:
        print(f"  ❌ Authentication failed: {e}")
        print()
        print("Fix checklist:")
        print("  1. Is 2-Step Verification ON for the Google account?")
        print("     → myaccount.google.com → Security → 2-Step Verification")
        print("  2. Did you generate an App Password for THIS account?")
        print("     → myaccount.google.com → Security → App Passwords")
        print("     → Select 'Mail' + 'Other device', copy the 16-char code")
        print("  3. Paste the App Password into secrets.toml → sender_password")
        print("     (spaces are fine, the code strips them automatically)")
        if "sideline.agency" in sender_email:
            print()
            print("  Note: sideline.agency looks like Google Workspace.")
            print("  Make sure the App Password is for THAT account, not a")
            print("  personal @gmail.com account.")
    except OSError as e:
        print(f"  ❌ Connection error: {e}")
        print("  → Check your internet connection / firewall / VPN.")
    except smtplib.SMTPException as e:
        print(f"  ❌ SMTP error: {e}")
    except Exception as e:
        print(f"  ❌ Unexpected error ({type(e).__name__}): {e}")
    print()

print("Both ports failed. Email will not be delivered until the issue above is fixed.")
