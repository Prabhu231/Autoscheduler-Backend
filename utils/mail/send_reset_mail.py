from .send_mail import send as send_mail
from decouple import config

def send_password_reset_mail(email, token):
    try:
        reset_link = f"{config('FRONTEND')}/reset-password?token={token}"

        subject = "Reset Your Autoscheduler Password"
        plain_message = f"""Hello,

We received a request to reset your password for your Autoscheduler account.

Click the link below to reset your password:
{reset_link}

The link will expire in 15 minutes.

If you didn't request this, you can safely ignore this email.

Thanks,
The Autoscheduler Team
"""

        html_message = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
            <div style="max-width: 600px; margin: auto; background-color: white; padding: 20px; border-radius: 8px;">
                <h2 style="color: #6a11cb;">Reset Your Password</h2>
                <p>We received a request to reset the password associated with this email address.</p>
                <p>Click the button below to set a new password:</p>
                <p style="text-align: center;">
                    <a href="{reset_link}" style="display: inline-block; background-color: #6a11cb; color: white; padding: 12px 20px; text-decoration: none; border-radius: 5px;">Reset Password</a>
                </p>
                <p>The link will expire in 15 minutes.</p>
                <p>If you didn't request a password reset, you can safely ignore this email.</p>
                <p>— The Autoscheduler Team</p>
            </div>
        </body>
        </html>
        """

        send_mail(
            subject=subject,
            message=plain_message,
            recipient_list=[email],
            html=html_message
        )

    except Exception as e:
        print(f"Error sending password reset email: {e}")
