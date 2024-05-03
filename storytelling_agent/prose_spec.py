import json
from typing import List
from pydantic import BaseModel
import jinja2

class ProseSpec(BaseModel):
    prose: str

json_schema = json.dumps(ProseSpec.model_json_schema(), indent=2)

old_prompt_string = """
Respond in JSON format using the following schema:

{{schema}}

<scene-information>
{{scene}}
</scene-information>

{% if previous_scene %}
Here is the previous scene:

<previous-scene>
{{previous_scene}}
</previous-scene>

{% endif %}

Here is the high level book specification:

<book-specification>
{{book_spec}}
</book-specification>

Follow the JSON schema. Only return the actual instances without any additional schema definition! Make sure your response is a dict and not a list! Output ONLY the JSON object!

{% if invalid_replies and error_message %}
  You already created the following output in a previous attempt: {{invalid_replies}}
  However, this doesn't comply with the format requirements from above and triggered this Python exception: {{error_message}}
  Correct the output and try again. Just return the corrected output without any extra explanations.
{% endif %}

"""

prompt_string = """
<scene-information>
{{scene}}
</scene-information>

{% if previous_scene %}
Here is the previous scene:

<previous-scene>
{{previous_scene}}
</previous-scene>

{% endif %}

Here is the high level book specification:

<book-specification>
{{book_spec}}
</book-specification>

Output ONLY the scene prose!

NEVER conclude the scene on your own, follow the beat instructions very closely. 
NEVER end with foreshadowing. 
NEVER write further than what I prompt you with. 
AVOID imagining possible endings, NEVER deviate from the instructions.

{% if invalid_replies and error_message %}
  You already created the following output in a previous attempt: {{invalid_replies}}
  However, this doesn't comply with the format requirements from above and triggered this Python exception: {{error_message}}
  Correct the output and try again. Just return the corrected output without any extra explanations.
{% endif %}

"""

def json_prompt(scene, previous_scene, book_spec):
    env = jinja2.Environment()
    template = env.from_string(prompt_string)
    
    rendered = template.render(scene=scene, previous_scene=previous_scene, book_spec=book_spec, schema=json_schema)
    return rendered