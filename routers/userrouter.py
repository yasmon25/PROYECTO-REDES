import time, json
from netmiko import ConnectHandler

# Obtener las ip's de los routers
#with open('./dispositivos.json', 'r') as f:
#    hosts = json.load(f)

hosts = {
	"R1": {"ip": "10.0.1.254"},
	"R2": {"ip": "10.0.2.254"},
	"R3": {"ip": "10.0.3.254"},
	"R4": {"ip": "10.0.4.254"}
}

# Ejecutar comandos
def exec_commands(comandos):
    try:
        for host in hosts.keys():  
     
            # Hacer conexión con el router
            connection = ConnectHandler(hosts[host]['ip'], device_type='cisco_ios', username='root', password='root')
            #time.sleep(1)

            for comando in comandos:
                print(connection.send_command_timing(comando))
                #time.sleep(1)
            
            connection.disconnect()
    except ValueError:
        return 'EROR(new_user): ' + ValueError + ' '
    return ''

# Agregar un nuevo usuario
def new_user_routers(username, password, privilige):

    comandos = ["enable", "conf terminal", "username " + username + " privilege " + privilige + " secret " + password, "exit", "write"]

    try:
        exec_commands(comandos)
        return ''    
    except ValueError:
        return 'EROR(new_user): ' + ValueError + ' '
            
# Eliminar usuario
def del_user_routers(username):

    if username == 'root':
        return 'ERROR(del_user): No se puede eliminar el usuario root'
    
    comandos = ["enable", "conf terminal", "no username " + username, "exit", "write"]

    try:
        exec_commands(comandos)
        return ''    
    except ValueError:
        return 'EROR(del_user): ' + ValueError + ' '

# Obtener usuarios
def get_users_routers():
    connection = ConnectHandler(hosts['R1']["ip"], device_type='cisco_ios', username='root', password='root')
    salida = connection.send_command_timing('show running-config | include username')
    
    arr = salida.split()

    if arr[0] != 'username':
        for i in range(len(arr)):
            if arr[i] == 'username':
                arr = arr[(i+1):]
                break
    times = len(arr) / 7

    users = []
    for i in range(int(times)):
        users.append([arr[i*7 + 1], arr[i*7 + 3]])

    return users

if __name__ == '__main__':
    
    new_user_routers('Prueba', '12345', '14')
    #del_user_routers('Yasmin')

    print(get_users_routers())

    
















































