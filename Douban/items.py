from scrapy import Item, Field


class CommMeta(Item):
    name = Field()
    movie_name = Field()
    movie_rating = Field()
    movie_time = Field()
    actor = Field()
    director = Field()
    comm = Field()


class StartMeta(Item):
    id = Field()
    rate = Field()
    title = Field()
    url = Field()
