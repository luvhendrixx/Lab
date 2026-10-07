import System.IO (hFlush, stdout)

promptAge :: IO Int
promptAge = do
  putStr "Enter your age: "
  hFlush stdout
  input <- getLine
  return (read input)

greet :: String -> Int -> String
greet name age = "Hello, " ++ name ++ "! \nYou are " ++ show age ++ " years old."

main :: IO ()
main = do
  putStr "Please enter your name: "
  hFlush stdout -- Crucial! It ensurs the prompt prints b4 waiting for input
  name <- getLine

  age <- promptAge
  -- bc age is a int and name is a string, u can't concatenate them directly with ++,
  -- the show function takes the int and converts it into a string.e.g 25 -> "25" so it can be safely used together
  -- contanation like in Rust and C++
  putStrLn (greet name age)