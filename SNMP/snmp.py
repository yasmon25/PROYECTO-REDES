from pysnmp.entity.rfc3413.oneliner import cmdgen

cmdGen = cmdgen.CommandGenerator()

system_name = "1.3.6.1.2.1.1.5.0"
system_contact = "1.3.6.1.2.1.1.4.0"
system_description = "1.3.6.1.2.1.1.1.0"
system_location = "1.3.6.1.2.1.1.6.0"



def get_data_router():
    nombre= ""
    direccion=""
    contacto=""
    descripcion=""

    errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
	    cmdgen.CommunityData('rw_4CM11'),
	    cmdgen.UdpTransportTarget(('10.0.4.254', 161)),
	    system_name,
	    system_contact,
        system_description,
        system_location
    )

    if errorIndication:
	    print(errorIndication)
    else:
        datos=[]
        for name, val in varBinds:
            datos.append(str(val))
        print(datos)
        return datos
        
