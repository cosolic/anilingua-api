from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        params = parse_qs(urlparse(self.path).query)
        jlpt = params.get('jlpt_level', ['N5'])[0]

        level_map = {
            'N5': 'Beginner', 'N4': 'Beginner',
            'N3': 'Intermediate', 'N2': 'Advanced', 'N1': 'Native'
        }
        difficulty = level_map.get(jlpt, 'Beginner')

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({
            'target_difficulty': difficulty,
            'message': f"Filter anime table by difficulty = '{difficulty}'"
        }).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()