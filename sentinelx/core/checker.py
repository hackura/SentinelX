
import shutil
from sentinelx.core.logger import log

def check_tool(tool_name):
    path = shutil.which(tool_name)
    if path:
        return path
    else:
        return None

def validate_tools(tool_config):
    missing = []
    for category in tool_config:
        for tool, details in tool_config[category].items():
            path = check_tool(details["path"])
            if not path:
                log.warning(f"Tool missing: {tool} (expected at {details["path"]})")
                missing.append(tool)
            else:
                log.debug(f"Tool found: {tool} at {path}")
    return missing
