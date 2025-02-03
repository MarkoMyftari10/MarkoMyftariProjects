from flask import Flask, render_template, request, redirect, url_for, session, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session as OrmSession
from sqlalchemy import create_engine, inspect
from functools import wraps
import smtplib
from email.message import EmailMessage
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/raportime'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'

Base = automap_base()
engine = create_engine('mysql://root@localhost/raportime')
Base.prepare(engine, reflect=True)
db = SQLAlchemy(app)
user_otp = {}

class user1(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
  
    def update(self, username, email):
        self.username = username
        self.email = email
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

def generate_otp():
    return str(random.randint(1000, 9999))

def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, public, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response
    return no_cache

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        otp = request.form.get('otp')
        if otp:
            if otp == user_otp.get(username):
                del user_otp[username]
                session['username'] = username  # Log the user in
                return redirect(url_for('index'))
            else:
                return "Invalid OTP. Please try again."
        else:
            user = user1.query.filter_by(username=username).first()
            if user:
                otp = generate_otp()
                send_otp_email(user.email, otp)
                user_otp[username] = otp  # Store OTP for validation
                return jsonify(success=True)
            else:
                return jsonify(success=False)
    return render_template('login.html')

@app.route('/send_otp', methods=['POST'])
def send_otp():
    data = request.json
    username = data.get('username')
    user = user1.query.filter_by(username=username).first()
    if user:
        otp = generate_otp()
        send_otp_email(user.email, otp)
        user_otp[username] = otp
        return jsonify(success=True)
    else:
        return jsonify(success=False)

@app.route('/users', methods=['GET'])
@nocache
def users():
    if 'username' not in session:
        return redirect(url_for('login'))
    all_users = user1.query.all()
    return render_template('users.html', users=all_users)

@app.route('/delete_user/<int:id>', methods=['POST'])
@nocache
def delete_user(id):
    if 'username' not in session:
        return redirect(url_for('login'))
    user = user1.query.get(id)
    if user:
        user.delete()
        return redirect(url_for('users'))
    else:
        return f"User with ID {id} not found."

@app.route('/update_user', methods=['POST'])
def update_user():
    if 'username' not in session:
        return redirect(url_for('login'))

    user_id = request.form['userId']
    username = request.form['username']
    email = request.form['email']

    user = user1.query.get(user_id)
    if user:
        user.update(username, email)
        return jsonify(success=True)
    else:
        return jsonify(success=False)

@app.route('/unintentional_action')
@nocache
def unintentional_action():
    return render_template('unintentional_action.html')

@app.route('/go_back')
@nocache
def go_back():
    if 'previous_page' in session:
        return redirect(session['previous_page'])
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

def send_otp_email(email, otp):
    from_mail = "raportimetest@gmail.com"
    msg = EmailMessage()
    msg['Subject'] = "OTP Verification"
    msg['From'] = from_mail
    msg['To'] = email
    msg.set_content("Use this OTP for verification: " + otp)

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login('raportimetest@gmail.com', 'qmjx hujk xsbw xblz')
        server.send_message(msg)

@app.route('/index')
@nocache
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    session['previous_page'] = url_for('index')
    return render_template('index.html')

@app.route('/krijo_raporte', methods=['GET', 'POST'])
@nocache
def krijo_raporte():
    if 'username' not in session:
        return redirect(url_for('login'))
    tables = Base.classes.keys()  # Get all table names from automap

    selected_table = request.form.get('table')  # Get the selected table from form
    filter_column = request.form.get('filter_column')
    filter_operator = request.form.get('filter_operator')
    filter_value = request.form.get('filter_value')
    data = None
    columns = None

    if selected_table:
        try:
            db_session = OrmSession(engine)
            if selected_table in Base.classes:
                table_class = Base.classes[selected_table]  # Get the table class
                query = db_session.query(table_class)

                # Apply filtering logic
                if filter_column and filter_operator and filter_value:
                    if filter_operator == 'contains':
                        query = query.filter(getattr(table_class, filter_column).like(f'%{filter_value}%'))
                    elif filter_operator == 'does_not_contain':
                        query = query.filter(~getattr(table_class, filter_column).like(f'%{filter_value}%'))
                    elif filter_operator == 'is':
                        query = query.filter(getattr(table_class, filter_column) == filter_value)
                    elif filter_operator == 'is_not':
                        query = query.filter(getattr(table_class, filter_column) != filter_value)
                    elif filter_operator == 'starts_with':
                        query = query.filter(getattr(table_class, filter_column).like(f'{filter_value}%'))
                    elif filter_operator == 'ends_with':
                        query = query.filter(getattr(table_class, filter_column).like(f'%{filter_value}'))
                    elif filter_operator == 'is_empty':
                        query = query.filter(getattr(table_class, filter_column) == None)
                    elif filter_operator == 'is_not_empty':
                        query = query.filter(getattr(table_class, filter_column) != None)

                result = query.all()  # Execute query

                if result:
                    columns = result[0].__table__.columns.keys()  # Get column names
                    data = [row.__dict__ for row in result]  # Convert row objects to dictionaries
                    for row in data:
                        row.pop('_sa_instance_state', None)  # Remove SQLAlchemy internal state

        except Exception as e:
            print(f"An error occurred: {e}")

    return render_template('krijo_raporte.html', tables=tables, data=data, columns=columns, selected_table=selected_table)

@app.route('/view_data/<table_name>', methods=['GET', 'POST'])
@nocache
def view_data(table_name):
    if 'username' not in session:
        return redirect(url_for('login'))

    try:
        inspector = inspect(engine)
        if table_name not in inspector.get_table_names():
            return f"Table '{table_name}' not found in the database.", 404

        db_session = OrmSession(engine)
        table_class = Base.classes[table_name]
        rows = db_session.query(table_class).all()
        columns = [column.name for column in table_class.__table__.columns]

        data = []
        for row in rows:
            data.append({column: getattr(row, column) for column in columns})

        return render_template('view_data.html', columns=columns, data=data, table_name=table_name)
    except Exception as e:
        return f"An error occurred: {e}"

@app.route('/delete_data/<table_name>/<int:id>', methods=['POST'])
@nocache
def delete_data(table_name, id):
    if 'username' not in session:
        return redirect(url_for('login'))

    try:
        inspector = inspect(engine)
        if table_name not in inspector.get_table_names():
            return f"Table '{table_name}' not found in the database.", 404

        db_session = OrmSession(engine)
        table_class = Base.classes[table_name]
        row = db_session.query(table_class).get(id)

        if not row:
            return f"Record with ID {id} not found in table '{table_name}'.", 404

        db_session.delete(row)
        db_session.commit()

        return redirect(url_for('view_data', table_name=table_name))
    except Exception as e:
        return f"An error occurred: {e}"

@app.route('/delete_row/<string:table_name>/<int:id>', methods=['POST'])
@nocache
def delete_row(table_name, id):
    if 'username' not in session:
        return redirect(url_for('login'))

    try:
        inspector = inspect(engine)
        if table_name not in inspector.get_table_names():
            return f"Table '{table_name}' not found in the database.", 404

        db_session = OrmSession(engine)
        table_class = Base.classes[table_name]
        row = db_session.query(table_class).get(id)

        if not row:
            return f"Record with ID {id} not found in table '{table_name}'.", 404

        db_session.delete(row)
        db_session.commit()

        return redirect(url_for('view_data', table_name=table_name))
    except Exception as e:
        return f"An error occurred: {e}"

@app.route('/edit_data/<table_name>/<int:id>', methods=['GET', 'POST'])
@nocache
def edit_data(table_name, id):
    if 'username' not in session:
        return redirect(url_for('login'))

    try:
        inspector = inspect(engine)
        if table_name not in inspector.get_table_names():
            return f"Table '{table_name}' not found in the database.", 404

        db_session = OrmSession(engine)
        table_class = Base.classes[table_name]
        row = db_session.query(table_class).get(id)

        if not row:
            return f"Record with ID {id} not found in table '{table_name}'.", 404

        if request.method == 'POST':
            for key, value in request.form.items():
                if key != 'id':
                    setattr(row, key, value)
            db_session.commit()
            return redirect(url_for('view_data', table_name=table_name))

        columns = [column.name for column in table_class.__table__.columns]
        return render_template('edit_data.html', columns=columns, row=row, table_name=table_name)
    except Exception as e:
        return f"An error occurred: {e}"

@app.route('/download_csv/<table_name>', methods=['GET'])
@nocache
def download_csv(table_name):
    if 'username' not in session:
        return redirect(url_for('login'))

    try:
        inspector = inspect(engine)
        if table_name not in inspector.get_table_names():
            return f"Table '{table_name}' not found in the database.", 404

        db_session = OrmSession(engine)
        table_class = Base.classes[table_name]
        rows = db_session.query(table_class).all()
        columns = [column.name for column in table_class.__table__.columns]

        csv_data = ','.join(columns) + '\n'
        for row in rows:
            csv_data += ','.join([str(getattr(row, column)) for column in columns]) + '\n'

        response = make_response(csv_data)
        response.headers['Content-Disposition'] = f'attachment; filename={table_name}.csv'
        response.headers['Content-Type'] = 'text/csv'
        return response
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == '__main__':
    app.run(debug=True)
