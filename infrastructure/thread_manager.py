import threading


class ThreadManager:

    @staticmethod
    def start(target, *args):
        thread = threading.Thread(target=target, args=args, daemon=True)
        thread.start()

        return thread