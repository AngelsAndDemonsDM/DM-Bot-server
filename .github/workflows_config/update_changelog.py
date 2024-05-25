import yaml
import os
from datetime import datetime

def load_changelog(file_path):
    try:
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        return []

def save_changelog(file_path, changelog):
    with open(file_path, 'w') as file:
        yaml.dump(changelog, file, default_flow_style=False, allow_unicode=True)

def extract_field(body, field_name):
    for line in body.split('\n'):
        if line.startswith(f'{field_name}:'):
            return line.split(':', 1)[1].strip()
    return None

def extract_changes(body):
    changes = []
    start_collecting = False
    for line in body.split('\n'):
        if line.startswith('changes:'):
            start_collecting = True
            continue
        if start_collecting:
            if line.strip() == '':
                break
            changes.append(line.strip('- ').strip())
    return changes

def main():
    changelog_file = '.github/changelog.yml'
    pr_body = os.getenv('PR_BODY')
    git_author = os.getenv('GIT_AUTHOR')
    date_today = datetime.today().strftime('%Y-%m-%d')

    changelog = load_changelog(changelog_file)

    new_version = extract_field(pr_body, 'version_update')
    author = extract_field(pr_body, 'autor')

    if not new_version:
        if changelog:
            new_version = changelog[0]['version']
        else:
            new_version = "0.0.0"

    if not author:
        author = git_author

    changes = extract_changes(pr_body)

    new_entry = {
        'version': new_version,
        'date': date_today,
        'author': author,
        'changes': changes
    }

    changelog.insert(0, new_entry)
    save_changelog(changelog_file, changelog)

if __name__ == "__main__":
    main()
