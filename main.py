import logging
from json import dumps
from aiohttp import web
import socket
import syslog


async def handle(request):
    try:
        ip = request.match_info.get('ip', "127.0.0.1")
        begin_port = int(request.match_info.get('begin_port', "8000"))
        end_port = int(request.match_info.get('end_port', "8000"))
        syslog.syslog(syslog.LOG_INFO, f'scan ports on {ip} from {begin_port} to {end_port}')
        ports_info = list()

        syslog.syslog(syslog.LOG_DEBUG, 'creating socket...')
        socket_check = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        syslog.syslog(syslog.LOG_DEBUG, 'socket created. start scanning ports')
        for port in range(begin_port, end_port + 1):
            state = "close" if socket_check.connect_ex((ip, port)) else "open"
            syslog.syslog(syslog.LOG_DEBUG, f'port {port} is {state}')
            ports_info.append({"port": str(port), "state": state})
        syslog.syslog(syslog.LOG_DEBUG, 'convert to json')
        text = dumps(ports_info)
        syslog.syslog(syslog.LOG_DEBUG, 'return result')
        return web.Response(text=text)
    except Exception as e:
        logging.warning(e)

syslog.syslog(syslog.LOG_INFO, 'running server')
app = web.Application()
app.add_routes([web.get('/scan/{ip}/{begin_port}/{end_port}', handle)])

if __name__ == '__main__':
    web.run_app(app)
