import json
import app.config as cfg
# with open(f"{cfg.BASE_DIR}/app/resources/instructions/output.json") as file:
f = open(f"{cfg.BASE_DIR}/app/resources/instructions/output.json")
json_data = json.load(f)
# Sample JSON data

# Initialize a dictionary to hold the results
author_stats = {}

def get_user_stats():
    f = open(f"{cfg.BASE_DIR}/app/resources/instructions/output.json")
    json_data = json.load(f)
    # Sample JSON data

    # Initialize a dictionary to hold the results
    author_stats = {}
# Iterate over the tickets in the JSON data
    for ticket in json_data['dummy']:
        assignee = ticket['Assignee']
        status = ticket['Status']

        # Skip if no assignee is specified
        if assignee == "Unassigned":
            continue

        # Initialize the author in the dictionary if not present
        if assignee not in author_stats:
            author_stats[assignee] = {'Pending': 0, 'Completed': 0}
        # Increment the count based on the status
        if status == "To Do":
            author_stats[assignee]['Pending'] += 1
        else:
            author_stats[assignee]['Completed'] += 1

    return author_stats
    # Print the results
    # print(json.dumps(author_stats , indent=4))

def get_per_user_ticket_assign():
    f = open(f"{cfg.BASE_DIR}/app/resources/instructions/output.json")
    json_data = json.load(f)
    # Iterate over the tickets in the JSON data
    ticket_assign_per_user = {}

    for ticket in json_data['dummy']:
        assignee = ticket['Assignee']

        # Skip if no assignee is specified
        if assignee == "Unassigned":
            continue

        # Initialize the author in the dictionary if not present
        if assignee not in ticket_assign_per_user:
            ticket_assign_per_user[assignee] = {"total_ticket_assign": 0}
        ticket_assign_per_user[assignee]['total_ticket_assign'] += 1
        # Increment the count based on the status

    return ticket_assign_per_user


