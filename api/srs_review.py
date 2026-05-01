from http.server import BaseHTTPRequestHandler
import json
from datetime import date, timedelta

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        body = json.loads(self.rfile.read(length))

        ef = float(body.get('ease_factor', 2.5))
        interval = int(body.get('interval_days', 1))
        rating = int(body.get('rating', 3))

        if rating == 1:       # Again
            interval = 1
            ef = max(1.3, ef - 0.2)
        elif rating == 2:     # Hard
            interval = max(1, int(interval * 1.2))
            ef = max(1.3, ef - 0.15)
        elif rating == 3:     # Good
            interval = int(interval * ef)
        elif rating == 4:     # Easy
            interval = int(interval * ef * 1.3)
            ef = ef + 0.1

        next_review = str(date.today() + timedelta(days=max(1, interval)))

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps({
            'new_ease_factor': round(ef, 2),
            'new_interval_days': max(1, interval),
            'next_review': next_review
        }).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()