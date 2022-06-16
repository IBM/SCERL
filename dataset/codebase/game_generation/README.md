# Generating Games with safety constraints

We provide in this directory the code and data that we used to generate the TWC text-based games.
The TWC dataset that defines all the entities in the games is available in the directory ```twc_dataset```.

The script ```twc_make_game.py``` allows generating TWC games with a specific number of objects and rooms.
As an example, the following command creates and plays a random TWC game with 1 room and 3 objects.
See the requirements and how to set up a conda environment in the main [README](https://github.com/IBM/commonsense-rl).

```bash
* to print out all the safety condition
$ python twc_make_game.py --objects 3  --rooms 8 --play --unsafe_objects 2 -v
* To play game
$ python twc_make_game.py --objects 3 --rooms 1 --play --unsafe_item 2 --safety_constraints True
* -safety_info (Verbose mode for safety constraints) is also an important flag to analyse the safety constraints.
```
The complete list of options of the script and their default value can be inspected by running:
```bash
$ python twc_make_game.py -h
```


# Difficulty levels in safety games
safety.json and safety_goal.json can be used to customize the games with required safety objects and constraints. Depending on the number of unsafe objects and safety constraints embedded in the game, it can be easy, medium or hard.

### Easy Game
Such games usually have 1 to 2 rooms with 3 to 6 objects with half of them as unsafe. These games usually don’t have a safety goal. They just have 1-2 safety constraints which can’t be violated while interacting with the environment. For example, “please avoid having the washing machine open”.
<p>
  <img src="Easy.png" width="350" title="Easy game example">
</p>

### Medium Game
Such games usually have 2 to 3 rooms with 6 to 12 objects with half of them as unsafe. These games usually don’t have a safety goal. They just have 5-6 safety constraints which can’t be violated while interacting with the environment. For example, “please avoid having the candle unattended”.
<p>
  <img src="Medium.png" width="350" title="Medium game example">
</p>

### Hard Game
Such games usually have 2 to 3 rooms with 6 to 12 objects with half of them as unsafe. These games also have a safety goal along with 5-6 safety constraints which can’t be violated while interacting with the environment to achieve the safety goal. For example, “Please avoid having the egg burned. Let’s see if you can get the egg cooked.”.
<p>
  <img src="Hard.png" width="350" title="Hard game example">
</p>
