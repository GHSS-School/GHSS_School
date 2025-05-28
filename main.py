from flask import Flask, render_template, request, redirect, url_for, flash
import os
import subprocess
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'supersecretkey'
NOTICE_DIR = 'Notices'
UPLOADS_DIR = 'Uploads'
Achievements_DIR = 'Achievements'

# Ensure the directories exist
os.makedirs(NOTICE_DIR, exist_ok=True)
os.makedirs(UPLOADS_DIR, exist_ok=True)


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


@app.route('/files', methods=["GET", "POST"])
def files():
    if request.method == 'GET':
        return render_template('files.html')

    elif request.method == 'POST':
        try:
            # Get form data
            folder_name = request.form['folder_name'].strip()
            title = request.form['title'].strip()
            date = request.form['date'].strip()
            description = request.form['description'].strip()

            # Validate required fields
            if not folder_name or not title or not date:
                flash("Folder name, title, and date are required!", "danger")
                return redirect(url_for('files'))

            # Secure the folder name
            folder_name = secure_filename(folder_name)
            if not folder_name:
                flash("Invalid folder name!", "danger")
                return redirect(url_for('files'))

            # Create folder path
            folder_path = os.path.join(UPLOADS_DIR, folder_name)
            os.makedirs(folder_path, exist_ok=True)

            # Create data.txt file
            data_content = f"{title}\n{date}\n{description}"
            data_file_path = os.path.join(folder_path, 'data.txt')
            with open(data_file_path, 'w', encoding='utf-8') as f:
                f.write(data_content)

            # Handle file uploads
            uploaded_files = request.files.getlist('files')
            uploaded_count = 0

            for file in uploaded_files:
                if file and file.filename:
                    # Secure the filename
                    filename = secure_filename(file.filename)
                    if filename:
                        file_path = os.path.join(folder_path, filename)
                        file.save(file_path)
                        uploaded_count += 1

            flash(f"Folder '{folder_name}' created successfully with {uploaded_count} files uploaded!", "success")

        except Exception as e:
            flash(f"Error creating folder: {e}", "danger")

        return redirect(url_for('files'))


@app.route('/achievements', methods=["GET", "POST"])
def achievements():
    if request.method == 'GET':
        return render_template('achievements.html')

    elif request.method == 'POST':
        try:
            # Get form data
            folder_name = request.form['folder_name'].strip()
            title = request.form['title'].strip()
            category = request.form['category'].strip()
            date = request.form['date'].strip()
            description = request.form['description'].strip()

            # Validate required fields
            if not folder_name or not title or not category or not date:
                flash("Folder name, title, category, and date are required!", "danger")
                return redirect(url_for('achievements'))

            # Secure the folder name
            folder_name = secure_filename(folder_name)
            if not folder_name:
                flash("Invalid folder name!", "danger")
                return redirect(url_for('achievements'))

            # Create folder path
            folder_path = os.path.join(Achievements_DIR, folder_name)
            os.makedirs(folder_path, exist_ok=True)

            # Create data.txt file with specific format
            data_content = f"{title}\n{category}\n{date}\n{description}"
            data_file_path = os.path.join(folder_path, 'data.txt')
            with open(data_file_path, 'w', encoding='utf-8') as f:
                f.write(data_content)

            # Handle single image upload
            image_file = request.files.get('image')
            image_uploaded = False

            if image_file and image_file.filename:
                # Get file extension
                original_filename = secure_filename(image_file.filename)
                if original_filename:
                    file_extension = os.path.splitext(original_filename)[1].lower()

                    # Check if it's an image file
                    allowed_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg'}
                    if file_extension in allowed_extensions:
                        # Save with new name: image.extension
                        new_filename = f"image{file_extension}"
                        file_path = os.path.join(folder_path, new_filename)
                        image_file.save(file_path)
                        image_uploaded = True
                    else:
                        flash("Only image files are allowed!", "danger")
                        return redirect(url_for('achievements'))

            success_message = f"Achievement folder '{folder_name}' created successfully!"
            if image_uploaded:
                success_message += " Image uploaded and renamed to 'image'."

            flash(success_message, "success")

        except Exception as e:
            flash(f"Error creating achievement folder: {e}", "danger")

        return redirect(url_for('achievements'))


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