from flask import Flask
from flask import render_template
from flask import redirect
from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo
from werkzeug.utils import secure_filename
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.abspath(os.getcwd()), 'static', 'img')


class SignUpForm(FlaskForm):
	user_id = StringField('Login', validators=[DataRequired(), Length(min=5, max=15, message='Login must have at least 5 characters')])
	user_password = PasswordField('Password', validators=[DataRequired()])
	user_password_2 = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('user_password', message='Password must be the same')])
	submit = SubmitField('Sign Up')
	def validate_username(self, user_id):
		excluded_chars = ' *?!"^+%&;/()=}][{$#'
		for char in self.user_id.data:
			if char in excluded_chars:
				raise ValidationError(f'Character {char} is not allowed in username.')


class SignInForm(FlaskForm):
	user_id = StringField('Login', validators=[DataRequired()])
	user_password = PasswordField('Password', validators=[DataRequired()])
	submit = SubmitField('Sign In')


@app.route('/', methods=['GET', 'POST'])
def main_page():
	if request.method == 'POST':
		if request.form.get('signin') == 'Sign In':
			return redirect('/signin')
		elif request.form.get('signup') == 'Sign Up' or request.form.get('signup2') == 'Sign Up':
			return redirect('/signup')
		else:
			pass
	return render_template('main_page.html', title='My Blog')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	form = SignUpForm()
	if form.validate_on_submit():
		return redirect('/myblog')
	return render_template('signup.html', title='Sign Up', form=form)


@app.route('/signin', methods=['GET', 'POST'])
def signin():
	form = SignInForm()
	if form.validate_on_submit():
		return redirect('/myblog')
	return render_template('signin.html', title='Sign In', form=form)


@app.route('/myblog', methods=['GET', 'POST'])
def myblog(path='', notes=[], paths=[]):
	if request.method == 'POST':
		note = request.form['note']
		file = request.files['file']
		if file:
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
			path = path[path.index('static'):]
		notes.append(note)
		paths.append(path)
		length = len(notes)
		return render_template('notes.html', notes=notes, paths=paths, length=length, title='My Blog')
	return render_template('logged_main_page.html', title='My Blog')


if __name__ == '__main__':
	app.run(port=8080, host='127.0.0.1', debug=True)
