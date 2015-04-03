# Player

## GET /api/player-battletag

Need to be authenticated with a BattleNet account.  
Return Battletag.

`{"battletag": "Jambon#1000"}`

## GET /api/player-characters

Need to be authenticated with a BattleNet account.  
Return characters list.

```
[  
  {  
    "level":3,
    "realm":"Uldaman",
    "class":1,
    "gender":0,
    "battlegroup":"Embuscade / Hinterhalt",
    "thumbnail":"uldaman/13/56595469-avatar.jpg",
    "region":"eu",
    "achievementPoints":0,
    "name":"Wargleb",
    "normalized_realm":"uldaman",
    "race":2
  },
  {  
    "realm":"Conseil des Ombres",
    "battlegroup":"Embuscade / Hinterhalt",
    "achievementPoints":8255,
    "class":7,
    "race":3,
    "spec":{  
      "icon":"spell_nature_lightning",
      "order":0,
      "backgroundImage":"bg-shaman-elemental",
      "description":"A spellcaster who harnesses the destructive forces of nature and the elements.",
      "name":"Elemental",
      "role":"DPS"
    },
    "thumbnail":"la-croisade-ecarlate/56/95089464-avatar.jpg",
    "normalized_realm":"conseil-des-ombres",
    "gender":0,
    "region":"eu",
    "name":"Bifilin",
    "level":91
  }
]
```

## GET /api/player-refresh

Need to be authenticated with a BattleNet account.
Refresh all BattleNet data related to this user.

`{"status": "ok", "reasions": []}`

# BattleNet data

## GET /api/regions

Return regions list.

```
[  
  {  
    "slug":"eu",
    "name":"Europe"
  },
  {  
    "slug":"us",
    "name":"US"
  },
  {  
    "slug":"kr",
    "name":"Korea"
  },
  {  
    "slug":"tw",
    "name":"Taiwan"
  }
]
```

## GET /api/realms?region=\<region_slug\>

Return realms list of a specific region.

```
[  
  {  
    "slug":"aegwynn",
    "name":"Aegwynn"
  },
  {  
    "slug":"aerie-peak",
    "name":"Aerie Peak"
  },
  {  
    "slug":"agamaggan",
    "name":"Agamaggan"
  }
]
```

## GET /api/bounty

Return bounties list.  
Fields returned will change.

```
{
  "count": 3,
  "num_pages": 1,
  "objects": [
    {
      "added_date": "2015-04-03 09:40:16.719981+00:00",
      "comments_count": 0,
      "destination_armory": "http://eu.battle.net/wow/eu/character/culte-de-la-rive-noire/Scaye/simple",
      "destination_character": "Scaye",
      "destination_faction": 0,
      "destination_faction_display": null,
      "destination_guild": "La L\u00e9gion de Stormwind",
      "destination_realm": "culte-de-la-rive-noire",
      "destination_realm_display": "Culte de la Rive noire",
      "id": 3,
      "is_private": false,
      "region": "eu",
      "region_display": "Europe",
      "source_armory": "http://eu.battle.net/wow/eu/character/conseil-des-ombres/Grokk/simple",
      "source_character": "Grokk",
      "source_guild": null,
      "source_realm": "conseil-des-ombres",
      "source_realm_display": "Conseil des Ombres",
      "status": 1,
      "status_display": "Ouverte",
      "updated_date": "2015-04-03 09:40:16.720088+00:00",
      "user": 3
    }
  ]
}
```

## POST /api/bounty

Create a new bounty.  
**Required fields**:

 - `region`
 - `source_realm`
 - `source_character`
 - `destination_realm`
 - `destination_character`
 - `reward`
 - `description`

**Optionnal fields**:

 - `is_private`

If success return bounty as json.
If failure: `{"status": "nok", "reasons" : []}`.


## GET /api/bounty/\<bounty_id\>

Return a bounty with more fields.

```
{
  "added_date": "2015-04-03 09:40:16.719981+00:00",
  "comments": {
    "count": 0,
    "num_pages": 1,
    "objects": [],
    "page": 1
  },
  "description": "the description",
  "description_as_html": "the description",
  "destination_armory": "http://eu.battle.net/wow/eu/character/culte-de-la-rive-noire/Scaye/simple",
  "destination_character": "Scaye",
  "destination_class_display": "Paladin",
  "destination_faction": 0,
  "destination_faction_display": "Alliance",
  "destination_guild": "La L\u00e9gion de Stormwind",
  "destination_level": 100,
  "destination_realm": "culte-de-la-rive-noire",
  "destination_realm_display": "Culte de la Rive noire",
  "destination_thumbnail": "https://eu.battle.net/static-render/eu/la-croisade-ecarlate/214/71613654-avatar.jpg?alt=wow/static/images/2d/avatar/1-0.jpg",
  "id": 3,
  "is_private": false,
  "region": "eu",
  "region_display": "Europe",
  "reward": "the reward",
  "reward_as_html": "the reward",
  "source_armory": "http://eu.battle.net/wow/eu/character/conseil-des-ombres/Grokk/simple",
  "source_character": "Grokk",
  "source_class_display": "D\u00e9moniste",
  "source_faction": 1,
  "source_faction_display": "Horde",
  "source_guild": null,
  "source_level": 24,
  "source_realm": "conseil-des-ombres",
  "source_realm_display": "Conseil des Ombres",
  "source_thumbnail": "https://eu.battle.net/static-render/eu/la-croisade-ecarlate/13/96534541-avatar.jpg?alt=wow/static/images/2d/avatar/2-0.jpg",
  "status": 1,
  "status_display": "Ouverte",
  "updated_date": "2015-04-03 09:40:16.720088+00:00",
  "user": 3,
  "winner_armory": null,
  "winner_character": null,
  "winner_class_display": null,
  "winner_faction": null,
  "winner_faction_display": null,
  "winner_guild": null,
  "winner_level": null,
  "winner_realm": null,
  "winner_realm_display": "Culte de la Rive noire"
}
```

## POST /api/bounty/\<bounty_id\>

Update a existing bounty.
Editable fields:

 - `description`
 - `reward`
 - `status`
 - `source_character`
 - `source_realm`
 - `is_private`
 - `winner_character`
 - `winner_realm`

If success, return edited bounty.
If failure: `{"status": "nok", "reasons" : []}`.
