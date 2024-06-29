from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    conn = sqlite3.connect('traffic_data.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT source_ip, COUNT(*) as packet_count, AVG(packet_size) as avg_size
        FROM traffic
        GROUP BY source_ip
        ORDER BY packet_count DESC
        LIMIT 10
    ''')
    top_ips = cursor.fetchall()
    
    cursor.execute('SELECT * FROM alerts ORDER BY timestamp DESC LIMIT 10')
    recent_alerts = cursor.fetchall()
    
    conn.close()
    
    return render_template('index.html', top_ips=top_ips, recent_alerts=recent_alerts)

if __name__ == '__main__':
    app.run(debug=True)