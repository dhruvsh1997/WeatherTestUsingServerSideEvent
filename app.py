from flask import Flask, Response, render_template
import random
import time
import json
from datetime import datetime

app = Flask(__name__)

# Simulated weather data
weather_data = {
    'temperature': 22.0,    # celsius
    'humidity': 65,        # percentage
    'pressure': 1013,      # hPa
    'condition': 'Partly Cloudy',
    'last_updated': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}

# Weather conditions for simulation
WEATHER_CONDITIONS = [
    'Sunny', 'Partly Cloudy', 'Cloudy', 'Light Rain', 
    'Heavy Rain', 'Thunderstorm', 'Snow'
]

def generate_weather_event():
    """Generate a new weather event with simulated data"""
    # Simulate gradual temperature changes
    weather_data['temperature'] = round(
        weather_data['temperature'] + random.uniform(-1, 1), 1
    )
    
    # Simulate humidity changes
    weather_data['humidity'] = max(30, min(95, 
        weather_data['humidity'] + random.randint(-5, 5)
    ))
    
    # Simulate pressure changes
    weather_data['pressure'] = max(990, min(1030, 
        weather_data['pressure'] + random.randint(-2, 2)
    ))
    
    # Occasionally change weather condition
    if random.random() < 0.1:  # 10% chance to change condition
        weather_data['condition'] = random.choice(WEATHER_CONDITIONS)
    
    weather_data['last_updated'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Format as SSE event
    event_data = {
        'temperature': weather_data['temperature'],
        'humidity': weather_data['humidity'],
        'pressure': weather_data['pressure'],
        'condition': weather_data['condition'],
        'timestamp': weather_data['last_updated']
    }
    
    # Create SSE message
    message = f"data: {json.dumps(event_data)}\n\n"
    return message

@app.route('/')
def dashboard():
    """Render the weather dashboard"""
    return render_template('weather_dashboard.html')

@app.route('/weather-updates')
def weather_updates():
    """SSE endpoint for weather updates"""
    def event_stream():
        while True:
            # Generate new weather data
            message = generate_weather_event()
            yield message
            print(f"Sent weather update: {message.strip()}")
            # Wait before next update
            time.sleep(1.5)
    
    return Response(
        event_stream(),
        mimetype='text/event-stream'
    )

if __name__ == '__main__':
    app.run(debug=True, threaded=True)