from homeassistant.data_entry_flow import RESULT_TYPE_FORM, RESULT_TYPE_CREATE_ENTRY
from homeassistant import config_entries
from .flow import Flow
from .step import Step
from .exceptions import AlreadyExistsError, UnknownFlowTypeError


class Manager:
    def __init__(
        self,
        entities,
        flow_manager: config_entries.ConfigEntriesFlowManager,
    ) -> None:
        self.flow_manager = flow_manager
        self.entities = [
            self.key({"domain": entry.domain, "title": entry.title})
            for entry in entities
        ]

    async def add_flow(self, flow) -> Flow:
        handler = flow["domain"]
        flow_key = self.key(flow)

        if flow_key in self.entities:
            raise AlreadyExistsError(f"Flow {flow_key} is already configured")

        res = await self.flow_manager.async_init(
            handler,
            context={
                "source": config_entries.SOURCE_USER,
                "show_advanced_options": True,
            },
        )

        type = res["type"]

        if type not in [RESULT_TYPE_FORM, RESULT_TYPE_CREATE_ENTRY]:
            raise UnknownFlowTypeError(f"Unknown type {type} for flow {flow_key}")

        return Flow(res, flow_key)

    async def add_step(self, flow: Flow, step, id) -> Step:
        flow_key = flow.key()

        res = await self.flow_manager.async_configure(flow.id(), step)

        type = res["type"]

        if type not in [RESULT_TYPE_FORM, RESULT_TYPE_CREATE_ENTRY]:
            raise UnknownFlowTypeError(
                f"Unknown type {type} for flow {flow_key} on step {id}"
            )

        return Step(res)

    def key(self, entry):
        return f"{entry['domain']}|{entry['title']}"