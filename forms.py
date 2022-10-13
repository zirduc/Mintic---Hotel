
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField,SelectField,IntegerField, TextAreaField
from wtforms.validators import DataRequired, Email, Length,EqualTo

class loginForm(FlaskForm):
    email = EmailField('Email', validators=[
        DataRequired(),
        Email(message='El formato del correo debe ser example@example.com')
    ])

    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=6, max=14, message='la contraseña debe tener enre 6 y 14 caracteres')
    ])


class registerForm(FlaskForm) :
    name = StringField('Name', validators=[
        DataRequired(),
        Length(min=4, max=10, message='debe contener entre 4 y 10 caracteres')
    ])

    email = EmailField('Email', validators=[
        DataRequired(),
        Email(message="Requiere el formato example@example.com")
    ])

    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=6, max=14, message='debe contener entre 6 y 14 caracteres'), 
        EqualTo('passwordAgain', message='Las contraseñas no coinciden')
    ])

    passwordAgain = PasswordField('Repeat Password')

    cargo = SelectField('Cargo', choices= [('cliente','cliente'),('administrador','administrador'),('super administrador','super adminisrador')])

class reservation (FlaskForm):

    habitacion = SelectField('Cual Habitación desea', choices=[
            ("habitacion 1", "habitacion 1"),
            ("habitacion 2", "habitacion 2"),
            ("habitacion 3", "habitacion 3"),
            ("habitacion 4", "habitacion 4"),
            ("habitacion 5", "habitacion 5"),
            ("habitacion 6", "habitacion 6"),
        ])
    dias = IntegerField('Cuantos dias se va a quedar', validators=[
        DataRequired()
    ])

    comentarios = TextAreaField('¿Desea dejar alguna recomendacion?', validators=[
        DataRequired(),
        Length(min="10")
    ])