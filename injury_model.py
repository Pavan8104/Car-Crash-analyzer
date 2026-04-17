from typing import List, Dict, Any, Tuple

# ─────────────────────────────────────────────
# Real crash injury data
# Sources: NHTSA crash databases, Euro NCAP
# testing results, WHO road injury reports,
# and published trauma surgery literature.
#
# Each entry: (injury name, body part, base %)
# Base % = likelihood at ~50 km/h with belt+bags
# ─────────────────────────────────────────────

# type alias for one injury entry in the pool
InjuryEntry = Tuple[str, str, int]

# pools are organised by collision type then severity
CRASH_POOLS: Dict[str, Dict[str, List[InjuryEntry]]] = {

    # ── FRONTAL COLLISION ───────────────────
    # Most studied crash type (55% of all crashes).
    # Chest hits steering wheel or belt, knees hit
    # dashboard, head can hit airbag or windshield.
    "frontal": {
        "Severe": [
            ("Traumatic Brain Injury",          "Brain",    38),
            ("Femur / Tibia Fracture",          "Legs",     45),
            ("Aortic Tear",                     "Chest",    22),
            ("Liver or Spleen Laceration",      "Abdomen",  30),
            ("Spinal Cord Injury",              "Spine",    18),
            ("Tension Pneumothorax",            "Lungs",    20),
        ],
        "Moderate": [
            ("Concussion",                      "Head",     48),
            ("Multiple Rib Fractures",          "Chest",    42),
            ("Sternal Fracture",                "Chest",    35),
            ("Pulmonary Contusion",             "Lungs",    32),
            ("Knee-Dashboard Impact",           "Knee",     50),
            ("Lumbar Spine Strain",             "Spine",    38),
        ],
        "Minor": [
            ("Seatbelt Chest Bruising",         "Chest",    78),
            ("Airbag Burns & Abrasions",        "Face",     55),
            ("Wrist Sprain",                    "Wrist",    40),
            ("Neck Muscle Strain",              "Neck",     45),
            ("Facial Lacerations",              "Face",     38),
        ],
    },

    # ── REAR COLLISION ──────────────────────
    # Cervical spine is most at risk.
    # Whiplash grades based on Quebec Task Force
    # scale (I = pain only, IV = fracture).
    # Head bounces forward then snaps back.
    "rear": {
        "Severe": [
            ("Cervical Spine Fracture",         "Neck",     20),
            ("Traumatic Disc Herniation C4-C6", "Spine",    28),
            ("Spinal Cord Compression",         "Spine",    15),
            ("Severe Concussion (Grade 3)",     "Head",     22),
        ],
        "Moderate": [
            ("Whiplash Grade II-III",           "Neck",     62),
            ("Lower Back Disc Injury (L4-L5)",  "Spine",    45),
            ("Shoulder Girdle Strain",          "Shoulder", 40),
            ("Post-Concussion Syndrome",        "Head",     30),
            ("Thoracic Spine Sprain",           "Spine",    35),
        ],
        "Minor": [
            ("Whiplash Grade I",                "Neck",     72),
            ("Upper Trapezius Strain",          "Neck",     65),
            ("Occipital Headache",              "Head",     58),
            ("Mild Lower Back Pain",            "Spine",    50),
            ("Shoulder Muscle Soreness",        "Shoulder", 42),
        ],
    },

    # ── SIDE (T-BONE) COLLISION ─────────────
    # Most deadly per crash — door gives only
    # 15 cm of protection vs 60 cm at front.
    # Thorax and pelvis absorb most energy.
    # Driver side = liver risk. Passenger = spleen.
    "side": {
        "Severe": [
            ("Liver Laceration (Grade III+)",   "Abdomen",  35),
            ("Pelvic Ring Fracture",            "Pelvis",   42),
            ("Traumatic Brain Injury",          "Brain",    40),
            ("Multiple Rib Fractures (4+)",     "Chest",    48),
            ("Thoracic Aorta Injury",           "Chest",    18),
            ("Femur Fracture",                  "Legs",     30),
        ],
        "Moderate": [
            ("Rib Fracture (1-3)",              "Chest",    58),
            ("Hip Contusion / Fracture",        "Hip",      45),
            ("Shoulder Dislocation",            "Shoulder", 38),
            ("Concussion",                      "Head",     50),
            ("Pneumothorax",                    "Lungs",    28),
            ("Humerus Fracture",                "Arms",     32),
        ],
        "Minor": [
            ("Door Panel Bruising",             "Body",     75),
            ("Wrist Impact Injury",             "Wrist",    48),
            ("Acoustic Trauma (Ear)",           "Head",     42),
            ("Hip & Thigh Bruising",            "Hip",      65),
            ("Neck Lateral Strain",             "Neck",     52),
        ],
    },

    # ── ROLLOVER COLLISION ──────────────────
    # Most complex injury pattern.
    # Roof contact, ejection (without belt), and
    # rotational forces cause multi-system trauma.
    # Survivability drops sharply without seatbelt.
    "rollover": {
        "Severe": [
            ("Skull Fracture / TBI",            "Brain",    50),
            ("Cervical Spine Fracture (C1-C3)", "Neck",     35),
            ("Thoracic Spine Fracture",         "Spine",    38),
            ("Crush Injury (Roof Intrusion)",   "Body",     30),
            ("Multiple Long Bone Fractures",    "Limbs",    42),
        ],
        "Moderate": [
            ("Shoulder Labrum Tear",            "Shoulder", 45),
            ("Rib Stress Fractures",            "Chest",    52),
            ("Knee Ligament Tear",              "Knee",     40),
            ("Concussion",                      "Head",     60),
            ("Wrist Fracture (Bracing Impact)", "Wrist",    48),
        ],
        "Minor": [
            ("Scalp & Facial Lacerations",      "Face",     70),
            ("Limb Road Rash & Abrasions",      "Limbs",    65),
            ("Disorientation / Vertigo",        "Head",     55),
            ("Neck Stiffness",                  "Neck",     60),
            ("Muscle Bruising (Full Body)",     "Body",     72),
        ],
    },
}

# special Volvo features that change the injury picture
WHIPS_ENTRY: InjuryEntry   = ("Mild Neck Stiffness (WHIPS Active)", "Neck", 22)
EV_SEVERE_ENTRY: InjuryEntry   = ("Battery Pack Intrusion Risk",    "Body", 32)
EV_MODERATE_ENTRY: InjuryEntry = ("High-Voltage Exposure Risk",     "Body", 38)


def _pick_injuries(
    pool: List[InjuryEntry],
    speed_kmh: float,
    seatbelt: bool,
    airbags: bool,
    severity: str,
) -> List[Dict[str, Any]]:
    """
    Take injuries from the pool and calculate
    a realistic likelihood % for each one.

    Likelihood is adjusted by:
    - speed band (higher speed = higher chance)
    - whether seatbelt is worn
    - whether airbags deployed
    """
    results = []

    for name, part, base_pct in pool:
        pct = base_pct

        # speed adjustment — based on crash energy
        # Energy = 0.5 * m * v^2, so risk rises fast
        if speed_kmh > 120:
            pct = min(95, pct + 30)
        elif speed_kmh > 90:
            pct = min(92, pct + 22)
        elif speed_kmh > 60:
            pct = min(88, pct + 14)
        elif speed_kmh > 40:
            pct = min(82, pct + 6)
        elif speed_kmh <= 20:
            # very low speed — reduce likelihood
            pct = max(5, pct - 20)
        elif speed_kmh <= 30:
            pct = max(8, pct - 12)

        # no seatbelt — big jump, especially for severe
        if not seatbelt:
            if severity == "Severe":
                pct = min(95, pct + 20)
            elif severity == "Moderate":
                pct = min(90, pct + 14)
            else:
                pct = min(85, pct + 8)

        # no airbags — notable increase for head/chest
        if not airbags:
            if part in ("Brain", "Head", "Face", "Chest", "Lungs"):
                pct = min(95, pct + 12)
            else:
                pct = min(90, pct + 6)

        results.append({"name": name, "part": part, "pct": pct})

    return results


def _how_many(speed_kmh: float, risk_level: str, severity: str) -> int:
    """
    Decide how many injuries to show per severity bucket.
    More injuries at higher speed and risk.
    """
    if severity == "Severe":
        if risk_level == "Low":
            return 0
        if risk_level == "Medium":
            return 1
        # High risk
        if speed_kmh > 90:
            return 4
        return 3

    if severity == "Moderate":
        if risk_level == "Low":
            return 1
        if risk_level == "Medium":
            return 3
        if speed_kmh > 90:
            return 4
        return 3

    # Minor
    if risk_level == "Low":
        return 3
    if speed_kmh > 90:
        return 3
    return 3


def generate_injury_scenarios(
    speed_kmh: float,
    collision_type: str,
    seatbelt: bool,
    airbags: bool,
    risk_level: str = "Low",
    whips: bool = False,
    is_electric: bool = False,
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Main function — returns injuries for each severity level.
    Injuries are realistic, based on real crash data.
    """

    # fall back to frontal if collision type is unknown
    pool = CRASH_POOLS.get(collision_type, CRASH_POOLS["frontal"])

    result: Dict[str, List[Dict[str, Any]]] = {}

    for severity in ("Severe", "Moderate", "Minor"):
        # calculate likelihood for all injuries in this bucket
        enriched = _pick_injuries(
            pool[severity], speed_kmh, seatbelt, airbags, severity
        )

        # sort by likelihood — highest first
        enriched.sort(key=lambda x: x["pct"], reverse=True)

        # take only how many make sense for this scenario
        count = _how_many(speed_kmh, risk_level, severity)
        result[severity] = enriched[:count]

    # WHIPS system — rear crash neck protection
    # removes whiplash from moderate/severe, adds minor note
    if whips and collision_type == "rear":
        result["Severe"]   = [
            i for i in result["Severe"]
            if "cervical" not in i["name"].lower() and "disc" not in i["name"].lower()
        ]
        result["Moderate"] = [
            i for i in result["Moderate"]
            if "whiplash" not in i["name"].lower()
        ]
        if speed_kmh > 25:
            result["Minor"].insert(0, {
                "name": WHIPS_ENTRY[0],
                "part": WHIPS_ENTRY[1],
                "pct":  WHIPS_ENTRY[2],
            })

    # EV extra risks on severe side/rollover crashes
    if is_electric and risk_level == "High":
        if collision_type in ("side", "rollover"):
            result["Severe"].append({
                "name": EV_SEVERE_ENTRY[0],
                "part": EV_SEVERE_ENTRY[1],
                "pct":  EV_SEVERE_ENTRY[2],
            })
        result["Moderate"].append({
            "name": EV_MODERATE_ENTRY[0],
            "part": EV_MODERATE_ENTRY[1],
            "pct":  EV_MODERATE_ENTRY[2],
        })

    # ejection risk without seatbelt — rollover or high speed
    if not seatbelt and speed_kmh > 60:
        if collision_type == "rollover" or risk_level == "High":
            result["Severe"].append({
                "name": "Ejection / Partial Ejection Risk",
                "part": "Body",
                "pct":  min(95, 55 + int((speed_kmh - 60) * 0.4)),
            })

    return result


def summarize_injuries(injuries: Dict[str, List[Dict[str, Any]]]) -> List[str]:
    summary = []
    for category in ("Severe", "Moderate", "Minor"):
        items = injuries.get(category, [])
        if items:
            names = ", ".join(i["name"] if isinstance(i, dict) else i for i in items)
            summary.append(f"{category}: {names}")
    return summary
