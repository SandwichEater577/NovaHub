import time
import threading
import os


class ValyxoJobsManager:
    def __init__(self):
        self.jobs = {}
        self.job_counter = 0
        self.lock = threading.Lock()

    def create_job(self, filepath):
        with self.lock:
            self.job_counter += 1
            pid = self.job_counter
            self.jobs[pid] = {
                "path": filepath,
                "status": "running",
                "thread": None,
                "start": time.time(),
                "stop": False
            }
            return pid

    def update_status(self, pid, status):
        with self.lock:
            if pid in self.jobs:
                self.jobs[pid]["status"] = status

    def stop_job(self, pid):
        with self.lock:
            if pid in self.jobs:
                self.jobs[pid]["stop"] = True
                self.jobs[pid]["status"] = "terminating"

    def list_jobs(self):
        with self.lock:
            for pid, info in sorted(self.jobs.items()):
                age = int(time.time() - info.get("start", time.time()))
                print(f"#{pid} {os.path.basename(info['path'])} [{info['status']}] ({age}s)")
