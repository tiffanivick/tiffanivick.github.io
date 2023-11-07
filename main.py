from flask import Flask, render_template, request, redirect, flash
from flask_mail import Mail, Message
from forms import ContactForm
from flask_bootstrap import Bootstrap5
from datetime import datetime
import requests
from dotenv import load_dotenv
import os
import json

load_dotenv()

my_email = os.getenv("MY_EMAIL")
endpoint_url = os.getenv("ENDPOINT_URL")
current_year = datetime.now().year

response = requests.get(endpoint_url)
response.raise_for_status()
projects = response.json()

with open('image-data.json') as json_file:
    image_data = json.load(json_file)

app = Flask(__name__)
bootstrap = Bootstrap5(app)
app.secret_key = os.getenv("SECRET_KEY")

mail = Mail()
app.config['MAIL_SERVER'] = os.getenv("MAIL_SERVER")
app.config['MAIL_PORT'] = int(os.getenv("MAIL_PORT"))
app.config['MAIL_USE_TLS'] = os.getenv("MAIL_USE_TLS").lower() == 'true'
app.config['MAIL_USE_SSL'] = os.getenv("MAIL_USE_SSL").lower() == 'true'
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
mail.init_app(app)


@app.route("/", methods=["GET", "POST"])
def home():
    form = ContactForm()
    if request.method == 'POST' and form.validate():
        if not form.validate():
            flash('All fields are required.')
            return render_template('index.html', form=form)
        else:
            msg = Message(form.subject.data, sender=request.form.get('email'), recipients=[my_email])
            msg.body = f'From: {form.name.data}\nEmail: {form.email.data}\nMessage: {form.message.data}'
            mail.send(msg)
            return redirect('email-sent', 302)
    elif request.method == 'GET':
        return render_template('index.html', form=form)
    return render_template("index.html", year=current_year, all_projects=projects)


@app.route("/projects/<int:index>", methods=["GET"])
def get_projects(index):
    requested_project = None
    for project in projects:
        if project["id"] == index:
            requested_project = project
    selected_id = str(index)
    project_images = image_data.get(selected_id, [])
    return render_template("portfolio-details.html", project=requested_project, selected_id=selected_id, project_images=project_images)


@app.route("/email-sent", methods=["GET"])
def email_sent():
    return render_template("email-sent.html")


if __name__ == '__main__':
    app.run(debug=True)

