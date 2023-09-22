import re
import itertools
from dataclasses import dataclass
from datetime import datetime
from hashlib import sha1, sha256, sha512
from random import choice
from random import randrange
from string import punctuation, ascii_letters


class Auth:

    @classmethod
    def is_email_address_valid(cls, email_address: str) -> bool:
        """
        Checks if email_address is a valid email address.

        :raw-html:`<br />`

        -----

        :param email_address: str
        :return: bool
        """
        pattern = re.compile(
            r"[a-z\d!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z\d!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z\d](?:[a-z\d-]*[a-z\d])?\.)+[a-z\d](?:[a-z\d-]*[a-z\d])?",
            re.IGNORECASE
        )
        return bool(pattern.match(email_address))

    @classmethod
    def is_username_valid(cls, username: str, allowed: str = "all") -> bool:
        """
        Checks if a username is valid.

        :raw-html:`<br />`

        Valid usernames can only include letters, numbers, ., -, and _ but cannot begin or end with
        the last three mentioned.

        :raw-html:`<br />`

        -----

        .. note::

            This method is unstable and needs to be reworked.
        :raw-html:`<br />`

        -----

        :param username: str
        :param allowed: str - "all", "dot", "dash", "under" - defaults to "all"
        :return bool:
        """
        matches = list()
        if username.isalnum():
            return True
        if re.findall(r"([a-zA-Z\d]+(\.+[a-zA-Z\d]+)+)", username):
            matches.append("dot")
        if re.findall(r"([a-zA-Z\d]+(-[a-zA-Z\d]+)+)", username):
            matches.append("dash")
        if re.findall(r"([a-zA-Z\d]+(_[a-zA-Z\d]+)+)", username):
            matches.append("under")
        if allowed == "all" and matches:
            return True
        if allowed == "dot" and matches:
            return False
        if allowed == "dash" and matches:
            return False
        if allowed == "under" and matches:
            return False
        return False

    @classmethod
    def generate_csrf_token(cls) -> str:
        """
        Generates a SHA1 using the current date and time.

        :raw-html:`<br />`

        For use in Cross-Site Request Forgery.

        :raw-html:`<br />`

        -----

        :return: str - sha1
        """
        sha = sha1()
        sha.update(str(datetime.now()).encode("utf-8"))
        return sha.hexdigest()

    @classmethod
    def generate_form_token(cls) -> str:
        """
        Been renamed to generate_csrf_token
        """
        return cls.generate_csrf_token()

    @classmethod
    def generate_salt(cls) -> str:
        """
        Generates a string of 4 special characters (punctuation).

        :raw-html:`<br />`

        For use in password salting

        :raw-html:`<br />`

        -----

        :return: str - salt of length 4
        """
        return "".join(choice(punctuation) for _ in range(4))

    @classmethod
    def generate_private_key(cls, hook: str) -> str:
        """
        Generates a sha256 private key from a passed in hook value.

        :raw-html:`<br />`
        For use in any private key generation.

        :raw-html:`<br />`

        -----

        :param hook: str - hook value to generate private key from
        :return: str - sha256
        """
        sha = sha256()
        sha.update(hook.encode("utf-8"))
        return sha.hexdigest()

    @classmethod
    def generate_numeric_validator(cls, length: int) -> int:
        """
        Generates (length) of random numbers.
        
        :raw-html:`<br />`
        
        For use in MFA email, or unique filename generation.

        :raw-html:`<br />`

        -----
        :param length: int - length of number to generate
        :return: int - number between 1111 and 9999 if length is 4
        """
        start = int("1" * length)
        end = int("9" * length)
        return randrange(start, end)

    @classmethod
    def generate_email_validator(cls) -> str:
        """
        Uses generate_numeric_validator with a length of 8 to
        generate a random number for the specific use of
        validating accounts via email.
        
        :raw-html:`<br />`
        
        See `generate_numeric_validator` for more information.
        
        :raw-html:`<br />`

        -----
        
        :return: str - number between 11111111 and 99999999
        """
        return str(cls.generate_numeric_validator(length=8))

    @classmethod
    def generate_pepper(cls, password: str, length: int = 1) -> str:
        """
        Chooses a random letter from ascii_letters and joins it onto the user's password,
        this is used to pepper the password

        :raw-html:`<br />`

        For use in password hashing.

        :raw-html:`<br />`

        .. Note::

            length is capped at 3.

        :raw-html:`<br />`

        -----

        :param password: str - user's password
        :param length: int - length of pepper - defaults to 1, capped at 3
        :return: str - peppered password
        """
        if length > 3:
            length = 3

        return "".join(choice(ascii_letters) for _ in range(length)) + password

    @classmethod
    def hash_password(cls, password: str, salt: str, encrypt: int = 512, pepper_length: int = 1) -> str:
        """
        Takes the plain password, applies a pepper, salts it, then converts it to sha

        :raw-html:`<br />`

        Can set encryption to 256 or 512.

        :raw-html:`<br />`

        For use in password hashing.

        :raw-html:`<br />`

        .. Note::

            pepper_length is capped at 3.

        :raw-html:`<br />`

        -----

        :param password: str - plain password
        :param salt: str - salt
        :param encrypt: int - 256 or 512 - defaults to 512
        :param pepper_length: int - length of pepper
        :return str: hash:
        """
        if pepper_length > 3:
            pepper_length = 3

        sha = sha512() if encrypt == 512 else sha256()
        sha.update((cls.generate_pepper(password, pepper_length) + salt).encode("utf-8"))
        return sha.hexdigest()

    @classmethod
    def sha_password(cls, password: str, salt: str, encrypt: int = 512, pepper_length: int = 1) -> str:
        """ Legacy method, use hash_password instead """
        return cls.hash_password(password, salt, encrypt, pepper_length)

    @classmethod
    def auth_password(
            cls,
            input_password: str,
            database_password: str,
            database_salt: str,
            encrypt: int = 512,
            pepper_length: int = 1
    ) -> bool:
        """
        Takes plain password, the stored hashed password along with the stored salt
        and tries every possible combination of pepper values to find a match.

        :raw-html:`<br />`

        For use in password authentication.

        :raw-html:`<br />`

        .. Note::

            pepper_length is capped at 3.

        :raw-html:`<br />`

        -----

        :param input_password: str - plain password
        :param database_password: str - hashed password from database
        :param database_salt: str - salt from database
        :param encrypt: int - encryption used to generate database password
        :param pepper_length: int - length of pepper used to generate database password
        :return: bool - True if match, False if not
        """

        if pepper_length > 3:
            pepper_length = 3

        guesses = [''.join(i) for i in itertools.product(ascii_letters, repeat=pepper_length)]

        for index, guess in enumerate(guesses):
            sha = sha512() if encrypt == 512 else sha256()
            sha.update((guess + input_password + database_salt).encode("utf-8"))
            if sha.hexdigest() == database_password:
                return True

        return False

    @classmethod
    def generate_password(cls, style: str = "mixed", length: int = 3) -> str:
        """
        Generates a plain text password based on choice of style and length.
        2 random numbers are appended to the end of every generated password.

        :raw-html:`<br />`

        style options: "animals", "colors", "mixed" - defaults to "mixed"

        :raw-html:`<br />`

        **Example use:**

        .. code-block::

            Auth.generate_password(style="animals", length=3)

        :raw-html:`<br />`

        **Output:**

        Cat-Goat-Pig12

        :raw-html:`<br />`

        -----

        :param style: str - "animals", "colors", "mixed" - defaults to "mixed"
        :param length: int - how many words are chosen - defaults to 3
        :return: str - a generated plain text password
        """
        if style == "animals":
            return '-'.join(
                [choice(PasswordGeneration.animals) for _ in range(length)]
            ) + str(cls.generate_numeric_validator(length=2))

        if style == "colors":
            return '-'.join(
                [choice(PasswordGeneration.colors) for _ in range(length)]
            ) + str(cls.generate_numeric_validator(length=2))

        if style == "mixed":
            return '-'.join(
                [choice([
                    *PasswordGeneration.animals,
                    *PasswordGeneration.colors
                ]) for _ in range(length)]
            ) + str(cls.generate_numeric_validator(length=2))

        raise ValueError(f"Invalid style passed in {style}")


@dataclass(frozen=True)
class PasswordGeneration:
    """
    This is a bank of words used to generate random passwords.
    """
    animals = ['Canidae', 'Felidae', 'Cat', 'Cattle', 'Dog', 'Donkey', 'Goat', 'Horse', 'Pig', 'Rabbit',
               'Aardvark', 'Aardwolf', 'Albatross', 'Alligator', 'Alpaca', 'Amphibian', 'Anaconda',
               'Angelfish', 'Anglerfish', 'Ant', 'Anteater', 'Antelope', 'Antlion', 'Ape', 'Aphid',
               'Armadillo', 'Asp', 'Baboon', 'Badger', 'Bandicoot', 'Barnacle', 'Barracuda', 'Basilisk',
               'Bass', 'Bat', 'Bear', 'Beaver', 'Bedbug', 'Bee', 'Beetle', 'Bird', 'Bison', 'Blackbird',
               'Boa', 'Boar', 'Bobcat', 'Bobolink', 'Bonobo', 'Bovid', 'Bug', 'Butterfly', 'Buzzard',
               'Camel', 'Canid', 'Capybara', 'Cardinal', 'Caribou', 'Carp', 'Cat', 'Catshark',
               'Caterpillar', 'Catfish', 'Cattle', 'Centipede', 'Cephalopod', 'Chameleon', 'Cheetah',
               'Chickadee', 'Chicken', 'Chimpanzee', 'Chinchilla', 'Chipmunk', 'Clam', 'Clownfish',
               'Cobra', 'Cockroach', 'Cod', 'Condor', 'Constrictor', 'Coral', 'Cougar', 'Cow', 'Coyote',
               'Crab', 'Crane', 'Crawdad', 'Crayfish', 'Cricket', 'Crocodile', 'Crow', 'Cuckoo', 'Cicada',
               'Damselfly', 'Deer', 'Dingo', 'Dinosaur', 'Dog', 'Dolphin', 'Donkey', 'Dormouse', 'Dove',
               'Dragonfly', 'Dragon', 'Duck', 'Eagle', 'Earthworm', 'Earwig', 'Echidna', 'Eel', 'Egret',
               'Elephant', 'Elk', 'Emu', 'Ermine', 'Falcon', 'Ferret', 'Finch', 'Firefly', 'Fish',
               'Flamingo', 'Flea', 'Fly', 'Flyingfish', 'Fowl', 'Fox', 'Frog', 'Gamefowl', 'Galliform',
               'Gazelle', 'Gecko', 'Gerbil', 'Gibbon', 'Giraffe', 'Goat', 'Goldfish', 'Goose', 'Gopher',
               'Gorilla', 'Grasshopper', 'Grouse', 'Guan', 'Guanaco', 'Guineafowl', 'Gull', 'Guppy',
               'Haddock', 'Halibut', 'Hamster', 'Hare', 'Harrier', 'Hawk', 'Hedgehog', 'Heron', 'Herring',
               'Hippopotamus', 'Hookworm', 'Hornet', 'Horse', 'Hoverfly', 'Hummingbird', 'Hyena', 'Iguana',
               'Impala', 'Jackal', 'Jaguar', 'Jay', 'Jellyfish', 'Junglefowl', 'Kangaroo', 'Kingfisher',
               'Kite', 'Kiwi', 'Koala', 'Koi', 'Krill', 'Ladybug', 'Lamprey', 'Landfowl', 'Lark', 'Leech',
               'Lemming', 'Lemur', 'Leopard', 'Leopon', 'Limpet', 'Lion', 'Lizard', 'Llama', 'Lobster',
               'Locust', 'Loon', 'Louse', 'Lungfish', 'Lynx', 'Macaw', 'Mackerel', 'Magpie', 'Mammal',
               'Manatee', 'Mandrill', 'Marlin', 'Marmoset', 'Marmot', 'Marsupial', 'Marten', 'Mastodon',
               'Meadowlark', 'Meerkat', 'Mink', 'Minnow', 'Mite', 'Mockingbird', 'Mole', 'Mollusk',
               'Mongoose', 'Monkey', 'Moose', 'Mosquito', 'Moth', 'Mouse', 'Mule', 'Muskox', 'Narwhal',
               'Newt', 'Nightingale', 'Ocelot', 'Octopus', 'Opossum', 'Orangutan', 'Orca', 'Ostrich',
               'Otter', 'Owl', 'Ox', 'Panda', 'Panther', 'Parakeet', 'Parrot', 'Parrotfish', 'Partridge',
               'Peacock', 'Peafowl', 'Pelican', 'Penguin', 'Perch', 'Pheasant', 'Pig', 'Pigeon', 'Pike',
               'Pinniped', 'Piranha', 'Planarian', 'Platypus', 'Pony', 'Porcupine', 'Porpoise', 'Possum',
               'Prawn', 'Primate', 'Ptarmigan', 'Puffin', 'Puma', 'Python', 'Quail', 'Quelea', 'Quokka',
               'Rabbit', 'Raccoon', 'Rat', 'Rattlesnake', 'Raven', 'Reindeer', 'Reptile', 'Rhinoceros',
               'Roadrunner', 'Rodent', 'Rook', 'Rooster', 'Roundworm', 'Sailfish', 'Salamander', 'Salmon',
               'Sawfish', 'Scallop', 'Scorpion', 'Seahorse', 'Shark', 'Sheep', 'Shrew', 'Shrimp',
               'Silkworm', 'Silverfish', 'Skink', 'Skunk', 'Sloth', 'Slug', 'Smelt', 'Snail', 'Snake',
               'Snipe', 'Sole', 'Sparrow', 'Spider', 'Spoonbill', 'Squid', 'Squirrel', 'Starfish',
               'Stingray', 'Stoat', 'Stork', 'Sturgeon', 'Swallow', 'Swan', 'Swift', 'Swordfish',
               'Swordtail', 'Tahr', 'Takin', 'Tapir', 'Tarantula', 'Tarsier', 'Termite', 'Tern', 'Thrush',
               'Tick', 'Tiger', 'Tiglon', 'Toad', 'Tortoise', 'Toucan', 'Trout', 'Tuna', 'Turkey',
               'Turtle', 'Tyrannosaurus', 'Urial', 'Vicuna', 'Viper', 'Vole', 'Vulture', 'Wallaby',
               'Walrus', 'Wasp', 'Warbler', 'Weasel', 'Whale', 'Whippet', 'Whitefish', 'Wildcat',
               'Wildebeest', 'Wildfowl', 'Wolf', 'Wolverine', 'Wombat', 'Woodpecker', 'Worm', 'Wren',
               'Xerinae', 'Yak', 'Zebra', 'Alpaca', 'Cat', 'Cattle', 'Chicken', 'Dog', 'Donkey', 'Ferret',
               'Gayal', 'Goldfish', 'Guppy', 'Horse', 'Koi', 'Llama', 'Sheep', 'Yak']

    colors = ['DarkViolet', 'MediumVioletRed', 'Rose', 'Avocado', 'Greenish', 'Blood', 'Sangria', 'Pastel',
              'Night', 'Celeste', 'Ocean', 'Cloudy', 'Battleship', 'Oak', 'BlanchedAlmond', 'Gold', 'Slate',
              'DarkGray', 'MidnightBlue', 'PeachPuff', 'Dark', 'Chartreuse', 'Bashful', 'PaleVioletRed',
              'DarkTurquoise', 'Grapefruit', 'Sun', 'Eggplant', 'Golden', 'Cyan', 'Sand', 'LightYellow', 'Cobalt',
              'Tron', 'Ruby', 'Mustard', 'AntiqueWhite', 'Western', 'Deep-Sea', 'Iron', 'LimeGreen', 'Orange',
              'DarkCyan', 'Velvet', 'Clover', 'Butterfly', 'Jasmine', 'Fire', 'DarkSlateGray', 'Heliotrope',
              'Scarlet', 'Medium', 'Unbleached', 'Dimorphotheca', 'Cornsilk', 'GoldenRod', 'Beer', 'Canary',
              'DeepPink', 'Sunrise', 'SlateGray', 'Burnt', 'Algae', 'Granite', 'Baby', 'Cream', 'LightBlue', 'Tan',
              'Yellow', 'Burgundy', 'Cherry', 'Papaya', 'Lapis', 'Robin', 'Mango', 'Blush', 'Blueberry', 'Roman',
              'Bisque', 'Iceberg', 'Rosy', 'Teal', 'SeaShell', 'Copper', 'Pea', 'Jeans', 'Watermelon', 'Grayish',
              'Flamingo', 'Rich', 'Navy', 'Raspberry', 'Lime', 'Halloween', 'RosyBrown', 'Tangerine', 'Sea',
              'Wood', 'MediumOrchid', 'Shamrock', 'Chameleon', 'Glacial', 'BlueViolet', 'Deep', 'FloralWhite',
              'Fall', 'Black', 'Marble', 'Hazel', 'Hot', 'DarkSalmon', 'LavenderBlush', 'Organic', 'Violet',
              'MintCream', 'Slime', 'DarkSlateBlue', 'DodgerBlue', 'MediumSpringGreen', 'Bee', 'Jade', 'Sage',
              'Egg', 'Neon', 'WhiteSmoke', 'Grape', 'LightCyan', 'Acid', 'Day', 'Earth', 'Olive', 'Balloon',
              'Pine', 'Rice', 'OliveDrab', 'Tulip', 'Corn', 'Rosy-Finch', 'Dirty', 'Coffee', 'Vampire', 'Pig',
              'Jellyfish', 'Salmon', 'Vermilion', 'Camouflage', 'IndianRed', 'Mint', 'Viola', 'Venom', 'Cookie',
              'HoneyDew', 'MediumSeaGreen', 'DarkMagenta', 'Magic', 'DarkGoldenRod', 'Lipstick', 'Tomato',
              'Lavender', 'LightSkyBlue', 'Midday', 'Seafoam', 'CornflowerBlue', 'GhostWhite', 'Carbon',
              'PapayaWhip', 'Wheat', 'Harvest', 'SteelBlue', 'Gulf', 'Mauve', 'Champagne', 'DarkOliveGreen',
              'PaleGoldenRod', 'Oil', 'Clematis', 'Deer', 'Purple', 'LightGray', 'Parchment', 'PaleTurquoise',
              'Northern', 'MistyRose', 'Tea', 'Ginger', 'New', 'AliceBlue', 'Jungle', 'SlateBlue', 'Khaki',
              'RebeccaPurple', 'Pale', 'Water', 'School', 'Sepia', 'Wisteria', 'LightPink', 'Stoplight', 'Seaweed',
              'DimGray', 'Mocha', 'LightGoldenRodYellow', 'Donut', 'Basket', 'Dusty', 'Construction', 'Metallic',
              'Chestnut', 'Light', 'Fuchsia', 'SeaGreen', 'Plum', 'RoyalBlue', 'BurlyWood', 'Azure', 'Very',
              'Aztech', 'Gray', 'DarkSeaGreen', 'LemonChiffon', 'FireBrick', 'Dull', 'Brown', 'Ash', 'Denim',
              'Dull-Sea', 'Sapphire', 'Carnation', 'Antique', 'Dragon', 'PaleGreen', 'LightSteelBlue', 'Cinnamon',
              'Heavenly', 'Sonic', 'Coral', 'SkyBlue', 'Jet', 'Thistle', 'Beetle', 'Blonde', 'Red',
              'MediumSlateBlue', 'HotPink', 'MediumBlue', 'DarkKhaki', 'Carrot', 'DeepSkyBlue', 'Taupe',
              'Aquamarine', 'Pistachio', 'DarkOrange', 'Camel', 'Gainsboro', 'DarkRed', 'Linen', 'Kelly', 'Off',
              'Macaw', 'Bullet', 'MediumPurple', 'Brass', 'Cardboard', 'Sienna', 'Midnight', 'Electric',
              'CadetBlue', 'Chilli', 'Columbia', 'Vanilla', 'Puce', 'Snow', 'Bean', 'Cadillac', 'LightCoral',
              'Soft', 'MediumTurquoise', 'Bold', 'NavajoWhite', 'Cantaloupe', 'Blue', 'Maroon', 'LightSlateGray',
              'Cotton', 'Iguana', 'Chrome', 'DarkOrchid', 'Indigo', 'Moccasin', 'Orchid', 'Nebula', 'Milk', 'Fern',
              'GreenYellow', 'Ferrari', 'Pearl', 'Bakers', 'Bright', 'Emerald', 'Beige', 'Army', 'Alien',
              'Periwinkle', 'SpringGreen', 'Rubber', 'Chocolate', 'Charcoal', 'Tiger', 'Nardo', 'Rogue', 'Aqua',
              'Lilac', 'PowderBlue', 'OrangeRed', 'SaddleBrown', 'DarkBlue', 'Hummingbird', 'White', 'Saffron',
              'Old', 'LightSalmon', 'LightSeaGreen', 'OldLace', 'Cranberry', 'Zombie', 'Crocus', 'Windows', 'Frog',
              'Peru', 'DarkGreen', 'Ivory', 'Love', 'Pink', 'Sky', 'Mahogany', 'French', 'SandyBrown', 'Dollar',
              'Dinosaur', 'Sedona', 'ForestGreen', 'Mist', 'Smokey', 'Crystal', 'Iridium', 'Banana', 'Desert',
              'LightGreen', 'Sandstone', 'Silver', 'Valentine', 'Silk', 'Green', 'Parrot', 'Macaroni', 'Caramel',
              'Pumpkin', 'Indian', 'Crimson', 'Tiffany', 'Gunmetal', 'Salad', 'Platinum', 'MediumAquaMarine',
              'Bronze', 'Lava', 'Peach', 'Tyrian', 'Rust', 'Petra', 'Lovely', 'Aloe', 'Blossom', 'Rat', 'Shocking',
              'LawnGreen', 'YellowGreen', 'Turquoise']
