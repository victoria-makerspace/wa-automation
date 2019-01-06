from config import config
from pydiscourse import DiscourseClient

client = DiscourseClient(
        config['discourse']['host'],
        config['discourse']['username'],
        config['discourse']['api-key'])
