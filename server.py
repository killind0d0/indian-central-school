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

import json
import base64

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
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        if self.path == "/api/save":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            try:
                payload = json.loads(body.decode("utf-8"))
                file_rel = payload.get("file", "")
                data = payload.get("data")
                allowed_files = {
                    "data/notices.json",
                    "data/achievements.json",
                    "data/faculty.json",
                    "data/campus.json",
                    "data/advisory.json"
                }
                if file_rel not in allowed_files or not isinstance(data, list):
                    self.send_response(400)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(b'{"error": "Invalid target file or data format"}')
                    return
                
                target_path = os.path.join(DIRECTORY, file_rel)
                with open(target_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"success": True, "count": len(data)}).encode("utf-8"))
            except Exception as ex:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(ex)}).encode("utf-8"))
            return

        elif self.path == "/api/upload":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            try:
                payload = json.loads(body.decode("utf-8"))
                folder = payload.get("folder", "assets/notices").strip("/\\")
                raw_filename = os.path.basename(payload.get("filename", "upload.jpg"))
                # Sanitize filename
                clean_name = "".join(c for c in raw_filename if c.isalnum() or c in "._-")
                if not clean_name:
                    clean_name = "upload.jpg"
                
                base64_data = payload.get("base64", "")
                if "," in base64_data:
                    base64_data = base64_data.split(",", 1)[1]
                
                allowed_folders = {"assets/notices", "assets/achievements", "assets/faculty", "assets/campus", "assets/committee", "assets/entrance"}
                if folder not in allowed_folders:
                    folder = "assets/notices"
                
                target_dir = os.path.join(DIRECTORY, folder)
                os.makedirs(target_dir, exist_ok=True)
                file_path = os.path.join(target_dir, clean_name)
                
                with open(file_path, "wb") as f:
                    f.write(base64.b64decode(base64_data))
                
                rel_path = f"{folder}/{clean_name}"
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"success": True, "path": rel_path}).encode("utf-8"))
            except Exception as ex:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(ex)}).encode("utf-8"))
            return

        self.send_response(404)
        self.end_headers()

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
