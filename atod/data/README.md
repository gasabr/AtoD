# Data description
All the data used by app is stored in AtoD.db. All *.json files are temporary.

## abilities_changes.json
This file defines changes in abilities descriptions.

There are similar properties which could be merged to one property, this file
defines mapping from old names to the new ones.

**IMPORTANT:** mappings there value equal to one of the capitalized properties:
AbilityDamage, AbilityCooldown... should be defined at the *end of file*, after
everything.