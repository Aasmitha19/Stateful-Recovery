from rocksdict import Rdict
import json
import os


class StateStore:

    def __init__(self):
        os.makedirs("state", exist_ok=True)
        self.db = Rdict("state/rocksdb")

    def save(self, truck_id, total, count):
        self.db[truck_id] = json.dumps({
            "total": total,
            "count": count
        })
        self.db.flush()

    def load(self, truck_id):
        data = self.db.get(truck_id)

        if data is None:
            return {"total": 0, "count": 0}

        return json.loads(data)

    def close(self):
        self.db.close()