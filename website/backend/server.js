/**
 * VALYXO - Backend Server
 * Node.js + Express + SQLite
 * v0.31 - December 2025
 */

const express = require('express');
const sqlite3 = require('sqlite3');
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');
const cors = require('cors');
require('dotenv').config();

const app = express();
const db = new sqlite3.Database('./database.db');

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static('../'));

// JWT Secret
const JWT_SECRET = process.env.JWT_SECRET || 'valyxo-secret-key-2025';

// Initialize Database
function initDatabase() {
    db.serialize(() => {
        db.run(`
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        `);

        db.run(`
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                token TEXT UNIQUE NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                expires_at DATETIME NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        `);

        db.run(`
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                description TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        `);

        console.log('✓ Database initialized');
    });
}

// Middleware: Verify JWT
function verifyToken(req, res, next) {
    const token = req.headers.authorization?.split(' ')[1];

    if (!token) {
        return res.status(401).json({ success: false, message: 'No token provided' });
    }

    try {
        const decoded = jwt.verify(token, JWT_SECRET);
        req.user = decoded;
        next();
    } catch (error) {
        return res.status(401).json({ success: false, message: 'Invalid token' });
    }
}

// Routes: Authentication

/**
 * POST /api/auth/register
 * Register new user
 */
app.post('/api/auth/register', async (req, res) => {
    const { username, email, password } = req.body;

    // Validation
    if (!username || !email || !password) {
        return res.status(400).json({ 
            success: false, 
            message: 'Missing required fields' 
        });
    }

    if (password.length < 6) {
        return res.status(400).json({ 
            success: false, 
            message: 'Password must be at least 6 characters' 
        });
    }

    try {
        // Hash password
        const hashedPassword = await bcrypt.hash(password, 10);

        // Insert user
        db.run(
            'INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
            [username, email, hashedPassword],
            function(err) {
                if (err) {
                    if (err.message.includes('UNIQUE')) {
                        return res.status(400).json({ 
                            success: false, 
                            message: 'Username or email already exists' 
                        });
                    }
                    throw err;
                }

                res.json({ 
                    success: true, 
                    message: 'User registered successfully',
                    userId: this.lastID
                });
            }
        );
    } catch (error) {
        console.error('Registration error:', error);
        res.status(500).json({ 
            success: false, 
            message: 'Registration failed' 
        });
    }
});

/**
 * POST /api/auth/login
 * Login user and return token
 */
app.post('/api/auth/login', (req, res) => {
    const { email, password } = req.body;

    if (!email || !password) {
        return res.status(400).json({ 
            success: false, 
            message: 'Email and password required' 
        });
    }

    db.get(
        'SELECT * FROM users WHERE email = ?',
        [email],
        async (err, user) => {
            if (err) {
                return res.status(500).json({ success: false, message: 'Database error' });
            }

            if (!user) {
                return res.status(401).json({ 
                    success: false, 
                    message: 'Invalid email or password' 
                });
            }

            try {
                const validPassword = await bcrypt.compare(password, user.password);

                if (!validPassword) {
                    return res.status(401).json({ 
                        success: false, 
                        message: 'Invalid email or password' 
                    });
                }

                // Create JWT
                const token = jwt.sign(
                    { id: user.id, username: user.username, email: user.email },
                    JWT_SECRET,
                    { expiresIn: '7d' }
                );

                res.json({
                    success: true,
                    message: 'Login successful',
                    token: token,
                    user: {
                        id: user.id,
                        username: user.username,
                        email: user.email
                    }
                });
            } catch (error) {
                console.error('Login error:', error);
                res.status(500).json({ success: false, message: 'Login failed' });
            }
        }
    );
});

// Routes: User

/**
 * GET /api/user/profile
 * Get current user profile
 */
app.get('/api/user/profile', verifyToken, (req, res) => {
    db.get(
        'SELECT id, username, email, created_at FROM users WHERE id = ?',
        [req.user.id],
        (err, user) => {
            if (err) {
                return res.status(500).json({ success: false, message: 'Database error' });
            }

            if (!user) {
                return res.status(404).json({ success: false, message: 'User not found' });
            }

            res.json({ success: true, user: user });
        }
    );
});

// Routes: Projects

/**
 * GET /api/projects
 * Get user's projects
 */
app.get('/api/projects', verifyToken, (req, res) => {
    db.all(
        'SELECT * FROM projects WHERE user_id = ? ORDER BY created_at DESC',
        [req.user.id],
        (err, projects) => {
            if (err) {
                return res.status(500).json({ success: false, message: 'Database error' });
            }

            res.json({ success: true, projects: projects });
        }
    );
});

/**
 * POST /api/projects
 * Create new project
 */
app.post('/api/projects', verifyToken, (req, res) => {
    const { name, description } = req.body;

    if (!name) {
        return res.status(400).json({ success: false, message: 'Project name required' });
    }

    db.run(
        'INSERT INTO projects (user_id, name, description) VALUES (?, ?, ?)',
        [req.user.id, name, description || ''],
        function(err) {
            if (err) {
                return res.status(500).json({ success: false, message: 'Database error' });
            }

            res.json({
                success: true,
                message: 'Project created',
                projectId: this.lastID
            });
        }
    );
});

// Health Check
app.get('/api/health', (req, res) => {
    res.json({ success: true, status: 'OK', version: '0.31' });
});

// 404 Handler
app.use((req, res) => {
    res.status(404).json({ success: false, message: 'Endpoint not found' });
});

// Error Handler
app.use((err, req, res, next) => {
    console.error('Error:', err);
    res.status(500).json({ success: false, message: 'Internal server error' });
});

// Start Server
const PORT = process.env.PORT || 3000;
initDatabase();

app.listen(PORT, () => {
    console.log(`
╔════════════════════════════════════╗
║    VALYXO Backend Server v0.31     ║
║    Running on http://localhost:${PORT}    ║
╚════════════════════════════════════╝
    `);
});

module.exports = app;
