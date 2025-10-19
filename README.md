# CTF Vulnerability Suite

⚠️ **CRITICAL SECURITY WARNING** ⚠️

**DO NOT EXPOSE PUBLICLY - USE IN ISOLATED CTF ENVIRONMENT ONLY**

This application contains intentional security vulnerabilities designed for educational Capture The Flag (CTF) competitions. It should NEVER be deployed in production environments or exposed to the internet without proper isolation.

## Overview

This Flask application provides two educational web security challenges:

1. **SQL Injection Challenge** (`/login/challenge1`) - Demonstrates classic SQL injection vulnerabilities
2. **Cross-Site Scripting (XSS) Challenge** (`/challenge2`) - Shows reflected XSS vulnerabilities

## Challenges

### Challenge 1: SQL Injection
- **Endpoint**: `/login/challenge1`
- **Vulnerability**: String interpolation in SQL queries
- **Goal**: Extract the flag from the admin user's bio
- **Flag**: `flag{sql_injection_mastery_2025}`
- **Hint**: Try usernames like `alice`, `bob`, or get creative with SQL syntax

### Challenge 2: Reflected XSS
- **Endpoint**: `/challenge2`
- **Vulnerability**: Unsanitized user input reflection
- **Goal**: Execute JavaScript to reveal the hidden flag
- **Flag**: `flag{xss_expert_2025}`
- **Hint**: The flag is hidden in the DOM and can be revealed with the `revealFlag()` function

## Quick Start

### Local Development

1. **Clone and setup**:
   ```bash
   git clone <repository-url>
   cd ctf-vuln-suite
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize database**:
   ```bash
   python seed_db.py
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```

5. **Access the application**:
   - Open http://localhost:5000 in your browser
   - Navigate to the challenges from the main page

### Docker Deployment

1. **Using Docker Compose (Recommended)**:
   ```bash
   docker-compose up --build
   ```

2. **Using Docker directly**:
   ```bash
   docker build -t ctf-vuln-suite .
   docker run -p 5000:5000 ctf-vuln-suite
   ```

3. **Access the application**:
   - Open http://localhost:5000 in your browser

### Production Deployment (Heroku/Cloud)

1. **Deploy to Heroku**:
   ```bash
   heroku create your-ctf-app-name
   git push heroku main
   ```

2. **Other cloud platforms**:
   - Use the provided `Dockerfile` and `docker-compose.yml`
   - Ensure proper network isolation and access controls

## Project Structure

```
ctf-vuln-suite/
├── app.py                 # Main Flask application with vulnerable endpoints
├── seed_db.py            # Database initialization and seeding script
├── requirements.txt      # Python dependencies
├── Procfile             # Heroku deployment configuration
├── Dockerfile           # Docker container configuration
├── docker-compose.yml   # Docker Compose orchestration
├── README.md            # This file
└── .gitignore          # Git ignore patterns
```

## Database Schema

The application uses SQLite with the following structure:

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    bio TEXT
);
```

**Seeded Users**:
- `alice` (password: `password123`) - Regular user
- `bob` (password: `secret456`) - Regular user  
- `admin` (password: `super_secure_admin_pass_2025`) - Contains SQL injection flag

## Security Vulnerabilities (Educational)

### 1. SQL Injection in `/login/challenge1`
```python
# VULNERABLE CODE - DO NOT USE IN PRODUCTION
query = f"SELECT username, bio FROM users WHERE username = '{user}'"
```

**Exploitation Examples**:
- `' OR '1'='1` - Bypass authentication
- `' UNION SELECT username, bio FROM users--` - Extract all users
- `admin'--` - Target specific user

### 2. Reflected XSS in `/challenge2`
```python
# VULNERABLE CODE - DO NOT USE IN PRODUCTION  
return render_template_string('...{{ query|safe }}...', query=query)
```

**Exploitation Examples**:
- `<script>alert('XSS')</script>` - Basic XSS test
- `<script>revealFlag()</script>` - Reveal hidden flag
- `<img src=x onerror=revealFlag()>` - Alternative payload

## Educational Notes

### SQL Injection Prevention
```python
# SECURE VERSION - Use parameterized queries
cursor.execute("SELECT username, bio FROM users WHERE username = ?", (user,))
```

### XSS Prevention
```python
# SECURE VERSION - Proper escaping (remove |safe filter)
return render_template_string('...{{ query }}...', query=query)
```

## Safety Guidelines

1. **Network Isolation**: Deploy only in isolated networks
2. **Access Control**: Restrict access to authorized participants only
3. **Monitoring**: Log all access and activities
4. **Time Limits**: Use temporary deployments for CTF events
5. **Cleanup**: Remove deployments after events conclude

## Troubleshooting

### Common Issues

1. **Database not found**:
   ```bash
   python seed_db.py
   ```

2. **Port already in use**:
   ```bash
   # Change port in app.py or kill existing process
   lsof -ti:5000 | xargs kill -9
   ```

3. **Docker build fails**:
   ```bash
   docker system prune -a
   docker-compose up --build --force-recreate
   ```

### Debug Mode

For development, enable debug mode in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5000)
```

## Contributing

This is an educational project. When contributing:

1. Maintain the intentional vulnerabilities for educational purposes
2. Add clear comments marking vulnerable code sections
3. Include security warnings in all documentation
4. Test thoroughly in isolated environments

## License

This project is for educational use only. Use at your own risk and ensure proper isolation from production systems.

---

**Remember: This application is intentionally insecure. Never deploy in production or expose to untrusted networks!**
