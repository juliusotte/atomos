from string import Template
from pathlib import Path

from atomos import config


def template(content: str, label: str = config.APP_NAME) -> str:
    location = Path(__file__).absolute().parent
    template_path = location / 'template.html'
    with open(template_path) as html_template:
        data = html_template.read()
        html_template.close()

    substitutions = {
        'content': content,
        'label': label,
    }

    return Template(data).substitute(substitutions)
