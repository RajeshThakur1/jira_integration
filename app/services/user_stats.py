import json
import app.config as cfg
# with open(f"{cfg.BASE_DIR}/app/resources/instructions/output.json") as file:
import pandas as pd
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


def get_reward_graph():
    # Assuming you've already read the CSV into a pandas DataFrame called df
    # Make sure to replace the path with the actual path to your CSV file
    df = pd.read_csv(
        f"{cfg.BASE_DIR}/app/resources/instructions/Rewards and Recognition.csv")

    # Normalize the award types to have consistent casing
    df['Award Type(Star, Surpass)'] = df['Award Type(Star, Surpass)'].str.upper()

    # Group by 'Award Type' to get counts for the inner pie
    award_type_counts = df['Award Type(Star, Surpass)'].value_counts().to_dict()

    # Group by both 'Award Type' and 'Employee Name' for the outer ring
    employee_awards = df.groupby(['Award Type(Star, Surpass)', 'Employee Name']).size().reset_index(name='Counts')

    # Sort the employee awards to maintain consistent order with the inner pie
    employee_awards = employee_awards.set_index('Award Type(Star, Surpass)').loc[award_type_counts.keys()].reset_index()

    # Convert to a list of dictionaries for JSON
    employee_awards_json = employee_awards.to_dict(orient='records')

    # Now you have the data in a structure that can be converted to JSON
    json_data = {
        "award_type_counts": award_type_counts,
        "employee_awards": employee_awards_json
    }

    # Serialize the data structure to a JSON formatted string
    json_output = json.dumps(json_data, indent=4)
    return json_data
