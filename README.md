Visualization of different ai search techniques on a variation of the [three musketeers game](https://en.wikipedia.org/wiki/Three_Musketeers_(game)). In this version of the game, soldiers do not move and there is a treasure (diamond) protected by at least one neighboring soldier. Musketeers can only move in up, down, left and right direction. The musketeer cannot move into a space that neither contains a soldier nor a diamond.

The search techniques try to figure out the minimum number of moves required by any of the musketeer to reach the diamond. The implementation returns the shortest path among the three paths found.

To run a given search, `cd` into that folder and run `python main.py`. The game board is read from the `input.txt` file in the folder. Conventions are:

* 0 for an empty space (there can be any number of empty spaces)
* 1 for a musketeer    (there can be a maximum of three musketeers)
* 2 for a soldier      (there can be any number of soldiers)
* 3 for a diamond      (there is only one diamond)

TODO - Make game visualization work correctly for IDA*.