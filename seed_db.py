#!/usr/bin/env python3
"""
Database Seeding Script for CTF Vulnerability Suite
Creates and populates the SQLite database with test data including flags.
"""

import sqlite3
import os

DATABASE = 'ctf_database.db'

def create_database():
    """Create and seed the CTF database"""
    
    # Remove existing database if it exists
    if os.path.exists(DATABASE):
        os.remove(DATABASE)
        print(f"Removed existing database: {DATABASE}")
    
    # Create new database connection
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    print(f"Creating database: {DATABASE}")
    
    # Create users table
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            bio TEXT
        )
    ''')
    
    # Insert seed data
    users_data = [
        ('alice', 'password123', 'Regular user Alice - loves cats and coding'),
        ('bob', 'secret456', 'Bob from accounting - enjoys fishing on weekends'),
        ('admin', 'super_secure_admin_pass_2025', 'Administrator account - flag{sql_injection_mastery_2025}')
    ]
    
    cursor.executemany(
        'INSERT INTO users (username, password, bio) VALUES (?, ?, ?)',
        users_data
    )
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    
    print("Database seeded successfully!")
    print("\nSeeded users:")
    print("- alice (password: password123)")
    print("- bob (password: secret456)")
    print("- admin (password: super_secure_admin_pass_2025) [Contains SQL injection flag]")
    print("\nDatabase is ready for CTF challenges!")

def verify_database():
    """Verify the database was created correctly"""
    if not os.path.exists(DATABASE):
        print(f"Error: Database {DATABASE} not found!")
        return False
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]
        print(f"\nVerification: Found {count} users in database")
        
        cursor.execute("SELECT username, bio FROM users")
        users = cursor.fetchall()
        
        print("\nUsers in database:")
        for username, bio in users:
            print(f"- {username}: {bio[:50]}{'...' if len(bio) > 50 else ''}")
        
        conn.close()
        return True
        
    except sqlite3.Error as e:
        print(f"Database verification failed: {e}")
        conn.close()
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("CTF Vulnerability Suite - Database Seeder")
    print("=" * 60)
    
    create_database()
    
    if verify_database():
        print("\n✅ Database setup completed successfully!")
        print("\n⚠️  SECURITY WARNING:")
        print("This database contains intentional vulnerabilities for educational purposes.")
        print("Do not use in production environments!")
    else:
        print("\n❌ Database setup failed!")
        exit(1)
