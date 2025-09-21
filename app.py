from flask import Flask, request, jsonify, render_template, session, redirect, url_for, Response
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import io
import csv
import os
import threading
import queue
import uuid
import json
import time

app = Flask(__name__)
# Prefer loading from environment; fall back to a dev default
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key')

# Single-page app route
@app.route('/')
def index():
    return render_template('index.html', user_email=session.get('user_email'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', user_email=session.get('user_email'))

    # POST
    email = request.form.get('email')
    if not email:
        return render_template('login.html', error='Email is required')
    session['user_email'] = email
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('user_email', None)
    return redirect(url_for('login'))

@app.route('/send-emails', methods=['POST'])
def send_emails():
    try:
        # Get credentials and form data from the request (no session storage)
        email_sender = request.form.get('email')
        email_password = request.form.get('password')
        csv_file = request.files.get('csv_file')
        mail_body = request.form.get('mail')
        subject = request.form.get('subject')
        image_attachment = request.files.get('image_attachment')
        
        if not email_sender or not email_password:
            return jsonify({'message': 'Email and password are required'}), 400
        if not csv_file or not subject or not mail_body:
            return jsonify({'message': 'CSV file, subject, and email body are required'}), 400

        # Read the CSV file and parse name/email combinations flexibly
        recipients = []
        try:
            csv_content = csv_file.stream.read().decode("UTF8")
            csv_reader = csv.reader(io.StringIO(csv_content))
            for row in csv_reader:
                if not row:
                    continue
                cells = [c.strip() for c in row if c and c.strip()]
                if not cells:
                    continue

                email_value = None
                name_value = None

                if len(cells) == 1:
                    # Only email provided
                    email_value = cells[0]
                else:
                    # Determine which cell is email
                    if '@' in cells[0]:
                        email_value = cells[0]
                        name_value = cells[1]
                    elif '@' in cells[1]:
                        name_value = cells[0]
                        email_value = cells[1]
                    else:
                        # Fallback assume first is email, second is name
                        email_value = cells[0]
                        name_value = cells[1]

                if not email_value or '@' not in email_value:
                    continue

                if not name_value:
                    local_part = email_value.split('@')[0]
                    name_value = local_part.replace('.', ' ').replace('_', ' ').title()

                recipients.append({'name': name_value, 'email': email_value})

        except Exception as e:
            return jsonify({'message': f'Error reading CSV file: {str(e)}'}), 400

        if not recipients:
            return jsonify({'message': 'No valid email addresses found in CSV file'}), 400

        # Prepare image attachment if provided
        image_data = None
        image_filename = None
        if image_attachment and image_attachment.filename:
            allowed_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp'}
            file_ext = os.path.splitext(image_attachment.filename)[1].lower()
            if file_ext not in allowed_extensions:
                return jsonify({'message': 'Invalid image format. Please use JPG, PNG, GIF, or BMP.'}), 400
            
            # Enforce a size cap of 10MB
            image_data = image_attachment.read()
            if len(image_data) > 10 * 1024 * 1024:
                return jsonify({'message': 'Attachment too large. Max size is 10MB.'}), 400
            image_filename = image_attachment.filename

        # Send emails
        successful_sends = 0
        failed_sends = 0
        
        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
                smtp.starttls()
                smtp.login(email_sender, email_password)
                
                for recipient in recipients:
                    try:
                        msg = MIMEMultipart()
                        msg['From'] = email_sender
                        msg['To'] = recipient['email']
                        msg['Subject'] = subject
                        
                        personalized_body = f"Hello {recipient['name']},\n\n{mail_body}"
                        msg.attach(MIMEText(personalized_body, 'plain'))
                        
                        if image_data and image_filename:
                            attachment = MIMEBase('application', 'octet-stream')
                            attachment.set_payload(image_data)
                            encoders.encode_base64(attachment)
                            attachment.add_header(
                                'Content-Disposition',
                                f'attachment; filename= {image_filename}'
                            )
                            msg.attach(attachment)
                        
                        smtp.sendmail(email_sender, recipient['email'], msg.as_string())
                        print(f"Mail sent to {recipient['name']} ({recipient['email']})")
                        successful_sends += 1
                        
                    except Exception as send_error:
                        print(f"Failed to send mail to {recipient['name']} ({recipient['email']}): {str(send_error)}")
                        failed_sends += 1
                        
        except smtplib.SMTPException as e:
            return jsonify({'message': f'SMTP error: {str(e)}'}), 500

        message = f'Email sending completed! Successfully sent: {successful_sends}, Failed: {failed_sends}'
        if image_filename:
            message += f' (with attachment: {image_filename})'
        return jsonify({'message': message}), 200

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'message': f'Failed to process request. Error: {str(e)}'}), 500

# ==========================
# Simple Job Status Tracking
# ==========================

# In-memory job registry: job_id -> {
#   'status': 'running'|'completed'|'failed',
#   'progress': {'sent': int, 'failed': int, 'total': int},
#   'results': [list of individual results],
#   'error': str (if failed)
# }
jobs = {}

def _parse_recipients_from_csv(file_storage):
    recipients = []
    csv_content = file_storage.stream.read().decode("UTF8")
    csv_reader = csv.reader(io.StringIO(csv_content))
    for row in csv_reader:
        if not row:
            continue
        cells = [c.strip() for c in row if c and c.strip()]
        if not cells:
            continue
        email_value = None
        name_value = None
        if len(cells) == 1:
            email_value = cells[0]
        else:
            if '@' in cells[0]:
                email_value = cells[0]
                name_value = cells[1]
            elif '@' in cells[1]:
                name_value = cells[0]
                email_value = cells[1]
            else:
                email_value = cells[0]
                name_value = cells[1]
        if not email_value or '@' not in email_value:
            continue
        if not name_value:
            local_part = email_value.split('@')[0]
            name_value = local_part.replace('.', ' ').replace('_', ' ').title()
        recipients.append({'name': name_value, 'email': email_value})
    return recipients

@app.route('/start-send', methods=['POST'])
def start_send():
    try:
        # Require login (email in session) and password from request
        session_email = session.get('user_email')
        if not session_email:
            return jsonify({'message': 'Please login first'}), 401

        email_sender = session_email
        email_password = request.form.get('password')
        if not email_password:
            return jsonify({'message': 'Missing app password'}), 400

        csv_file = request.files.get('csv_file')
        mail_body = request.form.get('mail')
        subject = request.form.get('subject')
        image_attachment = request.files.get('image_attachment')

        if not csv_file or not subject or not mail_body:
            return jsonify({'message': 'CSV file, subject, and email body are required'}), 400

        # Parse recipients
        try:
            recipients = _parse_recipients_from_csv(csv_file)
        except Exception as e:
            return jsonify({'message': f'Error reading CSV file: {str(e)}'}), 400

        if not recipients:
            return jsonify({'message': 'No valid email addresses found in CSV file'}), 400
        
        # Limit recipients for free tier (prevent timeout)
        if len(recipients) > 20:
            return jsonify({'message': 'Free tier limited to 20 recipients per batch. Please split your CSV.'}), 400

        # Attachment
        image_data = None
        image_filename = None
        if image_attachment and image_attachment.filename:
            allowed_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp'}
            file_ext = os.path.splitext(image_attachment.filename)[1].lower()
            if file_ext not in allowed_extensions:
                return jsonify({'message': 'Invalid image format. Please use JPG, PNG, GIF, or BMP.'}), 400
            image_data = image_attachment.read()
            if len(image_data) > 10 * 1024 * 1024:
                return jsonify({'message': 'Attachment too large. Max size is 10MB.'}), 400
            image_filename = image_attachment.filename

        # Create job
        job_id = str(uuid.uuid4())
        jobs[job_id] = {
            'status': 'running',
            'progress': {'sent': 0, 'failed': 0, 'total': len(recipients)},
            'results': [],
            'error': None
        }

        # Start thread
        worker = threading.Thread(
            target=_run_send_job_simple,
            args=(job_id, email_sender, email_password, recipients, subject, mail_body, image_data, image_filename),
            daemon=True
        )
        worker.start()

        return jsonify({'job_id': job_id}), 202
    except Exception as e:
        print(f"Error starting job: {str(e)}")
        return jsonify({'message': f'Failed to start job. Error: {str(e)}'}), 500

def _run_send_job_simple(job_id, email_sender, email_password, recipients, subject, mail_body, image_data, image_filename):
    successful_sends = 0
    failed_sends = 0
    total = len(recipients)
    results = []

    try:
        # Create SMTP connection with timeout
        smtp = smtplib.SMTP("smtp.gmail.com", 587, timeout=10)
        smtp.starttls()
        smtp.login(email_sender, email_password)

        for index, recipient in enumerate(recipients, start=1):
            try:
                msg = MIMEMultipart()
                msg['From'] = email_sender
                msg['To'] = recipient['email']
                msg['Subject'] = subject

                personalized_body = f"Hello {recipient['name']},\n\n{mail_body}"
                msg.attach(MIMEText(personalized_body, 'plain'))

                if image_data and image_filename:
                    attachment = MIMEBase('application', 'octet-stream')
                    attachment.set_payload(image_data)
                    encoders.encode_base64(attachment)
                    attachment.add_header('Content-Disposition', f'attachment; filename= {image_filename}')
                    msg.attach(attachment)

                smtp.sendmail(email_sender, recipient['email'], msg.as_string())
                successful_sends += 1
                results.append({
                    'type': 'success',
                    'index': index,
                    'email': recipient['email'],
                    'name': recipient['name']
                })
            except Exception as send_error:
                failed_sends += 1
                results.append({
                    'type': 'error',
                    'index': index,
                    'email': recipient['email'],
                    'name': recipient['name'],
                    'error': str(send_error)
                })
            finally:
                # Update progress
                jobs[job_id]['progress'] = {'sent': successful_sends, 'failed': failed_sends, 'total': total}
                jobs[job_id]['results'] = results
                # Small delay to prevent overwhelming Gmail
                time.sleep(0.5)
        
        smtp.quit()
        jobs[job_id]['status'] = 'completed'
    except Exception as e:
        jobs[job_id]['status'] = 'failed'
        jobs[job_id]['error'] = str(e)

@app.route('/job-status/<job_id>')
def job_status(job_id):
    if job_id not in jobs:
        return jsonify({'message': 'Job not found'}), 404
    
    job = jobs[job_id]
    return jsonify({
        'status': job['status'],
        'progress': job['progress'],
        'results': job['results'],
        'error': job['error']
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)