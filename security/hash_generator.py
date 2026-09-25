import hashlib
import json


def generate_hash(event_data):
    event_string = json.dumps(event_data, sort_keys=True)

    event_hash = hashlib.sha256(
        event_string.encode("utf-8")
    ).hexdigest()

    return event_hash


if __name__ == "__main__":

    event_data = {
        "event_id": "EVT001",
        "camera_id": "CAM01",
        "event_type": "PERSON_DETECTED",
        "timestamp": "2026-09-09T18:15:30",
        "confidence": 0.91,
        "zone": "RESTRICTED_ZONE",
        "status": "UNVERIFIED"
    }

    hash_value = generate_hash(event_data)

    print("\n--- BORDER SURVEILLANCE EVENT ---")
    print(json.dumps(event_data, indent=4))

    print("\n--- SHA-256 HASH ---")
    print(hash_value)