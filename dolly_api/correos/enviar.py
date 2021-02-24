import base64
import email.utils
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def enviar(html, para, titulo, correo):
    servidor = smtplib.SMTP('smtp.gmail.com',587)
    servidor.ehlo()
    servidor.starttls()
    servidor.ehlo()
    servidor.login('aris.bersain@gmail.com','@correo12345')
    mensaje = MIMEMultipart('alternative')
    mensaje['To'] = para
    mensaje['From'] = email.utils.formataddr(('Dolly','email-do-not-reply@dolly.com'))
    mensaje['Subject'] = titulo
    contenido = MIMEText(html, 'html')
    mensaje.attach(contenido)
    
    servidor.sendmail('aris.bersain@gmail.com', correo, mensaje.as_string())
    print('se envio correo de confirmacion')
    servidor.quit()

class Enviar():
    
    def confirmacion(usuario, token):
        id_bytes = usuario["id"].encode('ascii')
        base64_bytes = base64.b64encode(id_bytes)
        base64_id = base64_bytes.decode('ascii')

        token_bytes = token.encode('ascii')
        base64_bytes = base64.b64encode(token_bytes)
        base64_token = base64_bytes.decode('ascii')


        html = '''<h1>Hola {nombre}</h1>
            <p>
                Gracias por crear una cuenta con nosotros.<br><br/> 
                Para continuar, confirma tu email con el siguente boton
            </p>
            <form action="http://127.0.0.1:8000/confirmacion/" method="post" enctype="multipart/form-data">
                <input type="submit" value="Confirmar mi email" />
                <input type="hidden" name="id" value="{id}" />
                <input type="hidden" name="token" value="{key}" />
            </form>
            <p>
                Saludos.
                <br></br>
                El equipo de Dolly.
            <p/>'''.format(nombre=usuario["first_name"], id=base64_id, key=base64_token) 
        para = email.utils.formataddr((usuario["first_name"], usuario["email"]))
        titulo = "Confirmacion de cuenta"
        correo = usuario["email"]
        enviar(html, para, titulo, correo)
    
    def recuperar(usuario, token):
        email1 = usuario["email"]

        email_bytes = usuario["email"].encode('ascii')
        base64_bytes = base64.b64encode(email_bytes)
        base64_email = base64_bytes.decode('ascii')

        token_bytes = token.encode('ascii')
        base64_bytes = base64.b64encode(token_bytes)
        base64_token = base64_bytes.decode('ascii')

        html = '''<h1>Hola {nombre}</h1>
            <p>
                Hace poco pediste que se restableciera la contraseña de esta cuenta de Dolly:<br><br/> 
                {email1}
                <br><br/> 
                Para actualizar tu contraseña, haz clic en el siguiente botón:
            </p>
            <form action="http://127.0.0.1:8000/usuarios/{id}/" method="post" enctype="multipart/form-data">
                <input type="submit" value="Restablecer mi contraseña" />
                <input type="hidden" name="email" value="{email}" />
                <input type="hidden" name="token" value="{key}" />
            </form>
            <p>
                Saludos.
                <br></br>
                Equipo Dolly.
            <p/>'''.format(nombre=usuario["first_name"], id=usuario["id"], email1=email1,email=base64_email, key=base64_token) 
        para = email.utils.formataddr((usuario["first_name"], usuario["email"]))
        titulo = "Restablece tu contraseña de Dolly"
        correo = usuario["email"]
        enviar(html, para, titulo, correo)

    def invitacion(usuario, nombre, tablero):
        email1 = usuario["email"]
        html = '''<h1>Hola {nombre}</h1>
            <p>
                {nombre1} te ha invitado a unirse al tablero '{tablero}' de Dolly: 
                <br><br/> 
            </p>
            <form action="http://127.0.0.1:8000/" method="post" enctype="multipart/form-data">
                <input type="submit" value="Ir a tablero" />
            </form>
            <p>
                Saludos.
                <br></br>
                Equipo Dolly.
            <p/>'''.format(nombre=usuario["first_name"], nombre1=nombre, tablero=tablero) 
        para = email.utils.formataddr((usuario["first_name"], usuario["email"]))
        titulo = nombre + " te ha invitado a unirse al tablero '"+ tablero +"'"
        correo = usuario["email"]
        enviar(html, para, titulo, correo)