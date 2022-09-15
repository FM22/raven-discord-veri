from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import bot
import asyncio
from urllib.parse import urlparse
from urllib.parse import parse_qs

hostName = "131.111.179.83"
serverPort = 8080

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("Updating bot\n", "utf-8"))
        parsed_url = urlparse(self.path)
        id = parse_qs(parsed_url.query)['userid'][0]
        bot.client.loop.create_task(bot.client.on_ping(id=id))
        print("Ping to verify id: " + id)

def run_server():
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")