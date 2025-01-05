import re
import dns.resolver

def is_valid_format(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

def is_valid_domain(email):
    try:
        domain = email.split('@')[1]
        dns.resolver.resolve(domain, 'MX')
        return True
    except Exception:
        return False

def is_valid_email(email):
    if is_valid_format(email):
        return is_valid_domain(email)


