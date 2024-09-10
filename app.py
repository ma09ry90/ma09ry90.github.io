from flask import Flask, render_template, redirect, url_for, flash, request, session, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
import os
from config import Config
from forms import RegistrationForm, LoginForm, ResetPasswordForm, UploadBookForm, InviteForm
from models import User, Book, Shelf, Invite, db

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
bcrypt = Bcrypt(app)
mail = Mail(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['user_id'] = user.id
            flash('You have been logged in!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    return render_template('dashboard.html', user=user)

@app.route('/myshelf', methods=['GET', 'POST'])
def myshelf():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    books = Book.query.filter_by(user_id=user.id).all()
    invites = Invite.query.filter_by(inviter_id=user.id).all()
    
    form = InviteForm()
    if form.validate_on_submit():
        invite = Invite(email=form.email.data, shelf_id=1, inviter_id=user.id)  # Adjust as needed
        db.session.add(invite)
        db.session.commit()
        flash('Invitation sent!', 'success')
        # Send email invitation
        send_invitation_email(user, form.email.data)
        return redirect(url_for('myshelf'))
    
    return render_template('myshelf.html', user=user, books=books, invites=invites, form=form)

@app.route('/upload-book', methods=['GET', 'POST'])
def upload_book():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    form = UploadBookForm()
    if form.validate_on_submit():
        filename = secure_filename(form.book_file.data.filename)
        file_path = os.path.join('static/books', filename)
        form.book_file.data.save(file_path)
        
        book = Book(
            name=form.name.data,
            author=form.author.data,
            description=form.description.data,
            file_path=file_path,
            user_id=session['user_id']
        )
        db.session.add(book)
        db.session.commit()
        flash('Book has been uploaded!', 'success')
        return redirect(url_for('myshelf'))
    
    return render_template('upload-book.html', form=form)

@app.route('/calendar')
def calendar():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('calendar.html')

@app.route('/manage-invites')
def manage_invites():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    invites = Invite.query.filter_by(inviter_id=user.id).all()
    return render_template('manage-invites.html', invites=invites)

@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.get_reset_token()
            msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
            msg.body = f'''To reset your password, visit the following link:
{url_for('reset_password_token', token=token, _external=True)}

If you did not request this email, ignore it.
'''
            mail.send(msg)
            flash('An email has been sent with instructions to reset your password.', 'info')
            return redirect(url_for('login'))
        else:
            flash('Email not found.', 'danger')
    return render_template('reset-password.html', form=form)

@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password_token(token):
    user = User.verify_reset_token(token)
    if not user:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_password'))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated!', 'success')
        return redirect(url_for('login'))
    return render_template('reset-password.html', form=form)

def send_invitation_email(user, email):
    msg = Message('You have been invited to a shelf on UShelf',
                  sender='noreply@demo.com',
                  recipients=[email])
    msg.body = f'''You have been invited by {user.name} to join their shelf on UShelf.
Click the link below to accept the invitation:
{url_for('manage_invites', _external=True)}

If you did not request this, simply ignore this email.
'''
    mail.send(msg)

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    query = request.args.get('query')  # Get search query from URL parameter
    results = []
    
    if query:
        results = Book.query.filter(
            (Book.name.ilike(f'%{query}%')) | 
            (Book.author.ilike(f'%{query}%'))
        ).all()
    
    return render_template('search.html', results=results, query=query)