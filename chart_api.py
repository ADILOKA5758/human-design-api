import swisseph as swe
from flask import Flask, request, jsonify
import datetime

app = Flask(__name__)

@app.route('/chart', methods=['GET'])
def chart():
    try:
        date_str = request.args.get('tgl')  # format: YYYY-MM-DD
        time_str = request.args.get('jam')  # format: HH:MM
        dt = datetime.datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        jul_day = swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute / 60.0)
        lon, lat = 115.088, -8.112  # Singaraja
        swe.set_topo(lon, lat, 0)

        planets = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto']
        results = {}

        for i, name in enumerate(planets):
            pos, _ = swe.calc_ut(jul_day, i)
            results[name] = round(pos[0], 4)

        return jsonify({
            'datetime_utc': dt.isoformat(),
            'location': {'lon': lon, 'lat': lat},
            'planets': results
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500
