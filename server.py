import http.server
import mimetypes
import os
import sys
import socket

PORT = 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

# Ensure all essential mime types are registered
mimetypes.init()
mimetypes.add_type("image/webp", ".webp")
mimetypes.add_type("image/jpeg", ".jpeg")
mimetypes.add_type("image/jpeg", ".jpg")
mimetypes.add_type("image/png", ".png")
mimetypes.add_type("image/svg+xml", ".svg")
mimetypes.add_type("application/json", ".json")
mimetypes.add_type("text/javascript", ".js")
mimetypes.add_type("text/css", ".css")
mimetypes.add_type("text/html; charset=utf-8", ".html")

class MultiThreadedHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def log_message(self, format, *args):
        client_ip = self.client_address[0] if self.client_address else "unknown"
        print(f"[{self.log_date_time_string()}] [{client_ip}] {format % args}", flush=True)

    def end_headers(self):
        # Development / Live Showcase: No-cache ensures latest edits reflect immediately
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        self.send_header("Access-Control-Allow-Origin", "*")
        super().end_headers()

def get_lan_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "192.168.29.127"

if __name__ == "__main__":
    http.server.ThreadingHTTPServer.allow_reuse_address = True
    server = http.server.ThreadingHTTPServer(("0.0.0.0", PORT), MultiThreadedHandler)
    lan_ip = get_lan_ip()
    print("=" * 60, flush=True)
    print("  🏫 INDIAN CENTRAL SCHOOL - LIVE SHOWCASE SERVER", flush=True)
    print("=" * 60, flush=True)
    print(f"  ⚡ Local Phone:    http://localhost:{PORT}", flush=True)
    print(f"  ⚡ Wi-Fi / Hotspot: http://{lan_ip}:{PORT}", flush=True)
    print(f"  ⚡ Hotspot Clients: http://192.168.43.1:{PORT}", flush=True)
    print("=" * 60, flush=True)
    print(f"  📁 Serving from: {DIRECTORY}", flush=True)
    print("  🚀 Multi-Threaded & Ready for Demo!", flush=True)
    print("=" * 60, flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.", flush=True)
        server.server_close()
