from assemblyline_v4_service.common.base import ServiceBase
from assemblyline_v4_service.common.request import ServiceRequest
from assemblyline_v4_service.common.result import Result


class MBInfo(ServiceBase):
    def start(self):
        self.log.info(f"start() from {self.service_attributes.name} service called")

    def execute(self, request: ServiceRequest) -> None:
        request.result = Result()
        self.log.info(f"Got new file {request.sha256}")
