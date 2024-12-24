import cmd
from urllib.request import urlopen, Request
from string import Template
import json


class GithubActivityCLI(cmd.Cmd):
    """a class to handle everything about the cli"""

    prompt = "github-activity-cli>>"
    intro = "Welcome to GIthub Activity CLI. type 'help' to see all available commands"
    url = Template("https://api.github.com/users/$username/events")

    def to_dict(self, data):
        """converts json data to python dictionary"""
        dict_data = json.loads(data)
        return dict_data

    def get_events(self, url: str):
        """gets public events of a user from the github api"""
        if not url.startswith("http"):
            raise RuntimeError("Incorrect and possibly insecure protocol in url")

        httpRequest = Request(url, headers={"Accepts": "application/json"})

        with urlopen(httpRequest) as response:
            status_code = response.status
            content = response.read().decode()
            content_dict = self.to_dict(content)
            return status_code, content_dict

    def do_github_activity(self, username: str):
        url = self.url.substitute(username=username)
        status_code, content_dict = self.get_events(url)

        # print(type(content_dict))
        for activity in content_dict:
            if activity["type"] == "PushEvent":
                size = activity["payload"]["size"]
                repo_name = activity["repo"]["name"]
                if size == 1:
                    print(f"- pushed {size} commit to {repo_name}")
                else:
                    print(f"- pushed {size} commits to {repo_name}")
            elif activity["type"] == "PublicEvent":
                repo_name = activity["repo"]["name"]
                print(f"- made {repo_name} repository public")
            elif (
                activity["type"] == "WatchEvent"
                and activity["payload"]["action"] == "started"
            ):
                repo_name = activity["repo"]["name"]
                print(f"- starred {repo_name} repository")
            print("")  # print empty line for readability

    def do_exit(self, line):
        """command to exit the cli"""
        return True

    def postcmd(self, stop, line):
        """performed after each prompt"""
        print("")  # print empty line for better readibilty
        return super().postcmd(stop, line)


if __name__ == "__main__":
    GithubActivityCLI().cmdloop()
