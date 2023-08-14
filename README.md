# JMD Umodel BruteForcer

## Overview
The JMD Umodel BruteForcer is a GUI application designed to automate the generation and execution of various command-line options for the Unreal Model Viewer (UModel). 

It allows users to brute-force different combinations of switches to extract data from Unreal Engine game files efficiently.

Generally, this is recommended for "unsupported" games that may be supportable by attempting different game overrides and export options.

It also acts as a GUI for running UModel in a batch scenario without needing to use combinations of options to brute force.

## Features
1. **Dynamic Command Generation:** Generates different combinations of switches for UModel based on user-selected options.
2. **Real-time Checkbox Update:** Select All checkboxes for game switches and options with real-time GUI updates.
3. **Exclusive and Combinable Switches:** Supports exclusive and combinable switches for flexible command building.
4. **Output Sorting:** Sorts the commands by length, with the shortest commands coming last.
5. **Duplicate Command Handling:** Ensures no duplicate commands are built.
6. **Default File Extensions:** Sets default file extensions for specific folders if populated.
7. **Batch Output:** Additionally outputs the built commands to a Windows Batch file (`commands.bat`) for later use.

## WARNING:
Each of the checkbox options adds an additional pass to the brute forcing utility.

For example, If you choose 5 Permutation options with 1 game override, and have the Animations, Sounds, StaticMesh and Textures folders populated, then the tool will run Umodel 625 times for 1 file per folder. 2 games chosen will double this amount, and so on.

This is known as Permutations. In this specific case, there are 4 folders and each folder can be combined with any of the 5 options. 

The situation is akin to having 4 slots where each slot can be filled with one of 5 possible choices.

The principle here is that of the multiplication rule, which states that if you have *n* choices for one task and *m* choices for another task, then there are *n* X *m* choices for both tasks together.

For this specific scenario, there are 5 choices for the first folder, 5 choices for the second folder, 5 choices for the third folder, and 5 choices for the fourth folder, for **each file** in those folders.

Therefore, the total number of possible combinations can be calculated as: 5x5x5x5=**625 (PER FILE!)**

If each folder has 10 files in it matching the extensions searched, that would create **25,000** commands. (6,250 + 6,250 + 6,250 + 6,250)

## Contributing
Please feel free to open an issue or submit a pull request for any bugs, enhancements, or feature requests.

## Acknowledgments
Special thanks to Gildor and the Umodel community who made this project possible.