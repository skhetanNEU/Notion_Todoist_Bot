import time
import pytz
import json
import datetime
from todoist_api_python.api import TodoistAPI
from keep_alive import keep_alive

# To keep the server alive
keep_alive()

# Load the json file to get the todoist id
file = open('secret.json')
data = json.load(file)
todoistId = data['todoistId']
api = TodoistAPI(todoistId)


# Method to delete the older tasks in todoist
def delete_older_tasks():
    try:
        old_tasks = []

        tasks = api.get_tasks()
        for task in tasks:
            label = getattr(task, 'labels')
            if "Added_to_Notion" in label:
                old_tasks.append(task)

        # Iterate through the older tasks and delete them
        for task in old_tasks:
            task_id = getattr(task, 'id')
            api.delete_task(task_id=task_id)

    except Exception as error:
        print(error)


def main():
    while True:
        central_time_zone = pytz.timezone('US/Central')
        central_time_zone_time = datetime.datetime.now(central_time_zone)
        if central_time_zone_time.hour == 0 and 1 < central_time_zone_time.minute < 59:
            delete_older_tasks()

        # Run the next iteration after 40 minutes
        time.sleep(2400)


if __name__ == "__main__":
    main()
