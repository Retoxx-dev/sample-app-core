import aio_pika
import asyncio
import settings


class RabbitMQSender:
    def __init__(self, connection_string, queue_name):
        self.connection_string = connection_string
        self.queue_name = queue_name
        self.connection = None
        self.channel = None

    async def connect(self):
        self.connection = await aio_pika.connect_robust(
            self.connection_string, 
            heartbeat=60,
            on_connection_lost=self.on_connection_lost
        )

        self.channel = await self.connection.channel()
        settings.logging.info("Channel created")

        self.queue = await self.channel.declare_queue(self.queue_name,
                                                      durable=True)

        settings.logging.info("Connected to RabbitMQ!")

    async def send_message(self, message):
        if not self.connection:
            raise RuntimeError("RabbitMQ connection is not established!")

        message_obj = aio_pika.Message(body=message.encode())

        await self.channel.default_exchange.publish(message_obj,
                                                    routing_key=self.queue.name)

        settings.logging.info(" [x] Sent the message to the queue!")

    async def close(self):
        if self.connection:
            await self.connection.close()
            settings.logging.info("Connection to RabbitMQ closed!")

    def on_connection_lost(self, connection, exception):
        settings.logging.warning(f"Connection to RabbitMQ lost: {exception}")


sender = RabbitMQSender(settings.RABBITMQ_CONNECTION_STRING,
                        settings.RABBITMQ_QUEUE_NAME)
loop = asyncio.get_event_loop()
loop.create_task(sender.connect())
