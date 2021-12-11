import json
from flask import Flask, render_template, request, redirect, url_for
from routers.new_protocol import get_protocol, new_protocol as new_protocol_routers
from database.db import new_user, get_user, get_users, delete_user, update_user
from routers.user_router import new_user_routers, del_user_routers, get_users_routers
from topologia.topologia import main_topologia
from SNMP.snmp import get_data_router
import _thread


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
            print (response)
            if response:
                return redirect('/crud_user_system')
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

@app.route('/admin_pro', methods=['GET', 'POST'])
def admin_pro ():
    if request.method == 'POST':    
        protocol = request.form['new_protocol']
        return render_template('new_protocol.html', protocol=protocol)
    else:
        actual_protocol = get_protocol()
        return render_template('admin_pro.html', actual_protocol=actual_protocol)

@app.route('/new_protocol', methods=['GET', 'POST'])
def new_protocol():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        protocol = request.form['protocol']

        new_protocol_routers(protocol, username, password)

        return render_template('admin_pro.html', actual_protocol=protocol)
    else:
        return render_template('new_protocol.html')

@app.route('/crud_user_router', methods=['GET', 'POST'])
def userrouter ():
    if request.method == 'POST':        
        username = ''
        privilige = '15'

        return render_template('update_user_router.html', privilige=privilige, username=username)
    else:
        users = get_users_routers()
        return render_template('crud_user_router.html', users = users)

@app.route('/update_user_router', methods=['GET', 'POST'])
def update_user_router ():
    if request.method == 'POST':
        username_old = request.form['username_old']
        username = request.form['username']
        privilige = request.form['privilige']
        password = request.form['password']

        error = 'ERROR (update_user_router): '

        try:
            if username_old != '':
                error = error + del_user_routers(username_old)
            error = error + new_user_routers(username, password, privilige)     
      
            return redirect('/crud_user_router')
        except ValueError:
            return error + ValueError + ' '
    else:
        username = request.args.get('username')
        privilige = request.args.get('privilige')
	    
        return render_template('update_user_router.html', privilige=privilige, username=username)

@app.route('/delete_user_router/<string:username>')
def delete_user_router(username):
    
    error = 'ERROR (delete_user_router): '

    try:
        error = error + del_user_routers(username)
        return redirect('/crud_user_router')
    except ValueError:
        return error + ValueError + ' '

@app.route('/crud_user_system', methods=['GET', 'POST'])
def crud_user_system():
    if request.method == 'POST':
	    return render_template('registro.html')
    else:
        users = get_users()

        '''if users.count() == 0:
            return redirect('/login')
       '''
        return render_template('crud_user_system.html', users = users)
        
@app.route('/update_user_system', methods=['GET', 'POST'])
def update_user_system ():
    if request.method == 'POST':
        _id = request.form['_id']
        username = request.form['username']
        password = request.form['password']

        error = 'ERROR (update_user_system): '

        try:
            error = error + update_user(_id, username, password)
            return redirect('/crud_user_system')
        except ValueError:
            return error + ValueError + ' '
    else:
        _id = request.args.get('_id')
        username = request.args.get('username')
	    
        return render_template('update_user_system.html', _id=_id, username=username)

@app.route('/delete_user_system/<string:_id>')
def delete_user_system(_id):
    
    error = 'ERROR (delete_user_system): '

    try:
        error = error + delete_user(_id)
        return redirect('/crud_user_system')
    except ValueError:
        return error + ValueError + ' '  
    
@app.route('/data_router/<string:router>')
def data_router(router):
    
    if request.method == 'POST':
        username = request.form['username']
        direccion = request.form['direccion']
        descripcion = request.form['descripcion']

        new_protocol_routers(protocol, username, password)

        return render_template('admin_pro.html', actual_protocol=protocol)
    else:
        respuesta=get_data_router()
        return render_template('data_router.html',respuesta=respuesta)

if __name__ == '__main__':
    _thread.start_new_thread(main_topologia, ())
    app.run()

















