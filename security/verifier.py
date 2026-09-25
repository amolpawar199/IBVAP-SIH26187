import hashlib
import json


def generate_hash(event_data):
    event_string = json.dumps(event_data, sort_keys=True)
    return hashlib.sha256(event_string.encode("utf-8")).hexdigest()


def verify_hash(event_data, stored_hash):
    new_hash = generate_hash(event_data)
    return new_hash == stored_hash


# ORIGINAL EVENT
original_event = {
    "event_id": "EVT001",
    "camera_id": "CAM01",
    "event_type": "PERSON_DETECTED",
    "timestamp": "2026-09-09T18:15:30",
    "confidence": 0.91,
    "zone": "RESTRICTED_ZONE",
    "status": "UNVERIFIED"
}

# Generate hash BEFORE any modification
stored_hash = generate_hash(original_event)

print("\nOriginal Hash:")
print(stored_hash)


# SIMULATE DATA TAMPERING
modified_event = original_event.copy()
modified_event["confidence"] = 0.75 
print("TEST: modified confidence =", modified_event["confidence"])

print("\nModified confidence:")
print(modified_event["confidence"])


# Verify modified data against ORIGINAL stored hash
result = verify_hash(modified_event, stored_hash)

print("\nVerification Result:")

if result:
    print("✓ DATA AUTHENTIC - HASH MATCH")
else:
    print("⚠ DATA TAMPERED - HASH MISMATCH")
    