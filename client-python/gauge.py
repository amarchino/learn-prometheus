import signal, sys, time
from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime
from prometheus_client import start_http_server, Gauge

REQUEST_INPROGRESS = Gauge('app_requests_inprogress','number of application requests in progress')
REQUEST_LAST_SERVED = Gauge('app_last_served', 'Time the application was last served.')

APP_PORT = 8000
METRICS_PORT = 8001
webServer = None

def terminate(signal,frame):
    print("Start Terminating: %s" % datetime.now())
    webServer.server_close()
    sys.exit(0)

class HandleRequests(BaseHTTPRequestHandler):

    @REQUEST_INPROGRESS.track_inprogress()
    def do_GET(self):
        # REQUEST_INPROGRESS.inc()
        time.sleep(5)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>First Application</title></head><body style='color: #333; margin-top: 30px;'><center><h2>Welcome to our first Prometheus-Python application.</center></h2></body></html>", "utf-8"))
        REQUEST_LAST_SERVED.set_to_current_time()
        # REQUEST_LAST_SERVED.set(time.time())
        # REQUEST_INPROGRESS.dec()

if __name__ == "__main__":
    signal.signal(signal.SIGTERM, terminate)

    start_http_server(METRICS_PORT)
    server = HTTPServer(('0.0.0.0', APP_PORT), HandleRequests)
    server.serve_forever()