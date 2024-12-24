import cmd
from urllib.request import urlopen, Request
from string import Template
import json


class GithubActivityCLI(cmd.Cmd):
    """a class to handle everything about the cli"""

    prompt = "github-activity-cli>>"
    intro = "Welcome to GIthub Activity CLI. type 'help' to see all available commands"
    BASE_URL_TEMPLATE = Template("https://api.github.com/users/$username/events")

    def fetch_data(self, url: str):
        """fetchs raw json data from the github api"""
        try:
            if not url.startswith("http"):
                raise RuntimeError("Incorrect and possibly insecure protocol in url")
            request = Request(url, headers={"Accepts": "application/json"})
            with urlopen(request) as response:
                if response.status != 200:
                    raise RuntimeError(f"Api error: status {response.status}")
                return response.read().decode()
        except Exception as e:
            raise RuntimeError(f"Error fetching data: {e}")

    def parse_json(self, data: str) -> list:
        """parse json string in to python dictionary"""
        try:
            return json.loads(data)
        except json.JSONDecodeError:
            raise RuntimeError("Error parsing json response")

    def parse_event(self, event: dict) -> str:
        """Parse individual github activity event"""
        if event["type"] == "PushEvent":
            size = event["payload"]["size"]
            repo_name = event["repo"]["name"]
            return (
                f"- pushed {size} {'commit' if size==1 else 'commits'} to {repo_name}"
            )
        if event["type"] == "PublicEvent":
            repo_name = event["repo"]["name"]
            return f"- made {repo_name} repository public"
        if event["type"] == "WatchEvent":
            repo_name = event["repo"]["name"]
            return f"- Starred {repo_name} repository"
        return None

    def do_github_activity(self, username: str):
        """Fetch and display recent Github activity for the specified user"""
        if not username or not username.isalnum():
            print("Invalid username, please enter a valid Github username")
            return
        url = self.BASE_URL_TEMPLATE.substitute(username=username)
        try:
            raw_data = self.fetch_data(url)
            events = self.parse_json(raw_data)
            for event in events:
                parsed_event = self.parse_event(event)
                if parsed_event:
                    print(parsed_event)
                    print("\n")
        except RuntimeError as e:
            print(f"Error: {e}")

    def do_exit(self, line):
        """command to exit the cli"""
        return True


if __name__ == "__main__":
    GithubActivityCLI().cmdloop()
