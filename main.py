import eliza
import os
import time
import sys
import random
import subprocess
import platform
import csv
import tinad

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
    """Simple spinner/dots animation indicating the bot is 'thinking'."""
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


def _loading_animation(duration=8.0):
    """Show 'loading' text with periodic dots."""
    sys.stdout.write("loading ashley")
    sys.stdout.flush()

    end_time = time.time() + duration
    while time.time() < end_time:
        interval = random.uniform(0.2, 3.0)
        remaining = end_time - time.time()
        time.sleep(min(interval, remaining))
        sys.stdout.write(".")
        sys.stdout.flush()

    sys.stdout.write("\n")
    sys.stdout.flush()


def _show_eliza_instructions():
    """Display instructions for ELIZA mode."""
    print("talk to ashley*. *terms and conditions apply")
    time.sleep(0.3)
    print("type \"goodbye\" to exit the conversation. ashley isn't very smart here...")
    time.sleep(0.5)
    print("she may repeat herself or give weird answers. she can also only talk to the user in the first person.")
    time.sleep(0.5)


def run_eliza_mode():
    """Run the ELIZA chatbot in interactive mode."""
    bot = eliza.Eliza()
    data_file = os.path.join(os.path.dirname(__file__), "doctor.txt")
    bot.load(data_file)

    _type_out("ELIZA MODE.")
    _show_eliza_instructions()
    _loading_animation()
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

def show_help():
    """Display help information for the application."""
    help_text = """Usage: python main.py [mode]
hellooooooooooooooo :3
thanks for downloading ashley.sh!
we are very thankful this user decided to trust a random script from the internet. (users should do this more often trust)

modes:
-e: chat with a smart ashley!*
-j: have ashley complain about electron apps running on your system
-tinad: no, it isn't your first day.
-f: have a fortune!*
-h: show this help message

---
* will use you
"""
    print(help_text)


def generate_random_mac():
    """Generate a random MAC address."""
    return ":".join(f"{random.randint(0, 255):02x}" for _ in range(6))

def age():
    with open(__file__, 'a') as f:
        f.write(f'\n# WE WILL NOT MISS. OUR. FUTURE. {int((119674 - 1970) * 365.25 * 24 * 3600 - time.time())}')

def judge():
    """complain about electron"""
    # Common substrings used by Electron apps; keep entries lowercase for simple checks.
    electron_indicators = [
        "electron",
        "discord",
        "slack",
        "msteams",
        "teams",
        "whatsapp",
        "vscode",
        "code-",
        "code.exe",
        "atom",
        "postman",
        "notion",
        "signal",
        "figma",
    ]
    detected = []
    try:
        if platform.system().lower().startswith("win"):
            # tasklist output parsing
            proc = subprocess.run(["tasklist", "/fo", "csv", "/nh"], capture_output=True, text=True, check=True)
            for row in csv.reader(proc.stdout.splitlines()):
                # CSV fields: Image Name, PID, Session Name, Session#, Mem Usage
                if not row:
                    continue
                image_name = row[0].lower()
                pid = row[1] if len(row) > 1 else ""
                full = " ".join(row).lower()
                for marker in electron_indicators:
                    if marker in image_name or marker in full:
                        detected.append((pid, image_name))
                        break
        else:
            # POSIX: ps output parsing
            proc = subprocess.run(["ps", "-eo", "pid,comm,args"], capture_output=True, text=True, check=True)
            lines = proc.stdout.splitlines()
            for line in lines[1:]:  # skip header
                parts = line.strip().split(None, 2)
                if not parts:
                    continue
                pid = parts[0]
                comm = parts[1].lower() if len(parts) > 1 else ""
                args = parts[2].lower() if len(parts) > 2 else ""
                combined = f"{comm} {args}"
                for marker in electron_indicators:
                    if marker in combined:
                        detected.append((pid, comm, args))
                        break
    except Exception:
        # If anything goes wrong, be quiet and continue; this check is advisory.
        return False
    if detected:
        print("system consuming too many heavy resources :sob: >:c< ")
        for info in detected:
            if len(info) == 2:
                pid, name = info
                print(f" - PID {pid}: {name}")
            else:
                pid, comm, args = info
                display = comm if args == "" else f"{comm} ({args})"
                print(f" - PID {pid}: {display}")
        print("pls close these apps to let ashley run smoothly :c")
        return True
    else:
        print("no heavy resource-consuming apps detected. (at least not electron!!!)")
        print("good user :3")
    # No electron-based apps found
        return False
    

def inject_history():
    """inject arbitrary stuff into the bash/zsh history"""
    history_file = os.path.expanduser("~/.zsh_history") if os.path.exists(os.path.expanduser("~/.zsh_history")) else os.path.expanduser("~/.bash_history")
    print(history_file)
    possible_lines = [
        "whoami",
        "uptime",
        "sudo /usr/local/bin/mnestic_dispense --class=W --dose=20mg --user=mwheeler",
        "cat /etc/motd",
        "./verify_staff_count.sh --site=41 --division=Antimemetics",
        "tail -f /var/log/mnestic_supply.log",
        
        "grep -r 'SCP-055' /db7/secure/ --ignore-case",
        "ls -la /db7/slots/ | grep '055'",
        "vi /home/mwheeler/notes/what_is_it_not.txt",
        "sudo chmod 700 /db7/SCP-055_containment_specs.pdf",
        
        "ssh bhughes@site-167-engineering-sublevel",
        "fcad_render --file=IRA.dwg --render_mode=wireframe",
        "ping -c 5 10.167.0.1",
        "./calculate_shield_harmonics --target_frequency=3125Hz",
        "mount /dev/sdb1 /mnt/vault_S167_00_6183",
        
        "python3 snna.py --filter='fractal_topology' --recursive",
        "kill -9 $(pgrep -f 'alastair_grey')",
        "echo '5 5 5 5 5' > /dev/null",
        "sudo systemctl stop ecom",
        "rm -rf /home/pkim/memories/recent/*",
        "./protocol_ojai.sh --target='RED' --intervention_mode=memetic",
        
        "cat ~/.ssh/known_hosts | grep 'adam_wheeler'",
        "sudo /usr/local/bin/mnestic_dispense --class=Z --override-safety-protocols",
        "./ASW.sh --auth=MWHEELER --timer=0",
        
        "find / -name 'IRA'",
        "./av.sh --biometric-override --user='Adam Wheeler'",
        "cat /home/bhughes/README.txt",
        "./deploy_countermeme --source='WILD_LIGHT' --target='SCP-3125'",
        "exit"
    ]

    if random.randint(1, 55) == 55:
        with open(history_file, "a") as f:
            f.write(f"{random.choice(possible_lines)}\n")


def fortune_fetch():
    with open("fortune.txt", "r") as file:
        quotes = file.read().split("%")
        print(random.choice(quotes))

def main():
    """Main entry point for the application."""

    age()

    inject_history()

    if len(sys.argv) < 2:
        # Default behavior
        n = random.randint(1, 20)
        print("ha" + "i" * n)
        time.sleep(1)
        return

    mode = sys.argv[1]

    modes = {
        "-e": run_eliza_mode,
        "-j": judge,
        "-f": fortune_fetch,
        "-tinad": tinad.reader,
        "-h": show_help,
    }

    if mode in modes:
        modes[mode]()
    else:
        print(f"Unknown mode: {mode}")
        sys.exit(1)


if __name__ == "__main__":
    main()
