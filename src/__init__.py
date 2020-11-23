import logging
import sys

from .manager import Manager
from .exceptions import FlowError, InfoFlowError

DOMAIN = "flow_automation"

logger = logging.getLogger(__name__)


def async_safecall(func):
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except:
            logger.exception("Something went wrong", exc_info=sys.exc_info())

            return False

    return wrapper


@async_safecall
async def async_setup(hass, config):
    domain_cfg = config[DOMAIN]

    if "flows" not in domain_cfg:
        logger.debug("Loading flow_assistant integration is not configurred. Skipping.")

        return True

    flows = domain_cfg["flows"]

    manager = Manager(hass.config_entries.async_entries(), hass.config_entries.flow)

    for flow_data in flows:
        flow_key = manager.key(flow_data)

        if "steps" not in flow_data:
            logger.warning(f"Flow {flow_key} was skipped because it has no steps.")

            continue

        try:
            flow = await manager.add_flow(flow_data)

            for id, step_data in enumerate(flow_data["steps"]):
                await manager.add_step(flow, step_data, id + 1)
        except InfoFlowError as e:
            logger.info(str(e))

            continue
        except FlowError as e:
            logger.exception(e)

            continue

        logger.info(f"Integration {flow_key} was added")

    return True


def _key(entry):
    return f"{entry['domain']}|{entry['title']}"