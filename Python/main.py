import sys
import getpass

def get_password():
    return "python1234"

def verify_access():
    max_attempts = 3
    attempts = 0
    username = getpass.getuser()

    while attempts < max_attempts:
        user_input = getpass.getpass("What's the password? ")

        if user_input == get_password():
            print(f"Welcome back {username}!")
            return # exit func early on success

        attempts = attempts + 1
        remaining = max_attempts - attempts

        if remaining == 1:
            print("Warning! You have 1 attempt left, please be careful as data lost is irrecoverable\n")
        elif remaining > 1:
            print(f"Incorrect. You have {remaining} attempt(s) left.\n")

    # if the loop finishes without returning, all attempts failed
    print("Too many failed attempts. Initiating lockdown mode...")
    sys.exit(1)

def main():
    verify_access()

if __name__ == "__main__":
    main()