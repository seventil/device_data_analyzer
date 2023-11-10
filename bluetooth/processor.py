"""Module that contains class to transform commands, comming from TPC bluetooth
"""

import asyncio

EMF_MESSAGE_START = b"E="
EMF_MESSAGE_END = b"EMF_DATA_SENT"
STOP_BLT_COMMUNICATION_MESSAGE = "Connection Stopped"


class BltMessageProcessor:
    def __init__(self, command_queue: asyncio.Queue):
        self.command_queue = command_queue
        self.total_message = None

    async def process_received_message(self, received_message) -> None: 
        # TODO make sure that health check does not spoil emf gathering
        if EMF_MESSAGE_START in received_message and self.total_message is None:
            print(f"received emf message start E= in data {received_message}")
            self.total_message = []

        elif EMF_MESSAGE_END in received_message:
            total_command_message = "".join(self.total_message)
            command = self.process_command(total_command_message)
            await self.command_queue.put(command)
            self.total_message = None

        elif self.total_message is None: # this spoils emf
            command = self.process_command(received_message.decode("utf-8"))
            await self.command_queue.put(command)

        elif self.total_message is not None:
            self.total_message.append(received_message.decode("utf-8"))
            print("gathering emf")

    def process_command(self, command: str) -> dict:
        processed_command = {}
        for message in command.split("\r"):
            if "=" not in message: # and if = is not in message, the command is lost?
                continue

            key, value = message.split("=")
            if processed_command.get(key) is None:
                processed_command[key] = []
            processed_command[key].append(value)
        return processed_command