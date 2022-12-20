import json
import requests
import time
import pytz
from datetime import timedelta
from datetime import datetime as dt
from keep_alive import keep_alive

keep_alive()

file = open('secret.json')
data = json.load(file)
notionId = data['notionId']
tasksDatabase = data['tasksDatabase']

url = "https://api.notion.com/v1/databases/" + tasksDatabase + "/query"
payload = {"page_size": 100}
headers = {
    'Authorization': f'Bearer {notionId}',
    'Content-Type': 'application/json',
    'Notion-Version': '2022-06-28'
}


def get_task_creation_time(task):
    task_creation = task['created_time']
    task_creation_date = task_creation.split('T')[0]
    task_creation_time = task_creation.split('T')[1]
    task_creation_formatted_time = task_creation_time.split('.')[0]
    task_creation_formatted = task_creation_date + " " + task_creation_formatted_time

    task_creation_formatted_date_obj = dt.strptime(task_creation_formatted, "%Y-%m-%d %H:%M:%S")
    task_creation_date_timezone = task_creation_formatted_date_obj.astimezone(pytz.timezone('US/Central'))

    if task_creation_date_timezone.hour < 6:
        task_creation_date_timezone = task_creation_date_timezone.date() - timedelta(days=1)
    else:
        task_creation_date_timezone = task_creation_date_timezone.date()
    return task_creation_date_timezone


def get_new_tasks_for_today(tasks):
    new_tasks_for_today = []
    for task in tasks:
        props = task['properties']
        done = props['Done']
        if not done['checkbox']:
            print("------")

            time_zone = pytz.timezone('US/Central')
            today = dt.now(time_zone).date()
            task_creation_time = get_task_creation_time(task)

            if today > task_creation_time:
                today_prop = props['Today']
                today_prop_value = today_prop['checkbox']
                if not today_prop_value:
                    new_tasks_for_today.append(task)

            print("----")
    return new_tasks_for_today


def move_yesterday_tasks_to_today():
    response = requests.post(url, json=payload, headers=headers)
    result = response.json()
    tasks = result['results']

    new_tasks_for_today = get_new_tasks_for_today(tasks)

    for task in new_tasks_for_today:
        task_id = task['id']
        task_url = f"https://api.notion.com/v1/pages/{task_id}"
        update_data = {
            "properties": {
                "Today": {
                    "type": "checkbox",
                    "checkbox": True
                }
            }
        }
        new_data = json.dumps(update_data)
        response = requests.patch(url=task_url, headers=headers, data=new_data)
        print(response)


def main():
    while True:
        move_yesterday_tasks_to_today()
        # Next iteration after 30 minutes
        time.sleep(1800)


if __name__ == "__main__":
    main()
