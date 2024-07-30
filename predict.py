import asyncio
import random
import string
from typing import AsyncIterator

from cog import BasePredictor, Path, Input


sleepy = 1


class Predictor(BasePredictor):
    async def setup(self) -> None:
        pass

    async def predict(
        self,
        name: str = Input(default=None),
        name_file: Path = Input(default=None),
        n: int = 100,
        sleep: float = 0.0001,
        log: str = True,
    ) -> AsyncIterator[str]:
        if log:
            print("this is a log message")
        if not (name or name_file):
            raise ValueError("one of name or name_file is required")
        actual_name = open(name_file).read() if name_file else name
        letter = random.choice(string.ascii_letters)
        actual_name += letter
        for i in range(n):
            yield f"hello {actual_name} {i}"
            await asyncio.sleep(0.0001)
