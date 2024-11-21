from flask import Flask, send_file, render_template, request, jsonify
from io import BytesIO
import zipfile
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



# Replace with your email configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = ""
APP_PASSWORD = ""
app = Flask(__name__)


@app.route('/lane_v3')
def lane_v3():
    # Create a BytesIO object to hold the ZIP file
    zip_buffer = BytesIO()

    # Create a new ZIP file in the buffer
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        # Add some example files to the ZIP file
        zip_file.write('lane_v3/build.zip', 'build.zip')
        zip_file.write('lane_v3/dist.zip', 'dist.zip')
        zip_file.write('lane_v3/lane_v3.spec', 'lane_v3.spec')

    # Prepare the ZIP file for download
    zip_buffer.seek(0)
    return send_file(
        zip_buffer,
        as_attachment=True,
        download_name='files.zip',
        mimetype='application/zip'
    )



@app.route('/lane_v4')
def lane_v4():
    # Create a BytesIO object to hold the ZIP file
    zip_buffer = BytesIO()

    # Create a new ZIP file in the buffer
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        # Add some example files to the ZIP file
        zip_file.write('lane_v4/build.zip', 'build.zip')
        zip_file.write('lane_v4/dist.zip', 'dist.zip')
        zip_file.write('lane_v4/lane_v4.spec', 'lane_v4.spec')

    # Prepare the ZIP file for download
    zip_buffer.seek(0)
    return send_file(
        zip_buffer,
        as_attachment=True,
        download_name='files.zip',
        mimetype='application/zip'
    )



@app.route('/ppt')
def ppt():
    # Load the PowerPoint file into memory
    ppt_path = 'how_lane_detected.pptx'
    with open(ppt_path, 'rb') as ppt_file:
        ppt_data = BytesIO(ppt_file.read())

    # Prepare the PowerPoint file for download
    ppt_data.seek(0)
    return send_file(
        ppt_data,
        as_attachment=True,
        download_name='how_lane_detected.pptx',
        mimetype='application/vnd.openxmlformats-officedocument.presentationml.presentation'
    )


@app.route('/support')
def home():
    return render_template('index.html')


@app.route('/send_email', methods=['POST'])
def send_email():
    if request.method == 'POST':
        try:
            email = request.form['email']
            query = request.form['query']

            # Create message
            msg = MIMEMultipart()
            msg['From'] = SENDER_EMAIL
            msg['To'] = SENDER_EMAIL
            msg['Subject'] = f"New Query from {email}"

            body = f"From: {email}\nQuery: {query}"
            msg.attach(MIMEText(body, 'plain'))

            # Create SMTP connection with authentication
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()
            server.login(SENDER_EMAIL, APP_PASSWORD)  # Login using App Password

            # Send email
            server.send_message(msg)
            server.quit()

            return jsonify({"message": "Email sent successfully!"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
