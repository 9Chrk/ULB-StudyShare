"""Constantes utilisées dans l'application"""

import re


# limites de la base de données
USERNAME_MAX_LENGTH = 50
PASSWORD_MAX_LENGTH = 255
EMAIL_MAX_LENGTH    = 255

# Regex basique
# exemple de validation: <>@<>.<>
EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
