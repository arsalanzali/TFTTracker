# app.py
import csv
from flask import Flask, render_template, request, flash, redirect, url_for
import main

app = Flask(__name__)

app.secret_key = 'sameeWarwickShyvanna'
@app.route('/', methods=['GET', 'POST'])
def index():
    augments_data = []
    units_data = []
    comp_data = []
    traits_data = []

    if request.method == 'POST':
        region = request.form['region']
        username = request.form['username']

        # Run the main script
        main.run_main(username, region)

        # Read augments.csv
        with open('augments.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            augments_data = list(reader)

        # Read traits.csv
        with open('traits.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            traits_data = list(reader)

        # Read units.csv
        with open('units.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            units_data = list(reader)

        # Read comp.csv
        with open('comp.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            comp_data = list(reader)

    return render_template('index.html', augments=augments_data, units=units_data, comp=comp_data, traits=traits_data)

if __name__ == '__main__':
     app.run(host='0.0.0.0', port=5000)
