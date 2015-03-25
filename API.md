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
[  
  {  
    "fields":{  
      "status":1,
      "destination_character":"Numeil",
      "destination_realm":"conseil-des-ombres",
      "user":2,
      "source_character":"Bodoc",
      "reward":"- 10 Golds",
      "region":"eu",
      "description":"I want to kill this guy !",
      "updated_date":"2015-03-20T19:53:14.326Z",
      "source_realm":"conseil-des-ombres",
      "added_date":"2015-03-20T19:53:14.326Z"
    },
    "model":"bounties.bounty",
    "pk":1
  }
]
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
