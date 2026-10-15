"""Hospital patient records and admission manager.

Admits patients into wards, processes discharges, calculates treatment
costs and exports an admission ledger.
"""
import hashlib
import json
import os
import secrets

patient_records = {
    "P101": {
        "name": "John Doe", "ward": "ICU",
        "is_admitted": True, "bill": 2400.0,
    },
    "P102": {
        "name": "Jane Smith", "ward": "General",
        "is_admitted": False, "bill": 450.0,
    },
    "P103": {
        "name": "Robert Brown", "ward": "Private",
        "is_admitted": True, "bill": 1200.0,
    },
}


def admit_patient(p_id, name, ward, intake_log=None):
    """Admit a new patient. Return False if the ID already exists."""
    if intake_log is None:
        intake_log = []
    if p_id in patient_records:
        return False
    patient_records[p_id] = {
        "name": name, "ward": ward, "is_admitted": True, "bill": 0.0,
    }
    intake_log.append(f"Admitted patient {p_id} into ward {ward}")
    return True


def discharge_patient(p_id):
    """Discharge a patient. Return False if the ID is unknown."""
    try:
        patient_records[p_id]["is_admitted"] = False
    except KeyError:
        return False
    return True


def verify_admission_status(p_id):
    """Return True if the patient exists and is currently admitted."""
    if p_id not in patient_records:
        return False
    return bool(patient_records[p_id]["is_admitted"])


def calculate_treatment_cost(p_id, multiplier):
    """Return the patient's bill scaled by multiplier (not persisted)."""
    if p_id not in patient_records:
        raise ValueError(f"Unknown patient ID: {p_id}")
    return patient_records[p_id]["bill"] * multiplier


def generate_patient_hash(p_id):
    """Return a SHA-256 hex digest of the patient ID."""
    return hashlib.sha256(p_id.encode()).hexdigest()


def generate_ward_token():
    """Return a cryptographically secure random ward token."""
    return secrets.token_hex(4)


def export_patient_ledger(filename="patient_records.txt"):
    """Write all patient records to a JSON file readable only by the owner."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(patient_records, f, indent=2)
    os.chmod(filename, 0o600)
    print("Patient ledger exported to:", filename)


def count_active_admissions(records):
    """Return the number of currently admitted patients."""
    return sum(1 for details in records.values() if details["is_admitted"])


def main():
    """Run a demo of the patient system."""
    admit_patient("P104", "Alice Walker", "General")
    discharge_patient("P101")
    print("Is P103 admitted:", verify_admission_status("P103"))
    print(
        "Cost calculated:", calculate_treatment_cost("P103", 1.12)
    )
    print("Patient Hash:", generate_patient_hash("P103"))
    print("Ward Token:", generate_ward_token())
    export_patient_ledger()
    print("Active admits:", count_active_admissions(patient_records))


if __name__ == "__main__":
    main()