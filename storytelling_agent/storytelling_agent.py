import time
import json
import traceback
import logging

from openai import OpenAI

logger = logging.getLogger(__name__)

client = None

SUPPORTED_BACKENDS = ["openrouter"]

def _query_chat_openrouter(endpoint, api_key, messages, retries=3,
    request_timeout=120, max_tokens=4096, model='openai/gpt-3.5-turbo-1106',
    extra_options={}):
    endpoint = endpoint.rstrip('/')

    global client
    if client is None:
        client = OpenAI(api_key=api_key, base_url=endpoint)

    while retries > 0:
        try:           
            response = client.chat.completions.create(
                messages=messages, 
                model=model,
                max_tokens=max_tokens,
                timeout=request_timeout
            )

            if messages and messages[-1]["role"] == "assistant":
                result_prefix = messages[-1]["content"]
            else:
                result_prefix = ''
            
            content = response.choices[0].message.content
            return content
        except Exception:
            traceback.print_exc()
            print('Timeout error, retrying...')
            retries -= 1
            time.sleep(5)
    else:
        return {}

class StoryAgent:
    def __init__(self, backend_uri, api_key='', backend="hf", request_timeout=120,
                 max_tokens=4096, n_crop_previous=400,
                 prompt_engine=None, form='novel', model='openchat/openchat-7b',
                 extra_options={}, scene_extra_options={}):

        self.backend = backend.lower()
        if self.backend not in SUPPORTED_BACKENDS:
            raise ValueError("Unknown backend")

        if prompt_engine is None:
            from storytelling_agent import prompts
            self.prompt_engine = prompts
        else:
            self.prompt_engine = prompt_engine

        self.form = form
        self.max_tokens = max_tokens
        self.extra_options = extra_options
        self.scene_extra_options = extra_options.copy()
        self.scene_extra_options.update(scene_extra_options)
        self.backend_uri = backend_uri
        self.api_key = api_key
        self.n_crop_previous = n_crop_previous
        self.request_timeout = request_timeout
        self.model = model

    def query_chat(self, messages, retries=3):
        if self.backend == "openrouter":
            result = _query_chat_openrouter(
                self.backend_uri, self.api_key, messages, retries=retries,
                request_timeout=self.request_timeout,
                max_tokens=self.max_tokens,model=self.model, extra_options=self.extra_options)
        return result

    def init_book_spec(self, topic):
        """Creates initial book specification - returns string"""
        messages = self.prompt_engine.init_book_spec_messages(topic, self.form)
        book_spec = self.query_chat(messages)

        return messages, book_spec

    def enhance_book_spec(self, spec):
        """Enhance book specification"""
        messages = self.prompt_engine.enhance_book_spec_messages(spec, self.form)
        book_spec = self.query_chat(messages)

        return messages, book_spec

    def json_book_spec(self, book_spec):
        """return JSON representation of book spec"""

        messages = self.prompt_engine.json_book_spec_messages(book_spec)
        as_json = self.query_chat(messages)

        return messages, as_json

    def create_plot(self, book_spec, plot_template='save the cat'):
        """Create initial by-plot outline of form"""
        messages = self.prompt_engine.create_plot_messages(book_spec, self.form, plot_template=plot_template)
        plot = self.query_chat(messages)
        return messages, plot

    def json_plot(self, plot):
        messages = self.prompt_engine.json_plot_messages(plot)
        as_json = self.query_chat(messages)

        return messages, as_json

    def scene_beats_from_summary(self, book_spec, json_plot):
        """Creates a by-scene breakdown of all chapters"""
        all_messages = []
        plot = json.loads(json_plot)
        for story_beat in plot['story_beats']:
            logger.info(story_beat['name'] + '...')
            messages = self.prompt_engine.scene_beats_from_summary_messages(self.form, book_spec, story_beat['description'])
            all_messages.append(messages)

            scene_beats = self.query_chat(messages)
            story_beat['scene_beats'] = json.loads(scene_beats)['scenes']

        return all_messages, json.dumps(plot, indent=2)
 
    def write_a_scene(self, scene: str,  previous_scene: str|None, book_spec: str):
        """Generates a scene text for a form"""
        messages = self.prompt_engine.scene_messages(scene, previous_scene, book_spec, self.form)
        prose = self.query_chat(messages)
        #prose = json.loads(prose, strict=False)['prose'].replace('\\n', '\n')

        return messages, prose

    def generate_story(self, topic, plot_template, book_folder):
        """Example pipeline for a novel creation"""
        GENERATE_SPEC = True
        GENERATE_PLOT = True
        GENERATE_OUTLINE = True
        GENERATE_PROSE = True

        import os
        path = os.curdir + '/books/' + book_folder
        os.mkdir(path)
        path += '/'

        logger.info(f"Generating book spec for a {topic}")
        if GENERATE_SPEC:
            _, book_spec = self.init_book_spec(topic)
            _, book_spec = self.enhance_book_spec(book_spec)
            _, book_spec = self.json_book_spec(book_spec)
            with open(path + 'book_spec.json', 'w') as f:
                f.write(book_spec)
        else:
            with open(path + 'book_spec.json', 'r') as f:
                book_spec = f.read()

        logger.info('Generating plot...')
        if GENERATE_PLOT:
            _, plot = self.create_plot(book_spec, plot_template)
            _, plot = self.json_plot(plot)
            with open(path + 'plot.json', 'w') as f:
                f.write(plot)
        else:
            with open(path + 'plot.json', 'r') as f:
                plot = f.read()


        logger.info('Generating scene beats from plot summary...')
        if GENERATE_OUTLINE:
            _, outline = self.scene_beats_from_summary(book_spec, plot)
            with open(path + 'detailed_outline.json', 'w') as f:
                f.write(outline)
        else:
            with open(path + 'detailed_outline.json', 'r') as f:
                outline = f.read()

        logger.info('Detailed outline complete. Time to write!')
        if GENERATE_PROSE:
            outline = json.loads(outline)

            chapters = []
            for story_beat in outline['story_beats']:
                chapter = {
                    "name": story_beat['name'],
                    "text": []
                }

                logger.info(story_beat['name'].upper())

                previous_scene = ''
                for scene_beat in story_beat['scene_beats']:
                    scene_spec = json.dumps(scene_beat, indent=2)
                    logger.info(scene_beat['event'])

                    _, prose = self.write_a_scene(scene_spec, previous_scene, book_spec)

                    chapter['text'].append(prose)
                    previous_scene = prose

                chapters.append(chapter)

            with open(path + 'chapters.json', 'w') as f:
                f.write(json.dumps(chapters, indent=2))

            with open(path + 'book.txt', 'w') as f:
                for chapter in chapters:
                    f.write('\n' + chapter['name'].upper() + '\n\n')
                    f.writelines(chapter['text'])
                    f.write('\n')


    def nop(self):
        pass
