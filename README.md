# The Legend of Tao (TLoT)
**TLoT** is a pseudo-open-world exploration roleplaying game with a reminisence of The Legend of Zelda™ and Rogue. The objective for this game is to defeat the *"Red Turtles"* get the highest score as possible. But there's a catch, everytime a new game starts you'd always have a new procedural generated world to explore! Exploration is also encouraged as there will be items to find in-game; but beware, you might get a game over because you take a big risk...

This game is actually an academic project which is a part of the 01219114/01219115 Programming 1 course at Kasetsart University. The game is made possible using Python 3 and the builtin module, [turtle](https://docs.python.org/3/library/turtle.html).

## Features
- The game can be run on any platform with Tk-supported Python 3 (3.7 or higher) installed.
- A large procedural generated[ᴬ](https://en.wikipedia.org/wiki/Cellular_automaton) world at a size of 24x24 everytime you start a new game.
- Items that you can pickup and use during the gameplay to aid you.
- The ability to continue from where you left off in-game with custom `.save` file.
- ...and more?
  
## Required Software
- Python >= 3.7 w/ Tk/Tcl installed
- That's it.

## Launch Instructions
Make sure you have all the required software installed.
```bash
~/ > git clone https://github.com/GToidZ/tlot.git
~/ > cd tlot
tlot/ > python app.py
```

## Program Design
Since there are too many classes, we'll go through important ones.

`Game` : This class is used for being a standalone instance for the screens and turtles to render. Some various global properties are also stored here.

`GameScreen` : An abstract class replicating what `Screen` in `turtle` should be but minimal. The class has abstract methods to initialize and keep up the updates of a screen. It also can be extended to have various screen types.

`GameWorld` : This class generates a world with a random seed and can be stored for later use. It contains universal properties of a world, for example, the item locations.

`Player` : This class is used to determine the universal properties that a player has, most of the data in this class is persistent and will be used in saving/loading the game.

`PlayerController` : This class is a wrapper for `Player` class to have temporal variables. Additionally, it is used to initialize a player object which go on screen.

`Entity` : This class is an abstract wrapper for `Turtle` to recognize them as entities. Upon creation of new entities, they are also registered to the `Game` class as well.

`Item` : This class contains various properties but also has abstract method such as `use(player)` to support the extension of the ever-growing number of Items.

`Inventory` : This class links to the player for mainting what `Item`(s) do the player owns. It also acts as a middleware for game saving/loading.

`GameData` : This class operates the File I/O and the game saving/loading. It takes the properties of `Player` and `GameWorld` in order to serialize/deserialize as game data. This makes the game possible to continue from the latest state where the player is playing.

## Code Structure
`app.py` : The main file for executing the start of the program.

`cartography.py` : The file for world generation-related functions and for managing the game world's properties.

`data.py` : The file for game data saving and loading.

`entities.py` : The file for all entities such as Player and Enemy. It also has included the controlling-based functions for player.

`items.py` : The file for item definitions and storing their functionalities.

`util.py` : The middleware file to reach other class methods that are risking circular imports.

`window.py` : The file containing the mostly `turtle` functions, to keep track of screen and most importantly as a core to display everything.

`saveformat.txt` : The file for referencing the `.save` format. It contains instructions on how to read the file too.