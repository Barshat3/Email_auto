from flask import Flask, request, jsonify, render_template
import smtplib
from email.mime.text import MIMEText
import io  # To handle CSV file-like object

app = Flask(__name__)

# Route for the homepage
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send-emails', methods=['POST'])
def send_emails():
    try:
        # Get the CSV file and email details from the form
        csv_file = request.files.get('csv_file')
        email_sender = request.form.get('email')
        email_password = request.form.get('password')
        mail_body = request.form.get('mail')
        subject = request.form.get('subject')  # Get the subject

        if not csv_file or not email_sender or not email_password or not subject:
            return jsonify({'message': 'Missing required fields'}), 400

        # Read the CSV file using a file-like object (StringIO)
        recipients = []
        stream = io.StringIO(csv_file.stream.read().decode("UTF8"))
        for line in stream:
            recipients.append(line.strip())

        # Sending emails using provided email credentials
        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
                smtp.starttls()
                smtp.login(email_sender, email_password)
                for receiver in recipients:
                    mail = MIMEText(mail_body)
                    mail['From'] = email_sender
                    mail['To'] = receiver
                    mail["Subject"] = subject  # Set the subject
                    smtp.sendmail(email_sender, receiver, mail.as_string())
                    print(f"Mail sent to {receiver}")
        except smtplib.SMTPException as e:
            return jsonify({'message': f'Failed to send emails. SMTP error: {str(e)}'}), 500

        return jsonify({'message': 'Emails sent successfully!'}), 200

    except Exception as e:
        # Catch any other exceptions and log the error
        print(f"Error: {str(e)}")
        return jsonify({'message': f'Failed to process request. Error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
