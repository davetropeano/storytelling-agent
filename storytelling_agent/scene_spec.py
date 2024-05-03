import json
from typing import List
from pydantic import BaseModel
import jinja2

class SceneSpec(BaseModel):
    characters: List[str]
    place: str
    time: str
    event: str
    conflict: str
    story_value: str
    story_value_charge: str
    mood: str
    outcome: str

class SceneListSpec(BaseModel):
    scenes: List[SceneSpec]

json_schema = json.dumps(SceneListSpec.model_json_schema(), indent=2)

prompt_string = """
Break the following chapter summary into scenes (number of scenes depends on how packed a chapter is). 
Respond in JSON format using the following schema:

{{schema}}

Here is the chapter summary:

<chapter-summary>
{{summary}}
</chapter-summary>

Make sure to include all the information for a given field. Follow the JSON schema. Only return the actual instances without any additional schema definition! Make sure your response is a dict and not a list! Output ONLY the JSON object!

{% if invalid_replies and error_message %}
  You already created the following output in a previous attempt: {{invalid_replies}}
  However, this doesn't comply with the format requirements from above and triggered this Python exception: {{error_message}}
  Correct the output and try again. Just return the corrected output without any extra explanations.
{% endif %}

"""

def json_prompt(summary):
    env = jinja2.Environment()
    template = env.from_string(prompt_string)
    
    rendered = template.render(summary=summary, schema=json_schema)
    return rendered