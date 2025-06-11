from dotenv import load_dotenv
from assistant import Assistant

if __name__ == "__main__":
    load_dotenv()
    assistant = Assistant()
    assistant.run()
