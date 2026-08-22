from langchain_community.tools import DuckDuckGoSearchRun


class WebSearch:

    def __init__(self):
        self.search = DuckDuckGoSearchRun()

    def search_web(self, query: str) -> str:

        if not query or not query.strip():
            return ""

        result = self.search.run(
            query.strip()
        )

        if not result:
            return ""

        return result[:4000]