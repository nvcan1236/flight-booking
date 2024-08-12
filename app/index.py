from flask import render_template

from app import app, login as app_login


@app_login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)
    return None;


@app.route('/')
def index():
    return render_template('profile.html')


if __name__ == '__main__':
    app.run(debug=True)
