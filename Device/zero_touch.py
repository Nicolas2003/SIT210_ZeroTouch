from multiprocessing import Process, Pipe, set_start_method
from record import stream_record, end_record
from identify import stream_identify
from display import stream_display_users


def main():
    print("[Main] Setting up pipes...")

    # Pipe1: Record → Identification
    footage_send, footage_recv = Pipe()

    # Pipe2: Identification → Display
    results_send, results_recv = Pipe()

    print("[Main] Starting processes...")

    # Core 3: Face identification
    p2 = Process(target=stream_identify, args=("./Users", footage_recv, results_send))
    p2.start()

    # Core 4: Display faces
    p3 = Process(target=stream_display_users, args=(results_recv,))
    p3.start()

    # Core 2: Footage streaming
    # p1 = Process(target=stream_record, args=(footage_send,))
    # p1.start()
    stream_record(footage_send)
    p2.terminate()
    p3.terminate()

    print("[Main] All processes started. Press Ctrl+C to stop.")

    try:
        # p1.join()
        p2.join()
        p3.join()
        end_record()

    except KeyboardInterrupt:
        print("[Main] Shutting down processes...")

        # Terminate each process on interrupt
        # p1.terminate()
        p2.terminate()
        p3.terminate()

        # p1.join()
        p2.join()
        p3.join()

    print("[Main] Program ended.")

if __name__ == '__main__':
    set_start_method("fork")
    main()
