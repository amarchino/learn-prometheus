import random, signal, sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime
from prometheus_client import start_http_server, Counter

REQUEST_COUNT = Counter('app_requests_count', 'total app http request count',['app_name', 'endpoint'])
RANDOM_COUNT = Counter('app_random_count','increment counter by random value')

APP_PORT = 8000
METRICS_PORT = 8001
webServer = None

def terminate(signal,frame):
    print("Start Terminating: %s" % datetime.now())
    webServer.server_close()
    sys.exit(0)

class HandleRequests(BaseHTTPRequestHandler):

    def do_GET(self):
        REQUEST_COUNT.labels('prom_python_app', self.path).inc()
        random_val = random.random()*10
        RANDOM_COUNT.inc(random_val)
        
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>First Application</title></head><body style='color: #333; margin-top: 30px;'><center><h2>Welcome to our first Prometheus-Python application.</center></h2></body></html>", "utf-8"))

if __name__ == "__main__":
    signal.signal(signal.SIGTERM, terminate)

    start_http_server(METRICS_PORT)
    webServer = HTTPServer(('0.0.0.0', APP_PORT), HandleRequests)
    webServer.serve_forever()