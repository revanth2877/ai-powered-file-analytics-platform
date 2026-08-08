import sqlite3

def init_db():
    conn = sqlite3.connect('file_analytics.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scan_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            total_files INTEGER,
            duplicates INTEGER,
            storage TEXT,
            scan_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()


def save_scan(stats):
    conn = sqlite3.connect('file_analytics.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO scan_history(total_files, duplicates, storage)
        VALUES (?, ?, ?)
    ''', (
        stats['total_files'],
        stats['duplicates'],
        stats['storage']
    ))

    conn.commit()
    conn.close()


def get_history():
    conn = sqlite3.connect('file_analytics.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT total_files, duplicates, storage, scan_time
        FROM scan_history
        ORDER BY id DESC
    ''')

    rows = cursor.fetchall()

    conn.close()
    return rows