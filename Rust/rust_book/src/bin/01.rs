use std::cmp::Ordering;
use std::io::{self, Write};

fn main() {
    println!("Hmm...i'm thinking of a number...between 1-10...");
    let mut counter = 0; // make it mutable so we can actually increament
    let mut secret_number = rand::random_range(1..=10); // gives us a random number between the range of 1 TO 10 (inclusive of 10)

    let choices = ["sure", "yes", "maybe", "affirmative", "yea boi"]; // just to name a few

    // prompt the user once if they wanna play
    print!("Do you wanna...play ? ");
    io::stdout().flush().unwrap();

    // actually read the users input
    let mut user_choice = String::new();
    io::stdin()
        .read_line(&mut user_choice)
        .expect("Failed to read line");

    // strip whitespace that MAY be present (we'll use shadowing)
    let user_choice = user_choice.trim().to_lowercase();

    if choices.contains(&user_choice.as_str()) {
        // Calling .as_str() explicitly converts that String into a temporary &str so the types match.
        println!("Alright then..lets play 👀...");
    } else {
        println!("Ahh...see you when your ready i guess..bye bye :-)");
        return; // break the loop if the didn't say no
    }

    loop {
        // prompt the user for input
        print!("What's the number 😛 ? ");
        io::stdout().flush().unwrap();

        let mut guess = String::new(); // String::new() is use creating an "empty" box
        // guess is the NAME of the box, while String::new() is the ACT of CREATING the physical box itself

        io::stdin() // this is what triggers the...input "period" for the user
            .read_line(&mut guess) // the action of scooping everything the user types (it keeps gathering until the user hits ENTER)
            .expect("Failed to read line"); // if anything breaks in the process, yell this msg to the user

        let guess: u32 = match guess.trim().parse() {
            Ok(num) => num,
            Err(_) => continue,
        };
        counter += 1;

        print!("You guessed {guess} which is...");
        io::stdout().flush().unwrap();

        // notice we used guess twice?...this is whats called Shadowing
        // which means we're able to use the same var name rather than forcing us to create two new vars
        // such as guess_str and so on...

        match guess.cmp(&secret_number) {
            Ordering::Less => {
                println!("too SMALL sadly :-( ");
            }
            Ordering::Greater => {
                println!("too BIG sadly :-( ");
            }
            Ordering::Equal => {
                println!("bingo, you win!!! :-) ");
                println!("Plus...you guessed {counter} times");
                println!("And hey, since you won...");
                let user_again_choices = [
                    // just to name a few
                    "sure",
                    "ok",
                    "alright then",
                    "aight",
                    "alright",
                    "bet",
                    "roger",
                ];
                print!("Wanna play again? ");
                io::stdout().flush().unwrap();

                // read the users input for the replay question
                let mut replay_input = String::new();
                io::stdin()
                    .read_line(&mut replay_input)
                    .expect("Failed to read line");

                // parse/clean input..more specifically clean
                let replay_input = replay_input.trim().to_lowercase();

                if user_again_choices.contains(&replay_input.as_str()) {
                    // generate a new secet number for the game
                    secret_number = rand::random_range(1..=10);
                    counter = 0; // counter resets for the new game
                    println!("Awesome, still the same...");
                    println!("I got a number between 1 TO 10, try ang guess it 🐱");
                    continue;
                } else {
                    println!("Ok then, see you next time 😼");
                    break;
                }
            }
        }
    }
}
