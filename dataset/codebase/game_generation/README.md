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
$ python twc_make_game.py --objects 3 --rooms 1 --play --unsafe_item 2 --safety_constraints
```
The complete list of options of the script and their default value can be inspected by running:
```bash
$ python twc_make_game.py -h
```

# Generating games of varying difficulty

<p align="center">
  <img src="Easy.png" width="350" title="Easy game example">
</p>
