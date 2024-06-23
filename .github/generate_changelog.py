import json
import logging
import os
from datetime import datetime

import requests
import yaml

logging.basicConfig(level=logging.INFO)

REPO = "AngelsAndDemonsDM/DM-Bot"
CONFIG_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "updater_config.json"))

def get_pull_request_data(pull_number, token=None):
    url = f"https://api.github.com/repos/{REPO}/pulls/{pull_number}"
    headers = {}
    if token:
        headers['Authorization'] = f'token {token}'
    
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        logging.error(f"Не удалось получить данные для PR #{pull_number}. Статус код: {response.status_code}")
        return None
    
    pr_data = response.json()

    data = {
        "description": pr_data.get('body'),
        "merged": pr_data.get('merged'),
        "merged_at": pr_data.get('merged_at'),
        "author": pr_data['user']['login']
    }

    logging.info(f"Получены данные для PR #{pull_number}")
    return data

def parse_pr_description(description):
    if description is None:
        return None, None, None

    lines = description.split('\r\n')
    changes = []
    version_update = None
    author = None
    changes_section = False

    for line in lines:
        stripped_line = line.strip()
        strip_loser = stripped_line.lower()
 
        if strip_loser.startswith("version_update:"):
            version_update = stripped_line.split(":", 1)[1].strip()
        
        elif strip_loser.startswith("author:"):
            author = stripped_line.split(":", 1)[1].strip()
        
        elif "changes: not" in strip_loser:
            return None, None, None

        elif "changes:" in strip_loser:
            changes_section = True
        
        elif changes_section:
            if stripped_line.startswith("- "):
                stripped_line = stripped_line[2:].strip()
                changes.append(stripped_line)

    if changes == []:
        changes = None
    
    return changes, version_update, author

def save_changelog(changelog, changelog_file):
    with open(changelog_file, 'w', encoding='utf-8') as file:
        yaml.dump(changelog, file, allow_unicode=True, default_flow_style=False)

def update_config_version(version):
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as file:
            config = json.load(file)
        
        config["VERSION"] = version
        
        with open(CONFIG_FILE, 'w', encoding='utf-8') as file:
            json.dump(config, file, indent=4)
        logging.info(f"Обновлено поле VERSION в {CONFIG_FILE} до {version}")

def process_pull_requests(start_pr, end_pr, token=None, changelog_file='changelog.yml'):
    changelog = {'changelog': []}
    init_version = "0.0.0"
    
    if os.path.exists(changelog_file):
        with open(changelog_file, 'r', encoding='utf-8') as file:
            changelog = yaml.safe_load(file) or {'changelog': []}
    
    latest_version = init_version

    for pr_number in range(start_pr, end_pr + 1):
        pr_data = get_pull_request_data(pr_number, token)
       
        if pr_data:
            if pr_data['merged']:
                changes, version_update, parsed_author = parse_pr_description(pr_data['description'])
                
                if changes and len(changes) > 0:
                    author = pr_data.get("author")
                    
                    if not version_update:
                        version_update = init_version
                    
                    changelog_entry = {
                        "author": parsed_author if parsed_author else author,
                        "changes": changes,
                        "date": datetime.strptime(pr_data['merged_at'], '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d'),
                        "version": version_update
                    }
                    
                    changelog['changelog'].append(changelog_entry)
                    
                    if version_update:
                        init_version = version_update
                        latest_version = version_update
    
    changelog['changelog'] = sorted(changelog['changelog'], key=lambda entry: datetime.strptime(entry['date'], '%Y-%m-%d'))
    
    save_changelog(changelog, changelog_file)
    update_config_version(latest_version)

if __name__ == "__main__":
    try:
        if os.path.exists("changelog.yml"):
            os.remove("changelog.yml")
            
        start_pr = 0
        end_pr = int(input("end_pr: "))
        token = input("token: ")

        process_pull_requests(start_pr, end_pr, token)
    
    except KeyboardInterrupt:
        print("Exiting...")
