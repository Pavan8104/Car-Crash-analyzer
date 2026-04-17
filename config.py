# all project constants live here
# so we never have magic numbers scattered in code

# ── speed thresholds (km/h) ──────────────────
SPEED_LOW       = 30    # below this = low energy crash
SPEED_MID       = 60    # below this = medium energy crash
SPEED_HIGH      = 100   # below this = high energy crash
                        # above 100  = extreme crash

# ── risk score thresholds ────────────────────
RISK_HIGH_SCORE   = 5   # score >= this → High risk
RISK_MEDIUM_SCORE = 3   # score >= this → Medium risk

# ── physics constants ────────────────────────
GRAVITY_MS2     = 9.81  # m/s^2
KMH_TO_MS       = 1 / 3.6  # multiply kmh by this to get m/s

# ── injury count caps per risk level ─────────
MAX_INJURIES = {
    "Low":    {"Severe": 0, "Moderate": 1, "Minor": 3},
    "Medium": {"Severe": 1, "Moderate": 3, "Minor": 3},
    "High":   {"Severe": 4, "Moderate": 4, "Minor": 3},
}

# ── alert channels ───────────────────────────
CHANNEL_4G        = "4G / 5G"
CHANNEL_SMS       = "SMS + App Push"
CHANNEL_SATELLITE = "Satellite"

# ── G-force thresholds ───────────────────────
# above these levels the human body starts to suffer
GFORCE_MINOR      = 4    # minor soft tissue
GFORCE_MODERATE   = 10   # rib fractures possible
GFORCE_SEVERE     = 20   # life-threatening injuries
GFORCE_FATAL_RISK = 40   # survivability drops sharply

# ── health score weights ─────────────────────
# used by health_monitor.py
HEALTH_WEIGHTS = {
    "ncap_stars":      0.30,  # safety rating matters most
    "airbag_ok":       0.20,  # airbag system readiness
    "crumple_quality": 0.20,  # crumple zone efficiency
    "belt_status":     0.15,  # seatbelt worn
    "speed_margin":    0.15,  # how far under care-key limit
}
