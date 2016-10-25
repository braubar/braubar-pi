import http.server

class PowerstripRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"<html><head><title>PowerStrip HTTP Emulator GET</title>")
        self.wfile.write(b"</head><body><p>Ich Lebe!</p>")
        self.wfile.write(b"</body></html>")

    def do_POST(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"<html><head><title>PowerStrip HTTP Emulator</title>")
        self.wfile.write(b"<script>____sockstates____1_1_1_1</script>")
        self.wfile.write(b"</head><body><p>alles an</p>")
        self.wfile.write(b"</body></html>")


def run():
    server_address = ("powerstrip", 8080)
    http_server = http.server.HTTPServer(server_address, PowerstripRequestHandler)
    http_server.server_port = 8080
    http_server.serve_forever()

run()
