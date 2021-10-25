from flask import Flask, render_template, request, redirect, url_for

app=Flask(__name__)

@app.route('/')
def home ():
	return render_template('home.html')

@app.route('/login')
def login ():
	return render_template('login.html')

@app.route('/registro')
def registro ():
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

if __name__ == '__main__':
    app.run()
