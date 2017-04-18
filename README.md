# MinecraftPiStuff
A collection of experiments &amp; games using Minecraft Pi edition on Raspberry Pi

# minefield/minefield.py

**UPDATE (2017-04-17):** MineField now has it own repository: [DrGFreeman/MineField](https://github.com/DrGFreeman/MineField). The game has been translated to English with english comments and detailed README file. The code also got multiple improvements.

This is a game where the player has to find and destroy a block while avoiding stepping on hidden land mines. The player uses a mine proximity indicator built with leds connected to GPIO pins to avoid land mines. The game is fully functional.

# zombies/
This folder is an experiment to develop a zombie AI. Work in-progress. Launch zombies/testZombies.py to try it. The zombies AI runs well and fast however update speed in MCPI (block creation/deletion) slows down when the number of zombies increase above ~40.
