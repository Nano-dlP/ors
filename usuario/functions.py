import random
import string

def generate_random_password(length=8):
    """
    Genera una contraseña aleatoria segura con letras, números y símbolos.
    Evita caracteres confusos como comillas, espacios o barras invertidas.
    """

    if length < 4:
        raise ValueError("La longitud de la contraseña debe ser al menos 4 caracteres.")

    # Definir los conjuntos de caracteres permitidos
    safe_punctuation = "!#$%&()*+,-./:;<=>?@[]^_{|}~"  # sin comillas, sin barra invertida
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits

    # Combinar todos los caracteres válidos
    all_characters = lowercase + uppercase + digits + safe_punctuation

    # Garantizar que tenga al menos un carácter de cada tipo
    password = [
        random.choice(lowercase),
        random.choice(uppercase),
        random.choice(digits),
        random.choice(safe_punctuation)
    ]

    # Completar hasta el largo deseado
    password += random.choices(all_characters, k=length - 4)

    # Mezclar el orden
    random.shuffle(password)

    # Devolver como string
    return ''.join(password)



def validate_password_strength(password):
    if len(password) < 8:
        return False, "Debe tener al menos 8 caracteres."
    if not any(c.islower() for c in password):
        return False, "Debe contener al menos una letra minúscula."
    if not any(c.isupper() for c in password):
        return False, "Debe contener al menos una letra mayúscula."
    if not any(c.isdigit() for c in password):
        return False, "Debe contener al menos un número."
    if not any(c in "!#$%&()*+,-./:;<=>?@[]^_{|}~" for c in password):
        return False, "Debe contener al menos un carácter especial."
    return True, "Contraseña válida."
