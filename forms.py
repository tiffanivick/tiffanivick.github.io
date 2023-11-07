from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class ContactForm(FlaskForm):
    name = StringField("Your Name", validators=[DataRequired(message="Please enter your name.")])
    email = StringField("Your Email", validators=[DataRequired(message="Please enter your email address."), Email("This field requires a valid email address.")])
    subject = StringField("Subject", validators=[DataRequired(message="Please enter a subject."), Length(max=100)])
    message = TextAreaField("Message", validators=[DataRequired(message="Please enter a message."), Length(min=4)])
    submit = SubmitField("Send Message")
