from string import ascii_letters, digits, punctuation
from EXCEPTIONS import ValidationError
import re

def IsValidName(name: str):
    """Return True if the name contains only letters and digits."""
    if not name or not isinstance(name, str):
        return False
    for n in name:
        if not (n in (ascii_letters+digits+' '+'-'+'_')):
            return False
    return True

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
def IsValidEmail(email: str) -> bool:
    """Validate email structure using regex."""
    if not email or not isinstance(email, str):
        return False
    return bool(EMAIL_REGEX.match(email))

def StrengthOfPswd(pswd: str) -> int:
    """Evaluate password strength from 0–5."""
    if not pswd or not isinstance(pswd, str):
        return 0
    score = 0
    if len(pswd) >= 8:
        score += 1
    if any(c.islower() for c in pswd):
        score += 1
    if any(c.isupper() for c in pswd):
        score += 1
    if any(c.isdigit() for c in pswd):
        score += 1
    if any(c in punctuation for c in pswd):
        score += 1
    return score
