# Import necessary modules from Flask and other libraries
from flask import Flask, render_template, request, redirect
import sqlite3
import shortuuid

# create flask app
app = Flask(__name__)

# create a SQLite database and table to store urls
conn = sqlite3.connect('urls.db')
conn.execute('CREATE TABLE IF NOT EXISTS urls (id INTEGER PRIMARY KEY AUTOINCREMENT, short TEXT, long TEXT)')
conn.commit()
conn.close()

# Define the route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# define the route for URL shortening
@app.route('/shorten', methods=['POST'])
def shorten():
    # extract the long URL
    long_url = request.form['long_url']

    # generate a unique short code using shortuuid
    short_code = shortuuid.uuid()[:8]

    # save the mapping to the database
    conn = sqlite3.connect('urls.db')
    conn.execute('INSERT INTO urls (short, long) VALUES (?, ?)', (short_code, long_url))
    conn.commit()
    conn.close()

    # create the shortened URL
    short_url = f"{request.host_url}{short_code}"

    # render the template with the shortened URL
    return render_template('index.html', short_url=short_url)

# define the route for URL redirect
@app.route('/<short_code>')
def redirect_to_long(short_code):
    # get the long URL from the database based on the short code
    conn = sqlite3.connect('urls.db')
    result = conn.execute('SELECT long FROM urls WHERE short = ?', (short_code,)).fetchone()
    conn.close()

    # redirect to the long URL if found, if not found return a 404 error
    if result:
        long_url = result[0]
        return redirect(long_url)
    else:
        return "URL not found", 404

# run the development server only if this script is executed as the main program
if __name__ == '__main__':
    app.run(debug=True)

