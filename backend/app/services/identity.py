import re

def normalize_email(email: str) -> str:
    email = email.lower()
    if "@gmail.com" in email:
        local, domain = email.split("@")
        local = local.split("+")[0]      # remove alias
        local = local.replace(".", "")   # remove dots
        return f"{local}@{domain}"
    return email


def normalize_phone(phone: str) -> str:
    return re.sub(r"\D", "", phone)
