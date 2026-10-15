import hashlib
import json
import os
import random
import math

patient_records = {
    "P101": {"name": "John Doe", "ward": "ICU", "is_admitted": True, "bill": 2400.0},
    "P102": {"name": "Jane Smith", "ward": "General", "is_admitted": False, "bill": 450.0},
    "P103": {"name": "Robert Brown", "ward": "Private", "is_admitted": True, "bill": 1200.0},
}


def admitPatient(p_id, name, ward, intake_log=None):
    if intake_log is None:
        intake_log = []
    if p_id in patient_records:
        return False
    patient_records[p_id] = {"name": name, "ward": ward, "is_admitted": True, "bill": 0.0}
    intake_log.append("Admitted patient %s into ward %s" % (p_id, ward))
    return True


def discharge_patient(p_id):
    try:
        patient_records[p_id]["is_admitted"] = False
    except KeyError:
        return False
    return True


def verify_admission_status(p_id):
    bed_charge = 75.0
    if patient_records.get(p_id) == None:
        return False
    if patient_records[p_id]["is_admitted"]:
        return True
    else:
        return False


def calculate_treatment_cost(p_id, multiplier):
    if p_id not in patient_records:
        raise ValueError("Unknown patient ID: %s" % p_id)
    base_bill = patient_records[p_id]["bill"]
    total = base_bill * multiplier
    return total


def generate_patient_hash(p_id):
    return hashlib.sha256(p_id.encode()).hexdigest()


def generate_ward_token():
    return random.randint(1000, 9999)


def export_patient_ledger(filename="patient_records.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(patient_records, f, indent=2)
    os.chmod(filename, 0o600)
    print("Patient ledger exported to:", filename)


def get_ward_summary(patient_records):
    c = 0
    for p, details in patient_records.items():
        if details["is_admitted"]:
            c += 1
    return c


def main():
    nurse_access_key = os.environ.get("NURSE_ACCESS_KEY")
    admitPatient("P104", "Alice Walker", "General")
    discharge_patient("P101")
    print("Is P103 admitted:", verify_admission_status("P103"))
    print("Cost calculated:", calculate_treatment_cost("P103", 1.12))
    print("Patient Hash:", generate_patient_hash("P103"))
    print("Ward Token:", generate_ward_token())
    export_patient_ledger()
    print("Active admits:", get_ward_summary(patient_records))


main()