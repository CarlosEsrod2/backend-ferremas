import smtplib
from email.message import EmailMessage

def enviar_correo_bienvenida(destinatario_email, nombre_usuario):
    remitente = 'correo@gmail.com'
    contraseña = 'password'

    mensaje = EmailMessage()
    mensaje['Subject'] = '¡Gracias por registrarte en Ferremas!'
    mensaje['From'] = remitente
    mensaje['To'] = destinatario_email
    mensaje.set_content(f'Hola {nombre_usuario},\n\n¡Gracias por registrarte en Ferremas! Te damos la bienvenida.')

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(remitente, contraseña)
            smtp.send_message(mensaje)
        print('Correo enviado con éxito.')
        return True
    except Exception as e:
        print(f'Error al enviar correo: {e}')
        return False
