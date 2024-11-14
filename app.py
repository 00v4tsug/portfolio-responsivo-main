from flask import Flask, render_template, redirect, request, flash, jsonify
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os
load_dotenv()

app = Flask(__name__)
app.secret_key = 'gustavo'

app.config['ENV'] = 'production'
app.config['DEBUG'] = False
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": os.getenv("EMAIL"),
    "MAIL_PASSWORD": os.getenv("SENHA")
}

app.config.update(mail_settings)
mail = Mail(app)

class Contato:
    def __init__(self, nome, email, mensagem):
        self.nome = nome
        self.email = email
        self.mensagem = mensagem

@app.route('/')
def index():
    if request.args.get("check") == "1":
        # Retorna um JSON indicando que o conteúdo está pronto para ser exibido
        return jsonify({"status": "ready"})
    return render_template('index.html')

@app.route('/send', methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        formContato = Contato(
            request.form["nome"],
            request.form["email"],
            request.form["mensagem"]
        )

        msg = Message(
            subject = f'{formContato.nome} te enviou uma mensagem no portfólio',
            sender = app.config.get("MAIL_USERNAME"),
            recipients= ['00v4tsug@gmail.com', app.config.get("MAIL_USERNAME")],
            body = f'''
            
            {formContato.nome} com o e-mail {formContato.email}, te enviou a seguinte mensagem:

            {formContato.mensagem}

            '''
        )
        mail.send(msg)
        flash('Mensagem enviada com sucesso!')
    return redirect('/home')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)