# CUSTOM SEARCH ENGINE
## SETUP 1 (INDEX FILES PROVIDED)
If the index files have been provided to you. There are 2 folders: `iclusters`  and `ioi`. Unzip the file and dump the folders inside the `app\Indexer` so that it look like the following:

.(root_folder)
- dataset
    - DEV
    - ANALYST
- code
    - app
    - Indexer
        - ...
        - iclusters
        - ioi
        - ...

Put the files(json) provided by the Professor in the same root as the `code` folder as: `dataset/DEV` is you want to test DEV or `dataset/ANALYST` is you want to test ANALYST dataset. See above picture for reference. To run the webapp run the following command inside the code folder:

`python webapp.py`

## SETUP 2 (BUILD INDEX)
Open `indexer.py`.

### Step 1: Uncomment code between the following comments
```
## START: STAGE 1: Build initial index
...
## END: STAGE 1: Build initial index
```
Run `python indexer.py`. This would create a partial index for the pages.

### Step 2: Comment the above part of the code and uncomment the 
```
## START: STAGE 2: Build index of index
...
## END: STAGE 2: Build index of index
```
Run `python indexer.py` again to merge the partial indexes and then create the index-of-index and the parallel cluster of custom trie datastructure.

You can continue with Step 1. `/tmp` folder can be deleted but `/ioi`  and `/iclusters` is important for the search to run properly.
