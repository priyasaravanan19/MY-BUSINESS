
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import resend
import os
import html
import re

# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

# ============================================================
# FLASK APP
# ============================================================

app = Flask(__name__)
CORS(app)

# ============================================================
# RESEND CONFIGURATION
# ============================================================

RESEND_API_KEY = os.getenv("RESEND_API_KEY")

BUSINESS_EMAIL = os.getenv(
    "BUSINESS_EMAIL",
    "priya19072006@gmail.com"
)

FROM_EMAIL = os.getenv(
    "FROM_EMAIL",
    "Pragu Software Solutions <onboarding@resend.dev>"
)

if not RESEND_API_KEY:
    raise RuntimeError("RESEND_API_KEY is missing from .env")

if not BUSINESS_EMAIL:
    raise RuntimeError("BUSINESS_EMAIL is missing from .env")

resend.api_key = RESEND_API_KEY


# ============================================================
# COMMON VALIDATION AND EMAIL FUNCTIONS
# ============================================================

def valid_email(email):
    """Basic email validation."""
    return bool(
        re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email)
    )


def send_business_email(subject, reply_email, email_html):
    """Send a website enquiry to the business inbox."""
    return resend.Emails.send({
        "from": FROM_EMAIL,
        "to": [BUSINESS_EMAIL],
        "reply_to": reply_email,
        "subject": subject,
        "html": email_html
    })


def error_response(message, status=400):
    return jsonify({
        "success": False,
        "message": message
    }), status


# ============================================================
# HOME / HEALTH CHECK
# ============================================================

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "success": True,
        "message": "Pragu Software Solutions API is running."
    }), 200


# ============================================================
# CONTACT FORM API
# ============================================================

@app.route("/api/contact", methods=["POST"])
def contact():
    try:
        if not request.is_json:
            return error_response("Request must contain JSON data.")

        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            return error_response("Invalid request data.")

        name = str(data.get("name") or "").strip()
        email = str(data.get("email") or "").strip()
        phone = str(data.get("phone") or "").strip()
        subject = str(data.get("subject") or "").strip()
        message = str(data.get("message") or "").strip()

        if not name:
            return error_response("Please enter your name.")

        if not valid_email(email):
            return error_response("Please enter a valid email address.")

        if not subject:
            return error_response("Please enter a subject.")

        if not message:
            return error_response("Please enter your message.")

        if (
            len(name) > 150
            or len(email) > 254
            or len(phone) > 40
            or len(subject) > 200
            or len(message) > 10000
        ):
            return error_response("Some fields exceed the allowed length.")

        safe_name = html.escape(name)
        safe_email = html.escape(email)
        safe_phone = html.escape(phone or "Not provided")
        safe_subject = html.escape(subject)
        safe_message = html.escape(message).replace("\n", "<br>")

        email_html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width">
            <title>New Contact Enquiry</title>
        </head>
        <body style="margin:0;padding:30px;background:#F8F7FF;
                     font-family:Arial,Helvetica,sans-serif;">
            <div style="max-width:650px;margin:auto;background:#FFFFFF;
                        border-radius:16px;overflow:hidden;
                        border:1px solid #E5E7EB;">
                <div style="padding:28px;background:#6D4AFF;color:#FFFFFF;">
                    <h1 style="margin:0;font-size:24px;">
                        New Contact Enquiry
                    </h1>
                    <p>Pragu Software Solutions</p>
                </div>
                <div style="padding:30px;color:#17142F;">
                    <p>A new message was submitted through your website.</p>
                    <p><strong>Name:</strong> {safe_name}</p>
                    <p><strong>Email:</strong> {safe_email}</p>
                    <p><strong>Phone:</strong> {safe_phone}</p>
                    <p><strong>Subject:</strong> {safe_subject}</p>
                    <h3>Message</h3>
                    <div style="padding:18px;background:#F8FAFC;
                                border-left:4px solid #6D4AFF;
                                border-radius:8px;line-height:1.7;
                                overflow-wrap:anywhere;">
                        {safe_message}
                    </div>
                </div>
            </div>
        </body>
        </html>
        """

        send_business_email(
            f"New Contact Enquiry - {subject}",
            email,
            email_html
        )

        print("Contact email accepted by Resend.")

        return jsonify({
            "success": True,
            "message": "Your message has been sent successfully."
        }), 200

    except Exception as error:
        app.logger.exception("Contact email sending failed: %s", error)

        return error_response(
            "Unable to send your message right now. Please try again later.",
            500
        )


# ============================================================
# QUOTE REQUEST API
# ============================================================

@app.route("/api/quote", methods=["POST"])
def quote():
    try:
        if not request.is_json:
            return error_response("Request must contain JSON data.")

        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            return error_response("Invalid request data.")

        # Get the quote form fields
        name = str(data.get("name") or "").strip()
        email = str(data.get("email") or "").strip()
        phone = str(data.get("phone") or "").strip()
        service = str(data.get("service") or "").strip()
        budget = str(data.get("budget") or "Not specified").strip()
        timeline = str(data.get("timeline") or "Not specified").strip()
        message = str(data.get("message") or "").strip()

        # Validate required fields
        if not name:
            return error_response("Please enter your name.")

        if not valid_email(email):
            return error_response("Please enter a valid email address.")

        if not service:
            return error_response("Please select a service.")

        if not message:
            return error_response("Please describe your project.")

        # Validate field lengths
        if (
            len(name) > 150
            or len(email) > 254
            or len(phone) > 40
            or len(service) > 150
            or len(budget) > 100
            or len(timeline) > 100
            or len(message) > 10000
        ):
            return error_response("Some fields exceed the allowed length.")

        # Escape user input before inserting it into HTML
        safe_name = html.escape(name)
        safe_email = html.escape(email)
        safe_phone = html.escape(phone or "Not provided")
        safe_service = html.escape(service)
        safe_budget = html.escape(budget or "Not specified")
        safe_timeline = html.escape(timeline or "Not specified")
        safe_message = html.escape(message).replace("\n", "<br>")

        # Build the quote request email
        email_html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width">
            <title>New Quote Request</title>
        </head>
        <body style="margin:0;padding:30px;background:#F8F7FF;
                     font-family:Arial,Helvetica,sans-serif;">
            <div style="max-width:650px;margin:auto;background:#FFFFFF;
                        border-radius:16px;overflow:hidden;
                        border:1px solid #E5E7EB;">
                <div style="padding:28px;background:#6D4AFF;color:#FFFFFF;">
                    <h1 style="margin:0;font-size:24px;">
                        New Quote Request
                    </h1>
                    <p>Pragu Software Solutions</p>
                </div>

                <div style="padding:30px;color:#17142F;">
                    <p>A new project quote request was submitted.</p>

                    <h3>Customer Details</h3>
                    <p><strong>Name:</strong> {safe_name}</p>
                    <p><strong>Email:</strong> {safe_email}</p>
                    <p><strong>Phone:</strong> {safe_phone}</p>

                    <h3>Project Details</h3>
                    <p><strong>Service:</strong> {safe_service}</p>
                    <p><strong>Budget:</strong> {safe_budget}</p>
                    <p><strong>Timeline:</strong> {safe_timeline}</p>

                    <h3>Project Description</h3>
                    <div style="padding:18px;background:#F8FAFC;
                                border-left:4px solid #6D4AFF;
                                border-radius:8px;line-height:1.7;
                                overflow-wrap:anywhere;">
                        {safe_message}
                    </div>

                    <p style="margin-top:25px;color:#64748B;font-size:12px;">
                        Reply to this email to respond to the customer.
                    </p>
                </div>
            </div>
        </body>
        </html>
        """

        # Send the quote request to your business email
        send_business_email(
            f"New Quote Request - {service}",
            email,
            email_html
        )

        print("Quote email accepted by Resend.")
        print("Recipient:", BUSINESS_EMAIL)

        return jsonify({
            "success": True,
            "message": "Your quote request has been sent successfully."
        }), 200

    except Exception as error:
        app.logger.exception("Quote email sending failed: %s", error)

        return error_response(
            "Unable to send your quote request right now. Please try again later.",
            500
        )


# ============================================================
# RUN FLASK SERVER
# ============================================================

if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
