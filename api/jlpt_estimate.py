from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        params = parse_qs(urlparse(self.path).query)
        n5 = int(params.get('n5', [0])[0])
        n4 = int(params.get('n4', [0])[0])
        n3 = int(params.get('n3', [0])[0])
        n2 = int(params.get('n2', [0])[0])
        n1 = int(params.get('n1', [0])[0])

        total = n5 + n4 + n3 + n2 + n1
        thresholds = {'N5': 800, 'N4': 1500, 'N3': 3750, 'N2': 6000, 'N1': 10000}

        if total == 0:
            result = {'level': 'N5', 'progress_pct': 0}
        else:
            cumulative = n5 + n4*2 + n3*3 + n2*4 + n1*5
            score = cumulative / total
            if score < 1.5:
                pct = min(100, int((n5 / thresholds['N5']) * 100))
                result = {'level': 'N5', 'progress_pct': pct}
            elif score < 2.5:
                pct = min(100, int(((n5+n4) / thresholds['N4']) * 100))
                result = {'level': 'N4', 'progress_pct': pct}
            elif score < 3.5:
                pct = min(100, int(((n5+n4+n3) / thresholds['N3']) * 100))
                result = {'level': 'N3', 'progress_pct': pct}
            elif score < 4.5:
                pct = min(100, int(((n5+n4+n3+n2) / thresholds['N2']) * 100))
                result = {'level': 'N2', 'progress_pct': pct}
            else:
                pct = min(100, int((total / thresholds['N1']) * 100))
                result = {'level': 'N1', 'progress_pct': pct}

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(result).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()