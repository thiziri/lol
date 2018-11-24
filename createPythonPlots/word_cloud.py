# Start with loading all necessary libraries
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

text = """
    how does interlibrary loan work
    what countries did immigrants come from during the immigration
    what can be powered by wind
    how jameson irish whiskey is made
    how many days are in a leap year
    what company is cricket wireless by
    what does karma mean in buddhism
    what are points on a mortgage
    what is a wwII theater
    when did ms .drgs go into effect
    who makes skittles ?
    who won the 1967 nba championship
    What Is Range in Math
    WHAT IS PARESTHESIAS OF HANDS
    what is general chu chicken
    what was the city of Mithridates
    what is the la tour de france
    when was the tacoma bridge collapse ?
    where was hillary clinton born
    what is the type of democracy in which all citizens have the right to make government decisions
    what were 3 important things that douglas MacArthur did ?
"""
# Create and generate a word cloud image:
STOPWORDS = ["the", "of"]
stopwords = set(STOPWORDS)
wordcloud = WordCloud(max_font_size=50, max_words=100, background_color="white", stopwords=stopwords).generate(text)

# Display the generated image:
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()