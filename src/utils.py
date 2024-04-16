from src import constants as c

from re import sub



def show_version():
    version_info = f"""
    Version: {c.release_data['version']}
    Release date: {c.release_data['date']}
    """    
    return version_info


def show_help():
    help_info = f"""
    Help info here
    """
    return help_info


def snake(string):
  return '_'.join(
    sub('([A-Z][a-z]+)', r' \1',
    sub('([A-Z]+)', r' \1',
    string.replace('-', ' '))).split()).lower()

