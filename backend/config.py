import os
from dotenv import load_dotenv


# load env variables
load_dotenv()
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
