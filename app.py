from flask import Flask, request, jsonify, render_template
import json
import random

app = Flask(__name__)

# Sample data of destinations and activities
with open('data/places.json') as f:
    PLACES = json.load(f)

def generate_itinerary(destination, budget, interests, days):
    # Filter places by destination and interests
    matching_places = [
        place for place in PLACES if destination.lower() in place['location'].lower()
        and any(interest in place['tags'] for interest in interests.split(','))
    ]

    # Check if there are matching places
    if not matching_places:
        return ["No matching places found. Please adjust your preferences."]

    # Shuffle the matching places for random selection
    random.shuffle(matching_places)

    # Basic logic to distribute the itinerary over the given days
    itinerary = []
    total_cost = 0
    daily_budget = budget / days

    for day in range(1, days + 1):
        # Ensure we cycle through the matching places
        day_plan = matching_places[(day - 1) % len(matching_places)]
        cost = day_plan['cost']  # Assuming each place has a 'cost' attribute
        total_cost += cost
        
        # Check if the cost exceeds the daily budget
        if cost > daily_budget:
            return ["Your budget does not allow for a full itinerary. Please adjust your budget or interests."]
        
        itinerary.append(f"Day {day}: Visit {day_plan['name']} - {day_plan['description']} (Cost: ${cost:.2f})")

    return itinerary

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    itinerary = generate_itinerary(
        data['destination'], float(data['budget']), data['interests'], int(data['days'])
    )
    return jsonify(itinerary=itinerary)

@app.route('/suggest', methods=['GET'])
def suggest():
    query = request.args.get('query', '').lower()
    destination_suggestions = []
    interest_suggestions = []

    # Create suggestions based on the query
    for place in PLACES:
        if query in place['location'].lower() and place['location'] not in destination_suggestions:
            destination_suggestions.append(place['location'])
        if query in place['tags']:
            interest_suggestions.append(place['tags'])

    return jsonify({
        'destinations': destination_suggestions,
        'interests': list(set(interest_suggestions))  # Remove duplicates
    })

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
