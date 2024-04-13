from src import constants as c

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

