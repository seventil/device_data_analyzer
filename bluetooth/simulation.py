import asyncio
from bluetooth.processor import BltMessageProcessor

EMF_MESSAGE_START = b"E="
EMF_MESSAGE_END = b"EMF_DATA_SENT"
STOP_BLT_COMMUNICATION_MESSAGE = "Connection Stopped"


class BltMessageProcessorSimulation(BltMessageProcessor):
    def __init__(self, command_queue: asyncio.Queue):
        super().__init__(command_queue)
        self.message = [
            b'WHO=TPC-7PRO #91\rK0Text=CT\rK1Text=Al\rK2Text=Ni\rK3Text=--\r',
            b'B=N_CHRG\r', b'SCALE=HRc\r', b'CALIB=CT\r', b'B=72\r',
            b'B=N_CHRG\r', b'SCALE=HB\r', b'CALIB=CT\r', b'B=72\r',
            b'RECALC\r', b'K=0.531\r', b'H=345\r',
            b'E=01845\rE=01845\rE=01845\rE=01845\rE=01845\rE=01845\rE=01845\rE=01846\rE=01846\rE=01846\rE=01847\rE=01847\rE=01847\rE=01848\rE=01848\rE=01848\rE=01848\rE=01848\rE=01848\rE=0',
            b'1849\rE=01849\rE=01849\rE=01849\rE=01849\rE=01849\rE=01849\rE=01849\rE=01849\rE=01849\rE=01849\rE=01848\rE=01848\rE=01848\rE=01848\rE=01848\rE=01848\rE=01848\rE=01848\rE=01848\r',
            b'R=0.000600\r', b'V=0.629000\r', b'EMF_DATA_SENT\r',
        ]*3

    def message_generator(self):
        for bit in self.message:
            yield bit

    async def scan_tpc_devices(self):
        await asyncio.sleep(1)
        self._tpc_devices = {"name": "test_tpc"}
        await self.command_queue.put(self._tpc_devices)

    async def run_client_for_device(self, device_name: str):
        print(f"connect to device {self._tpc_devices}")
        print(f"requested for {device_name}")
        await self.simulate_callback_handler()

    async def simulate_callback_handler(self):
        message_gen = self.message_generator()
        while True:
            try:
                received_message = next(message_gen)
                
                await self.process_received_message(received_message)

            except StopIteration as e:
                print('Stopped receiving messages from LTE device', e)
                await self.command_queue.put(STOP_BLT_COMMUNICATION_MESSAGE)
                break
            await asyncio.sleep(0.35)