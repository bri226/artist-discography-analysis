# Import required libraries
import matplotlib.pyplot as plt
from nrclex import NRCLex
from wordcloud import WordCloud, STOPWORDS
import nltk
nltk.download('punkt')

# Define the lyrics of the song
lyrics = """Today I feel between clouds\n
I think I'm going to explode\n
And I get tangled with the hours\n
I don't know if you will arrive\n
And when you look back you get closer, now\n
My body shudders when I see you walk\n
And when I feel the burning night on my skin\n
My heart shakes, I am reborn again\n

[Chorus]\n
Tonight I'm going to dance with you\n
The moment is ours and it does not end
Tonight I'm going to dream with you\n
That life is rhythm, it is joy\n
Tonight I'm going to dance with you\n
Being with you makes me free\n
Tonight I'm going to dream with you\n
That love is ours and it does not end\n
You might also like[Verse 2]\n
I'm going back happy\n
I feel like screaming\n
If you want I must see you\n
You just tell me and that's it\n
And with the sun the darkness will go away\n
The energy in our body will never stop\n
This is the rhythm, the one that makes me vibrate\n
And even if I wanted to stop, I can't stop\n

[Chorus]\n
Tonight I'm going to dance with you\n
The moment is ours and it does not end
Tonight I'm going to dream with you\n
That life is rhythm, it is joy\n
Tonight I'm going to dance with you\n
Being with you makes me free\n
Tonight I'm going to dream with you\n
That love is ours and it does not end\n

Tonight I'm going to dance with you\n
The moment is ours and it does not end
Tonight I'm going to dream with you\n
That life is rhythm, it is joy\n

Tonight I'm going to dance with you\n
Being with you makes me free\n
Tonight I'm going to dream with you\n
That life is rhythm, it is joy\n
Tonight I'm going to dance with you\n
The moment is ours and it does not end
Tonight I'm going to dream with you\n
That life is rhythm, it is joy\n

Tonight I'm going to dance with you\n

Tonight I'm going to dream with you"""

# Splitting the lyrics into lines for emotion analysis
lines = lyrics.split('\n')

# Emotion Analysis using NRCLex
emotion_scores = { 'fear': 0, 'anger': 0, 'anticip': 0, 'trust': 0, 'surprise': 0, 'positive': 0, 'negative': 0, 'sadness': 0, 'disgust': 0, 'joy': 0 }

for line in lines:
    if line.strip():  # Check if the line is not empty
        text_object = NRCLex(line)
        for emotion in emotion_scores.keys():
            emotion_scores[emotion] += text_object.affect_frequencies.get(emotion, 0)

# Normalizing the scores
total_lines = len([line for line in lines if line.strip()])
for emotion in emotion_scores:
    emotion_scores[emotion] /= total_lines

# Visualization - Bar Chart
emotions = list(emotion_scores.keys())
scores = list(emotion_scores.values())

plt.figure(figsize=(10, 6))
bars = plt.bar(emotions, scores, color='skyblue')

# Adding value labels on each bar
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), ha='center', va='bottom')

plt.xlabel('Emotions')
plt.ylabel('Scores')
plt.title('Emotion Analysis of "your song choice"')
plt.xticks(rotation=45)
plt.show()

# Word Cloud Generation
# Define a set of words to exclude (common and explicit words)
explicit_stopwords = {'[Coro]', 'explicit2', 'explicit3'}  # Replace with actual explicit words
stopwords = set(STOPWORDS).union(explicit_stopwords)

wordcloud = WordCloud(width=800, height=800, 
                      background_color='white', 
                      stopwords=stopwords, 
                      min_font_size=10).generate(lyrics)

# Displaying the Word Cloud
plt.figure(figsize=(8, 8), facecolor=None) 
plt.imshow(wordcloud) 
plt.axis("off") 
plt.tight_layout(pad=0)
plt.show()