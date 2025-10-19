#!/usr/bin/env python3
"""
CTF Vulnerability Suite - Educational Flask Application
WARNING: Contains intentional security vulnerabilities for educational purposes only!
DO NOT deploy in production or expose to the internet.
"""

import sqlite3
import os
from flask import Flask, request, render_template_string, jsonify

app = Flask(__name__)

# Database configuration
DATABASE = 'ctf_database.db'

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    """Main landing page"""
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>CTF Vulnerability Suite</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #333; text-align: center; }
            .challenge { background: #e8f4fd; padding: 20px; margin: 20px 0; border-radius: 5px; border-left: 4px solid #007acc; }
            .warning { background: #fff3cd; padding: 15px; margin: 20px 0; border-radius: 5px; border-left: 4px solid #ffc107; color: #856404; }
            a { color: #007acc; text-decoration: none; font-weight: bold; }
            a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚨 CTF Vulnerability Suite 🚨</h1>
            
            <div class="warning">
                <strong>⚠️ EDUCATIONAL USE ONLY ⚠️</strong><br>
                This application contains intentional security vulnerabilities for CTF training purposes.
                Do not deploy in production or expose to the internet!
            </div>
            
            <div class="challenge">
                <h3>Challenge 1: SQL Injection</h3>
                <p>Test your SQL injection skills on our "very secure" login page.</p>
                <a href="/login/challenge1">🎯 Access Challenge 1</a>
            </div>
            
            <div class="challenge">
                <h3>Challenge 2: Cross-Site Scripting (XSS)</h3>
                <p>Find and exploit the reflected XSS vulnerability.</p>
                <a href="/challenge2">🎯 Access Challenge 2</a>
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
    
    if request.method == 'POST':
        user = request.form.get('user', '')
        
        if user:
            try:
                conn = get_db_connection()
                # VULNERABILITY: Direct string interpolation in SQL query
                # This allows SQL injection attacks
                query = f"SELECT username, bio FROM users WHERE username = '{user}'"
                
                print(f"[DEBUG] Executing query: {query}")  # For educational purposes
                
                cursor = conn.execute(query)
                result = cursor.fetchall()
                conn.close()
                
            except sqlite3.Error as e:
                error = f"Database error: {str(e)}"
    
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Very Secured Login Page</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #333; text-align: center; margin-bottom: 30px; }
            .form-group { margin: 20px 0; }
            label { display: block; margin-bottom: 5px; font-weight: bold; }
            input[type="text"] { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; }
            button { background: #007acc; color: white; padding: 12px 24px; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; }
            button:hover { background: #005a9e; }
            .result { background: #d4edda; padding: 15px; margin: 20px 0; border-radius: 4px; border: 1px solid #c3e6cb; }
            .error { background: #f8d7da; padding: 15px; margin: 20px 0; border-radius: 4px; border: 1px solid #f5c6cb; color: #721c24; }
            .hint { background: #e2e3e5; padding: 15px; margin: 20px 0; border-radius: 4px; font-size: 14px; }
            .back-link { margin-top: 20px; }
            .back-link a { color: #007acc; text-decoration: none; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔒 A Very Secured Login Page 🔒</h1>
            
            <form method="POST">
                <div class="form-group">
                    <label for="user">Username:</label>
                    <input type="text" id="user" name="user" placeholder="Enter your username" value="{{ request.form.get('user', '') }}">
                </div>
                <button type="submit">Login</button>
            </form>
            
            {% if error %}
            <div class="error">{{ error }}</div>
            {% endif %}
            
            {% if result %}
            <div class="result">
                <h3>Login Results:</h3>
                {% for row in result %}
                <p><strong>User:</strong> {{ row.username }}</p>
                <p><strong>Bio:</strong> {{ row.bio }}</p>
                <hr>
                {% endfor %}
            </div>
            {% endif %}
            
            <div class="hint">
                <strong>💡 Hint:</strong> Try different usernames like 'alice', 'bob', or maybe something more creative...
                What happens if you use special characters? 🤔
            </div>
            
            <div class="back-link">
                <a href="/">← Back to Main Page</a>
            </div>
        </div>
    </body>
    </html>
    ''', result=result, error=error, request=request)

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

if __name__ == '__main__':
    # Initialize database on startup
    if not os.path.exists(DATABASE):
        print("Database not found. Please run 'python seed_db.py' first.")
        exit(1)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
