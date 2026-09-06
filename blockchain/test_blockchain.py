from blockchain import Blockchain


blockchain = Blockchain()


event = {
    "camera_id": "CAM-01",
    "person_id": 1,
    "event_type": "Restricted Zone Intrusion",
    "severity": "HIGH"
}


block = blockchain.add_event(event)


print("\n==============================")
print("     BLOCKCHAIN RECORD")
print("==============================")

print("Block Index   :", block["index"])
print("Timestamp     :", block["timestamp"])
print("Event         :", block["event"])
print("Previous Hash :", block["previous_hash"])
print("Hash          :", block["hash"])


print("\n==============================")
print("Blockchain Valid:", blockchain.verify_chain())
print("==============================")