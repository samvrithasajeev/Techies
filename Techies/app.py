from flask import Flask, render_template, request, jsonify, session, redirect
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3, os, random, string, smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from functools import wraps

app = Flask(__name__)
app.secret_key = 'smartbudget_secret_2024'
DB = os.path.join(os.path.dirname(__file__), 'budget.db')

# ─────────────────────────────────────────────────────────
# !! CHANGE THESE TO YOUR GMAIL CREDENTIALS !!
# Go to Google Account → Security → App Passwords → Generate
# Use that 16-character app password below (not your real Gmail password)
# ─────────────────────────────────────────────────────────
GMAIL_USER = 'anamikalilly2005@gmail.com'
GMAIL_PASS = 'tcwy xivd ccbw ppce'
# ─────────────────────────────────────────────────────────

# In-memory OTP store: { email: { otp, expires } }
otp_store = {}

# ─── DATABASE ────────────────────────────────────────────
def db():
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    c.execute("PRAGMA foreign_keys=ON")
    return c

def init_db():
    with db() as c:
        c.executescript("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS budgets(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER, month TEXT, monthly_budget REAL DEFAULT 0,
            UNIQUE(user_id, month),
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
        );
        CREATE TABLE IF NOT EXISTS categories(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER, name TEXT,
            opening_balance REAL DEFAULT 0, month TEXT,
            created_at TEXT DEFAULT(datetime('now')),
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
        );
        CREATE TABLE IF NOT EXISTS transactions(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER, category_id INTEGER,
            type TEXT CHECK(type IN('income','expense')),
            amount REAL, reason TEXT DEFAULT '', date TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY(category_id) REFERENCES categories(id) ON DELETE CASCADE
        );
        """)

# ─── DECORATORS ──────────────────────────────────────────
def login_required(f):
    @wraps(f)
    def dec(*a, **k):
        if 'uid' not in session:
            if request.path.startswith('/api/'):
                return jsonify({'error': 'Unauthorized'}), 401
            return redirect('/')
        return f(*a, **k)
    return dec

def guest_only(f):
    @wraps(f)
    def dec(*a, **k):
        if 'uid' in session:
            return redirect('/dashboard')
        return f(*a, **k)
    return dec

# ─── EMAIL HELPER ─────────────────────────────────────────
def send_otp_email(to_email, otp, name):
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = 'BudgetSmart — Your Password Reset OTP'
        msg['From']    = GMAIL_USER
        msg['To']      = to_email

        html = f"""
        <div style="font-family:Arial,sans-serif;max-width:480px;margin:0 auto;background:#0f172a;color:#e2e8f0;border-radius:16px;overflow:hidden">
          <div style="background:linear-gradient(135deg,#059669,#10b981);padding:28px 32px;text-align:center">
            <div style="font-size:2.5rem">₹</div>
            <h1 style="margin:8px 0 4px;font-size:1.4rem;color:#fff">BudgetSmart</h1>
            <p style="color:#d1fae5;font-size:.9rem;margin:0">Password Reset Request</p>
          </div>
          <div style="padding:32px">
            <p style="margin:0 0 12px">Hi <strong>{name}</strong>,</p>
            <p style="margin:0 0 20px;color:#94a3b8">We received a request to reset your password. Use the OTP below to continue. It expires in <strong style="color:#fcd34d">10 minutes</strong>.</p>
            <div style="background:#1e293b;border:1px solid rgba(16,185,129,.3);border-radius:12px;padding:20px;text-align:center;margin:0 0 20px">
              <p style="margin:0 0 6px;font-size:.8rem;color:#94a3b8;text-transform:uppercase;letter-spacing:.08em">Your OTP</p>
              <div style="font-size:2.2rem;font-weight:800;letter-spacing:.3em;color:#10b981">{otp}</div>
            </div>
            <p style="margin:0;font-size:.82rem;color:#64748b">If you did not request this, you can safely ignore this email. Do not share this OTP with anyone.</p>
          </div>
        </div>
        """
        msg.attach(MIMEText(html, 'html'))

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(GMAIL_USER, GMAIL_PASS)
            smtp.sendmail(GMAIL_USER, to_email, msg.as_string())
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False

# ─── PAGE ROUTES ─────────────────────────────────────────
@app.route('/')
@guest_only
def index():
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user={
        'name':  session['uname'],
        'email': session['uemail'],
        'id':    session['uid']
    })

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# ─── AUTH API ─────────────────────────────────────────────
@app.route('/api/register', methods=['POST'])
def register():
    d     = request.get_json()
    name  = (d.get('name') or '').strip()
    email = (d.get('email') or '').strip().lower()
    pwd   = d.get('password') or ''
    if not name:     return jsonify({'error': 'Name is required.'})
    if not email:    return jsonify({'error': 'Email is required.'})
    if len(pwd) < 6: return jsonify({'error': 'Password must be at least 6 characters.'})
    try:
        with db() as c:
            cur = c.execute("INSERT INTO users(name,email,password) VALUES(?,?,?)",
                            (name, email, generate_password_hash(pwd)))
            uid = cur.lastrowid
        session.clear()
        session['uid']    = uid
        session['uname']  = name
        session['uemail'] = email
        return jsonify({'success': True, 'redirect': '/dashboard'})
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Email already registered.'})

@app.route('/api/login', methods=['POST'])
def login():
    d     = request.get_json()
    email = (d.get('email') or '').strip().lower()
    pwd   = d.get('password') or ''
    if not email or not pwd:
        return jsonify({'error': 'Email and password required.'})
    with db() as c:
        u = c.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
    if not u or not check_password_hash(u['password'], pwd):
        return jsonify({'error': 'Invalid email or password.'})
    session.clear()
    session['uid']    = u['id']
    session['uname']  = u['name']
    session['uemail'] = u['email']
    return jsonify({'success': True, 'redirect': '/dashboard'})

# ─── FORGOT PASSWORD API ──────────────────────────────────
@app.route('/api/forgot-password', methods=['POST'])
def forgot_password():
    d     = request.get_json()
    email = (d.get('email') or '').strip().lower()
    if not email:
        return jsonify({'error': 'Email is required.'})
    with db() as c:
        u = c.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
    if not u:
        # Don't reveal if email exists — show generic message
        return jsonify({'success': True, 'message': 'If this email is registered, an OTP has been sent.'})

    # Generate 6-digit OTP
    otp = ''.join(random.choices(string.digits, k=6))
    otp_store[email] = {
        'otp':     otp,
        'expires': datetime.now() + timedelta(minutes=10),
        'name':    u['name']
    }

    sent = send_otp_email(email, otp, u['name'])
    if not sent:
        return jsonify({'error': 'Failed to send email. Check server Gmail config.'})

    return jsonify({'success': True, 'message': 'OTP sent to your email. Check your inbox.'})

@app.route('/api/verify-otp', methods=['POST'])
def verify_otp():
    d     = request.get_json()
    email = (d.get('email') or '').strip().lower()
    otp   = (d.get('otp') or '').strip()
    if not email or not otp:
        return jsonify({'error': 'Email and OTP are required.'})
    record = otp_store.get(email)
    if not record:
        return jsonify({'error': 'No OTP found. Please request a new one.'})
    if datetime.now() > record['expires']:
        otp_store.pop(email, None)
        return jsonify({'error': 'OTP has expired. Please request a new one.'})
    if record['otp'] != otp:
        return jsonify({'error': 'Incorrect OTP. Please try again.'})
    return jsonify({'success': True, 'message': 'OTP verified.'})

@app.route('/api/reset-password', methods=['POST'])
def reset_password():
    d        = request.get_json()
    email    = (d.get('email') or '').strip().lower()
    otp      = (d.get('otp') or '').strip()
    new_pwd  = d.get('password') or ''

    if not email or not otp or not new_pwd:
        return jsonify({'error': 'All fields are required.'})
    if len(new_pwd) < 6:
        return jsonify({'error': 'Password must be at least 6 characters.'})

    record = otp_store.get(email)
    if not record:
        return jsonify({'error': 'Session expired. Please start again.'})
    if datetime.now() > record['expires']:
        otp_store.pop(email, None)
        return jsonify({'error': 'OTP expired. Please start again.'})
    if record['otp'] != otp:
        return jsonify({'error': 'Invalid OTP.'})

    with db() as c:
        c.execute("UPDATE users SET password=? WHERE email=?",
                  (generate_password_hash(new_pwd), email))
    otp_store.pop(email, None)
    return jsonify({'success': True, 'message': 'Password reset successful. You can now log in.'})

# ─── BUDGET API ───────────────────────────────────────────
@app.route('/api/budget', methods=['GET'])
@login_required
def get_budget():
    month = request.args.get('month', datetime.now().strftime('%Y-%m'))
    with db() as c:
        r = c.execute("SELECT monthly_budget FROM budgets WHERE user_id=? AND month=?",
                      (session['uid'], month)).fetchone()
    return jsonify({'monthly_budget': r['monthly_budget'] if r else 0})

@app.route('/api/budget', methods=['POST'])
@login_required
def save_budget():
    d      = request.get_json()
    month  = (d.get('month') or '').strip()
    budget = float(d.get('monthly_budget', 0) or 0)
    if not month: return jsonify({'error': 'Month required.'})
    with db() as c:
        c.execute("""INSERT INTO budgets(user_id,month,monthly_budget) VALUES(?,?,?)
                     ON CONFLICT(user_id,month) DO UPDATE SET monthly_budget=excluded.monthly_budget""",
                  (session['uid'], month, budget))
    return jsonify({'success': True, 'monthly_budget': budget})

# ─── CATEGORIES API ───────────────────────────────────────
@app.route('/api/categories', methods=['GET'])
@login_required
def get_categories():
    month = request.args.get('month', datetime.now().strftime('%Y-%m'))
    with db() as c:
        rows = c.execute(
            "SELECT * FROM categories WHERE user_id=? AND month=? ORDER BY created_at ASC",
            (session['uid'], month)).fetchall()
    return jsonify({'categories': [dict(r) for r in rows]})

@app.route('/api/categories', methods=['POST'])
@login_required
def add_category():
    d       = request.get_json()
    name    = (d.get('name') or '').strip()
    month   = (d.get('month') or '').strip()
    opening = float(d.get('opening_balance', 0) or 0)
    if not name:  return jsonify({'error': 'Name required.'})
    if not month: return jsonify({'error': 'Month required.'})
    with db() as c:
        cur = c.execute(
            "INSERT INTO categories(user_id,name,opening_balance,month) VALUES(?,?,?,?)",
            (session['uid'], name, opening, month))
    return jsonify({'success': True, 'id': cur.lastrowid})

@app.route('/api/categories/<int:cid>', methods=['PUT'])
@login_required
def edit_category(cid):
    d       = request.get_json()
    name    = (d.get('name') or '').strip()
    opening = float(d.get('opening_balance', 0) or 0)
    if not name: return jsonify({'error': 'Name required.'})
    with db() as c:
        c.execute("UPDATE categories SET name=?,opening_balance=? WHERE id=? AND user_id=?",
                  (name, opening, cid, session['uid']))
    return jsonify({'success': True})

@app.route('/api/categories/<int:cid>', methods=['DELETE'])
@login_required
def delete_category(cid):
    with db() as c:
        c.execute("DELETE FROM categories WHERE id=? AND user_id=?", (cid, session['uid']))
    return jsonify({'success': True})

# ─── TRANSACTIONS API ─────────────────────────────────────
@app.route('/api/transactions', methods=['GET'])
@login_required
def get_transactions():
    cid = request.args.get('category_id', type=int)
    if not cid: return jsonify({'error': 'category_id required.'})
    with db() as c:
        rows = c.execute(
            "SELECT * FROM transactions WHERE category_id=? AND user_id=? ORDER BY date DESC, id DESC",
            (cid, session['uid'])).fetchall()
    return jsonify({'transactions': [dict(r) for r in rows]})

@app.route('/api/transactions', methods=['POST'])
@login_required
def add_transaction():
    d      = request.get_json()
    cid    = int(d.get('category_id', 0) or 0)
    ttype  = d.get('type', '')
    amount = float(d.get('amount', 0) or 0)
    reason = (d.get('reason') or '').strip()
    date   = (d.get('date') or '').strip()
    if not cid:                            return jsonify({'error': 'Category required.'})
    if ttype not in ('income', 'expense'): return jsonify({'error': 'Invalid type.'})
    if amount <= 0:                        return jsonify({'error': 'Amount must be > 0.'})
    if not date:                           return jsonify({'error': 'Date required.'})
    with db() as c:
        cat = c.execute("SELECT id FROM categories WHERE id=? AND user_id=?",
                        (cid, session['uid'])).fetchone()
        if not cat: return jsonify({'error': 'Category not found.'})
        cur = c.execute(
            "INSERT INTO transactions(user_id,category_id,type,amount,reason,date) VALUES(?,?,?,?,?,?)",
            (session['uid'], cid, ttype, amount, reason, date))
    return jsonify({'success': True, 'id': cur.lastrowid})

@app.route('/api/transactions/<int:tid>', methods=['PUT'])
@login_required
def edit_transaction(tid):
    d      = request.get_json()
    ttype  = d.get('type', '')
    amount = float(d.get('amount', 0) or 0)
    reason = (d.get('reason') or '').strip()
    date   = (d.get('date') or '').strip()
    if ttype not in ('income', 'expense'): return jsonify({'error': 'Invalid type.'})
    if amount <= 0: return jsonify({'error': 'Amount must be > 0.'})
    if not date:    return jsonify({'error': 'Date required.'})
    with db() as c:
        c.execute("UPDATE transactions SET type=?,amount=?,reason=?,date=? WHERE id=? AND user_id=?",
                  (ttype, amount, reason, date, tid, session['uid']))
    return jsonify({'success': True})

@app.route('/api/transactions/<int:tid>', methods=['DELETE'])
@login_required
def delete_transaction(tid):
    with db() as c:
        c.execute("DELETE FROM transactions WHERE id=? AND user_id=?", (tid, session['uid']))
    return jsonify({'success': True})

# ─── SUMMARY API ──────────────────────────────────────────
@app.route('/api/summary', methods=['GET'])
@login_required
def get_summary():
    month = request.args.get('month', datetime.now().strftime('%Y-%m'))
    uid   = session['uid']
    with db() as c:
        br     = c.execute("SELECT monthly_budget FROM budgets WHERE user_id=? AND month=?",
                            (uid, month)).fetchone()
        budget = br['monthly_budget'] if br else 0
        cats   = c.execute(
            "SELECT * FROM categories WHERE user_id=? AND month=? ORDER BY created_at ASC",
            (uid, month)).fetchall()
        total_exp   = 0
        chart_data  = []
        cat_details = []
        for cat in cats:
            txns = c.execute(
                "SELECT type,amount FROM transactions WHERE category_id=? AND user_id=?",
                (cat['id'], uid)).fetchall()
            inc = sum(t['amount'] for t in txns if t['type'] == 'income')
            exp = sum(t['amount'] for t in txns if t['type'] == 'expense')
            rem = cat['opening_balance'] + inc - exp
            total_exp += exp
            chart_data.append({'name': cat['name'], 'expense': exp})
            cat_details.append({
                'id': cat['id'], 'name': cat['name'],
                'opening_balance': cat['opening_balance'],
                'remaining': rem, 'income': inc, 'expense': exp
            })
    rem_bal = budget - total_exp
    usage   = round((total_exp / budget) * 100, 1) if budget > 0 else 0
    return jsonify({
        'monthly_budget': budget, 'total_expense': total_exp,
        'remaining_balance': rem_bal, 'usage_pct': usage,
        'chart_data': chart_data, 'categories': cat_details
    })

# ─── RUN ──────────────────────────────────────────────────
if __name__ == '__main__':
    init_db()
    print("\n✅ Smart Budget Planner running!")
    print("🌐 Open: http://localhost:5000")
    print(f"📧 Sending email from: {GMAIL_USER}\n")
    app.run(debug=True, port=5000)