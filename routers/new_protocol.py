import paramiko, getpass, time, json

with open('new_protocol.json', 'r') as x:
    commands = json.load(x)

with open('ospf_networks.json', 'r') as x:
    ospf_networks = json.load(x)

with open('network_id.json', 'r') as x:
    network_id = json.load(x)

with open('routers_ip.json', 'r') as x:
    routers_ip = json.load(x)

with open('kill_old_protocol.json', 'r') as x:
    commands_kill = json.load(x)

max_buffer = 65535
def clear_buffer(conexion):
    if conexion.recv_ready():
        return conexion.recv(max_buffer)

def get_protocol():
    conexion = paramiko.SSHClient()
    conexion.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    conexion.connect("10.0.4.254", username="root", password="root", look_for_keys=False, allow_agent=False)

    nueva_conexion = conexion.invoke_shell()
    salida = clear_buffer(nueva_conexion)
    time.sleep(1)
    
    nueva_conexion.send("show run | i router\n")
    time.sleep(1)
    salida = nueva_conexion.recv(max_buffer)
    nueva_conexion.close()
    print(salida.split()[6].decode().upper())
    return salida.split()[6].decode().upper()

def new_protocol(protocol, username, password):
    
    for router_id in range(1,5):
        conexion = paramiko.SSHClient()
        conexion.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        conexion.connect(routers_ip[str(router_id)], username=username, password=password, look_for_keys=False, allow_agent=False)

        nueva_conexion = conexion.invoke_shell()
        salida = clear_buffer(nueva_conexion)
        #time.sleep(2)

        commandos = commands[protocol]
        i = 0
        for command in commandos:
            if "{network}" in command:
                if protocol == "OSPF":
                    command = command.format(network = ospf_networks[ str(router_id) ][i - 1])
                else:
                    command = command.format(network = network_id[str(router_id)] )
                i += 1
            nueva_conexion.send(command.rstrip()+"\n")
            time.sleep(1)
            salida = nueva_conexion.recv(max_buffer)
            print(salida)
            salida=clear_buffer(nueva_conexion)
        nueva_conexion.close()
    time.sleep(10)
    kill_old_protocol(protocol, username, password)

def kill_old_protocol(protocol, username, password):
    for router_id in range(1,5):
        conexion = paramiko.SSHClient()
        conexion.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        conexion.connect(routers_ip[str(router_id)], username=username, password=password, look_for_keys=False, allow_agent=False)

        nueva_conexion = conexion.invoke_shell()
        salida = clear_buffer(nueva_conexion)
        time.sleep(2)

        commandos = commands_kill[protocol]
        for command in commandos:
            nueva_conexion.send(command.rstrip()+"\n")
            time.sleep(1)
            salida = nueva_conexion.recv(max_buffer)
            print(salida)
            #salida=clear_buffer(nueva_conexion)

        nueva_conexion.close()
    

if __name__ == '__main__':
    new_protocol("EIGRP", "root", "root")

