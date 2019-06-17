import os
import requests

data = []
for i in range(1, 100):
    r = requests.get('https://git.example.com/api/v4/projects?private_token=provate_token&per_page=100&page=%s'%i)
    d = r.json()
    if r.status_code != 200:
        print(r.text)
        break
    data.extend(d)

for d in data:
    git_url = d['ssh_url_to_repo']
    path_with_namespace = d['path_with_namespace']
    print(git_url, path_with_namespace)
    os.system('git clone %s %s'%(git_url, path_with_namespace))
