from datetime import timedelta
import re

def least_collisions(schedule, parallels):
    """
    Calculate the number of collisions (overlapping classes) in the schedule.
    This function aims to minimize the number of times classes overlap on the same day.
    """
    total_collisions = 0
    for day in schedule:
        # Sort classes by start time for each day to detect overlaps
        sorted_classes = sorted(day, key=lambda x: x["start"])
        for i in range(1, len(sorted_classes)):
            # Check if the current class overlaps with the previous one
            if sorted_classes[i]["start"] < sorted_classes[i - 1]["end"]:
                total_collisions += 1
    return total_collisions  # Lower values indicate fewer or no collisions

def least_time_in_school(schedule, parallels):
    """
    Minimize the total time spent in school per day by condensing classes.
    The aim is to create more compact daily schedules with fewer spread-out hours.
    """
    total_time = 0
    for day in schedule:
        if len(day) > 1:
            start_time = min(session["start"] for session in day)
            end_time = max(session["end"] for session in day)
            total_time += (end_time - start_time).seconds / 3600  # Convert to hours
    return total_time  # Lower values indicate more condensed schedules

def minimum_gaps(schedule, parallels):
    """
    Minimize gaps between consecutive classes on the same day.
    Calculates the time difference between consecutive classes and sums them.
    """
    total_gaps = 0
    for day in schedule:
        sorted_classes = sorted(day, key=lambda x: x["start"])
        for i in range(1, len(sorted_classes)):
            gap = sorted_classes[i]["start"] - sorted_classes[i - 1]["end"]
            total_gaps += max(0, gap.seconds / 3600)  # Convert to hours
    return total_gaps  # Lower values indicate fewer or smaller gaps

def teacher_preference(schedule, parallels, preferred_teachers, blacklisted_teachers):
    """
    Adjust the schedule based on teacher preferences.
    Prioritize preferred teachers and avoid blacklisted teachers.
    """
    preferred = set(re.split(r",\s*", preferred_teachers.strip())) if preferred_teachers else set()
    blacklisted = set(re.split(r",\s*", blacklisted_teachers.strip())) if blacklisted_teachers else set()
    
    score = 0
    for day in schedule:
        for session in day:
            teacher = session.get("teacher")
            if teacher in preferred:
                score -= 1  # Reward preferred teachers
            elif teacher in blacklisted:
                score += 1  # Penalize blacklisted teachers
    return score  # Lower score is better, as it indicates more preferred teachers and fewer blacklisted ones

# List of strategies and their names for selection in the UI
names = ["Least collisions", "Least time in school", "Minimum gaps", "Teacher preference"]
functions = [least_collisions, least_time_in_school, minimum_gaps, teacher_preference]
weights = [None, None, None, None]  # Weights can be added or adjusted based on importance
