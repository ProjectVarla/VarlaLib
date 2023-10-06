from asyncio import (
    FIRST_COMPLETED,
    AbstractEventLoop,
    Future,
    Queue,
    create_task,
    new_event_loop,
    wait,
)
from os import getpid, kill

# from signal import CTRL_C_EVENT, SIGINT
from sys import platform, stdout
from threading import Thread
from typing import Any, Set

from websockets.exceptions import ConnectionClosed
from websockets.frames import Close
from websockets.legacy.client import connect

from VarlaLib.Context import context

from ...Decorations import Colorize, Colors


# def exit_from_event_loop_thread(
#     loop: AbstractEventLoop,
#     stop: Future[None],
# ) -> None:
#     loop.stop()
#     if not stop.done():
#         # When exiting the thread that runs the event loop, raise
#         # KeyboardInterrupt in the main thread to exit the program.
#         if platform == "win32":
#             ctrl_c = CTRL_C_EVENT
#         else:
#             ctrl_c = SIGINT
#         kill(getpid(), ctrl_c)


# def print_during_input(string: str) -> None:
#     stdout.write(
#         # Save cursor position
#         "\N{ESC}7"
#         # Add a new line
#         "\N{LINE FEED}"
#         # Move cursor up
#         "\N{ESC}[A"
#         # Insert blank line, scroll last line down
#         "\N{ESC}[L"
#         # Print string in the inserted blank line
#         f"{string}\N{LINE FEED}"
#         # Restore cursor position
#         "\N{ESC}8"
#         # Move cursor down
#         "\N{ESC}[B"
#     )
#     stdout.flush()


# def print_over_input(string: str) -> None:
#     stdout.write(
#         # Move cursor to beginning of line
#         "\N{CARRIAGE RETURN}"
#         # Delete current line
#         "\N{ESC}[K"
#         # Print string
#         f"{string}\N{LINE FEED}"
#     )
#     stdout.flush()


# async def nothing():
#     return None


# async def run_client(
#     uri: str,
#     loop: AbstractEventLoop,
#     inputs: Queue[str],
#     stop: Future[None],
#     varla,
# ) -> None:
#     try:
#         websocket = await connect(uri)
#     except Exception as exc:
#         varla.error(f"Failed to connect to {uri}: {exc}.")
#         websocket = None

#     try:
#         while True:
#             incoming: Future[Any] = create_task(
#                 websocket.recv() if websocket else nothing()
#             )
#             outgoing: Future[Any] = create_task(inputs.get())
#             done: Set[Future[Any]]
#             pending: Set[Future[Any]]
#             done, pending = await wait(
#                 [incoming, outgoing, stop], return_when=FIRST_COMPLETED
#             )
#             if websocket:

#                 # Cancel pending tasks to avoid leaking them.
#                 if incoming in pending:
#                     incoming.cancel()
#                 if outgoing in pending:
#                     outgoing.cancel()

#                 if incoming in done:
#                     try:
#                         message = incoming.result()
#                     except ConnectionClosed:
#                         break
#                     else:
#                         if isinstance(message, str):
#                             # print_during_input(
#                             #     Colorize(
#                             #         text=f"FileManager >> ",
#                             #         style=Colors.MD.BOLD,
#                             #         foreground=Colors.FG.CYAN,
#                             #     )
#                             #     + message
#                             # )
#                             varla.say(message, name="FileManager")

#                         else:
#                             print_during_input("< (binary) " + message.hex())

#             if outgoing in done:

#                 message = outgoing.result()
#                 # await websocket.send(message)
#                 varla.parse_command(message)

#             if stop in done:
#                 break
#     except Exception as e:
#         print(e)
#         await varla.say(e)
#     finally:
#         if websocket:
#             await websocket.close()
#             assert (
#                 websocket.close_code is not None and websocket.close_reason is not None
#             )
#             close_status = Close(websocket.close_code, websocket.close_reason)

#         # print_over_input(f"Connection closed: {close_status}.")
#         varla.say(str(websocket))
#         exit_from_event_loop_thread(loop, stop)


# def run_socket(uri, varla):
#     # Create an event loop that will run in a background thread.
#     context.loop = new_event_loop()

#     # Due to zealous removal of the loop parameter in the Queue constructor,
#     # we need a factory coroutine to run in the freshly created event loop.
#     async def queue_factory() -> Queue[str]:
#         return Queue()

#     # Create a queue of user inputs. There's no need to limit its size.
#     context.inputs: Queue[str] = context.loop.run_until_complete(queue_factory())

#     # Create a stop condition when receiving SIGINT or SIGTERM.
#     context.stop: Future[None] = context.loop.create_future()

#     # Schedule the task that will manage the connection.
#     context.loop.create_task(
#         run_client(uri, context.loop, context.inputs, context.stop, varla)
#     )

#     # Start the event loop in a background thread.
#     context.thread = Thread(target=context.loop.run_forever)
#     context.thread.start()


def test(uri, varla) -> None:

    try:
        import readline  # noqa
    except ImportError:  # Windows has no `readline` normally
        pass

    context.thread = None
    context.socket_id = None

    # # Create an event loop that will run in a background thread.
    # loop = new_event_loop()

    # # Due to zealous removal of the loop parameter in the Queue constructor,
    # # we need a factory coroutine to run in the freshly created event loop.
    # async def queue_factory() -> Queue[str]:
    #     return Queue()

    # # Create a queue of user inputs. There's no need to limit its size.
    # inputs: Queue[str] = loop.run_until_complete(queue_factory())

    # # Create a stop condition when receiving SIGINT or SIGTERM.
    # stop: Future[None] = loop.create_future()

    # # Schedule the task that will manage the connection.
    # context.loop = loop
    # loop.create_task(run_client(uri, loop, inputs, stop, varla))

    # # Start the event loop in a background thread.
    # thread = Thread(target=loop.run_forever)
    # thread.start()

    # Read from stdin in the main thread in order to receive signals.
    try:
        while True:
            # Since there's no size limit, put_nowait is identical to put.
            message = varla.ask()

            if message == "status":
                print(context)

            elif context.thread:
                context.loop.call_soon_threadsafe(context.inputs.put_nowait, message)

            else:

                varla.parse_command(message)
    except Exception as e:  # (KeyboardInterrupt, EOFError):  # ^C, ^D
        print("hello", e)
        raise e
        # if context.thread:
        #     context.loop.call_soon_threadsafe(context.stop.set_result, None)

        #     # # Wait for the event loop to terminate.
        #     context.thread.join()

        #     # # For reasons unclear, even though the loop is closed in the thread,
        #     # # it still thinks it's running here.
        #     context.loop.close()
