-- define a custom data type for membership tiers
-- this is like a enum in Rust/C/C++
data Tier = Bronze | Silver | Gold

-- pattern matching: we match against the exact struct of the input
getDiscount :: Tier -> Double -- this variable takes in a tier (the struct) and gives back a Double
getDiscount Bronze = 0.05 -- if input is Bronze, return a 5% discount
getDiscount Silver = 0.10 -- 10% discount
getDiscount Gold = 0.20 -- 20% discount

-- immutability in action
-- this var takes in a Double + a Tier (the struct) and spits out a Double?
calculateTotal :: Double -> Tier -> Double
-- the below gives names to the two inputs (originalPrice.e.g 100 and tier.e.g Bronze)
-- so if u look at main, this is how it ought to work
calculateTotal originalPrice tier =
  let discount = getDiscount tier -- this var (discount) only stores data from the var getDiscount and tier
  -- so if tier = bronze, then getDiscount tier becomes 0.05, so discount (the local var) becomes.. discount = 0.05
  -- discountPercentage = 0.99 <- if you tried to change 'discount' here, GHC (haskells compiler) would throw an error
      finalPrice = originalPrice * (1 - discount) -- this becomes 100.0 * (1 - 0.05) = 95.0 which is stored in the var finalPrice
   in finalPrice -- this means, create these local values, then the result of the let expression is finalPrice
  -- so roughly, create discount (var) -> create finalPrice (var) -> return finalPrice (var)

-- means main is an IO action
-- the () is like "void" in C...ok...techinically its...
-- main performs IO and the resulting value is the unit value ().i.e there's nothign meaningful for us to use
-- so its "sort of contains a value.i.e The return value"
main :: IO ()
main = do
  -- "do" syntax starts a sequence of IO actions
  let itemPrice = 100.0
  putStr "---Haskell Playground ---" -- putStr prints strings
  print (calculateTotal itemPrice Bronze)
  print (calculateTotal itemPrice Gold)
