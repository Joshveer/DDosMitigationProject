import sqlite3
import time
import numpy as np
import subprocess

def get_baseline_stats():
    conn = sqlite3.connect('traffic_data.db')
    cursor = conn.cursor()
    
    # Fetch packet counts per source_ip
    cursor.execute('''
        SELECT COUNT(*) as packet_count
        FROM traffic 
        GROUP BY source_ip
    ''')
    
    # Fetch all rows from the query
    rows = cursor.fetchall()
    
    # Calculate average and standard deviation using numpy
    if rows:
        packet_counts = [row[0] for row in rows]
        avg_packet_count = np.mean(packet_counts)
        std_deviation = np.std(packet_counts)
    else:
        avg_packet_count = 0
        std_deviation = 0
    
    conn.close()
    
    return avg_packet_count, std_deviation

def detect_anomalies(avg, stdev):
    conn = sqlite3.connect('traffic_data.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT COUNT(*) as packet_count, AVG(packet_size) as avg_size, source_ip
        FROM traffic
        WHERE timestamp >= datetime('now', '-1 minute')
        GROUP BY source_ip
        ORDER BY packet_count DESC
    ''')
    
    results = cursor.fetchall()
    anomalies = []
    
    for row in results:
        packet_count, avg_size, source_ip = row
        z_score = (packet_count - avg) / stdev if stdev > 0 else 0
        
        if z_score > 3:  # Three-sigma rule
            anomalies.append((source_ip, packet_count, avg_size, z_score))
            
            cursor.execute('''
                INSERT INTO alerts (alert_type, source_ip, details)
                VALUES (?, ?, ?)
            ''', ('High Traffic', source_ip, f'Packet count: {packet_count}, Z-score: {z_score:.2f}'))
    
    conn.commit()
    conn.close()
    return anomalies

def block_ip(ip):
    subprocess.run(['iptables', '-A', 'INPUT', '-s', ip, '-j', 'DROP'])
    print(f"Blocked IP: {ip}")

def monitor_traffic():
    baseline_avg, baseline_stdev = get_baseline_stats()
    
    while True:
        anomalies = detect_anomalies(baseline_avg, baseline_stdev)
        
        print("\nDetected Anomalies:")
        for anomaly in anomalies:
            source_ip, packet_count, avg_size, z_score = anomaly
            print(f"IP: {source_ip}, Packets: {packet_count}, Avg Size: {avg_size:.2f}, Z-score: {z_score:.2f}")
            
            if z_score > 5:  # Extreme anomaly
                block_ip(source_ip)
        
        time.sleep(60)  # Wait for 1 minute before next check

if __name__ == "__main__":
    monitor_traffic()
