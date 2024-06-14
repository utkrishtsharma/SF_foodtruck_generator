import pandas as pd
from flask import Flask, render_template, request
import os
import re
from math import ceil

app = Flask(__name__)

# Load data
data_file = 'data/food_trucks.csv'
food_trucks = pd.read_csv(data_file)

# Function to create a safe filename
def safe_filename(name):
    return re.sub(r'[^a-zA-Z0-9_-]', '_', name.lower())

# Function to safely convert to string
def safe_str(value):
    try:
        return str(value).lower()
    except Exception:
        return ''

# Collect information for index
food_truck_info = []
for _, row in food_trucks.iterrows():
    filename = f"{safe_filename(row['Applicant'])}.html"
    food_truck_info.append({
        'name': row['Applicant'],
        'filename': filename,
        'location': f"{row['LocationDescription']}, {row['Address']}",
        'facility_type': row['FacilityType'],
        'food_items': safe_str(row['FoodItems']),  # Ensure correct key usage and convert to string
        'schedule': row['Schedule'],
        'days_hours': row['dayshours'],
        'status': row['Status'],
        'address': row['Address'],
        'latitude': row['Latitude'],
        'longitude': row['Longitude'],
        'google_maps_url': f"https://www.google.com/maps?q={row['Latitude']},{row['Longitude']}"
    })

@app.route('/')
@app.route('/page/<int:page>')
def index(page=1):
    per_page = 6
    search_query = request.args.get('search')
    if search_query:
        filtered_food_trucks = [truck for truck in food_truck_info if search_query.lower() in truck['food_items']]
    else:
        filtered_food_trucks = food_truck_info
    total = len(filtered_food_trucks)
    pages = ceil(total / per_page)
    start = (page - 1) * per_page
    end = start + per_page
    food_trucks_page = filtered_food_trucks[start:end]
    return render_template('index.html', food_trucks=food_trucks_page, page=page, pages=pages, search_query=search_query)

@app.route('/food_trucks/<filename>')
def food_truck(filename):
    for truck in food_truck_info:
        if truck['filename'] == filename:
            return render_template('base.html', **truck)
    return "Food truck not found", 404

if __name__ == '__main__':
    app.run(debug=True)
