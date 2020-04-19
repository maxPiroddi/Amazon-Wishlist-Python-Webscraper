import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(PRICE_LIST):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    login_email = os.environ.get('EMAIL_USER')
    login_password = os.environ.get('EMAIL_KEY')
    recipient_email = os.environ.get('EMAIL_RECIPIENT')

    server.login(login_email, login_password)

    subject = 'Your Daily Price Update'
    body = format_data(PRICE_LIST)

    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail(
        login_email,
        recipient_email,
        msg
    )

    print('Email has been sent.')
    server.quit()


def format_data(PRICE_LIST):
    htmlpush = ""
    for item in PRICE_LIST:
        header = f"<h3>{item['title']}</h3>"
        img = f"<img src={item['img']} />"
        price = f"<p>{item['price']}</p>"
        url = f"<p>{item['url']}</p>"
        linebreak = "<br />"
        htmlpush = htmlpush + header + img + price + url + linebreak
    html = f"""\
            <html>
            <head></head>
            <body>
                {htmlpush}
            </body>
            </html>
        """
    return html