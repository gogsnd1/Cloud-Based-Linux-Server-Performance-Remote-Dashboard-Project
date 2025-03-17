from flask import Flask, jsonify, render_template
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///metrics.db'
db = SQLAlchemy(app)

# Define monitored servers here
SERVERS = {
    'Server 1': 'http://34.138.191.128:5000/stats',
    'Server 2': 'http://34.27.200.243:5000/stats',
}

# Database model
class Metric(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    server_name = db.Column(db.String(50))
    cpu = db.Column(db.Float)
    memory = db.Column(db.Float)
    disk = db.Column(db.Float)
    load1 = db.Column(db.Float)

with app.app_context():
    db.create_all()

# Store the latest stats from all servers
latest_stats = {}

def fetch_metrics():
    global latest_stats
    with app.app_context():
        for name, url in SERVERS.items():
            try:
                response = requests.get(url, timeout=5)
                response.raise_for_status()
                data = response.json()
                
                latest_stats[name] = data
                
                # Store data in the database
                metric = Metric(
                    server_name=name,
                    cpu=data['cpu_usage_percent'],
                    memory=data['memory_usage_percent'],
                    disk=data['disk_usage_percent'],
                    load1=data['load_average'][0]
                )
                db.session.add(metric)
                db.session.commit()
            except requests.RequestException as e:
                latest_stats[name] = {'error': str(e)}

scheduler = BackgroundScheduler()
scheduler.add_job(fetch_metrics, 'interval', seconds=60)
scheduler.start()

@app.route('/stats', methods=['GET'])
def get_stats():
    return jsonify(latest_stats)

@app.route('/history', methods=['GET'])
def get_history():
    data = Metric.query.order_by(Metric.timestamp.desc()).limit(50).all()
    history = [{
        'timestamp': metric.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        'server': metric.server_name,
        'cpu': metric.cpu,
        'memory': metric.memory,
        'disk': metric.disk,
        'load1': metric.load1
    } for metric in data]
    return jsonify(history)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    fetch_metrics()  # initial fetch on startup
    app.run(host='0.0.0.0', port=8000, debug=True)
