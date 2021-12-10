import os
from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException
from collections import namedtuple
from graphviz import Digraph
import time

instru = "show cdp neighbors detail"

Router = namedtuple('Router', ['destination_host', 'management_ip'])

def show_cdp(ip):
    device = {
        'device_type': 'cisco_ios',
        'host': ip,
        'username': 'root',
        'password': 'root'
    }
    try:
        with ConnectHandler(**device) as net_connect:
            #print("Me regresa: ", net_connect.send_command(instru, use_textfsm=True))
            return net_connect.send_command(instru, use_textfsm=True)
    except NetmikoAuthenticationException:
        print('Authetication error')
    except NetmikoTimeoutException:
        print('Timeout error')
    except Exception as e:
        print(e)
        print('Network error')

def get_topology(main_router):
    routers = []
    next_router = [main_router]
    visited_routers = [main_router.destination_host]
    network = Digraph(comment = 'Network')

    while next_router:
        router = next_router.pop(0)
        routers.append(router)
        network.node(router.destination_host)
        #print(router.management_ip)
        #print(show_cdp(router.management_ip))
        for neighbor in show_cdp(router.management_ip):
            network.edge(router.destination_host, neighbor['destination_host'])
            if neighbor['destination_host'] not in visited_routers:
                visited_routers.append(neighbor['destination_host'])
                next_router.append(Router(neighbor['destination_host'], neighbor['management_ip']))

    return routers, network

def main_topologia():
    while True:
        print("Topologia")
        #time.sleep(60)
        main_router = Router('R4.teamdinamita.mx', '10.0.4.254')
        routers, topology = get_topology(main_router)
        for router in routers:
            print(router)
        #print(topology.source)
        topology.format = 'png'
        topology.render(directory='./static').replace('\\', '/')
        time.sleep(10)

if __name__ == '__main__':
    main_router = Router('R4.teamdinamita.mx', '10.0.4.254')
    routers, topology = get_topology(main_router)
    for router in routers:
        print(router)
    print(topology.source)
    topology.format = 'png'
    topology.render(directory='../static').replace('\\', '/')


