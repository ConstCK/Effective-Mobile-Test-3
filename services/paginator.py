from typing import Generator


class PaginatorService:
    def __init__(self) -> None:
        pass

    @staticmethod
    def paginate_data(data: list[dict[str, str | int]], size: int = 5) -> Generator:
        """Пагинация выдаваемых данных по размеру (size)"""
        start: int = 0
        while start < len(data):
            yield data[start:size + start]
            start += size
