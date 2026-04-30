from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# -------------------------------
# Parking Slots (x, y positions)
# -------------------------------
slots = {
    1: (0, 1),
    2: (1, 2),
    3: (2, 1),
    4: (3, 3)
}

# -------------------------------
# Destinations
# -------------------------------
destinations = {
    "Main Entrance": (0, 0),
    "Elevator": (5, 5),
    "Food Court": (8, 2),
    "Exit Gate": (0, 10)
}

# -------------------------------
# Distance Function
# -------------------------------
def distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# -------------------------------
# Root Route (IMPORTANT)
# -------------------------------
@app.route('/')
def home():
    return "Smart Parking Backend is LIVE 🚀"

# -------------------------------
# Test API Route (IMPORTANT)
# -------------------------------
@app.route('/api')
def api_test():
    return jsonify({"message": "API working ✅"})

# -------------------------------
# Quick Parking (Greedy)
# -------------------------------
def greedy_assign(destination):
    dest = destinations[destination]
    best_slot = min(slots, key=lambda s: distance(slots[s], dest))
    return best_slot, distance(slots[best_slot], dest)

# -------------------------------
# Smart Parking (DP-like)
# -------------------------------
def dp_assign(destination):
    dest = destinations[destination]

    best_slot = None
    min_dist = float('inf')

    for s in slots:
        d = distance(slots[s], dest)
        if d < min_dist:
            min_dist = d
            best_slot = s

    return best_slot, min_dist

# -------------------------------
# API: Park Car
# -------------------------------
@app.route('/api/park', methods=['POST'])
def park():
    data = request.json
    destination = data.get("destination")
    mode = data.get("mode")

    if destination not in destinations:
        return jsonify({"error": "Invalid destination"}), 400

    if mode == "greedy":
        slot, dist = greedy_assign(destination)
    else:
        slot, dist = dp_assign(destination)

    return jsonify({
        "slot": slot,
        "distance": dist
    })

# -------------------------------
# API: Compare
# -------------------------------
@app.route('/api/compare', methods=['POST'])
def compare():
    data = request.json
    destination = data.get("destination")

    if destination not in destinations:
        return jsonify({"error": "Invalid destination"}), 400

    g_slot, g_dist = greedy_assign(destination)
    d_slot, d_dist = dp_assign(destination)

    return jsonify({
        "greedy": {
            "slot": g_slot,
            "distance": g_dist
        },
        "dp": {
            "slot": d_slot,
            "distance": d_dist
        }
    })

# -------------------------------
# Run Server (Render compatible)
# -------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)