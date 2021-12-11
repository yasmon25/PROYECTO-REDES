import time, json, paramiko

# Obtener las ip's de los routers
#with open('./dispositivos.json', 'r') as f:
#    hosts = json.load(f)

hosts = {
	"1": {"ip": "10.0.1.254"},
	"2": {"ip": "10.0.2.254"},
	"3": {"ip": "10.0.3.254"},
	"4": {"ip": "10.0.4.254"}
}

max_buffer = 65535
def clear_buffer(conexion):
    if conexion.recv_ready():
        return conexion.recv(max_buffer)

# Agregar un nuevo usuario
def new_user_routers(username, password, privilige):

    commands = ["conf terminal", 
                "username " + username + 
                " privilege " + privilige + 
                " secret " + password,
                "exit", 
                "write"]

    for router_id in range(1,5):
        conexion = paramiko.SSHClient()
        conexion.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        conexion.connect(hosts[str(router_id)]["ip"], username="root", password="root", look_for_keys=False, allow_agent=False)

        nueva_conexion = conexion.invoke_shell()
        salida = clear_buffer(nueva_conexion)
        #time.sleep(1)

        for command in commands:

            nueva_conexion.send(command.rstrip()+"\n")
            time.sleep(1)
            salida = nueva_conexion.recv(max_buffer)
            print(salida)
            salida=clear_buffer(nueva_conexion)

        nueva_conexion.close()
    return ''
            
# Eliminar usuario
def del_user_routers(username):
    
    commands = ["conf terminal", "no username " + username, "exit", "write"]

    for router_id in range(1,5):
        conexion = paramiko.SSHClient()
        conexion.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        conexion.connect(hosts[str(router_id)]["ip"], username="root", password="root", look_for_keys=False, allow_agent=False)

        nueva_conexion = conexion.invoke_shell()
        salida = clear_buffer(nueva_conexion)
        #time.sleep(1)

        for command in commands:

            nueva_conexion.send(command.rstrip()+"\n")
            time.sleep(1)
            salida = nueva_conexion.recv(max_buffer)
            print(salida)
            salida=clear_buffer(nueva_conexion)

        nueva_conexion.close()
    return ''

# Obtener usuarios
def get_users_routers():

    conexion = paramiko.SSHClient()
    conexion.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    conexion.connect("10.0.4.254", username="root", password="root", look_for_keys=False, allow_agent=False)

    nueva_conexion = conexion.invoke_shell()
    salida = clear_buffer(nueva_conexion)
    time.sleep(1)

    nueva_conexion.send("show running-config | include username\n")
    time.sleep(1)
    salida = nueva_conexion.recv(max_buffer)
    #print(salida)
    users = salida
    salida=clear_buffer(nueva_conexion)

    nueva_conexion.close()

    final = []
    users = users.decode().split('\n')
    for user in users:
        if 'privilege' in user:
            aux = user.split()
            final.append([aux[1], aux[3]])

    return final

if __name__ == '__main__':
    
    #new_user_routers('Prueba', '12345', '14')
    #del_user_routers('Yasmin')

    print(get_users_routers())

    
















































