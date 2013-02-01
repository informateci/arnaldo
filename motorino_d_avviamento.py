import SimpleHTTPServer
import SocketServer

import subprocess

PORT    = 8000
PROCESS = None

def rinasci_arnaldo():
    global PROCESS

    if PROCESS is not None:
        PROCESS.terminate()

    subprocess.check_call(['git', 'pull'])
    PROCESS = subprocess.Popen(['python', 'arnaldo.py'])

class ServerHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_the_404(self):
        p='<html><h1>ONORE AL COMMENDATORE</h1><audio autoplay loop><source src="http://www.fileden.com/files/2009/3/22/2374149/Giorgio%20Moroder%20-%20Einzelganger%20%281%29%20-%20Einzelganger.mp3" type="audio/mp3"></audio><p><img alt="" src="http://25.media.tumblr.com/tumblr_lxom7sxjDv1qcy8xgo1_500.gif" class="alignnone" width="500" height="333"></p></html>'
        self.send_response(404)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-length", str(len(p)))
        self.end_headers()
        self.wfile.write(p)
        self.wfile.flush()
        self.connection.shutdown(1)

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

