from flask import Flask, request, jsonify
from datetime import date, timedelta

app = Flask(__name__)

@app.after_request
def add_cors(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

@app.route('/api/srs_review', methods=['POST', 'OPTIONS'])
def srs_review():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    body = request.get_json()
    ef = float(body.get('ease_factor', 2.5))
    interval = int(body.get('interval_days', 1))
    rating = int(body.get('rating', 3))

    if rating == 1:
        interval = 1
        ef = max(1.3, ef - 0.2)
    elif rating == 2:
        interval = max(1, int(interval * 1.2))
        ef = max(1.3, ef - 0.15)
    elif rating == 3:
        interval = int(interval * ef)
    elif rating == 4:
        interval = int(interval * ef * 1.3)
        ef = ef + 0.1

    next_review = str(date.today() + timedelta(days=max(1, interval)))
    return jsonify({
        'new_ease_factor': round(ef, 2),
        'new_interval_days': max(1, interval),
        'next_review': next_review
    })

@app.route('/api/jlpt_estimate', methods=['GET'])
def jlpt_estimate():
    n5 = int(request.args.get('n5', 0))
    n4 = int(request.args.get('n4', 0))
    n3 = int(request.args.get('n3', 0))
    n2 = int(request.args.get('n2', 0))
    n1 = int(request.args.get('n1', 0))

    total = n5 + n4 + n3 + n2 + n1
    thresholds = {'N5': 800, 'N4': 1500, 'N3': 3750, 'N2': 6000, 'N1': 10000}

    if total == 0:
        return jsonify({'level': 'N5', 'progress_pct': 0})

    cumulative = n5 + n4*2 + n3*3 + n2*4 + n1*5
    score = cumulative / total

    if score < 1.5:
        result = {'level': 'N5', 'progress_pct': min(100, int((n5 / thresholds['N5']) * 100))}
    elif score < 2.5:
        result = {'level': 'N4', 'progress_pct': min(100, int(((n5+n4) / thresholds['N4']) * 100))}
    elif score < 3.5:
        result = {'level': 'N3', 'progress_pct': min(100, int(((n5+n4+n3) / thresholds['N3']) * 100))}
    elif score < 4.5:
        result = {'level': 'N2', 'progress_pct': min(100, int(((n5+n4+n3+n2) / thresholds['N2']) * 100))}
    else:
        result = {'level': 'N1', 'progress_pct': min(100, int((total / thresholds['N1']) * 100))}

    return jsonify(result)

@app.route('/api/anime_recommend', methods=['GET'])
def anime_recommend():
    jlpt = request.args.get('jlpt_level', 'N5')
    level_map = {
        'N5': 'Beginner', 'N4': 'Beginner',
        'N3': 'Intermediate', 'N2': 'Advanced', 'N1': 'Native'
    }
    difficulty = level_map.get(jlpt, 'Beginner')
    return jsonify({
        'target_difficulty': difficulty,
        'message': f"Filter anime table by difficulty = '{difficulty}'"
    })
