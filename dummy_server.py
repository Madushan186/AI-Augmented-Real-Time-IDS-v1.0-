
import http.server
import socketserver

PORT = 8080

Handler = http.server.SimpleHTTPRequestHandler

try:
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"✅ Dummy Victim Server listening on Port {PORT}")
        print("   This ensures the attacker gets a '200 OK' and can send packets fast!")
        httpd.serve_forever()
except OSError as e:
    print(f"❌ Error: Port {PORT} is occupied. {e}")
except KeyboardInterrupt:
    print("\n🛑 Server stopped.")
