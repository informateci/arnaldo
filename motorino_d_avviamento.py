import SimpleHTTPServer
import SocketServer

import subprocess

PORT    = 8000
PROCESS = None

def rinasci_arnaldo():
    global PROCESS

    if PROCESS is not None:
        PROCESS.terminate()
    
    PROCESS = subprocess.Popen(['python', 'arnaldo.py'])

class ServerHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_the_404(self):
        self.send_error(404, 'ONORE AL COMMENDATORE')

    def do_the_dance(self):
        rinasci_arnaldo()

    def do_GET(self):
        self.do_the_404()

    def do_POST(self):
        if self.path != '/github':
            self.do_the_404()
            return
        
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write('ONORE AL COMMENDATORE')
        self.do_the_dance()

if __name__ == '__main__':
    print 'Starting arnaldo'
    rinasci_arnaldo()
   
    print "Starting webserver (%s)" % (PORT,)
    httpd = SocketServer.TCPServer(("", PORT), ServerHandler)
    httpd.serve_forever()

