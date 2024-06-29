from scapy.all import rdpcap
import sqlite3
import ipaddress

def is_private_ip(ip):
    return ipaddress.ip_address(ip).is_private

conn = sqlite3.connect('traffic_data.db')
cursor = conn.cursor()

packets = rdpcap('traffic_capture.pcap')

for packet in packets:
    if packet.haslayer('IP'):
        ip = packet['IP']
        source_ip = ip.src
        dest_ip = ip.dst
        protocol = ip.proto
        size = len(packet)
        flags = str(ip.flags) if hasattr(ip, 'flags') else ''
        
        src_port = packet[ip.name].sport if hasattr(packet[ip.name], 'sport') else 0
        dst_port = packet[ip.name].dport if hasattr(packet[ip.name], 'dport') else 0

        if not is_private_ip(source_ip) and not is_private_ip(dest_ip):
            cursor.execute('''
                INSERT INTO traffic (source_ip, destination_ip, protocol, packet_size, flags, src_port, dst_port)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (source_ip, dest_ip, protocol, size, flags, src_port, dst_port))

conn.commit()
conn.close()