from config.notion import NOTION_TOKEN
from notion_client import Client

notion = Client(auth=NOTION_TOKEN)
