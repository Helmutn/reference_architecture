import threading


class ThreadManager:

    def start(self, target, *args):

        thread = threading.Thread(
            target=target,
            args=args,
            daemon=True
        )

        thread.start()

        return thread