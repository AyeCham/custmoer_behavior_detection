from flask import Flask, jsonify, render_template_string
import csv
import os

app = Flask(__name__)

CSV_FILE = 'engagement_log.csv'

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Engagement Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Inter', sans-serif;
            margin: 0;
            background-color: #f0f2f5;
            display: flex;
        }
        .sidebar {
            flex: 0 0 220px;
            background-color: #1c1f26;
            color: white;
            height: 100vh;
            padding: 30px 20px;
            box-shadow: 2px 0 8px rgba(0,0,0,0.1);
            position: fixed;
        }
        .sidebar h2 {
            font-size: 1.4rem;
            text-align: center;
            margin-bottom: 40px;
        }
        .sidebar nav a {
            display: block;
            color: #ccc;
            text-decoration: none;
            margin: 15px 0;
            transition: 0.2s;
        }
        .sidebar nav a:hover {
            color: white;
        }
        .main-container {
            margin-left: 220px;
            flex: 1;
            padding: 30px;
        }
        header {
            font-size: 2rem;
            font-weight: bold;
            margin-bottom: 20px;
            color: #007bff;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        th, td {
            border: 1px solid #ccc;
            padding: 8px 12px;
            text-align: left;
        }
        th {
            background-color: #eee;
        }
    </style>
</head>
<body>
    <div class="sidebar">
        <h2>Innergy Lab</h2>
        <nav>
            <a href="/">Dashboard</a>
        </nav>
    </div>

    <div class="main-container">
        <header>Engagement Log</header>
        <table id="historyTable">
            <thead>
                <tr>
                    <th>Customer ID</th>
                    <th>Staff ID</th>
                    <th>Start Time</th>
                    <th>End Time</th>
                    <th>Duration (sec)</th>
                </tr>
            </thead>
            <tbody></tbody>
        </table>
    </div>

    <script>
    function loadHistory() {
        fetch('/history')
            .then(response => response.json())
            .then(data => {
                const tableBody = document.getElementById('historyTable').querySelector('tbody');
                tableBody.innerHTML = '';

                const columns = ['Customer_ID', 'Staff_ID', 'Start_Time', 'End_Time', 'Duration_sec'];

                // Sort by latest Timestamp descending
                data.sort((a, b) => new Date(b.Timestamp) - new Date(a.Timestamp));

                data.forEach(entry => {
                    const row = document.createElement('tr');
                    columns.forEach(col => {
                        const cell = document.createElement('td');
                        cell.textContent = entry[col] || '';
                        row.appendChild(cell);
                    });
                    tableBody.appendChild(row);
                });
            })
            .catch(err => console.error('Failed to load history', err));
    }

    loadHistory();
    setInterval(loadHistory, 2000);
    </script>
</body>
</html>
'''

@app.route('/')
def dashboard():
    return render_template_string(HTML_TEMPLATE)

@app.route('/history')
def history():
    history_data = []
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                history_data.append(row)
    return jsonify(history_data)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
