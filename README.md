# Crash Analysis & Injury Prediction System

A practical engineering tool for simulating vehicle crash scenarios, calculating impact physics, predicting injury risk, and generating realistic injury scenarios.

## Features

- Modular Python backend with separate physics, prediction, and injury model components
- Input validation and structured report output
- Command-line interface for crash simulation
- Streamlit frontend with a clean, professional UI
- Rule-based injury predictions dependent on speed, collision type, seatbelt use, and airbag presence

## Tech Stack

- Python 3
- Streamlit for frontend UI

## How to Run

### Install dependencies

```bash
python3 -m pip install -r requirements.txt
```

### Run CLI analysis

```bash
python main.py --speed 70 --collision side --seatbelt --airbags
```

### Run Streamlit UI

```bash
streamlit run streamlit_app.py
```

## Example Usage

```bash
python main.py --speed 80 --collision frontal --seatbelt --airbags --json
```

### Sample Output

```json
{
  "summary": {
    "risk_level": "Medium",
    "impact_force_kN": 400.0,
    "impact_energy_kJ": 425.9
  },
  "injuries": {
    "Minor": [],
    "Moderate": ["rib fracture", "disorientation"],
    "Severe": ["arm fracture", "organ damage", "spinal injury", "pelvis fracture"]
  },
  "safety_suggestions": [
    "Check vehicle deformation and report pain in neck, chest, or abdomen."
  ]
}
```

## Future Improvements

- Add more detailed vehicle and occupant profiles
- Introduce damage severity scoring and confidence ranges
- Add historical crash scenario templates and report export
- Expand UI with scenario comparison and charts 
This is only idea for education
