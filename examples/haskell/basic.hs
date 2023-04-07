topLeveValue :: Integer
topLeveValue = 5

-- f :: Int -> Int
-- f x =
--   x + woot + 6
--   where woot :: Integer
--         woot = 10


printInc n = print plusTwo
  where plusTwo = n + 2


g :: Num a => a -> a
g x = x + x


myHusky :: Int
myHusky = 4


data Doggies a =
    Husky a
  | Mastiff a
  | Tag a
  deriving (Eq, Show)

data GroupTag a =
    MyTag Int a
    deriving (Eq, Show)
