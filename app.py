from flask import Flask, render_template, request, redirect, url_for, session, send_file
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'


# ---------------- LOGIN ----------------
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == 'admin' and password == 'admin123':
            session['user'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid credentials')

    return render_template('login.html')


# ---------------- DASHBOARD ----------------
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))

    return render_template(
        'index.html',
        total_files=3,
        duplicate_count=0,
        storage_used=0.07
    )


# ---------------- SEARCH ----------------
@app.route('/search')
def search():
    if 'user' not in session:
        return redirect(url_for('login'))

    files = ['report.txt', 'data.csv', 'notes.docx']
    query = request.args.get('q', '')

    results = [f for f in files if query.lower() in f.lower()] if query else []

    return render_template('search.html', query=query, results=results)


# ---------------- ANALYTICS ----------------
@app.route('/analytics')
def analytics():
    if 'user' not in session:
        return redirect(url_for('login'))

    return render_template('analytics.html')


# ---------------- AI ASSISTANT ----------------
@app.route('/assistant', methods=['GET', 'POST'])
def assistant():
    if 'user' not in session:
        return redirect(url_for('login'))

    answer = ''

    if request.method == 'POST':
        question = request.form.get('question', '').lower()

        if 'how many files' in question:
            answer = 'There are 3 files in the system.'
        elif 'duplicate' in question:
            answer = 'No duplicate files were found.'
        elif 'storage' in question:
            answer = 'Storage used is 0.07 KB.'
        else:
            answer = 'I am your AI assistant. Try asking about files, duplicates, or storage.'

    return render_template('assistant.html', answer=answer)


# ---------------- DOWNLOAD REPORT ----------------
@app.route('/download-report')
def download_report():
    if 'user' not in session:
        return redirect(url_for('login'))

    report_path = 'report.txt'

    with open(report_path, 'w') as f:
        f.write('AI Powered File Analytics Report\n')
        f.write('--------------------------------\n')
        f.write('Total Files: 3\n')
        f.write('Duplicate Files: 0\n')
        f.write('Storage Used: 0.07 KB\n')

    return send_file(report_path, as_attachment=True)


# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


# ---------------- RENDER DEPLOYMENT ----------------
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)