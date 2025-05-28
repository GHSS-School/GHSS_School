from flask import Flask, render_template, request, redirect, url_for, flash
import os
import subprocess

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
            pin = 'true' if 'pin' in request.form else 'false'

            category = request.form['category'].strip()
            content = request.form['content'].strip()

            # Construct the file content
            file_content = f"{title}\n{date}\n{category}\n{pin}\n{content}"

            # Save to a .txt file
            filepath = os.path.join(NOTICE_DIR, f"{notice_id}.txt")
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(file_content)

            flash(f"Notice {notice_id}.txt created successfully!", "success")
        except Exception as e:
            flash(f"Error creating notice: {e}", "danger")

        return redirect(url_for('index'))

    return render_template('index.html')



@app.route('/upload', methods=['POST'])
def upload_notice():
    # This is the empty function triggered by the upload button
    print("Upload button pressed.")
    subprocess.run(["git", "add", "."])
    subprocess.run(['git', 'commit', '-m', '"Update"'])
    subprocess.run(['git', 'push', '-u', 'origin', 'main'])

    return "<h1> Successfully Made the changes to the website </h1>"


if __name__ == '__main__':
    app.run(debug=True)

