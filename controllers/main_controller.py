class MainController:

    def __init__(self, model, data_service, event_bus):
        self.model = model
        # self.logger = logger_service
        self.data_service = data_service
        self.event_bus = event_bus

    def power_on(self, ip):
        # result = self.device_service.power_on(ip)
        # if result:
        self.event_bus.emit("log", f"{ip} Powered on")

    def power_off(self, ip):
        # result = self.device_service.power_off(ip)
        # if result:
        self.event_bus.emit("log", f"{ip} Powered off")
