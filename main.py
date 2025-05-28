from flask import Flask, render_template, request, redirect, url_for, flash
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'
NOTICE_DIR = 'Notices'

# Ensure the Notices directory exists
os.makedirs(NOTICE_DIR, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            notice_id = request.form['noticeId'].strip()
            title = request.form['title'].strip()
            date = request.form['date'].strip()
            category = request.form['category'].strip()
            content = request.form['content'].strip()

            # Construct the file content
            file_content = f"{title}\n{date}\n{category}\n{content}"

            # Save to a .txt file
            filepath = os.path.join(NOTICE_DIR, f"{notice_id}.txt")
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(file_content)

            flash(f"Notice {notice_id}.txt created successfully!", "success")
        except Exception as e:
            flash(f"Error creating notice: {e}", "danger")

        return redirect(url_for('index'))

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

