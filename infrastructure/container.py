from models.device_model import DeviceModel

from services.device_service import DeviceService
from services.monitoring_service import MonitoringService
from services.logging_service import LoggingService

from controllers.main_controller import MainController

from infrastructure.event_bus import EventBus
from infrastructure.thread_manager import ThreadManager


class Container:

    def __init__(self):

        self.event_bus = EventBus()

        self.model = DeviceModel()

        self.thread_manager = ThreadManager()

        self.device_service = DeviceService()

        self.logging_service = LoggingService(
            self.event_bus
        )

        self.monitoring_service = MonitoringService(
            self.event_bus
        )

        self.controller = MainController(
            self.model,
            self.device_service,
            self.monitoring_service,
            self.logging_service
        )