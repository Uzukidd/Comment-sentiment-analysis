from wordcloud import WordCloud as wc


def wordCloudSpawn(text) :

    wordclouds = wc(#mask = mask,
                   font_path ='..\\Resources\\font.ttf',
                   width = 4096,
                   height = 2048,
                   mode = 'RGBA',
                   prefer_horizontal = 1.0,
                   scale = 1,
                   max_words = 200,
                   background_color = '#000000',
                   color_func = random_color_func).generate_from_frequencies(text)

    wordclouds.to_file('..\\wordcloud.png')

    return wordclouds





def random_color_func(word=None, font_size=None, position=None, orientation=None, font_path=None, random_state=None):
    r = 255
    g = 255
    b = 255
    return "rgb({}, {}, {})".format(r, g, b)
