import paramiko, getpass, time, json

username = "cisco"
password = "cisco"



max_buffer = 65535
def clear_buffer(conexion):
    if conexion.recv_ready():
        return conexion.recv(max_buffer)
    
        
def RIP(router,direccion):
    contadorComando = 0
    conexion = paramiko.SSHClient()
    conexion.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    conexion.connect(router, username=usuario, password=password, look_for_keys=False, allow_agent=False)
    nueva_conexion = conexion.invoke_shell()
    salida = clear_buffer(nueva_conexion)
    time.sleep(2)
    with open("RIP.txt", 'r') as f:
        for comando in comandos:
            contadorComando+=1
            if contadorComando==8:
                comando=comando.format(direccion=nombre_ruta)
            nueva_conexion.send(comando.rstrip()+"\n")
            time.sleep(2)
            salida = nueva_conexion.recv(max_buffer)
            print(salida)
            salida=clear_buffer(nueva_conexion)
    nueva_conexion.close()
    
def OSPF(router,direccion):
    contadorComando = 0
    conexion = paramiko.SSHClient()
    conexion.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    conexion.connect(router, username=usuario, password=password, look_for_keys=False, allow_agent=False)
    nueva_conexion = conexion.invoke_shell()
    salida = clear_buffer(nueva_conexion)
    time.sleep(2)
    with open("OSPF.txt", 'r') as f:
        for comando in comandos:
            contadorComando+=1
            if contadorComando==6:
                comando=comando.format(direccion=nombre_ruta)
            nueva_conexion.send(comando.rstrip()+"\n")
            time.sleep(2)
            salida = nueva_conexion.recv(max_buffer)
            print(salida)
            salida=clear_buffer(nueva_conexion)
    nueva_conexion.close()
    
def EIGRP(router,direccion):
    contadorComando = 0
    conexion = paramiko.SSHClient()
    conexion.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    conexion.connect(router, username=usuario, password=password, look_for_keys=False, allow_agent=False)
    nueva_conexion = conexion.invoke_shell()
    salida = clear_buffer(nueva_conexion)
    time.sleep(2)
    with open("EIGRP.txt", 'r') as f:
        for comando in comandos:
            contadorComando+=1
            if contadorComando==6:
                comando=comando.format(direccion=nombre_ruta)
            nueva_conexion.send(comando.rstrip()+"\n")
            time.sleep(2)
            salida = nueva_conexion.recv(max_buffer)
            print(salida)
            salida=clear_buffer(nueva_conexion)
    nueva_conexion.close()

def UsuarioTopo(nombreR,contraR,nivelR,router):
    contadorComando = 0
    conexion = paramiko.SSHClient()
    conexion.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    conexion.connect(router, username=usuario, password=password, look_for_keys=False, allow_agent=False)
    nueva_conexion = conexion.invoke_shell()
    salida = clear_buffer(nueva_conexion)
    time.sleep(2)
    with open("NuevoUSUARIO.txt","r") as file:
        for line in file:
            contadorLineaArchivo+=1
            if contadorLineaArchivo==2:
                comando=comando.format(nombreI=nombreR,nivelI=nivelR,contraI=contraR)
            nueva_conexion.send(comando.rstrip()+"\n")
            time.sleep(2)
            salida = nueva_conexion.recv(max_buffer)
            print(salida)
            salida=clear_buffer(nueva_conexion)
    nueva_conexion.close()