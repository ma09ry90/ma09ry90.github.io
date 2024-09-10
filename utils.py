import os
from flask_mail import Message
from app import mail, app

def save_book_file(book_file):
    # Save the uploaded book file to a directory and return the path
    filename = book_file.filename
    file_path = os.path.join(app.root_path, 'static/books', filename)
    book_file.save(file_path)
    return file_path

def send_invitation_email(user, email, shelf):
    token = user.get_reset_token()
    msg = Message('You are invited to a shelf on UShelf',
                  sender='noreply@demo.com',
                  recipients=[email])
    msg.body = f'''You have been invited by {user.name} to join their shelf on UShelf.
    Click the link below to accept the invitation:
    {url_for('accept_invite', token=token, _external=True)}

    If you did not request this, simply ignore this email.
    '''
    mail.send(msg)
