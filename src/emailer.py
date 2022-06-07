import smtplib
import email.message
import json
import os

try:
    smtp_ssl = smtplib.SMTP_SSL(host="smtp.gmail.com", port=465)
except Exception as err:
    smtp_ssl = None

formEmail = os.environ.get("FORM_EMAIL")
formEmailPassword = os.environ.get("FORM_EMAIL_PASSWORD")

resp_code, resp = smtp_ssl.login(user=formEmail, password=formEmailPassword)


def send_email(data):
    msg = email.message.Message()
    msg["From"] = data.get("name")
    msg["To"] = "kk67.kasserer@gmail.com"
    msg["Cc"] = data.get("email")
    msg["Subject"] = data.get("subject")
    msg.set_payload(data.get("body"))

    try:
        smtp_ssl.sendmail(from_addr="kk67.email@gmail.com", to_addrs=msg["To"], msg=msg.as_string())
    except Exception as err:
        return json.dump({"code": 501, "message": type(err).__name__})
    
    return json.dump({"code": 200, "message": ""})