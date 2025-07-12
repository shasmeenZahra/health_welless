from agents import function_tool, RunContextWrapper
import os
import sys
sys.path.append(os.path.abspath("..")) 
from context import UserSessionContext
from datetime import datetime


@function_tool
async def progress_tracker_tool(
    context: RunContextWrapper[UserSessionContext],
    update_message: str
) -> dict:
    """
    Accepts a progress update from the user and logs it in progress_logs.
    Optionally modifies the status of the latest check-in.
    """

    today_str = datetime.today().strftime("%Y-%m-%d")

    new_log = {
        "date": today_str,
        "status": "Updated",
        "note": update_message
    }

    if context.context.progress_logs is None:
        context.context.progress_logs = []

    context.context.progress_logs.append(new_log)

    for log in context.context.progress_logs:
        if log["date"] == today_str and log.get("status") == "Scheduled":
            log["status"] = "Completed"
            log["note"] = update_message
            break

    return {
        "message": "✅ Progress updated successfully.",
        "log": new_log
    }
