import asyncio

class AsyncQueue:
    def __init__(self):
        self.queue = asyncio.Queue()
        self.lock = asyncio.Lock()

    async def add(self, item):
        async with self.lock:  # Гарантия последовательного добавления
            await self.queue.put(item)
            position = self.queue.qsize()  # Определяем позицию элемента
        print(f"Элемент {item} добавлен в очередь. Его позиция: {position}")
        return position

    async def process(self):
        while True:
            item = await self.queue.get()
            print(f"Обрабатываю элемент: {item}")
            await asyncio.sleep(1)  # Симуляция обработки
            self.queue.task_done()

async def main():
    async_queue = AsyncQueue()

    # Добавление элементов в очередь
    await async_queue.add("A")
    asyncio.create_task(async_queue.process())
    await async_queue.add("B")
    await async_queue.add("C")

    # Обработка очереди
    #asyncio.create_task(async_queue.process())

    # Ждем завершения обработки всех элементов
    await async_queue.queue.join()

# Запускаем asyncio-программу
asyncio.run(main())
