from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from typing import List


def generate_word_cloud(results_dict: dict, date_list: List[str], num_search_results: int)-> None:
    """Generate a word cloud from the dictionary, using an image as mask"""

    word_input = ''
    stopwords = set(STOPWORDS)
    stopwords.update(['say', 'says'])

    # Create image mask
    mask = np.array(Image.open("img/mickey_mouse.jpg"))

    # Add words from each headline to dictionary
    for i in range(len(date_list)):
        date = date_list[i]
        for j in range(num_search_results):
            key = str(date) + ',' + str(j)
            try:
                title = results_dict.get(key)
                title_split = title.split(' ')

                for val in title_split:
                    tokens = val.split(' ')

                    # Converts word to lowercase
                    for i in range(len(tokens)):
                        tokens[i] = tokens[i].lower()

                        word_input += " ".join(tokens) + " "
            except:
                continue

    wordcloud = WordCloud(max_font_size=40, stopwords=stopwords, background_color="white", mode="RGBA", min_font_size=0, mask=mask, relative_scaling=0).generate(word_input)  #

    # Retrieve colors from image
    image_colors = ImageColorGenerator(mask)
    plt.imshow(wordcloud.recolor(color_func=image_colors), interpolation="bilinear")
    plt.axis("off")

    # Store word cloud as PNG image
    plt.savefig("img/word_cloud_palm.png", format="png")
    plt.show()

    return None

