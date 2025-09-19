from flask import Flask, request, render_template, flash
import smtplib
from email.message import EmailMessage
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"  # for flash messages

# Email credentials (use environment variables or config in production)
EMAIL_ADDRESS = "hemanthkumarchowdisetti999@gmail.com" \
""
EMAIL_PASSWORD = "aeek aqnv ppnu qqzk"


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get form data
        subject = request.form.get("subject")
        content = request.form.get("content")
        recipients = request.form.get("recipients")  # comma separated emails

        if not subject or not content or not recipients:
            flash("Please fill all the fields!", "error")
            return render_template("index.html")


        # Prepare email message
        msg = EmailMessage()
        msg["From"] = EMAIL_ADDRESS
        msg["Subject"] = subject
        msg.set_content(content)

        # Attach resume file
        resume_path = os.path.join(os.getcwd(), "resume", "hemanth.pdf")
        with open(resume_path, "rb") as f:
            file_data = f.read()
            file_name = os.path.basename(resume_path)
        msg.add_attachment(file_data, maintype="application", subtype="pdf", filename=file_name)

        # Send mail to each recipient
        recipient_list = [email.strip() for email in recipients.split(",") if email.strip()]
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                for recipient in recipient_list:
                    msg["To"] = recipient
                    smtp.send_message(msg)
                    del msg["To"]  # remove for next recipient

            flash(f"Emails sent successfully to {len(recipient_list)} recipients!", "success")
        except Exception as e:
            flash(f"An error occurred: {e}", "error")

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
