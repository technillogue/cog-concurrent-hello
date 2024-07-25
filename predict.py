import asyncio
import random
import logging
import string
import random
from typing import AsyncIterator, Optional

from cog import BasePredictor, Path, Input


def handle_error(task: "asyncio.Task[None]") -> None:
    if task.cancelled():
        return
    exc = task.exception()
    if exc:
        logging.error("caught exception", exc_info=exc)
    print(task)


sleepy = 1


class Predictor(BasePredictor):
    async def setup(self) -> None:
        pass

    #     self.task = asyncio.create_task(self.work())
    #     self.task.add_done_callback(handle_error)
    #     self.batch: list[tuple[str, asyncio.Queue[str]]] = []

    # async def work(self) -> None:
    #     while 1:
    #         if not self.batch:
    #             await asyncio.sleep(sleepy * 5)
    #             continue
    #         batch, self.batch = self.batch, []
    #         for i in range(10):
    #             for input, output in batch:
    #                 await output.put(f"hello {input} (#{i})")
    #             await asyncio.sleep(sleepy)
    #         await asyncio.sleep(sleepy)

    async def predict(
        self,
        name: str = Input(default=None),
        name_file: Path = Input(default=None),
        n: int = 100,
        sleep: float = 0.0001,
    ) -> AsyncIterator[str]:
        print("this is a log message")
        if not (name or name_file):
            raise ValueError("one of name or name_file is required")
        actual_name = open(name_file).read() if name_file else name
        letter = random.choice(string.ascii_letters)
        actual_name += letter
        for i in range(n):
            yield f"hello {actual_name} {i}"
            await asyncio.sleep(0.0001)
