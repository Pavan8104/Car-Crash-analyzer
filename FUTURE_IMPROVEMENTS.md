# Future Improvements

## 1. Vehicle-Specific Physics

The impact force calculation assumes a fixed 1500 kg mass and 0.1s stopping time. A hatchback and an SUV crash very differently. Adding vehicle mass as a user input, along with crumple zone length, would make the physics output much more accurate. A vehicle type selector (sedan, SUV, truck) with preset values would be the easiest way to do this.

## 2. ML-Based Injury Prediction

The injury model runs on hand-written if/else rules. It gets the basics right but can't account for passenger age, road surface, or pre-existing conditions. Training a small decision tree or logistic regression model on NHTSA crash data would replace the guesswork with something backed by real-world numbers.

## 3. Per-Occupant Analysis

Every crash analysis currently treats the vehicle as having one generic occupant. In practice, the driver, front passenger, and rear passengers all face different risks. The system should accept a list of occupants — seat position, age, seatbelt — and produce a separate injury breakdown for each one.

## 4. Saving Results

Results disappear after each run. A SQLite database or even a CSV log would fix this. Once stored, a history view in the UI becomes possible, along with PDF export for documentation or insurance purposes.

## 5. Crash Location on a Map

If the crash coordinates are known, plotting them on a map gives immediate context — speed limits, road type, nearby intersections. OpenStreetMap via Folium would handle this without any paid API keys.

## 6. More Specific Emergency Guidance

The current safety suggestions say things like "seek immediate medical evaluation." That's too vague. Based on severity, the tool should distinguish between calling 911 on the spot, going to urgent care within hours, or watching for delayed symptoms at home.

## 7. Mobile-Friendly UI

The Streamlit interface works on desktop but not on a phone. A PWA wrapper or a lightweight React frontend over the Flask API would make it usable at the roadside. Voice input would be a further improvement for hands-free entry.

## 8. Tests

No tests exist for any module. The physics formulas, risk scoring, and injury logic all need pytest coverage — especially edge cases like speed = 0, speed = 250, and every combination of seatbelt/airbag.

## 9. API Docs

The Flask endpoints have no documentation. Adding Swagger via Flasgger would make the API usable by third parties without digging through the source.

## 10. Two-Vehicle Collisions

The system only models single-vehicle scenarios. Head-on and T-bone crashes involve two vehicles with different speeds and masses. The physics module needs to accept both vehicle profiles and compute the energy exchange between them.

---

**Start here:**
- Add vehicle mass input — 30 min, immediate accuracy gain
- SQLite result logging — 1 hr, unlocks history
- pytest for physics.py and predictor.py — 1–2 hrs, prevents regressions
- PDF export in Streamlit — 2 hrs, makes it presentable
