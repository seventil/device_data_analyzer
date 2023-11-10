import asyncio
from processor import BltMessageProcessor
from bleak import BleakScanner, BleakClient

STOP_BLT_COMMUNICATION_MESSAGE = "Connection Stopped"
EMF_MESSAGE_START = b"E="
EMF_MESSAGE_END = b"EMF_DATA_SENT"
TPC_NAME_PREFIX = "TPC-7"
HEALTH_CHECK_INTERVAL = 32

TPC_7_89_MAC = "04:91:62:A5:0B:43"
TPC_NAMES = ["TPC-7 #89", "TPC-7PRO #91"]
TPC_RTX = "49535343-1e4d-4bd9-ba61-23c647249616"
TPC_TX = "49535343-8841-43f4-a8d4-ecbe34729bb3"
TBluetoothUUID = "49535343-FE7D-4AE5-8FA9-9FAFD205E455"

class BltMessageProcessorBleak(BltMessageProcessor):

    def __init__(self, command_queue):
        super().__init__(command_queue)
        self._tpc_devices = None
        self._device_client = None
        self._health_check_task = None
    
    async def scan_tpc_devices(self): # TODO crashes when no devices, should just send command with empty list of devices
        nearby_lte_devices = await BleakScanner().discover()
        if nearby_lte_devices is None:
            raise LookupError(f"No LTE devices were not found")

        tpc_devices = {}

        for device in nearby_lte_devices:
            name = device.name
            if name is None:
                continue
            if TPC_NAME_PREFIX in name:
                tpc_devices[device.name] = device
        if len(tpc_devices.keys()) > 0:
            print(f"found the following lte devices: {tpc_devices}")
            self._tpc_devices = tpc_devices
        else:
            raise LookupError(f"{TPC_NAME_PREFIX} were not found in broadcasting LTE devices")
        print("finished scan")

    async def run_client_for_device(self, device_name: str): # TODO crashes when device is turned off, # TODO cancel error on app exit # TODO run client should be device agnostic
        print("function run client for device started")
        if self._device_client is not None:
            await self.stop_client_for_device()
        if self._tpc_devices is None:
            raise RuntimeError(f"Devices were not scanned, nothing to connect to")
        device = self._tpc_devices.get(device_name) # TODO get from None throuws exepction
        if device is None:
            raise RuntimeError(f"Device {device_name} was not available in scanned devices")

        self._device_client = BleakClient(device)
        await self._device_client.connect()
        await self._device_client.start_notify(TPC_RTX, self.callback_handler)

        # loop = asyncio.get_event_loop()
        # self._health_check_task = loop.create_task(self.health_check())
        # await self._health_check_task

    async def callback_handler(self, _, data): # TODO rewrite using simulation callback
        # TODO add healthcheck reset
        with open("inputdatalog.txt", "a") as fstream:
            fstream.write(str(data))
        await self.process_received_message(data)

    async def stop_client_for_device(self):
        print("stopping client")
        if self._device_client is not None:
            await self._device_client.stop_notify(TPC_RTX)
            await self._device_client.disconnect()
            await self.command_queue.put(STOP_BLT_COMMUNICATION_MESSAGE)
            self._device_client = None
            print("Client stopped")
        else:
            raise RuntimeError("No device client to stop assigned")
        if self._health_check_task is not None:
            self._health_check_task.cancel()
            self._health_check_task = None

    async def health_check(self):
        while True: # TODO better have some kind of counter, that resets on a received message in callback handler
            await asyncio.sleep(HEALTH_CHECK_INTERVAL)
            print("Implement healthcheck already") 