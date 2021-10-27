
from flask import Flask, render_template, request, redirect, url_for

from database.db import new_user, get_user, get_users, delete_user, update_user

app=Flask(__name__)

@app.route('/')
def home ():
	return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login ():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
 
        try:
            response = get_user(username, password)
            if response:
                return redirect('/menu')
            else:
                return redirect('/login')
        except ValueError:
            return 'ERROR (login): ' + ValueError
    else:
	    return render_template('login.html')      

@app.route('/registro', methods=['GET', 'POST'])
def registro ():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        error = ''

        try:
            error = error + new_user(username, password)
            return redirect('/login')
        except ValueError:
            return error + ValueError + ' '
    else:
	    return render_template('registro.html')

@app.route('/menu')
def menu ():
	return render_template('menu.html')

@app.route('/adminpro')
def adminpro ():
	return render_template('adminpro.html')

@app.route('/userrouter')
def userrouter ():
	return render_template('userrouter.html')

@app.route('/crudusersystem')
def crudusersystem():
    users = get_users()

    if users.count() == 0:
        return redirect('/login')

    return render_template('crudusersystem.html', users = users)

@app.route('/updateusersystem', methods=['GET', 'POST'])
def updateusersystem ():
    if request.method == 'POST':
        _id = request.form['_id']
        username = request.form['username']
        password = request.form['password']

        error = 'ERROR (updateusersystem): '

        try:
            error = error + update_user(_id, username, password)
            return redirect('/crudusersystem')
        except ValueError:
            return error + ValueError + ' '
    else:
        _id = request.args.get('_id')
        username = request.args.get('username')
	    
        return render_template('updateusersystem.html', _id=_id, username=username)

@app.route('/deleteusersystem/<string:_id>')
def deleteusersystem(_id):
    
    error = 'ERROR (deleteusersystem): '

    try:
        error = error + delete_user(_id)
        return redirect('/crudusersystem')
    except ValueError:
        return error + ValueError + ' '

if __name__ == '__main__':
    app.run()

















