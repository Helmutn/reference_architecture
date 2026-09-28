# from models.device_model import DeviceModel
from models.data_model import DataModel

from services.data_service import DataService
from services.monitoring_service import MonitoringService
from services.logging_service import LoggingService

from controllers.main_controller import MainController

from infrastructure.event_bus import EventBus
from infrastructure.thread_manager import ThreadManager


class Container:

    def __init__(self, model_address):

        self.event_bus = EventBus()

        self.model = DataModel(model_address)

        self.thread_manager = ThreadManager()

        self.data_service = DataService(self.model)

        self.logging_service = LoggingService(self.event_bus)

        self.monitoring_service = MonitoringService(self.event_bus)

        self.controller = MainController(self.model, self.data_service, self.event_bus)