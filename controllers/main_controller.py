class MainController:

    def __init__(
        self,
        model,
        device_service,
        monitoring_service,
        logger_service,
    ):

        self.model = model
        self.device_service = device_service
        self.monitoring_service = monitoring_service
        self.logger = logger_service

    def power_on(self, ip):
        result = self.device_service.power_on(ip)
        if result:
            self.logger.log(f"{ip} eingeschaltet")

    def power_off(self, ip):
        result = self.device_service.power_off(ip)
        if result:
            self.logger.log(f"{ip} ausgeschaltet")