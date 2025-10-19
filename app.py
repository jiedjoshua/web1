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
                        error = "❌ Login Unsuccessful - Invalid username or password combination"
                else:
                    error = "❌ Login Unsuccessful - No matching user found in database"
                
            except sqlite3.Error as e:
                # Show detailed database errors (helpful for SQL injection learning)
                error_msg = str(e)
                if "syntax error" in error_msg.lower():
                    error = f"🚨 Database Syntax Error: {error_msg}"
                elif "no such column" in error_msg.lower():
                    error = f"🚨 Database Schema Error: {error_msg}"
                elif "unrecognized token" in error_msg.lower():
                    error = f"🚨 Database Token Error: {error_msg}"
                else:
                    error = f"🚨 Database Error: {error_msg}"
                
                # Also log the failed query for educational purposes
                print(f"[ERROR] SQL Error with query: {query}")
                print(f"[ERROR] Error details: {error_msg}")
        else:
            if not username and not password:
                error = "❌ Login Unsuccessful - Username and password are required"
            elif not username:
                error = "❌ Login Unsuccessful - Username field cannot be empty"
            elif not password:
                error = "❌ Login Unsuccessful - Password field cannot be empty"
    
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
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }
            
            .login-container {
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(10px);
                border-radius: 20px;
                padding: 40px;
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
                width: 100%;
                max-width: 450px;
                border: 1px solid rgba(255, 255, 255, 0.2);
            }
            
            .logo {
                text-align: center;
                margin-bottom: 30px;
            }
            
            .logo h1 {
                color: #333;
                font-size: 28px;
                font-weight: 700;
                margin-bottom: 5px;
            }
            
            .logo p {
                color: #666;
                font-size: 14px;
            }
            
            .form-group {
                margin-bottom: 25px;
                position: relative;
            }
            
            .form-group label {
                display: block;
                margin-bottom: 8px;
                color: #333;
                font-weight: 600;
                font-size: 14px;
            }
            
            .form-group input {
                width: 100%;
                padding: 15px 20px;
                border: 2px solid #e1e5e9;
                border-radius: 12px;
                font-size: 16px;
                transition: all 0.3s ease;
                background: #f8f9fa;
            }
            
            .form-group input:focus {
                outline: none;
                border-color: #667eea;
                background: white;
                box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
            }
            
            .login-btn {
                width: 100%;
                padding: 15px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                border-radius: 12px;
                font-size: 16px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s ease;
                margin-bottom: 20px;
            }
            
            .login-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
            }
            
            .success {
                background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                color: white;
                padding: 20px;
                border-radius: 12px;
                margin: 20px 0;
                text-align: center;
            }
            
            .success h3 {
                margin-bottom: 15px;
                font-size: 20px;
            }
            
            .user-card {
                background: rgba(255, 255, 255, 0.2);
                padding: 15px;
                border-radius: 8px;
                margin: 10px 0;
                border-left: 4px solid #00f2fe;
            }
            
            .error {
                background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
                color: white;
                padding: 20px;
                border-radius: 12px;
                margin: 20px 0;
                text-align: center;
                border: 2px solid rgba(255, 107, 107, 0.5);
                box-shadow: 0 10px 25px rgba(255, 107, 107, 0.3);
                animation: shake 0.5s ease-in-out;
            }
            
            .error strong {
                display: block;
                font-size: 18px;
                margin-bottom: 8px;
            }
            
            .database-error {
                background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
                border: 2px solid rgba(231, 76, 60, 0.5);
                font-family: 'Courier New', monospace;
                text-align: left;
            }
            
            @keyframes shake {
                0%, 100% { transform: translateX(0); }
                25% { transform: translateX(-5px); }
                75% { transform: translateX(5px); }
            }
            
            .hint-box {
                background: linear-gradient(135deg, #feca57 0%, #ff9ff3 100%);
                color: #333;
                padding: 20px;
                border-radius: 12px;
                margin: 25px 0;
                border-left: 4px solid #ff6b6b;
            }
            
            .hint-box h4 {
                margin-bottom: 10px;
                color: #2c2c2c;
            }
            
            .injection-examples {
                background: #2c3e50;
                color: #ecf0f1;
                padding: 15px;
                border-radius: 8px;
                margin: 15px 0;
                font-family: 'Courier New', monospace;
                font-size: 14px;
            }
            
            .injection-examples h5 {
                color: #e74c3c;
                margin-bottom: 10px;
            }
            
            .payload {
                background: rgba(231, 76, 60, 0.1);
                padding: 8px;
                border-radius: 4px;
                margin: 5px 0;
                border-left: 3px solid #e74c3c;
            }
            
            .back-link {
                text-align: center;
                margin-top: 25px;
            }
            
            .back-link a {
                color: #667eea;
                text-decoration: none;
                font-weight: 600;
                transition: all 0.3s ease;
            }
            
            .back-link a:hover {
                color: #764ba2;
            }
            
            .security-badge {
                display: inline-block;
                background: #27ae60;
                color: white;
                padding: 5px 12px;
                border-radius: 20px;
                font-size: 12px;
                font-weight: 600;
                margin-left: 10px;
            }
        </style>
    </head>
    <body>
        <div class="login-container">
            <div class="logo">
                <h1>🏦 SecureBank</h1>
                <p>Enterprise Banking Portal <span class="security-badge">🔒 SECURED</span></p>
            </div>
            
            <form method="POST">
                <div class="form-group">
                    <label for="username">👤 Username</label>
                    <input type="text" id="username" name="username" placeholder="Enter your username" value="{{ request.form.get('username', '') }}" required>
                </div>
                
                <div class="form-group">
                    <label for="password">🔑 Password</label>
                    <input type="password" id="password" name="password" placeholder="Enter your password" value="{{ request.form.get('password', '') }}" required>
                </div>
                
                <button type="submit" class="login-btn">🚀 Secure Login</button>
            </form>
            
            {% if error %}
            <div class="error {% if 'Database' in error %}database-error{% endif %}">
                {% if 'Database' in error %}
                    <strong>🚨 SYSTEM ERROR</strong>
                    <div style="margin-top: 10px; font-size: 14px;">{{ error }}</div>
                    <div style="margin-top: 10px; font-size: 12px; opacity: 0.8;">
                        💡 This error might reveal information about the database structure...
                    </div>
                {% else %}
                    <strong>🔒 ACCESS DENIED</strong>
                    <div style="margin-top: 8px;">{{ error }}</div>
                    <div style="margin-top: 10px; font-size: 14px; opacity: 0.9;">
                        🛡️ SecureBank Authentication System
                    </div>
                {% endif %}
            </div>
            {% endif %}
            
            {% if login_success and result %}
            <div class="success">
                <h3>✅ Login Successful!</h3>
                <p>Welcome to SecureBank Portal</p>
                {% for row in result %}
                <div class="user-card">
                    <strong>👤 User:</strong> {{ row.username }}<br>
                    <strong>📝 Profile:</strong> {{ row.bio }}
                </div>
                {% endfor %}
            </div>
            {% endif %}
            
            <div class="hint-box">
                <h4>🎯 Challenge Instructions</h4>
                <p><strong>Goal:</strong> Bypass the authentication system without knowing valid credentials!</p>
                <p><strong>Current Status:</strong> Normal login attempts with wrong passwords will fail.</p>
                
                <div class="injection-examples">
                    <h5>💉 Try these SQL injection payloads:</h5>
                    <div class="payload">Username: admin" OR 1=1 --</div>
                    <div class="payload">Username: " OR "1"="1" --</div>
                    <div class="payload">Username: admin" OR "a"="a</div>
                    <div class="payload">Password: anything (when using above)</div>
                </div>
                
                <p><strong>💡 How it works:</strong> The login checks if username AND password match. 
                But SQL injection can make the WHERE clause return multiple rows or always be true, 
                bypassing the authentication logic!</p>
                
                <p><strong>🔍 Test it:</strong> Try "admin" + "wrongpassword" first (should fail), 
                then try the SQL injection payloads above!</p>
            </div>
            
            <div class="back-link">
                <a href="/">← Back to Challenge Hub</a>
            </div>
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
        <title>Search Results - XSS Challenge</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #333; text-align: center; }
            .search-box { margin: 20px 0; }
            .search-box input { width: 70%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; }
            .search-box button { padding: 10px 20px; background: #007acc; color: white; border: none; border-radius: 4px; cursor: pointer; }
            .results { background: #f8f9fa; padding: 20px; margin: 20px 0; border-radius: 4px; }
            .hint { background: #e2e3e5; padding: 15px; margin: 20px 0; border-radius: 4px; font-size: 14px; }
            .back-link { margin-top: 20px; }
            .back-link a { color: #007acc; text-decoration: none; }
            .hidden-flag { display: none; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔍 Advanced Search Portal</h1>
            
            <div class="search-box">
                <form method="GET">
                    <input type="text" name="q" placeholder="Enter your search query..." value="{{ query }}">
                    <button type="submit">Search</button>
                </form>
            </div>
            
            {% if query %}
            <div class="results">
                <h3>Search Results for: {{ query|safe }}</h3>
                <p>No results found for your query. Please try a different search term.</p>
            </div>
            {% endif %}
            
            <div class="hint">
                <strong>💡 Hint:</strong> This search function reflects your input directly into the page. 
                Try entering some HTML or JavaScript in the search box. What happens?<br>
                <strong>🎯 Goal:</strong> Execute JavaScript to reveal the hidden flag in the DOM!
            </div>
            
            <!-- Hidden flag that can be revealed through XSS -->
            <div class="hidden-flag" id="flag-container">
                <p><strong>🚩 FLAG:</strong> flag{xss_expert_2025}</p>
            </div>
            
            <div class="back-link">
                <a href="/">← Back to Main Page</a>
            </div>
        </div>
        
        <script>
            // Function to reveal flag (can be called via XSS)
            function revealFlag() {
                document.getElementById('flag-container').style.display = 'block';
                document.getElementById('flag-container').style.background = '#d4edda';
                document.getElementById('flag-container').style.padding = '15px';
                document.getElementById('flag-container').style.border = '2px solid #28a745';
                document.getElementById('flag-container').style.borderRadius = '4px';
            }
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
            ('admin', 'super_secure_admin_pass_2025', 'Administrator account - flag{sql_injection_mastery_2025}')
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
