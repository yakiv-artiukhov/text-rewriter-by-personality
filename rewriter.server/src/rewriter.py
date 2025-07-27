from collections.abc import Generator

from .langchain_gemini import get_prompt_template, template_message, template_message_streamed
from .prompt_templates.rewriter_by_personality import rewriter_prompt_template

user_request_xml = """
<text_fragment>{}</text_fragment>
<personality_description>{}</personality_description>
""" 

def rewrite_by_personality(text_fragment: str, personality_description: str) -> str:
    
    prompt_template = get_prompt_template(rewriter_prompt_template)
    message = user_request_xml.format(text_fragment, personality_description)
    
    return template_message(message, prompt_template)

def rewrite_by_personality_streamed(text_fragment: str, personality_description: str) -> Generator[str, None, None]:
    
    prompt_template = get_prompt_template(rewriter_prompt_template)
    message = user_request_xml.format(text_fragment, personality_description)

    return template_message_streamed(message, prompt_template)






# test_fragment = "The rain had just stopped, leaving the streets slick and shimmering under the glow of streetlamps. Puddles mirrored the sky, still heavy with clouds that refused to move on. I walked slowly, the quiet drip of water from rooftops the only sound for blocks. There was a strange comfort in the emptiness, like the world had decided to whisper instead of shout."
# test_fragment_huge = """I woke before the alarm, the kind of waking that comes not from rest, but from something unsettled beneath the surface. Outside, the sky was a dull gray, hinting at rain but refusing to commit. I made coffee without thinking—each motion muscle memory—grinding beans, pouring water, watching steam curl like smoke from a small fire. The silence of the apartment felt too sharp, too full. I sat by the window, the cup warm in my hands, watching people drift by on the street below—umbrellas, scarves, rushed steps. Everyone seemed to know where they were going. I wasn’t sure I did.
# The clock ticked loudly in the kitchen, and for some reason, I couldn’t stop hearing it. It marked time not like a guide, but like a warning.
# I thought about texting someone. I didn’t. I thought about going somewhere. I didn’t. I thought about change—the kind you don’t see coming, and the kind you beg for.
# A single crow landed on the fire escape and looked at me, head tilted, eyes too aware. I almost nodded at it, as if to say, “Yes. I see it too.”
# The rain began finally, soft and slow, more like a whisper than a storm. It didn’t feel like a beginning or an ending. Just a quiet continuation.
# I took another sip of coffee. It had gone cold."""
# test_personality = "A tech bro who just sold his startup"

# res = rewriter_by_personality(test_fragment, test_personality)
# print(f"res type: {type(res)} + \n")
# print("res:\n" + res + "\n")


# res_streamed = rewriter_by_personality_streamed(test_fragment, test_personality)
# print(f"res_streamed type: {type(res_streamed)} + \n")
# print("res_streamed:\n")
# for chunk in res_streamed:
#     print(chunk, end="|", flush=True)


# res_streamed_huge = rewriter_by_personality_streamed(test_fragment_huge, test_personality)
# print(f"res_streamed type: {type(res_streamed_huge)}\n")
# print("res_streamed:\n")
# for chunk in res_streamed_huge:
#     print(chunk, end="|", flush=True)
