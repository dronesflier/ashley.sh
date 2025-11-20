import eliza
import os
import time
import sys, random

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "-e":
            bot = eliza.Eliza()
            data_file = os.path.join(os.path.dirname(__file__), "doctor.txt")
            bot.load(data_file)

            def _type_out(text, speed=0.08, cursor="█"):
                """
                Type out text using a per-character delay clamped to 0.01-0.2 seconds.
                Adds a small random jitter per character to feel more natural.
                """
                # Ensure numeric speed and clamp to 0.01..0.2
                try:
                    speed = float(speed)
                except Exception:
                    speed = 0.08
                speed = max(0.01, min(0.2, speed))

                jitter_amount = 0.012  # +/- jitter applied per character

                if not text:
                    # Briefly show cursor for empty text then remove it cleanly.
                    sys.stdout.write(cursor)
                    sys.stdout.flush()
                    time.sleep(speed)
                    sys.stdout.write("\b \b")
                    sys.stdout.flush()
                    print()
                    return

                for ch in text:
                    sys.stdout.write(ch + cursor)
                    sys.stdout.flush()

                    # Add a slight random jitter so typing doesn't feel too mechanical.
                    char_speed = speed + random.uniform(-jitter_amount, jitter_amount)
                    char_speed = max(0.01, min(0.2, char_speed))
                    time.sleep(char_speed)

                    # Move back one position so the next character overwrites the cursor.
                    sys.stdout.write("\b")
                    sys.stdout.flush()

                # Remove the final cursor by overwriting it with a space and moving back.
                sys.stdout.write(" \b")
                sys.stdout.flush()
                print()

            def _thinking(duration, prefix="Ashley is typing"):
                # Simple spinner/dots animation indicating the bot is "thinking"
                spinner = ["   ", ".  ", ".. ", "..."]
                end_time = time.time() + duration
                while time.time() < end_time:
                    for s in spinner:
                        sys.stdout.write("\r" + prefix + s)
                        sys.stdout.flush()
                        time.sleep(0.20)
                        if time.time() >= end_time:
                            break
                # Clear the line
                sys.stdout.write("\r" + " " * (len(prefix) + 3) + "\r")
                sys.stdout.flush()

            _type_out("ELIZA MODE.")

            print("talk to ashley*. *terms and conditions apply")
            time.sleep(0.3)
            print("type \"goodbye\" to exit the conversation. ashley isn't very smart here...")
            time.sleep(0.5)
            print("she may repeat herself or give weird answers. she can also only talk to the user in the first person.")
            time.sleep(0.5)
            # Show "loading" with periodic dots for a total of 8 seconds
            sys.stdout.write("loading ashley")
            sys.stdout.flush()

            total_wait = 8.0
            end_time = time.time() + total_wait
            while time.time() < end_time:
                # pick an interval between 0.2 and 3.0 seconds, but don't oversleep past end_time
                interval = random.uniform(0.2, 3.0)
                remaining = end_time - time.time()
                time.sleep(min(interval, remaining))

                sys.stdout.write(".")
                sys.stdout.flush()

            sys.stdout.write("\n")
            sys.stdout.flush()

            # Type the initial greeting
            _type_out(bot.initial())

            try:
                while True:
                    said = input("> ")
                    response = bot.respond(said)
                    if response is None:
                        break
                    
                    if response.lower() == "goodbye":
                        break

                    # Show a short "thinking" animation before typing the reply
                    thinking_time = min(0.02 * len(response) + random.uniform(0.2, 0.6), 4.0)
                    _thinking(thinking_time)

                    # Type out the response with a speed tuned to its length
                    _type_out(response)

            except (KeyboardInterrupt, EOFError):
                pass

            # Type the final message
            _type_out(bot.final())
            sys.exit(0)

    n = random.randint(1, 20)
    print("ha" + "i" * n)
    time.sleep(1)


if __name__ == "__main__":
    main()