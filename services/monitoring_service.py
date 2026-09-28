import time
import random


class MonitoringService:

    def __init__(self, event_bus):
        self.event_bus = event_bus
        self.running = False

    def start(self):
        self.running = True
        while self.running:
            status = random.choice(["ONLINE", "OFFLINE", "UNKNOWN", "INACTIVE", "ACTIVE"])
            self.event_bus.emit("device_status", status)
            time.sleep(2)

    def stop(self):
        self.running = False