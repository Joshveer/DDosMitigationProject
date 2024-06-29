# DDoS Detection and Mitigation System

## Overview
This project implements a comprehensive DDoS (Distributed Denial of Service) detection and mitigation system on a Linux server. It combines network traffic analysis, SQL database management, web server setup, and web dashboard development using Python, Flask, Apache, and various networking tools.

## Features
- **Local Web Server Setup**: Utilizes Apache for hosting a simple HTML page to simulate normal web traffic.
- **Traffic Generation**: Uses Apache JMeter to generate simulated user traffic for testing purposes.
- **DDoS Attack Simulation**: Employs hping3 to simulate SYN flood attacks on the web server for testing and validation.
- **Traffic Capture and Analysis**: Utilizes tcpdump to capture network traffic and stores data in a SQL database for analysis.
- **Detection Algorithms**: Develops Python scripts to analyze captured traffic data for anomalies indicative of DDoS attacks.
- **Mitigation Strategies**: Implements automated IP blocking using iptables to mitigate identified malicious traffic.
- **Web Dashboard**: Develops a Flask-based web dashboard to visualize traffic data, detection results, and system status.
- **Maintenance and Monitoring**: Includes scheduled database backups and system performance monitoring using Linux tools like cron, htop, and netstat.
