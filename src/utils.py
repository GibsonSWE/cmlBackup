from src import constants as c

from re import sub


# Output version information to terminal
def show_version():
    version_info = f"""
    Version: {c.release_data['version']}
    Release date: {c.release_data['date']}
    """    
    return version_info


# Output help to terminal
def show_help():
    help_info = f"""
    Help info here
    """
    return help_info


# Converts string to snake-case
def snake(string):
  return '_'.join(
    sub('([A-Z][a-z]+)', r' \1',
    sub('([A-Z]+)', r' \1',
    string.replace('-', ' '))).split()).lower()

