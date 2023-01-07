from starlette.types import ASGIApp, Message, Receive, Scope, Send


class RequestIDMiddleware:
    def __init__(self, app: ASGIApp, x_request_id_header: str, counter_prefix: str):
        """
        The __init__ function is called when an instance of the class is created.
        It initializes attributes that are common to all instances of the class.

        :param app:ASGIApp: Used to Pass the asgiapp instance to which this middleware will be attached.
        :param x_request_id_header:str: Used to Set the header name that will be used to retrieve the request id from.
        :param counter_prefix:str: Used to Prefix the request counter.
        :return: The values of the parameters passed to it.
        """

        self.app = app
        self.x_request_id_header = str.encode(x_request_id_header)
        self.request_counter = 1
        self.counter_prefix = counter_prefix

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        self.request_counter += 1
        # skip adding new one, if there is x-request-id
        headers = scope["headers"]
        for (header, h_value) in headers:
            if header == self.x_request_id_header:
                await self.app(scope, receive, send)
                return
        request_id = str.encode(f"{self.counter_prefix}-{self.request_counter}")
        headers.append((self.x_request_id_header, request_id))

        responder = _RequestIDResponder(self.app, self.x_request_id_header, request_id)
        await responder(scope, receive, send)


class _RequestIDResponder:
    def __init__(
        self, app: ASGIApp, x_request_id_header: bytes, request_id: bytes
    ) -> None:
        self.x_request_id_header = x_request_id_header
        self.request_id = request_id
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        self.send = send
        await self.app(scope, receive, self.my_send)

    async def my_send(self, message: Message) -> None:
        message_type = message["type"]
        if message_type == "http.response.start":
            headers = message["headers"]
            headers.append((self.x_request_id_header, self.request_id))

        await self.send(message)
