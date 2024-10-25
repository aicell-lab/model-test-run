from typing import List, Callable, Any
from hypha.connection import Hypha
import inspect

def service_method(func):
    func._is_service = True
    return func

class ServiceRegistry:
    def __init__(self):
        ...

    @service_method
    def hello_world_task(self, context=None) -> str:
        return "hello world!"
    
    def _get_service_methods(self) -> List[Callable]:
        """Collect only methods marked as service methods."""
        methods = inspect.getmembers(self, predicate=inspect.ismethod)
        return [method for _, method in methods if getattr(method, '_is_service', False)]
    
    def get_services(self) -> List[Callable]:
        return self._get_service_methods()

async def register_services():
    services = ServiceRegistry().get_services()
    server = await Hypha.authenticate()
    if server:
        service_info = await Hypha.register_service(server_handle=server, callbacks=services)
        Hypha.print_services(service_info=service_info, callbacks=services)
