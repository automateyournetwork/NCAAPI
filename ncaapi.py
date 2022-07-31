import requests
import os
import json
import yaml
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")

template_dir = Path(__file__).resolve().parent
env = Environment(loader=FileSystemLoader(str(template_dir)))
start_season = 2001
end_season = 2021

while start_season <= end_season:
    url = f"https://api.collegefootballdata.com/stats/season/advanced?year={ start_season }"

    payload={}
    headers = {
      'Authorization': f'Bearer { TOKEN }'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    formatted_json = json.dumps(response.json(), indent=4, sort_keys=True)

    with open(f'{ start_season }/JSON/{ start_season } NCAA Football Statistics.json', 'w' ) as f:
        f.write(formatted_json)

    formatted_yaml = yaml.dump(json.loads(formatted_json), default_flow_style=False)

    with open(f'{ start_season }/YAML/{ start_season } NCAA Football Statistics.yaml', 'w' ) as f:
        f.write(formatted_yaml)

    csv_template = env.get_template('csv.j2')      
    csv_output = csv_template.render(data_to_template = json.loads(formatted_json))

    with open(f'{ start_season }/CSV/{ start_season } NCAA Football Statistics.csv', 'w' ) as f:
        f.write(csv_output)

    markdown_template = env.get_template('markdown.j2')      
    markdown_output = markdown_template.render(data_to_template = json.loads(formatted_json))

    with open(f'{ start_season }/Markdown/{ start_season } NCAA Football Statistics.md', 'w' ) as f:
        f.write(markdown_output)

    html_template = env.get_template('html.j2')      
    html_output = html_template.render(data_to_template = json.loads(formatted_json), season=start_season)

    with open(f'{ start_season }/HTML/{ start_season } NCAA Football Statistics.html', 'w' ) as f:
        f.write(html_output)

    mindmap_template = env.get_template('mindmap.j2')
    for team in json.loads(formatted_json):
        mindmap_output = mindmap_template.render(data_to_template = team, season=start_season)

        with open(f'{ start_season }/Mindmaps/{ start_season } { team["team"] } Statistics Mindmap.md', 'w' ) as f:
            f.write(mindmap_output)

    start_season = start_season + 1