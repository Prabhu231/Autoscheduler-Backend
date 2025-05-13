from .send_mail import send as send_mail
from decouple import config

def send_welcome_mail(recipient_list):
    frontend_url = config("FRONTEND")
    send_mail(
        subject='Welcome to Autoscheduler! Simplify Your Email Scheduling',
        message="""Welcome to Autoscheduler!

Thank you for joining Autoscheduler. We're excited to help you streamline your email communications!

Key Feature: Bulk Email Scheduling with BCC
- Schedule emails in advance
- Send to up to 50 BCC recipients
- Save time and stay organized

To get started, log into your account and schedule your first email.

Happy emailing!

The Autoscheduler Team

-----
© 2025 Autoscheduler Inc. All rights reserved.
You received this email because you signed up for Autoscheduler.
""",
        recipient_list=recipient_list,
        html=f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome to Autoscheduler</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            margin: 0;
            padding: 0;
            background-color: #f9f6ff;
        }}
        .container {{
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background-color: #ffffff;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        .header {{
            background: linear-gradient(135deg, #6a3093 0%, #a044ff 100%);
            padding: 30px 20px;
            text-align: center;
            border-radius: 8px 8px 0 0;
            margin-bottom: 20px;
        }}
        .header h1 {{
            color: #ffffff;
            margin: 0;
            font-size: 28px;
            font-weight: 700;
        }}
        .header p {{
            color: #f0f6ff;
            margin: 10px 0 0;
            font-size: 16px;
        }}
        .content {{
            padding: 0 20px 20px;
        }}
        .feature-box {{
            background-color: #f3e6ff;
            border-left: 4px solid #8a3ffc;
            padding: 15px;
            margin-bottom: 20px;
            border-radius: 0 4px 4px 0;
        }}
        .button {{
            display: inline-block;
            background: linear-gradient(135deg, #6a3093 0%, #a044ff 100%);
            color: #ffffff !important;
            text-decoration: none;
            padding: 12px 25px;
            border-radius: 4px;
            font-weight: bold;
            margin: 20px 0;
            text-align: center;
            font-size: 16px;
            line-height: 1.4;
        }}
        .features {{
            margin: 20px 0;
        }}
        .feature-item {{
            display: flex;
            align-items: flex-start;
            margin-bottom: 12px;
            padding: 10px;
            background-color: #f8f0ff;
            border-radius: 4px;
        }}
        .footer {{
            text-align: center;
            padding-top: 20px;
            border-top: 1px solid #e0e0e0;
            margin-top: 20px;
            color: #666;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Welcome to Autoscheduler!</h1>
            <p>Simplify Your Email Communications</p>
        </div>
        
        <div class="content">
            <p>Dear User,</p>
            <p>Thank you for joining Autoscheduler! We're excited to help you take control of your email communications.</p>
            
            <div class="feature-box">
                <h3>Our Key Feature: Bulk Email Scheduling</h3>
                <ul>
                    <li>Schedule emails in advance</li>
                    <li>Send to up to 50 BCC recipients</li>
                    <li>Manage your communications effortlessly</li>
                </ul>
            </div>
            
            <h3 style="color: #8a3ffc;">Why Choose Autoscheduler:</h3>
            <div class="features">
                <div class="feature-item">
                    <div>
                        <strong>Flexible Scheduling</strong>
                        <p>Plan and schedule your emails days or weeks in advance</p>
                    </div>
                </div>
                <div class="feature-item">
                    <div>
                        <strong>BCC Support</strong>
                        <p>Send to up to 50 recipients while maintaining privacy</p>
                    </div>
                </div>
                <div class="feature-item">
                    <div>
                        <strong>Easy Management</strong>
                        <p>Simple interface to track and manage your scheduled emails</p>
                    </div>
                </div>
            </div>
            
            <div style="text-align: center;">
                <a href="{frontend_url}/auth/login" class="button">Login and Start Scheduling</a>
            </div>
            
            <p>Happy emailing!</p>
            <p><strong>The Autoscheduler Team</strong></p>
        </div>
        
        <div class="footer">
            <p>© 2025 Autoscheduler Inc. All rights reserved.</p>
            <p>You received this email because you signed up for Autoscheduler.</p>
        </div>
    </div>
</body>
</html>
"""

)