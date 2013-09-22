import SimpleHTTPServer
import SocketServer
import pickle
import subprocess
import signal
import urlparse 
import json
import hashlib
import redis

PORT    = 8000
PROCESS = None

def rinasci_arnaldo():
    global PROCESS

    if PROCESS is not None:
        PROCESS.send_signal(signal.SIGUSR1)

    subprocess.check_call(['git', 'pull'])
    PROCESS = subprocess.Popen('python arnaldo.py irc.freenode.net ##informateci arnaldo'.split())
    subprocess.Popen('rm -f arnaldo.commit'.split())
    accendi_il_cervello()


def accendi_il_cervello():
    try:
        brain = redis.Redis("localhost")
    except:
        sys.exit("Insane in the membrane!!!")

    hs=hashlib.md5(open('SUB-EST2011-01.csv').read()).hexdigest()
    if brain.get("cyfhash") != hs:
        brain.set("cyfhash",hs)
        cyf = open('SUB-EST2011-01.csv', 'r')
        cy = cyf.read()
        cyf.close()
        print "Rigenero CITTA"
        brain.delete("CITTA")
        for c in [[a.split(',')[1].upper() for a in (cy).split(",,,,")[6:-11]]][0]:
            brain.rpush("CITTA", c) # in CITTA c'e' la lista delle citta' maiuscole

    hs=hashlib.md5(open('nounlist.txt').read()).hexdigest()
    if brain.get("nnfhash") != hs:
        brain.set("nnfhash",hs)
        nnf = open('nounlist.txt', 'r')
        nn = nnf.read()
        nnf.close()
        print "Rigenero NOMICEN"
        brain.delete("NOMICEN")
        for n in nn.split('\n'):
            brain.rpush("NOMICEN", n.upper()) # in NOMIc'e' la lista dei nomi (comuni) inglesi in maiuscolo

    hs=hashlib.md5(open('attardi.txt').read()).hexdigest()
    if brain.get("attaffhash") != hs:
        brain.set("attaffhash",hs)
        attaf = open('attardi.txt', 'r')
        atta = attaf.readlines()
        attaf.close()
        print "Rigenero ATTARDI"
        brain.delete("ATTARDI")
        for a in [x.capitalize()[:-1] for x in atta]:
            brain.rpush("ATTARDI", a) # in NOMIc'e' la lista dei nomi (comuni) inglesi in maiuscolo

    hs=hashlib.md5(open('prov1.pkl').read()).hexdigest()
    if brain.get("prov1fhash") != hs:
        brain.set("prov1fhash",hs)
        pkl_file = open('prov1.pkl', 'rb')
        PROV1 = pickle.load(pkl_file)
        pkl_file.close()
        print "Rigenero PROV1"
        brain.delete("PROV1")
        for p1 in PROV1: #lista prima meta' dei proverbi in PROV1
            brain.rpush("PROV1"," ".join(p1))
        del(PROV1)

    hs=hashlib.md5(open('prov2.pkl').read()).hexdigest()
    if brain.get("prov2fhash") != hs:
        brain.set("prov2fhash",hs)
        pkl_file = open('prov2.pkl', 'rb')
        PROV2 = pickle.load(pkl_file)
        pkl_file.close()
        print "Rigenero PROV2"
        brain.delete("PROV2")
        for p2 in PROV2: #lista 2a meta' dei proverbi in PROV2
            brain.rpush("PROV2"," ".join(p2))
        del(PROV2)

class ServerHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_the_404(self):
        p='<html><h1>ONORE AL COMMENDATORE</h1><audio autoplay loop><source src="http://k002.kiwi6.com/hotlink/7dfwc95g6j/ztuovbziexvt.128.mp3" type="audio/mp3"></audio><p><img alt="" src="http://25.media.tumblr.com/tumblr_lxom7sxjDv1qcy8xgo1_500.gif" class="alignnone" width="500" height="333"></p></html>'
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
        length = int(self.headers['Content-Length'])
        post_data = urlparse.parse_qs(self.rfile.read(length).decode('utf-8'))
        author=None
        message=None
        for key, value in post_data.iteritems():
            if key=="payload" and len(value)>0:
                payload=json.loads(value[0])
                commits=payload.get('commits',None)
                if commits != None and len(commits)>0:
                    author=commits[0].get('author',None)
                    message=commits[0].get('message',None)
                    author=author.get('name',None)
                    print "<%s>: %s"%(author,message)
                    
        if author!=None and message !=None:
            f=open("arnaldo.commit",'w')
            f.write("%s:%s"%(author,message))
            f.close()

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

