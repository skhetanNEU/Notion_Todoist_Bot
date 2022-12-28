import json
import requests
import time
from todoist_api_python.api import TodoistAPI
from keep_alive import keep_alive

# To keep the server alive
keep_alive()

# Load the file and get the databases id and todoist id
file = open('secret.json')
data = json.load(file)
notionId = data['notionId']
tasksDatabase = data['tasksDatabase']
officeTasks = data['officeTasks']
studyTasks = data['studyTasks']
collegeTasks = data['collegeTasks']
laterTasks = data['laterTasks']
todoistId = data['todoistId']
collegeTasksProjectID = data['collegeTasksProjectID']
studyTasksProjectID = data['studyTasksProjectID']
officeTasksProjectID = data['officeTasksProjectID']
laterTasksProjectID = data['laterTasksProjectID']
file.close()

url = 'https://api.notion.com/v1/pages'
headers = {
    'Authorization': f'Bearer {notionId}',
    'Content-Type': 'application/json',
    'Notion-Version': '2022-06-28'
}

todoist_api = TodoistAPI(todoistId)


def get_relation(project_id):
    if project_id == collegeTasksProjectID:
        return collegeTasks, "College"
    elif project_id == studyTasksProjectID:
        return studyTasks, "Study"
    elif project_id == officeTasksProjectID:
        return officeTasks, "Office"
    elif project_id == laterTasksProjectID:
        return laterTasks, "Later"


def add_to_notion(new_tasks):
    for task in new_tasks:
        is_due_today = False
        task_name = getattr(task, 'content')
        project_id = getattr(task, 'project_id')
        task_labels = getattr(task, 'labels')
        if len(task_labels) == 1:
            is_due_today = True
        relation_id, relation_name = get_relation(project_id)
        data_input = {
            "parent": {"type": "database_id", "database_id": tasksDatabase},
            "properties": {
                "Task": {
                    "type": "title",
                    "title": [{"type": "text", "text": {"content": task_name}}]
                },
                "Project": {
                    "type": "relation",
                    "relation": [{
                        "id": relation_id,
                        "synced_property_name": relation_name
                    }]
                },
                "Today": {
                    "type": "checkbox",
                    "checkbox": is_due_today
                }
            }
        }
        response = requests.post(url, headers=headers, json=data_input)
        print(response.json())


def main():
    while True:
        try:
            # Find the new tasks in todoist
            tasks = todoist_api.get_tasks()
            new_tasks = []
            for task in tasks:
                label = getattr(task, 'labels')
                if len(label) == 0:
                    new_tasks.append(task)
                elif len(label) == 1:
                    if label[0] == 'Today':
                        new_tasks.append(task)

            # Add the new tasks to notion
            add_to_notion(new_tasks)

            # Update the tasks in todoist with the tag "Added_to_Notion"
            for task in new_tasks:
                task_id = getattr(task, 'id')
                todoist_api.update_task(task_id=task_id, labels=['Added_to_Notion'])

        except Exception as error:
            print(error)

        # Run again after 1 minute
        time.sleep(60)


if __name__ == "__main__":
    main()
