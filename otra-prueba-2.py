
from nrclex import NRCLex
text = 'As the curtains parted, revealing a room full of familiar faces, she gasped in surprise at the unexpected birthday celebration.'
emotion = NRCLex(text)
print(emotion.top_emotions)

# {'full': ['positive'], 
#  'familiar': ['positive', 'trust'], 
#  'surprise': ['fear', 'joy', 'positive', 'surprise'], 
#  'unexpected': ['anticipation', 'fear', 'joy', 'negative', 'positive', 'surprise'], 
#  'birthday': ['anticipation', 'joy', 'positive', 'surprise'], 
#  'celebration': ['anticipation', 'joy', 'positive', 'surprise', 'trust']}