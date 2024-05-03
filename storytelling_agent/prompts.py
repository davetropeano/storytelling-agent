system = """
You are a best selling pulp fiction writer.
Always cut the bullshit and provide concise outlines with useful details.
Do not turn your stories into fairy tales, be realistic.
"""

book_spec_fields = ['Genre', 'Place', 'Time', 'Theme',
                    'Tone', 'POV', 'Characters', 'Premise']

book_spec_definition = """
Genre: genre
Place: place
Time: period
Theme: main topics
Tone: tone
POV: point of view
Characters: use specific names already!
Premise: describe some concrete events already!
"""


scene_spec_format = """
Characters: character list
Place: place
Time: absolute or relative time
Event: what happens
Conflict: scene micro-conflict
Story value: story value affected by the scene
Story value charge: the charge of story value by the end of the scene (positive or negative)
Mood: mood
Outcome: the result
"""

prev_scene_intro = "Here is the ending of the previous scene:"
cur_scene_intro = "Here is the last written snippet of the current scene:"

def init_book_spec_messages(topic, form):
    messages = [
        {"role": "system", "content": system},
        {"role": "user",
         "content": f"Create a short book specification for a bestseller-grade {form} with the following topic: {topic}. Make sure to give each character a name."
                    f"Format your answer like this:{book_spec_definition}"},
    ]
    return messages

def enhance_book_spec_messages(book_spec, form):
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content":
            f"Make this specification for a bestseller-grade {form} more detailed "
            f"(specific settings, major events that differentiate the {form} "
            f"from others). Do not change the format or add more fields."
            f"Specification:{book_spec}"}
    ]
    return messages

from storytelling_agent import book_spec as book_spec

def json_book_spec_messages(text_book_spec):
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": book_spec.json_prompt(text_book_spec)},
    ]
    return messages

structure_24_chapter = """
1. Really Bad Day: establishes the character's flaws and desires through a conflict or problem they face
2. Something Peculiar: presents an unusual event that the protagonist ignores, foreshadowing future challenges
3. Grasping at Straws: shows the protagonist struggling to maintain control over their world, while questioning their choices and feeling a pull towards a different world. The INCITING INCIDENT marks a significant shift in the story with an event that disrupts the protagonist's status quo.
4. Call to Adventure: presents an extraordinary event that the protagonist cannot ignore, forcing them to confront new challenges
5. Head in Sand: shows the protagonist resisting the Call to Adventure, longing for their previous ordinary life
6. Pull out Rug: presents a personal and significant event that compels the protagonist to take action, despite their reluctance.
7. Enemies & Allies: introduces the protagonist to new characters, including potential allies, enemies, mentors, or love interests
8. Games & Trials: sees the protagonist facing challenges, undergoing training, and learning to harness newfound abilities
9. Earning Respect: focuses on the protagonist achieving a small victory, gaining begrudging respect, and boosting their self-confidence. The 1st FIRST PINCH POINT marks the protagonist's first major interaction with the antagonist or forces of evil, raising the stakes and increasing tension.
10. Forces of Evil: sees the protagonist facing the true dangers and implications of their involvement and confronting the antagonist's ultimate goal
11. Problem Revealed: sees the protagonist feeling excluded and demanding answers, showcasing their shaken confidence and newfound determination
12. Truth & Ultimatum: reveals critical information that alters the protagonist's worldview, forcing them to choose whether to commit to the journey ahead or not. The MIDPOINT marks the protagonist's transition from a defensive, reactive role to a proactive one, determined to fight back and win.
13. Mirror Stage: sees the protagonist transitioning from a passive, reactive role to a deliberate, active one, armed with new information and understanding of risks
14. Plan of Attack: sees the protagonist devising a plan with allies to confront the antagonist, considering potential obstacles and challenges
15. Crucial Role: sees the protagonist taking on a critical task with significant responsibility for the outcome of the conflict. The 2nd PINCH POINT marks a significant turning point in the story, where the protagonist faces forces representing the antagonist's interests
16. Direct Conflict: sees the protagonist and allies directly confronting the antagonist's higher-level forces, heightening tension and leaving the protagonist in a precarious situation
17. Surprise Failure: sees the protagonist's plan unraveling disastrously, leading to serious consequences and shattering strategies
18. Shocking Revelation: sees the protagonist uncovering crucial information about the antagonist's true identity or plan, raising the stakes and impacting the protagonist's emotional state, desires, and needs. The 2nd PLOT POINT plunges the protagonist into their darkest hour, where they suffer a crushing defeat, leading to a change in mindset and ultimately transforming into the hero needed to defeat the villain.
19. Giving Up: The protagonist loses confidence and gives up after a disastrous defeat, emphasizing their deteriorating mental state.
20. Pep Talk: An ally's pep talk helps rebuild the protagonist's confidence and inspires them to choose a new path forward.
21. Seizing the Sword: The protagonist addresses their fatal flaw, seizes the sword, and prepares to confront the antagonist. In the FINAL BATTLE the protagonist finds the resolve to confront the antagonist despite seemingly hopeless odds, leading to a dramatic turning point in the story.
22. Ultimate Defeat: The protagonist faces ultimate defeat at the hands of the antagonist, leading to a realization of their flaws and what must be done to overcome them.
23. Unexpected Victory: At the brink of defeat, the protagonist reveals a hidden weapon or ally and undergoes the final transformation in their character arc, leading to a triumphant victory.
24. Bittersweet Return: The protagonist emerges victorious, returns to the Ordinary World transformed, and ties up loose ends in the narrative. In REBIRTH the protagonist reflects on their growth and faces earlier challenges with newfound confidence.
25. Death of Self (optional): The protagonist experiences a rebirth and completes their character arc through a significant transformation.
"""

structure_save_the_cat = """
Act 1: The Beginning
1. Opening Image: A single scene beat that shows a “before” snapshot of the protagonist and the flawed world that he or she lives in.
2. Theme Stated: A single scene beat in which a statement is made by someone (other than the protagonist) that hints at what the protagonist will learn before the end of the story.
3. Setup: A multi-scene beat in which the reader gets to see what the protagonist’s life and the world are like–flaws and all. It’s also where important supporting characters and the protagonist’s initial goal (or the thing the protagonist thinks will fix his or her life) is introduced.
4. Catalyst: A single scene beat in which a life-changing event happens to the protagonist and catapults him or her into a new world or a new way of thinking. In other words, after this moment, there’s no going back to the “normal world” introduced in the setup.
5. Debate: A multi-scene beat where the protagonist debates what he or she will do next. Usually, there is some kind of question haunting them like, “should I do this?” or “should I do that?” The purpose of this beat is to show that the protagonist is reluctant to change for one reason or another.
6. Break Into Two: A single scene beat in which the protagonist decides to accept the call to adventure, leave their comfort zone, try something new, or to venture into a new world or way of thinking. It’s the bridge between the beginning (Act 1) and middle (Act 2) of the story.

Act 2A: The Middle (Part 1)
7. B Story: A single scene beat that introduces a new character or characters who will ultimately serve to help the hero learn the theme (or lesson) of the story. This character could be a love interest, a nemesis, a mentor, a family member, a friend, etc.
8. Fun and Games: A multi-scene beat where the reader gets to see the protagonist either shinning or floundering in their new world. In other words, they are either loving their new world or hating it.
9. Midpoint: A single scene beat where the fun and games section either culminates in a “false victory” (if your protagonist has been succeeding thus far) or a “false defeat” (if your protagonist has been floundering thus far) or a. In romance novels, this could be a kiss (or more), a declaration of love, or a marriage proposal. In a mystery or thriller, this could be a game-changing plot twist or a sudden ticking clock that ups the ante. This could even be a celebration or the first big public outing where the protagonist officially declares themselves a part of their new world. Whatever happens during this beat, it should raise the stakes and push the protagonist toward making a real change before moving forward.

Act 2B: The Middle (Part 2)
10. Bad Guys Close In: If the protagonist had a “false victory” at the Midpoint, this multi-scene beat would be a downward path where things get worse and worse for him or her. On the other hand, if the Midpoint was a “false defeat,” this section will be an upward path where things get better and better. Regardless of the path your protagonist takes during this multi-scene beat, his or her deep-rooted fear or false belief (their internal bad guys) and the antagonist (external bad guys) are closing in.
11. All is Lost: A single scene beat where something happens, that when combined with the threat of the bad guys closing in, pushes your protagonist to their lowest point.
12. Dark Night of the Soul: A multi-scene beat in which the protagonist takes time to process everything that’s happened so far. This is his or her darkest hour—the moment right before he or she figures out the solution to their big problem and learns the theme or life lesson of the story.
13. Break Into Three: A single scene beat where the protagonist realizes what he or she must do to fix not only the external story problems but more importantly, their internal problems as well.

Act 3: The End
14. Finale: A multi-scene beat where the protagonist proves they have learned the story’s theme and acts on the plan he or she made in the Break Into Three scene. 
15. Final Image: A single scene beat that shows the reader an “after” snapshot of your protagonist’s life and how much he or she has changed since the beginning of the story.
"""

plot_structure = {
    "derek murphy plot outline": structure_24_chapter,
    "save the cat": structure_save_the_cat
}

def create_plot_messages(book_spec, form, plot_template):
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": (
            f"Come up with a plot for a bestseller-grade {form} using the {plot_template} plot structure below taking inspiration from the book specification given below. Include ALL plot points and SECTION BREAKS listed in the specification.\n\n"
            f"<plot-structure>{plot_structure[plot_template]}</plot-structure>\n\n"
            f"<book-specification>{book_spec}</book-structure>"
            )}
    ]
    return messages

from storytelling_agent import plot_spec as plot_spec

def json_plot_messages(text_plot):
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": plot_spec.json_prompt(text_plot)},
    ]
    return messages

from storytelling_agent import scene_spec as scene_spec

def scene_beats_from_summary_messages(form, book_spec, summary):
    content = (
        f"Here is the overall book specification with the main characters:\n\n"
        f"<book-specification>{book_spec}</book-specification>"
    )
    json_prompt = scene_spec.json_prompt(summary)
    content =  json_prompt + content

    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": content}
    ]
    return messages

from storytelling_agent import prose_spec as prose_spec

def scene_messages(scene: str, previous_scene: str|None, book_spec: str, form: str):
    system = """
You are an expert fiction writer.

Always keep the following rules in mind:
- Use American English spelling, grammar, and colloquialisms/slang.
- Write in active voice.
- Write detailed scenes with lively dialogue.
- Always follow the "show, don't tell" principle.
- Avoid adverbs and cliches and overused/commonly used phrases. Aim for fresh and original descriptions.
- Convey events and story through dialogue.
- Mix short, punchy sentences with long, descriptive ones. Drop fill words to add variety.
- Skip "he/she said said" dialogue tags and convey people's actions or face expressions through their speech.
- Avoid mushy dialog and descriptions, have dialogue always continue the action, never stall or add unnecessary fluff. Vary the descriptions to not repeat yourself.
- Put dialogue on its own paragraph to separate scene and action.
- Reduce indicators of uncertainty like "trying" or "maybe".
    """
    content = (
        f"Write a detailed scene based on the scene information given below.\n"
        f"Be creative, explore interesting characters and unusual settings. Do NOT use foreshadowing.\n\n"
    )
    json_prompt = prose_spec.json_prompt(scene, previous_scene, book_spec)
    content += json_prompt

    messages = [
        {"role": "system", "content": f"You are writing a {form}." + system},
        {"role": "user", "content": content },
    ]
    return messages
