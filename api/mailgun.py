import os

import requests


def send_simple_message(subject, recipient, text, html):
    return requests.post(
        f"https://api.mailgun.net/v3/{os.getenv('MAILGUN_DOMAIN')}/messages",
        auth=("api", os.getenv("MAILGUN_API_KEY")),
        data={
            "from": f"GoKag <mailgun@{os.getenv('MAILGUN_DOMAIN')}>",
            "to": [{recipient}],
            "subject": subject,
            "html": html,
            "text": text,
        },
    )
