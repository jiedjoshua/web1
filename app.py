#!/usr/bin/env python3
"""
CTF Vulnerability Suite - Educational Flask Application
WARNING: Contains intentional security vulnerabilities for educational purposes only!
DO NOT deploy in production or expose to the internet.
"""

import sqlite3
import os
import logging
from flask import Flask, request, render_template_string, jsonify

# Configure logging for Railway debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Database configuration
DATABASE = 'ctf_database.db'

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/health')
def health_check():
    """Health check endpoint for Railway"""
    try:
        # Check if database exists and is accessible
        conn = get_db_connection()
        cursor = conn.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]
        conn.close()
        
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'users_count': count,
            'message': 'CTF Vulnerability Suite is running'
        }), 200
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'message': 'Database connection failed'
        }), 500

@app.route('/')
def index():
    """Main landing page"""
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>HackLab - Vulnerability Training Suite</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 50%, #16213e 100%);
                min-height: 100vh;
                color: #fff;
                padding: 20px;
            }
            
            .container {
                max-width: 1200px;
                margin: 0 auto;
            }
            
            .header {
                text-align: center;
                margin-bottom: 50px;
                padding: 40px 0;
            }
            
            .header h1 {
                font-size: 48px;
                font-weight: 700;
                background: linear-gradient(135deg, #ff6b6b, #4ecdc4, #45b7d1);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                margin-bottom: 10px;
                text-shadow: 0 0 30px rgba(255, 107, 107, 0.5);
            }
            
            .header .subtitle {
                font-size: 18px;
                color: #a0a0a0;
                margin-bottom: 30px;
            }
            
            .warning {
                background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
                padding: 25px;
                border-radius: 15px;
                margin: 30px 0;
                text-align: center;
                border: 1px solid rgba(255, 107, 107, 0.3);
                box-shadow: 0 10px 30px rgba(255, 107, 107, 0.2);
            }
            
            .warning strong {
                font-size: 20px;
                display: block;
                margin-bottom: 10px;
            }
            
            .challenges-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
                gap: 30px;
                margin: 40px 0;
            }
            
            .challenge-card {
                background: rgba(255, 255, 255, 0.05);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 20px;
                padding: 30px;
                transition: all 0.3s ease;
                position: relative;
                overflow: hidden;
            }
            
            .challenge-card::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 4px;
                background: linear-gradient(135deg, #ff6b6b, #4ecdc4);
            }
            
            .challenge-card:hover {
                transform: translateY(-10px);
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
                border-color: rgba(255, 255, 255, 0.2);
            }
            
            .challenge-icon {
                font-size: 48px;
                margin-bottom: 20px;
                display: block;
            }
            
            .challenge-card h3 {
                font-size: 24px;
                margin-bottom: 15px;
                color: #fff;
            }
            
            .challenge-card p {
                color: #b0b0b0;
                margin-bottom: 25px;
                line-height: 1.6;
            }
            
            .challenge-link {
                display: inline-block;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 12px 25px;
                border-radius: 25px;
                text-decoration: none;
                font-weight: 600;
                transition: all 0.3s ease;
                border: 1px solid rgba(255, 255, 255, 0.2);
            }
            
            .challenge-link:hover {
                transform: translateY(-2px);
                box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
                text-decoration: none;
            }
            
            .difficulty {
                position: absolute;
                top: 20px;
                right: 20px;
                background: rgba(255, 255, 255, 0.1);
                padding: 5px 12px;
                border-radius: 15px;
                font-size: 12px;
                font-weight: 600;
            }
            
            .difficulty.beginner { background: rgba(76, 175, 80, 0.3); }
            .difficulty.intermediate { background: rgba(255, 193, 7, 0.3); }
            
            .stats {
                display: flex;
                justify-content: space-around;
                margin: 40px 0;
                text-align: center;
            }
            
            .stat-item {
                background: rgba(255, 255, 255, 0.05);
                padding: 20px;
                border-radius: 15px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
            
            .stat-number {
                font-size: 32px;
                font-weight: 700;
                color: #4ecdc4;
                display: block;
            }
            
            .stat-label {
                color: #a0a0a0;
                font-size: 14px;
                margin-top: 5px;
            }
            
            @media (max-width: 768px) {
                .challenges-grid {
                    grid-template-columns: 1fr;
                }
                
                .header h1 {
                    font-size: 36px;
                }
                
                .stats {
                    flex-direction: column;
                    gap: 20px;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🔥 HackLab</h1>
                <p class="subtitle">Advanced Vulnerability Training Suite</p>
            </div>
            
            <div class="warning">
                <strong>⚠️ EDUCATIONAL ENVIRONMENT ONLY ⚠️</strong>
                This platform contains intentional security vulnerabilities for ethical hacking training.<br>
                <strong>DO NOT</strong> deploy in production or expose to the internet!
            </div>
            
            <div class="stats">
                <div class="stat-item">
                    <span class="stat-number">2</span>
                    <div class="stat-label">Active Challenges</div>
                </div>
                <div class="stat-item">
                    <span class="stat-number">100%</span>
                    <div class="stat-label">Vulnerable</div>
                </div>
                <div class="stat-item">
                    <span class="stat-number">∞</span>
                    <div class="stat-label">Learning Potential</div>
                </div>
            </div>
            
            <div class="challenges-grid">
                <div class="challenge-card">
                    <div class="difficulty beginner">BEGINNER</div>
                    <span class="challenge-icon">💉</span>
                    <h3>SQL Injection Challenge</h3>
                    <p>Exploit a realistic banking login portal with classic SQL injection vulnerabilities. Perfect for learning authentication bypass techniques.</p>
                    <a href="/login/challenge1" class="challenge-link">🎯 Start Challenge</a>
                </div>
                
                <div class="challenge-card">
                    <div class="difficulty intermediate">INTERMEDIATE</div>
                    <span class="challenge-icon">🔥</span>
                    <h3>Cross-Site Scripting (XSS)</h3>
                    <p>Find and exploit reflected XSS vulnerabilities in a search portal. Learn to execute JavaScript and reveal hidden flags.</p>
                    <a href="/challenge2" class="challenge-link">🎯 Start Challenge</a>
                </div>
            </div>
        </div>
    </body>
    </html>
    ''')

@app.route('/login/challenge1', methods=['GET', 'POST'])
def sql_injection_challenge():
    """
    INTENTIONALLY VULNERABLE: SQL Injection Challenge
    This endpoint demonstrates a classic SQL injection vulnerability
    """
    result = None
    error = None
    login_success = False
    
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        
        if username and password:
            try:
                conn = get_db_connection()
                # VULNERABILITY: Direct string interpolation in SQL query
                # This allows SQL injection attacks like: admin" OR 1=1 --
                query = f"SELECT username, password, bio FROM users WHERE username = '{username}' AND password = '{password}'"
                
                print(f"[DEBUG] Executing query: {query}")  # For educational purposes
                
                cursor = conn.execute(query)
                result = cursor.fetchall()
                conn.close()
                
                # Only consider login successful if we have results AND the password actually matches
                # This forces users to use SQL injection to bypass authentication
                if result:
                    # Check if any returned row has matching credentials
                    valid_login = False
                    for row in result:
                        if row['username'] == username and row['password'] == password:
                            valid_login = True
                            break
                    
                    if valid_login or len(result) > 1:  # Multiple results = SQL injection success
                        login_success = True
                    else:
                        error = "Login Unsuccessful - Invalid username or password combination"
                else:
                    error = "Login Unsuccessful - No matching user found in database"
                
            except sqlite3.Error as e:
                # Handle SQL errors more gracefully for better injection experience
                error_msg = str(e)
                print(f"[ERROR] SQL Error with query: {query}")
                print(f"[ERROR] Error details: {error_msg}")
                
                # For syntax errors, show a more generic message to avoid breaking the flow
                if any(keyword in error_msg.lower() for keyword in ["syntax error", "unrecognized token", "near"]):
                    error = "Login Unsuccessful - Invalid characters in input"
                elif "no such column" in error_msg.lower():
                    error = f"Database Schema Error: {error_msg}"
                else:
                    error = "Login Unsuccessful - Database connection error"
        else:
            if not username and not password:
                error = "Login Unsuccessful - Username and password are required"
            elif not username:
                error = "Login Unsuccessful - Username field cannot be empty"
            elif not password:
                error = "Login Unsuccessful - Password field cannot be empty"
    
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>SecureBank Login Portal</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: #000000;
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }
            
            .login-container {
                background: #1a1a1a;
                border-radius: 20px;
                padding: 40px;
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
                width: 100%;
                max-width: 450px;
                border: 1px solid #333;
            }
            
            .logo {
                text-align: center;
                margin-bottom: 30px;
            }
            
            .logo h1 {
                color: #fff;
                font-size: 28px;
                font-weight: 700;
                margin-bottom: 5px;
            }
            
            .logo p {
                color: #ccc;
                font-size: 14px;
            }
            
            .form-group {
                margin-bottom: 25px;
                position: relative;
            }
            
            .form-group label {
                display: block;
                margin-bottom: 8px;
                color: #fff;
                font-weight: 600;
                font-size: 14px;
            }
            
            .form-group input {
                width: 100%;
                padding: 15px 20px;
                border: 2px solid #444;
                border-radius: 12px;
                font-size: 16px;
                transition: all 0.3s ease;
                background: #2a2a2a;
                color: #fff;
            }
            
            .form-group input:focus {
                outline: none;
                border-color: #666;
                background: #333;
                box-shadow: 0 0 0 3px rgba(102, 102, 102, 0.1);
            }
            
            .login-btn {
                width: 100%;
                padding: 15px;
                background: #333;
                color: white;
                border: 2px solid #555;
                border-radius: 12px;
                font-size: 16px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s ease;
                margin-bottom: 20px;
            }
            
            .login-btn:hover {
                background: #444;
                border-color: #666;
            }
            
            .success {
                background: #2a2a2a;
                color: white;
                padding: 20px;
                border-radius: 12px;
                margin: 20px 0;
                text-align: center;
                border: 2px solid #4a4a4a;
            }
            
            .success h3 {
                margin-bottom: 15px;
                font-size: 20px;
            }
            
            .user-card {
                background: #333;
                padding: 15px;
                border-radius: 8px;
                margin: 10px 0;
                border-left: 4px solid #666;
            }
            
            .error {
                background: #2a2a2a;
                color: #ff6b6b;
                padding: 20px;
                border-radius: 12px;
                margin: 20px 0;
                text-align: center;
                border: 2px solid #ff6b6b;
            }
            
            .error strong {
                display: block;
                font-size: 18px;
                margin-bottom: 8px;
            }
            
            .database-error {
                background: #2a2a2a;
                border: 2px solid #e74c3c;
                font-family: 'Courier New', monospace;
                text-align: left;
                color: #e74c3c;
            }
            
        </style>
    </head>
    <body>
        <div class="login-container">
            <div class="logo">
                <h1>SecureBank</h1>
                <p>Enterprise Banking Portal</p>
            </div>
            
            <form method="POST">
                <div class="form-group">
                    <label for="username">Username</label>
                    <input type="text" id="username" name="username" placeholder="Enter your username" value="{{ request.form.get('username', '') }}" required>
                </div>
                
                <div class="form-group">
                    <label for="password">Password</label>
                    <input type="password" id="password" name="password" placeholder="Enter your password" value="{{ request.form.get('password', '') }}" required>
                </div>
                
                <button type="submit" class="login-btn">Login</button>
            </form>
            
            {% if error %}
            <div class="error {% if 'Database' in error %}database-error{% endif %}">
                {% if 'Database' in error %}
                    <strong>SYSTEM ERROR</strong>
                    <div style="margin-top: 10px; font-size: 14px;">{{ error }}</div>
                {% else %}
                    <strong>ACCESS DENIED</strong>
                    <div style="margin-top: 8px;">{{ error }}</div>
                {% endif %}
            </div>
            {% endif %}
            
            {% if login_success and result %}
            <div class="success">
                <h3>Login Successful!</h3>
                <p>Welcome to SecureBank Portal</p>
                {% for row in result %}
                <div class="user-card">
                    <strong>User:</strong> {{ row.username }}<br>
                    <strong>Profile:</strong> {{ row.bio }}
                </div>
                {% endfor %}
            </div>
            {% endif %}
        </div>
    </body>
    </html>
    ''', result=result, error=error, login_success=login_success, request=request)

@app.route('/challenge2')
def xss_challenge():
    """
    INTENTIONALLY VULNERABLE: Reflected XSS Challenge
    This endpoint reflects user input without proper sanitization
    """
    query = request.args.get('q', '')
    
    # VULNERABILITY: Direct inclusion of user input without sanitization
    # This allows XSS attacks through the 'q' parameter
    
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Search Portal</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: #000000;
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }
            
            .search-container {
                background: #1a1a1a;
                border-radius: 20px;
                padding: 40px;
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
                width: 100%;
                max-width: 600px;
                border: 1px solid #333;
            }
            
            .logo {
                text-align: center;
                margin-bottom: 30px;
            }
            
            .logo h1 {
                color: #fff;
                font-size: 28px;
                font-weight: 700;
                margin-bottom: 5px;
            }
            
            .logo p {
                color: #ccc;
                font-size: 14px;
            }
            
            .search-form {
                margin-bottom: 25px;
                display: flex;
                gap: 10px;
            }
            
            .search-form input {
                flex: 1;
                padding: 15px 20px;
                border: 2px solid #444;
                border-radius: 12px;
                font-size: 16px;
                transition: all 0.3s ease;
                background: #2a2a2a;
                color: #fff;
            }
            
            .search-form input:focus {
                outline: none;
                border-color: #666;
                background: #333;
                box-shadow: 0 0 0 3px rgba(102, 102, 102, 0.1);
            }
            
            .search-btn {
                padding: 15px 25px;
                background: #333;
                color: white;
                border: 2px solid #555;
                border-radius: 12px;
                font-size: 16px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s ease;
            }
            
            .search-btn:hover {
                background: #444;
                border-color: #666;
            }
            
            .results {
                background: #2a2a2a;
                padding: 20px;
                border-radius: 12px;
                margin: 20px 0;
                border: 2px solid #444;
                color: #fff;
            }
            
            .results h3 {
                margin-bottom: 15px;
                color: #fff;
            }
            
            .results p {
                color: #ccc;
            }
            
            .hidden-flag {
                display: none;
                background: #2a2a2a;
                padding: 20px;
                border-radius: 12px;
                margin: 20px 0;
                border: 2px solid #4a4a4a;
                color: #fff;
                text-align: center;
            }
        </style>
    </head>
    <body>
        <div class="search-container">
            <div class="logo">
                <h1>Search Portal</h1>
                <p>Advanced Search System</p>
            </div>
            
            <form method="GET" class="search-form">
                    <input type="text" name="q" placeholder="Enter your search query..." value="{{ query }}">
                <button type="submit" class="search-btn">Search</button>
                </form>
            
            {% if query %}
            <div class="results">
                <h3>Search Results for: {{ query|safe }}</h3>
                <p>No results found for your query. Please try a different search term.</p>
            </div>
            {% endif %}
            
            <!-- Hidden flag that can be revealed through XSS -->
            <div class="hidden-flag" id="flag-container">
                <p><strong>FLAG:</strong> flag{n4dale_mo_boi!}</p>
            </div>
        </div>
        
        <script>
            var _0xa1b2c3 = ['flag-container', 'style', 'display', 'block', '#2a2a2a', '20px', '2px solid #4CAF50', '12px', '#4CAF50'];
            var _0xd4e5f6 = function(_0x123456) {
                var _0x789abc = document['getElementById'](_0xa1b2c3[0]);
                if (_0x789abc) {
                    _0x789abc[_0xa1b2c3[1]][_0xa1b2c3[2]] = _0xa1b2c3[3];
                    _0x789abc[_0xa1b2c3[1]]['background'] = _0xa1b2c3[4];
                    _0x789abc[_0xa1b2c3[1]]['padding'] = _0xa1b2c3[5];
                    _0x789abc[_0xa1b2c3[1]]['border'] = _0xa1b2c3[6];
                    _0x789abc[_0xa1b2c3[1]]['borderRadius'] = _0xa1b2c3[7];
                    _0x789abc[_0xa1b2c3[1]]['color'] = _0xa1b2c3[8];
                }
            };
            
            document['addEventListener']('DOMContentLoaded', function() {
                var _0xabc123 = new URLSearchParams(window['location']['search']);
                var _0xdef456 = _0xabc123['get']('q');
                if (_0xdef456 && (_0xdef456['includes']('<script>') || _0xdef456['includes']('&lt;script&gt;'))) {
                    setTimeout(_0xd4e5f6, 500);
                }
            });
            
            var _0x987654 = window['alert'];
            window['alert'] = function(_0x654321) {
                _0xd4e5f6();
                _0x987654(_0x654321);
            };
        </script>
    </body>
    </html>
    ''', query=query)

def init_db_if_needed():
    """Initialize database if it doesn't exist (for Railway/cloud deployments)"""
    if not os.path.exists(DATABASE):
        print("Database not found. Initializing...")
        import subprocess
        try:
            subprocess.run(['python', 'seed_db.py'], check=True)
            print("Database initialized successfully!")
        except subprocess.CalledProcessError as e:
            print(f"Failed to initialize database: {e}")
            # Try to create a minimal database as fallback
            create_minimal_db()

def create_minimal_db():
    """Create minimal database as fallback"""
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                bio TEXT
            )
        ''')
        
        users_data = [
            ('alice', 'password123', 'Regular user Alice - loves cats and coding'),
            ('bob', 'secret456', 'Bob from accounting - enjoys fishing on weekends'),
            ('admin', 'super_secure_admin_pass_2025', 'Administrator account - flag{h4ck3r_yarns?}')
        ]
        
        cursor.executemany(
            'INSERT INTO users (username, password, bio) VALUES (?, ?, ?)',
            users_data
        )
        
        conn.commit()
        conn.close()
        print("Minimal database created successfully!")
        
    except Exception as e:
        print(f"Failed to create minimal database: {e}")

# Initialize database on module load for production deployments
try:
    if not os.path.exists(DATABASE):
        logger.info("Database not found. Creating minimal database...")
        create_minimal_db()
        logger.info("Database initialization completed")
    else:
        logger.info(f"Database {DATABASE} already exists")
except Exception as e:
    logger.error(f"Database initialization failed: {e}")
    # Continue anyway, app might still work

if __name__ == '__main__':
    # Get port from environment variable (Railway, Heroku, etc.) or default to 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
