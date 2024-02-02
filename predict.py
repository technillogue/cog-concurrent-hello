import asyncio
import logging
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
        self.task = asyncio.create_task(self.work())
        self.task.add_done_callback(handle_error)
        self.batch: list[tuple[str, asyncio.Queue[str]]] = []

    async def work(self) -> None:
        while 1:
            if not self.batch:
                await asyncio.sleep(sleepy * 5)
                continue
            batch, self.batch = self.batch, []
            for i in range(10):
                for input, output in batch:
                    await output.put(f"hello {input} (#{i})")
                await asyncio.sleep(sleepy)
            await asyncio.sleep(sleepy)

    async def predict(
        self, name: str = Input(default=None), name_file: Path = Input(default=None)
    ) -> AsyncIterator[str]:
        q = asyncio.Queue()
        if not (name or name_file):
            raise ValueError("one of name or name_file is required")
        actual_name = open(name_file).read() if name_file else name
        self.batch.append((actual_name, q))
        for _ in range(10):
            yield await q.get()
