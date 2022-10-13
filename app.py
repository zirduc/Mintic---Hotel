
from flask import Flask, session, render_template, redirect, url_for, request, jsonify

from werkzeug.security import generate_password_hash, check_password_hash
from forms import loginForm, registerForm, reservation
import sqlite3 as sql


app = Flask(__name__)
app.secret_key = 'adadasdafasd'

@app.route('/')
def home():
    return redirect(url_for('signIn'))

@app.route('/auth/login', methods=['GET', 'POST'])
def signIn():
    if 'user' in session:
        return redirect(url_for('hotel'))

    form = loginForm()
    if (request.method == 'POST' and form.validate_on_submit()):
        email = request.form['email']
        password = request.form['password']

        conn = sql.connect('hotel-database.db')
        cursor = conn.cursor()
        buscar = f'SELECT * FROM usuarios where email="{email}"'
        cursor.execute(buscar)
        userPassword = cursor.fetchall()
        if (len(userPassword) == 0):
            return render_template('wrongValidation.html')

        print(userPassword)
        name = userPassword[0][0]
        passwordDb = userPassword[0][2]
        cargo = userPassword[0][3]

        print(passwordDb)
        passwordBoolean = check_password_hash(passwordDb, password)
        print(passwordBoolean)
        conn.commit()
        conn.close()

        if (passwordBoolean):
            print('la operación fue realizada satisfactoriamente')
            session['user'] = name
            session['email'] = email
            session['cargo'] = cargo
            return redirect(url_for('hotel'))
        else:
            print('la operación no se cumplio')
            return render_template('wrongValidation.html')

    return render_template('login.html', form=form)

@app.route('/auth/register', methods=['GET', 'POST'])
def signUp():
    if 'user' in session:
        return redirect(url_for('hotel'))

    form = registerForm()
    if (request.method == 'POST' and form.validate_on_submit()):
        name = request.form['name']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        cargo = request.form['cargo']

        conn = sql.connect('hotel-database.db')
        cursor = conn.cursor()
        buscar = f'SELECT * FROM usuarios where email="{email}"'
        cursor.execute(buscar)
        results = cursor.fetchall()
        if (len(results) > 0):
            return render_template('userExist.html')

        registrar = f"INSERT INTO usuarios VALUES ('{name}', '{email}', '{password}', '{cargo}')"
        cursor.execute(registrar)
        conn.commit()
        conn.close()
        print('registrado con exito')
        session['user'] = name
        session['email'] = email
        session['cargo'] = cargo
        return redirect(url_for('hotel'))


    return render_template('register.html', form = form)
    
@app.route('/hotel')
def hotel():
    if 'user' in session:
        return render_template('index.html')
    
    return render_template('notLogged.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('signIn'))



@app.route('/reservas', methods=['GET','POST'])
def reservarHabitacion():
    form = reservation()
    if 'user' in session:
        if request.method == 'POST':
            name = request.form['habitacion']

            conn = sql.connect('hotel-database.db')
            cursor = conn.cursor()
            buscarHabitacion= f'SELECT * FROM habitaciones where habitacion="{name}"'
            cursor.execute(buscarHabitacion)
            habitacionArr = cursor.fetchall()
            if len(habitacionArr) > 0:
                return render_template('habitacionExiste.html')

            disponible = 'no'
            dias = request.form['dias']
            comentarios = request.form['comentarios']
            print(dias)
            print(comentarios)
            usuario = session['user']

            registrarHabitacion = f"INSERT INTO habitaciones VALUES ('{usuario}','{name}', '{disponible}', '{dias}', '{comentarios}')"
            cursor.execute(registrarHabitacion)
            conn.commit()
            conn.close()
            return render_template('reservaSuccess.html')

        
        return render_template('reservaHabitacion.html', form=form)

    return render_template('notLogged.html')

# @app.route('/hotel')
# def hotel():
#     x = False
#     if (x and x.cargo == "administrador"):
#         return '<h1>Bienvenido juan a nuestro hotel</h1>'
#     else:
#         return '<h1>No Tiene Permiso</h1>'

if __name__ == '__main__':
    app.run(debug=True)