# Bulk Email Sender

A modern Flask web application for sending personalized bulk emails with live progress tracking via Server-Sent Events (SSE).

## Features

- **Personalized Emails**: Automatically adds "Hello [Name]," to each email
- **Flexible CSV Support**: Accepts `name,email` or `email,name` formats, or just email addresses
- **Image Attachments**: Support for JPG, PNG, GIF, BMP files (max 10MB)
- **Live Progress Tracking**: Real-time progress bar and per-recipient status updates
- **Secure Authentication**: Uses Gmail App Passwords (no password storage)
- **Modern UI**: Glass-morphism design with gradient backgrounds
- **Session Management**: Optional email login with browser-only password storage

## Screenshots

- Login page with gradient background and glass card design
- Sender page with file upload, form fields, and live progress panel
- Real-time progress updates showing sent/failed counts and recipient details

## Prerequisites

- Python 3.7+
- Gmail account with 2-Step Verification enabled
- Gmail App Password (see setup instructions below)

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Email_auto
   ```

2. **Install dependencies**
   ```bash
   pip install flask
   ```

3. **Set up Gmail App Password**
   - Go to [Google Account Security](https://myaccount.google.com/security)
   - Enable 2-Step Verification if not already enabled
   - Go to "App passwords" and generate a new password for "Mail"
   - Save the 16-character password (e.g., `abcd efgh ijkl mnop`)

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open in browser**
   - Navigate to `http://localhost:5000`
   - Login with your Gmail address and App Password

## Usage

### 1. Login
- Enter your Gmail address
- Optionally enter your Gmail App Password (stored only in browser)
- Click "Continue"

### 2. Prepare CSV File
Create a CSV file with recipients in one of these formats:
```
Name,Email
John Doe,john@example.com
Jane Smith,jane@example.com
```

Or just email addresses:
```
john@example.com
jane@example.com
```

### 3. Send Emails
- Upload your CSV file
- Optionally attach an image (JPG, PNG, GIF, BMP, max 10MB)
- Enter email subject and message
- Click "Send Personalized Emails"
- Watch live progress updates

### 4. Monitor Progress
The progress panel shows:
- Real-time progress bar
- Sent/Failed/Total counts
- Per-recipient success/failure details
- Final completion status

## File Structure

```
Email_auto/
├── app.py                 # Flask application with SSE endpoints
├── templates/
│   ├── index.html        # Main sender page with progress UI
│   └── login.html        # Login page with glass design
└── README.md             # This file
```

## API Endpoints

- `GET /` - Main sender page
- `GET /login` - Login page
- `POST /login` - Process login (stores email in session)
- `GET /logout` - Clear session and redirect to login
- `POST /start-send` - Start email sending job (returns job_id)
- `GET /events/<job_id>` - Server-Sent Events stream for progress

## Security Features

- **No Password Storage**: App passwords are stored only in browser sessionStorage
- **Session Management**: Only email addresses are stored in server sessions
- **Input Validation**: CSV parsing, file type/size validation
- **Error Handling**: Comprehensive error messages and fallbacks

## Configuration

### Environment Variables
- `FLASK_SECRET_KEY`: Secret key for session management (defaults to dev key)

### Gmail SMTP Settings
- Host: `smtp.gmail.com`
- Port: `587`
- Security: `STARTTLS`
- Authentication: Gmail App Password required

## Troubleshooting

### Common Issues

1. **"Username and Password not accepted" error**
   - Ensure 2-Step Verification is enabled on your Google account
   - Use App Password, not your regular Gmail password
   - Check that the App Password is 16 characters without spaces

2. **File upload not working when logged in**
   - Hard refresh the page (Ctrl+Shift+R)
   - Check browser console for JavaScript errors

3. **Progress not updating**
   - Ensure your proxy/firewall doesn't block Server-Sent Events
   - Check browser console for connection errors

4. **CSV parsing errors**
   - Ensure CSV has proper format: `name,email` or `email,name`
   - Check for empty rows or invalid email addresses

### Browser Compatibility
- Chrome 6+
- Firefox 6+
- Safari 5+
- Edge 12+

## Development

### Running in Development
```bash
python app.py
```
The app runs with `debug=True` for development.

### Production Deployment
1. Set `FLASK_SECRET_KEY` environment variable
2. Set `debug=False` in `app.py`
3. Use a production WSGI server (e.g., Gunicorn)
4. Configure reverse proxy for SSE support

## License

This project is open source and available under the MIT License.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review browser console for errors
3. Ensure Gmail App Password is correctly configured
4. Verify CSV file format

---

**Note**: This application is for legitimate bulk email sending only. Ensure compliance with anti-spam laws and email service provider terms of service.