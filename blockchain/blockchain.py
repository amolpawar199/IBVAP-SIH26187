import hashlib
import json 
import os 
from datetime import datetime


class Blockchain:

    def __init__(self):
        self.chain = []

        # Create first block
        self.create_block(
            event_data="GENESIS",
            previous_hash="0"
        )

    # --------------------------------------------------
    # CREATE HASH
    # --------------------------------------------------

    def calculate_hash(self, block):

        block_string = json.dumps(
            block,
            sort_keys=True
        )

        return hashlib.sha256(
            block_string.encode()
        ).hexdigest()

    # --------------------------------------------------
    # CREATE BLOCK
    # --------------------------------------------------

    def create_block(
        self,
        event_data,
        previous_hash
    ):

        block = {

            "index": len(self.chain),

            "timestamp": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

            "event": event_data,

            "previous_hash": previous_hash
        }

        # Generate block hash
        block["hash"] = self.calculate_hash(block)

        self.chain.append(block)

        return block

    # --------------------------------------------------
    # ADD SECURITY EVENT
    # --------------------------------------------------

    def add_event(self, event_data):

        previous_hash = self.chain[-1]["hash"]

        return self.create_block(
            event_data,
            previous_hash
        )

    # --------------------------------------------------
    # VERIFY BLOCKCHAIN
    # --------------------------------------------------

    def verify_chain(self):

        for i in range(1, len(self.chain)):

            current_block = self.chain[i]

            previous_block = self.chain[i - 1]

            # Check previous hash
            if current_block["previous_hash"] != previous_block["hash"]:
                return False

            # Recalculate current hash
            block_without_hash = {
                "index": current_block["index"],
                "timestamp": current_block["timestamp"],
                "event": current_block["event"],
                "previous_hash": current_block["previous_hash"]
            }

            recalculated_hash = self.calculate_hash(
                block_without_hash
            )

            # Check current hash
            if current_block["hash"] != recalculated_hash:
                return False

        return True