# Mission to Touch Down 🚀

A challenging space landing game built with Pygame where you must safely land your spacecraft on various celestial bodies, each with unique conditions and challenges.

## Features

- Multiple landing environments (Moon, Mars, Earth, Europa, Mystery Planet X)
- Realistic physics simulation
- Atmospheric effects and wind resistance
- Fuel management
- Visual landing aids and feedback
- Parachute deployment system
- Detailed HUD with critical flight data

## Installation

1. Clone this repository:
```bash
git clone https://github.com/YOUR_USERNAME/mission-to-touchdown.git
cd mission-to-touchdown
```

2. Create and activate a virtual environment (optional but recommended):
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## How to Play

Run the game:
```bash
python planet_lander.py
```

### Controls
- ↑ (Up Arrow): Fire main engine
- ← (Left Arrow): Move left
- → (Right Arrow): Move right
- SPACE: Deploy parachute (when in atmosphere)
- ESC: Quit game

### Landing Requirements
For a successful landing:
- Land on the designated landing pad
- Vertical speed must be less than 2 m/s
- Horizontal speed must be less than 1 m/s
- Don't run out of fuel!

## Game Environments

- **Moon**: Low gravity, no atmosphere - perfect for beginners
- **Mars**: Medium gravity, thin atmosphere with dust storms
- **Earth**: Strong gravity, thick atmosphere with strong winds
- **Europa**: Very low gravity, no atmosphere, icy surface
- **Mystery Planet X**: Random conditions for an extra challenge!

## Contributing

Feel free to fork this repository and submit pull requests with improvements! 