import logging
import asyncio
import uuid

from aiomultiprocess import Pool

class TransferScheduler:
    def __init__(self, source, destination, numTransfers: int):
        self.source = source
        self.destination = destination
        self.numTransfers = numTransfers
        self.transferID = uuid.uuid4().hex

    def makeTransferQueue(self):
        logging.info("Building queue...")
        for num in range(self.numTransfers):
            logging.debug(f"Added {num}/{self.numTransfers} transfers to queue")
            cmd = ['gfal-copy' , '-f']
            cmd += [f'https://{self.source}/testSourceFile{num}']
            cmd += [f'https://{self.destination}/testDestFile{num}_{self.transferID}']
            yield cmd
        logging.info("Queue built successfully")

    @staticmethod
    async def worker(cmd) -> None:
        while True:
            process = await asyncio.create_subprocess_exec(
            *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
            
            stdout, stderr = await process.communicate()
            result = stdout.decode().strip()

    async def runTransfers(self) -> None:
        queue = self.makeTransferQueue()

        logging.info("Starting Transfers")
        async with Pool(processes=2) as pool:
            await pool.map(self.worker, queue)

    def startTransfers(self) -> None:
        print(f"Running {self.numTransfers} {self.source} --> {self.destination} transfers...")
        asyncio.run(self.runTransfers())
