import json
from flask import Flask, render_template, request, redirect, url_for
from conexionSSH import *
from database.db import new_user, get_user, get_users, delete_user, update_user
from routers.userrouter import new_user_routers, del_user_routers, get_users_routers

app=Flask(__name__)

with open('dispositivos.json', 'r') as f:
    hosts = json.load(f)

with open('ipOSPF.json', 'r') as f:
    hosts2 = json.load(f)

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

@app.route('/cruduserrouter', methods=['GET', 'POST'])
def userrouter ():
    if request.method == 'POST':        
        username = ''
        privilige = '15'

        return render_template('updateuserrouter.html', privilige=privilige, username=username)
    else:
        users = get_users_routers()
        return render_template('cruduserrouter.html', users = users)

@app.route('/updateuserrouter', methods=['GET', 'POST'])
def updateuserrouter ():
    if request.method == 'POST':
        username_old = request.form['username_old']
        username = request.form['username']
        privilige = request.form['privilige']
        password = request.form['password']

        error = 'ERROR (updateuserrouter): '

        try:
            if username_old != '':
                error = error + del_user_routers(username_old)
            error = error + new_user_routers(username, password, privilige)     
      
            return redirect('/cruduserrouter')
        except ValueError:
            return error + ValueError + ' '
    else:
        username = request.args.get('username')
        privilige = request.args.get('privilige')
	    
        return render_template('updateuserrouter.html', privilige=privilige, username=username)

@app.route('/deleteuserrouter/<string:username>')
def deleteuserrouter(username):
    
    error = 'ERROR (deleteuserrouter): '

    try:
        error = error + del_user_routers(username)
        return redirect('/cruduserrouter')
    except ValueError:
        return error + ValueError + ' '

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

@app.route('/rip',methods=['POST'])
def rip():
    Router = request.form['RIPopcion']
    print(Router,hosts[Router]['ip'])
    RIP(Router,hosts[Router]['ip'])
    return render_template('adminpro.html')

@app.route('/ospf',methods=['POST'])
def ospf():
    Router = request.form['OSPFopcion']
    OSPF(Router,hosts[Router]['ip'])
    return render_template('adminpro.html')

@app.route('/eigrp',methods=['POST'])
def eigrp():
    Router = request.form['EIGRPopcion']
    EIGRP(Router,hosts[Router]['ip'])
    return render_template('adminpro.html')    
    

if __name__ == '__main__':
    app.run()

















