import pytz

def parse_message(message):
    user = message.from_user.username
    text = message.text
    timestamp = message.date.astimezone(pytz.timezone('America/Sao_Paulo')).strftime('%Y:%m:%d:%H:%M')
    return f"{timestamp} - {user}: {text}"