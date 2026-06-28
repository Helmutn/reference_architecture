class LoggingService:

    def __init__(self, event_bus):
        self.event_bus = event_bus

    def log(self, message):
        self.event_bus.emit("log", message)