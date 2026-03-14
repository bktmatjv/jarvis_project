from jarvis_scripts.script_manager import get_script
from tool_registry import get_tool


def execute(action: dict):

    print("EXECUTOR RECEIVED:", action)

    if not action:
        print("No action received")
        return


    # TOOL SYSTEM

    tool_name = action.get("tool")

    if tool_name:

        params = action.get("params", {})

        tool = get_tool(tool_name)

        if not tool:
            print("Tool not found:", tool_name)
            return

        print("Running tool:", tool_name)

        tool(params)

        return


    # SCRIPTS

    if action.get("action") == "run_script":

        script_name = action.get("name")

        script = get_script(script_name)

        if not script:
            print("Script not found")
            return

        for step in script:
            execute(step)