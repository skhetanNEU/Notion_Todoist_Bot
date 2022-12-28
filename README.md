# Notion Todoist Bot

## Overview
Notion provides the power to manage tasks and different projects in a very effective way but adding tasks is a pain. I have been in many such situations while travelling, studying, etc where I just remember that I have to do something but to add that task in notion (especially on my phone), I have to open the specific project and add it there. On the otherhand, apps like Todoist are very easy to add a task instantly but doesn't provide the power of managing things like Notion.

For a while, I used to double write the tasks. 
1. Write it in Todoist
2. Copy it in Notion when I sit in front of my machine.

To solve this problem, I created these scripts that would allow the following workflows - 
1. Automatically add a task to Notion after a new task has been added to Todoist.
2. Automatically marks the tasks with Today checkbox after the day the task was added.
3. Automatically delete the tasks from Todoist (which has been added to Notion) the next day so that Todoist remains clean and management of tasks resides in Notion.


## Other alternatives to this problem?
There are many other alternatives that allow you to handle this automation. Some of the most popular ones are Zapier and Make (Integromat) but both of them come with major restrictions for this use case i.e
1. Limiting the number of tasks in the free tier (Zapier provides 150 task per month)
2. Limiting the power and restricing what you can do with some properties. Manipulating values and then taking some action based on that wasn't that straightforward
3. and achieving that might require more tasks to be used with each entry into Notion.


## Notion database setup
Started with Thomas Frank's Ultimate Task template (https://thomasjfrank.com/templates/task-and-project-notion-template/) and customized it based on my needs, I use it for 3 type of tasks (Created 3 new projects in the template) - 
1. College Tasks
2. Study Tasks
3. Office Tasks (Since I am interning at a company)
4. Later tasks (Tasks which don't have a due date but need to be captured in Notion)

<img width="964" alt="image" src="https://user-images.githubusercontent.com/98121476/208753738-fcbf81b4-6c2d-4bc2-8362-aef172e7fc4a.png">


I added a Today's property (checkbox) which specified if a task is due today. I use this Today property to sort the table to have a clean look of all the tasks which are due today. 

<img width="1092" alt="image" src="https://user-images.githubusercontent.com/98121476/208755467-15f0b546-2d13-4f93-9dc1-6983ba52fe23.png">


I also added 2 views for each of the projects which displays tasks which are due today in that project and other view displays the remaining tasks

Separate views allows me to focus on tasks from a particular project more efficiently.

<img width="1013" alt="image" src="https://user-images.githubusercontent.com/98121476/208755575-1a2a4f46-5983-419e-9a1a-4a31804a4940.png">

[Reach out to me on LinkedIn if you would like to get this simplied template]


## Workflows
### 1. Add a task to Notion after a new task has been added to Todoist
When we add a new task in Todoist, it gets added to Notion automatically and a tag specifying "Added_to_Notion" gets added to the task in Todoist.

<img width="973" alt="image" src="https://user-images.githubusercontent.com/98121476/208761964-d6a81fdd-b318-4631-8dd7-e4174d33cd6d.png">

Task in Notion - 

<img width="757" alt="image" src="https://user-images.githubusercontent.com/98121476/208763216-033ed87d-9b03-443e-b579-8e59e95ac924.png">


### 2. Mark the today's property of the task so that we can look at tasks for today in a separate view
By default, the task gets added to Notion with Today marked as False (unless a Today tag is added to the task in Todoist). This flow makes sure that the tasks which are created today gets marked with Today in notion the very next day. This allows us to make sure tasks are not pending forever


### 3. Delete the tasks marked with "Added_to_Notion" from Todoist every morning to keep Todoist list clean
Every morning we delete the tasks from Todoist which have been added to Notion to keep our Todoist list clean. This can be checked by looking at the label "Added_to_Notion" in the task.


## Implementation

### Setup
Starting with the implementation, I created a new connection to get the notion api key and named it "python-bot". Once we had the key, we added the connection "python-bot" from all the projects and the main database page. 

By sharing all the pages, we can get the database ID of the projects and by doing a simple GET on todoist tasks, we can get to know the project ids for Todoist projects. Using all these keys and IDs I created the secret.json file containing all the required keys and ids.

I also got the api key for my todoist account and saved it in secret.json.

<img width="585" alt="SCR-20221219-ubr" src="https://user-images.githubusercontent.com/98121476/208767273-4de4eaad-35d5-4798-b9eb-8fba364f32d3.png">

### File
We created three scripts - 
1. todoist_to_notion.py - To manage the 1st workflow of adding a task to Notion after a new task has been added to Todoist
2. update_yesterday_tasks_notion.py - To manage the 2nd workflow of marking the today's checkbox of the task if the task was created in any of the previous days
3. delete_todoist_tasks.py - To manage the 3rd workflow of deleting the tasks from Todoist which have already been added to Notion.

### Hosting
Hosting these scripts to run forever was required so that we can write tasks in todoist whenever we want and be assured that it will be added to Notion within a minute. There are some easy paid options out there, but I used repl.it to host these scripts.

I created 1 repl for each of these scripts and ran those. There are 2 issues with repl.it which required some solution - 

1. In the free account of repl, the repl goes into sleep after some time, therefore I needed a way which would keep on pinging the repl in order to keep it awake forever. I used uptimerobot for this and created 3 monitors (1 for each repl) to keep them alive. The best video that explains how this work is - https://www.youtube.com/watch?v=S6pBLq8Jv_A
2. It was throwing errors to install the package "todoist_api_python" which is required for interaction with Todoist. To get around it, I had to make the following change in pyproject.toml file in each of the repls: python = ">=3.9,<4.0" under the section "[tool.poetry.dependencies]"


## How can you use it for your setup?
1. The first step in using this setup for yourself would be to setup your Notion with the database and setting up the projects you want.
2. Next would be to get the required database IDs and API keys for the secret.json file.
3. All the 3 python files can be used as it is with just one modification of the timezone. I am in central time zone therefore, I used "US/Central" at all places.
4. Creating repls and setting up monitors on uptime robot.
5. That's it you are done with a fully automated way of managing your tasks in Todoist and Notion and with all the setup free of cost.



#### If you like this work, please share it with your peers and Notion fans allowing them to utilize this easy and free solution. Please feel free to reach out to me on my [Linkedin] if you want to collaborate and work on cool ideas and making some useful automations.

[Linkedin]: https://www.linkedin.com/in/satvikkhetan/
