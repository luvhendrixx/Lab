import sys
from pathlib import Path

# dependency check
try:
    from plyer import notification

    HAS_PLYER = True
except ImportError:
    HAS_PLYER = False

ss_proc = 0

try:
    folder = Path.home() / "Pictures"

    if not folder.exists():
        print(f"Directory non-existent: {folder}")
        sys.exit(0)

    # Match both 'screenshot' and 'Screenshot'
    for file in folder.glob("[S|s]creenshot*"):
        if file.is_file():
            try:
                # Notify if plyer is installed and DBus is available
                if HAS_PLYER:
                    try:
                        notification.notify(
                            title="Screenshot Cleanup",  # pop up title
                            message=f"Deleting {file.name}",  # pop up message
                            app_name="Screenshot Cleaner",  # app name (so Dbus can know the name of the proc making this req, not required but good practice)
                            app_icon=f"{folder}/Icons/megan.jpeg",  # app icon (the one that'll appear on your notification panel)
                            timeout=3,  # how long the ss stays on the screen
                        )
                    except Exception:
                        pass  # Silently skip if DBus drops during shutdown (u won't see the pop up msg, but the file ought to be deleted still)

                file.unlink()
                print(f"Cleaning: {file.name}....")
                ss_proc += 1

            except Exception as e:
                print(f"Failed to delete {file.name}: {e}")

    if ss_proc == 0:
        print("Nothing found to clean. All good :-)")
    else:
        print(f"Finished cleaning up: {ss_proc} file(s)")

except Exception as e:
    print(f"An unexpected error occurred during execution: {e}")
