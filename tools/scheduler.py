from agents import (
    function_tool,
    RunContextWrapper
)
import os
import sys
sys.path.append(os.path.abspath("..")) 
from context import UserSessionContext
from datetime import datetime, timedelta

@function_tool
async def checkin_scheduler_tool(
    context: RunContextWrapper[UserSessionContext]
) -> dict:
    """
    Schedules a recurring weekly progress check-in and stores it in context.
    Adds next 4 weeks of check-in logs.
    """

    today = datetime.today()
    weekly_logs = []

    for i in range(4):
        checkin_date = today + timedelta(weeks=i)
        weekly_logs.append({
            "date": checkin_date.strftime("%Y-%m-%d"),
            "status": "Scheduled"
        })

    if context.context.progress_logs is None:
        context.context.progress_logs = []

    context.context.progress_logs.extend(weekly_logs)

    return {
        "message": f"✅ Weekly check-ins scheduled for the next 4 weeks.",
        "checkins": weekly_logs
    }
