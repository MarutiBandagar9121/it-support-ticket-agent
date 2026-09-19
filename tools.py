from data_utils import load_tickets
from langchain.tools import tool

PATH = "data/processed/sample_5000.csv"

_df = load_tickets(PATH)

@tool
def get_avg_resolution_time_based_on_ticket_priority(priority:str)->str:
    """
    Get the average resolution time based on ticket priority.

    Args:
        priority (str): The priority level of the ticket.
        priority here has fixed values: ['high', 'urgent', 'low', 'medium']
        Returns:
            str: A sentence stating the average resolution time in hours for the specified priority level.
    """
    
    filtered_df = _df[_df['priority'] == priority]
    if filtered_df.empty:
        return f"No tickets found with priority '{priority}'"
    avg_resolution_time = filtered_df['resolution_time_hours'].mean()
    return f"The average resolution time for priority '{priority}' is {avg_resolution_time:.2f} hours."