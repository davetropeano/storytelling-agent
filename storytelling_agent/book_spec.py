import json
from typing import List
from pydantic import BaseModel
import jinja2

class Character(BaseModel):
    name: str
    background: str

class BookSpec(BaseModel):
    genre: str
    place: str
    time: str
    theme: str
    tone: str
    point_of_view: str
    characters: List[Character]
    premise: str

json_schema = json.dumps(BookSpec.model_json_schema(), indent=2)

prompt_string = """
Reformat the information present in this specification to output it as a JSON object.

{{specification}}.

Only use information that is present in the passage. Make sure to include all the information for a given field. Follow this JSON schema. Only return the actual instances without any additional schema definition! Make sure your response is a dict and not a list! Output ONLY the JSON object!

{{schema}}

{% if invalid_replies and error_message %}
  You already created the following output in a previous attempt: {{invalid_replies}}
  However, this doesn't comply with the format requirements from above and triggered this Python exception: {{error_message}}
  Correct the output and try again. Just return the corrected output without any extra explanations.
{% endif %}
"""

def json_prompt(text_spec):
    env = jinja2.Environment()
    template = env.from_string(prompt_string)
    
    return template.render(specification=text_spec, schema=json_schema)