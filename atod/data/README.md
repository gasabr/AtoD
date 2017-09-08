### What is this folder?

This is there all the files for library are stored.

### Why there are these files?

To work properly AtoD only needs AtoD.db, all the other files are required to add new patches. They store some mappings, db_schemas and everything I changed in the original data.

### How to add patch

1. Create a folder `<version_name>` .

2. Copy content of `version-must-have` to your folder

3. Add missing files:

   * `npc_heroes.txt` -- heroes_descriptions
   * `npc_abilities.txt` -- abilities descriptions 
   * `dota_english` -- should contain abilities textual descriptions

4. Write in terminal

   ``` python
   >>> from atod.utils import update
   >>> update.add_patch('<patch_name>', '<full/path/to/your/folder>')
   ```

   When command is completed you are done.



### How to delete patch

```python
>>> from atod.utils import update
>>> update.delete_patch('<patch_name>')
```

