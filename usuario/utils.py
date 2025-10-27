import random
import string
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.conf import settings



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



def reset_user_password(email):
    """
    Busca un usuario por email, genera una nueva contraseña aleatoria,
    la guarda y la envía por correo.
    """
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return False, "No existe un usuario con ese correo."

    # Generar nueva contraseña
    new_password = generate_random_password(8)
    user.set_password(new_password)
    user.save()

    # Enviar correo
    subject = "Recuperación de contraseña"
    message = (
        f"Hola {user.username},\n\n"
        f"Se generó una nueva contraseña para tu cuenta.\n\n"
        f"Tu nueva contraseña es: {new_password}\n\n"
        f"Por razones de seguridad, te recomendamos cambiarla al ingresar."
    )
    try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
    except Exception as e:
        return False, f"No se pudo enviar el correo: {e}"

    return True, "Se envió una nueva contraseña a tu correo."



def enviar_password_por_email(usuario, nueva_password):
    """Envía la nueva contraseña por correo al usuario."""
    asunto = "Tu contraseña ha sido restablecida"
    mensaje = (
        f"Hola {usuario.first_name or usuario.username},\n\n"
        "Tu contraseña ha sido restablecida por un administrador.\n"
        f"Tu nueva contraseña es: {nueva_password}\n\n"
        "Te recomendamos cambiarla luego de iniciar sesión.\n\n"
        "Saludos,\nEquipo de Salud Mental"
    )

    send_mail(
        asunto,
        mensaje,
        settings.DEFAULT_FROM_EMAIL,
        [usuario.email],
        fail_silently=False,
    )