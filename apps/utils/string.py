import random
import string

from passlib.pwd import genphrase, genword

UNICODE_ASCII_CHARACTER_SET = string.ascii_letters + string.digits


def gen_random(length: int = 32, chars: str = None) -> str:
    rand = random.SystemRandom()
    return ''.join(
        rand.choice(chars or UNICODE_ASCII_CHARACTER_SET)
        for _ in range(length)
    )


def gen_id(length: int = None) -> str:
    """Generate readable random string"""
    return genphrase(entropy=56, sep="-", length=length)


def gen_apikey() -> str:
    """Generate APIKey: unreadable + readable random string"""
    return f'{genword(entropy=56, charset="hex")}.{gen_id()}'


def mask_email(email: str) -> str:
    """Anonymize email address (example: te***st@e******.com)"""
    username, domain = email.split('@')
    domain_parts = domain.split('.')
    masked_email = \
        f'{username[:2]}{"*" * len(username[2:])}' \
        f'@{domain_parts[0][0]}{"*" * len(domain_parts[0][1:])}' \
        f'{domain_parts[-1]}'
    return masked_email
