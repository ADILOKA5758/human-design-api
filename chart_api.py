import swisseph as swe
from flask import Flask, request, jsonify
import datetime
import os

app = Flask(__name__)

@app.route('/chart', methods=['GET'])
def chart():
    try:
        # Ambil parameter
        date_str = request.args.get('tgl')  # format: YYYY-MM-DD
        time_str = request.args.get('jam')  # format: HH:MM

        if not date_str or not time_str:
            return jsonify({'error': 'Parameter tgl dan jam wajib diisi'}), 400

        try:
            dt = datetime.datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        except ValueError:
            return jsonify({'error': 'Format tgl atau jam salah'}), 400

        # Konversi ke Julian Day
        jul_day = swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute / 60.0)

        # Lokasi default: Singaraja
        lon, lat = 115.088, -8.112
        swe.set_topo(lon, lat, 0)

        planets = [
            ('Sun', swe.SUN),
            ('Moon', swe.MOON),
            ('Mercury', swe.MERCURY),
            ('Venus', swe.VENUS),
            ('Mars', swe.MARS),
            ('Jupiter', swe.JUPITER),
            ('Saturn', swe.SATURN),
            ('Uranus', swe.URANUS),
            ('Neptune', swe.NEPTUNE),
            ('Pluto', swe.PLUTO)
        ]

        results = {}

        for name, pid in planets:
            try:
                pos, _ = swe.calc_ut(jul_day, pid)
                results[name] = round(pos[0], 4)
            except Exception as e:
                results[name] = None
                print(f"❌ Error menghitung {name}: {e}")

        return jsonify({
            'datetime_utc': dt.isoformat(),
            'location': {'lon': lon, 'lat': lat},
            'planets': results
        })

    except Exception as e:
        print(f"❌ ERROR BESAR: {e}")
        return jsonify({'error': str(e)}), 500

# Untuk running di Render
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
