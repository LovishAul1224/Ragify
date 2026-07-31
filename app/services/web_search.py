from langchain_community.tools import DuckDuckGoSearchRun


class WebSearch:

    def __init__(self):
        self.search = DuckDuckGoSearchRun()


    def search_web(self, query: str):

        result = self.search.run(query)

        return result[:4000]