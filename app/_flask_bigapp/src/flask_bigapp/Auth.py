# (c) 2021 - David Carmichael MIT License - version 2.0
from hashlib import sha1, sha256, sha512
from string import punctuation, digits, ascii_letters
from random import choice
from random import randrange
from datetime import datetime
from dataclasses import dataclass
from re import search


class Auth:

    @classmethod
    def valid_email_chars(cls) -> list:
        special_chars = ["@", ".", "-", "_"]
        alpha = []
        numeric = []
        for letter in ascii_letters:
            alpha.append(letter)
        for number in digits:
            numeric.append(number)
        return special_chars + alpha + numeric

    @classmethod
    def is_username_safe(cls, username: str) -> bool:
        """
        Checks username for any special characters.
        :param username:
        :return bool:
        """
        vec = cls.valid_email_chars()
        if "@" in username:
            for char in username:
                if char not in vec:
                    return False
            return bool(search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", username))
        if username.isalnum():
            return True
        return False

    @classmethod
    def generate_form_token(cls) -> str:
        """
        Generates a SHA1 using todays date and time.
        :return str: hash:
        """
        sha = sha1()
        sha.update(str(datetime.now()).encode("utf-8"))
        return sha.hexdigest()

    @classmethod
    def generate_salt(cls) -> str:
        """
        Generates a string of 4 special characters, for use in password salting
        :return str:
        """
        return "".join(choice(punctuation) for _ in range(4))

    @classmethod
    def generate_private_key(cls, hook: str) -> str:
        """
        Generates a private key for api access from a passed in hook value.
        :return str: hash:
        """
        sha = sha256()
        sha.update(hook.encode("utf-8"))
        return sha.hexdigest()

    @classmethod
    def generate_email_validator(cls) -> str:
        """
        Generates a string of 8 random numbers, for use in MFA email
        :return str:
        """
        return "".join(choice(digits) for _ in range(8))

    @classmethod
    def generate_pepper(cls, password: str):
        """
        Chooses a random letter from ascii_letters and joins it onto the user's password,
        this is used to pepper the password
        :param password:
        :return str:
        """
        return "".join(choice(ascii_letters) for _ in range(1)) + password

    @classmethod
    def sha_password(cls, password: str, salt: str, encrypt: int = 512) -> str:
        """
        Takes user's password, peppers in, salts it, then converts it to sha
        Can set encryption to 256/512 - 256 is system
        :param password:
        :param salt:
        :param encrypt:
        :return str: hash:
        """
        sha = sha512() if encrypt == 512 else sha256()
        sha.update((cls.generate_pepper(password) + salt).encode("utf-8"))
        return sha.hexdigest()

    @classmethod
    def auth_password(cls, input_password: str, database_password: str, database_salt: str,
                      encrypt: int = 512) -> bool:
        """
        Takes user's password (input_password), loops over all possible ascii_letters joining
        to the password as a pepper, then salts using salt value in the database, then converts it
        to sha, then compares that loop result to the database password to find a match
        Can set encryption to 256/512 - 256 is system
        :param input_password: str
        :param database_password: str
        :param database_salt: str
        :param encrypt: int
        :return bool:
        """
        for letter in list(ascii_letters):
            sha = sha512() if encrypt == 512 else sha256()
            sha.update((letter + input_password + database_salt).encode("utf-8"))
            if sha.hexdigest() == database_password:
                return True
        return False

    @classmethod
    def generate_password(cls, style: str, length: int) -> str:
        """
        Will return a plain text password based on choice of style and length.

        Combinations available:

        style: str "animals", length: int <number of animals returned>

        :param style: str
        :param length: int
        :return: str:
        """
        if style == "animals":
            _final = []
            for i in range(length):
                _random_index = randrange(0, len(PasswordGeneration.animals))
                _final.append(PasswordGeneration.animals[_random_index])
            return '-'.join(_final)


@dataclass
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
