from flask import Flask, jsonify
import psutil
import platform
import time

app = Flask(__name__)

def get_uptime():
	return time.time() - psutil.boot_time()

@app.route('/stats', methods=['GET'])
def get_stats():
	stats = {
		'cpu_usage_percent': psutil.cpu_percent(interval=1),
		'memory_usage_percent': psutil.virtual_memory().percent,
		'disk_usage_percent': psutil.disk_usage('/').percent,
		'system_uptime_seconds': get_uptime(),
		'load_average': psutil.getloadavg(),
		'system_info': platform.platform()
	}
	return jsonify(stats)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug=True)
