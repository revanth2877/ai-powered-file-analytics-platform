import matplotlib
matplotlib.use('Agg')

from flask import Flask, render_template, request, send_file, redirect, url_for, session
import matplotlib.pyplot as plt
import pandas as pd
import os
import hashlib

app = Flask(__name__)
app.secret_key = 'aiml_project_secret'

SCAN_PATH = r'C:\Users\revan\OneDrive\Desktop\test files\Documents\Documents'

USERNAME = 'admin'
PASSWORD = 'admin123'

# ---------- LOGIN ----------
@app.route('/login', methods=['GET', 'POST'])
def login():

    error = ''

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        if username == USERNAME and password == PASSWORD:

            session['user'] = username
            return redirect(url_for('home'))

        else:
            error = 'Invalid username or password'

    return render_template('login.html', error=error)


@app.route('/logout')
def logout():

    session.pop('user', None)
    return redirect(url_for('login'))


# ---------- DUPLICATE DETECTION ----------
def file_hash(path):

    hasher = hashlib.md5()

    with open(path, 'rb') as f:

        while chunk := f.read(4096):
            hasher.update(chunk)

    return hasher.hexdigest()


def find_duplicates():

    hashes = {}
    duplicates = []

    for file_name in os.listdir(SCAN_PATH):

        file_path = os.path.join(SCAN_PATH, file_name)

        if os.path.isfile(file_path):

            h = file_hash(file_path)

            if h in hashes:
                duplicates.append(file_name)
            else:
                hashes[h] = file_name

    return duplicates


# ---------- SEARCH ----------
def search_files(keyword):

    results = []

    for file_name in os.listdir(SCAN_PATH):

        if keyword.lower() in file_name.lower():
            results.append(file_name)

    return results


# ---------- FILE CATEGORIES ----------
CATEGORY_MAP = {
    '.txt': 'Text',
    '.md': 'Text',
    '.pdf': 'PDF',
    '.png': 'Image',
    '.jpg': 'Image',
    '.jpeg': 'Image',
    '.py': 'Code',
    '.ipynb': 'Code',
    '.csv': 'Spreadsheet',
    '.xlsx': 'Spreadsheet'
}


def categorize_files():

    counts = {}

    for file_name in os.listdir(SCAN_PATH):

        ext = os.path.splitext(file_name)[1].lower()
        category = CATEGORY_MAP.get(ext, 'Other')

        counts[category] = counts.get(category, 0) + 1

    return counts


# ---------- SHARED DATA ----------
def get_dashboard_data():

    duplicates_list = find_duplicates()
    categories = categorize_files()

    total_files = sum(categories.values())

    total_size = 0

    for file_name in os.listdir(SCAN_PATH):

        file_path = os.path.join(SCAN_PATH, file_name)

        if os.path.isfile(file_path):
            total_size += os.path.getsize(file_path)

    storage_kb = round(total_size / 1024, 2)

    stats = {
        'total_files': total_files,
        'duplicates': len(duplicates_list),
        'storage': f'{storage_kb} KB'
    }

    insights = []

    if stats['duplicates'] > 0:
        insights.append(f'{stats["duplicates"]} duplicate file(s) detected.')
    else:
        insights.append('No duplicate files detected.')

    if stats['total_files'] <= 10:
        insights.append('Storage usage is low.')

    insights.append('Recommendation: organize files by category.')

    # Chart
    labels = list(categories.keys())
    values = list(categories.values())

    plt.figure(figsize=(5,3))
    plt.bar(labels, values)
    plt.title('File Categories')
    plt.ylabel('Count')

    chart_path = os.path.join('static', 'chart.png')
    plt.savefig(chart_path, bbox_inches='tight')
    plt.close()

    return stats, insights, duplicates_list, categories


# ---------- AI ASSISTANT ----------
def ai_response(question, stats):

    q = question.lower()

    if 'total' in q or 'how many' in q:
        return f'There are {stats["total_files"]} files in the scanned folder.'

    elif 'duplicate' in q:
        return f'{stats["duplicates"]} duplicate files were detected.'

    elif 'storage' in q:
        return f'Storage usage is {stats["storage"]}.'

    elif 'recommend' in q:
        return 'I recommend organizing files by category and removing duplicate files.'

    else:
        return 'Ask about total files, duplicate files, storage usage, or recommendations.'


# ---------- HOME ----------
@app.route('/')
def home():

    if 'user' not in session:
        return redirect(url_for('login'))

    stats, insights, duplicates_list, categories = get_dashboard_data()

    return render_template(
        'index.html',
        stats=stats,
        insights=insights,
        duplicates_list=duplicates_list,
        categories=categories
    )


# ---------- ANALYTICS ----------
@app.route('/analytics')
def analytics():

    if 'user' not in session:
        return redirect(url_for('login'))

    stats, insights, duplicates_list, categories = get_dashboard_data()

    return render_template(
        'analytics.html',
        stats=stats,
        insights=insights,
        duplicates_list=duplicates_list,
        categories=categories
    )


# ---------- SEARCH PAGE ----------
@app.route('/search', methods=['GET', 'POST'])
def search():

    if 'user' not in session:
        return redirect(url_for('login'))

    results = []
    keyword = ''

    if request.method == 'POST':

        keyword = request.form['keyword']
        results = search_files(keyword)

    return render_template(
        'search.html',
        results=results,
        keyword=keyword
    )


# ---------- AI ASSISTANT PAGE ----------
@app.route('/assistant', methods=['GET', 'POST'])
def assistant():

    if 'user' not in session:
        return redirect(url_for('login'))

    answer = ''
    question = ''

    stats, insights, duplicates_list, categories = get_dashboard_data()

    if request.method == 'POST':

        question = request.form['question']
        answer = ai_response(question, stats)

    return render_template(
        'assistant.html',
        question=question,
        answer=answer
    )


# ---------- CSV REPORT ----------
@app.route('/download-report')
def download_report():

    if 'user' not in session:
        return redirect(url_for('login'))

    stats, insights, duplicates_list, categories = get_dashboard_data()

    data = {
        'Metric': ['Total Files', 'Duplicate Files', 'Storage Used'],
        'Value': [
            stats['total_files'],
            stats['duplicates'],
            stats['storage']
        ]
    }

    df = pd.DataFrame(data)

    report_path = 'file_report.csv'
    df.to_csv(report_path, index=False)

    return send_file(report_path, as_attachment=True)


# ---------- RUN ----------
if __name__ == '__main__':

    app.run(debug=True, port=5001)