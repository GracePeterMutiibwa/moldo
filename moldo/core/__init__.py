from .MoldoEntry import cast


class ParserInterface:
    def parse(self, moldoCode: str):
        return cast(moldoCode)


__all__ = ["ParserInterface"]
