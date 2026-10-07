import System.IO -- for IO operations
import Text.Read (readMaybe) -- for safe parsing

-- a loop that forces the user to enter a valid number
promptAge :: IO Int
promptAge = do
  putStr "Enter your age please: "
  hFlush stdout
  input <- getLine

  -- readMaybe returns a 'Maybe Int'
  -- it evals to 'Just number(Int)' if successful, or 'Nothing' if it fails
  case readMaybe input of -- read the input
    Just age -> return age -- rif input is ACTUALLY an Int(number), return age to whoever calls it (in this case, greetByAge)
    Nothing -> do
      -- if not, tell the user and prompt them again (recursion)
      putStrLn "That's not a valid number! Please try again"
      promptAge -- this is recursion! It runs the prompt again until valid input is provided

-- a helper function that uses if/else to pick a greeting
greetByAge :: String -> Int -> String
greetByAge name age
  | age < 0 = "Hello, " ++ name ++ "! Are you time travelling? Cause how are you " ++ show age ++ " years old bro?"
  | age < 18 = "Hey " ++ name ++ "! You're still a minor at " ++ show age ++ " years old"
  | age < 65 = "Welcome, " ++ name ++ ". You are in the working force at " ++ show age ++ " years old"
  | otherwise = "Greetings, " ++ name ++ "! Enjoy your retirement at " ++ show age ++ " years old"

main :: IO ()
main = do
  putStr "Please enter your name: "
  hFlush stdout
  name <- getLine

  age <- promptAge -- safely gets a validated Int without the risk of crashing
  putStrLn (greetByAge name age)