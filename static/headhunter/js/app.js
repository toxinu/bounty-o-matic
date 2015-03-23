angular.module('HeadHunterApp', [
  'restangular',
  'ui.router',
  'ui.select',
  'ngSanitize'
])

.config(function(RestangularProvider, $httpProvider) {

  RestangularProvider.setBaseUrl('/api');

  // $httpProvider.defaults.useXDomain = true;
  // $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
  // $httpProvider.defaults.headers.common['X-CSRF-Token'] = $("#csrf").val();
  // $httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8';
})

.config(function($stateProvider, $urlRouterProvider){

    $stateProvider
    .state('create', {
      url: '/create',
      controller: 'CreateCtrl',
      templateUrl: '/static/headhunter/js/tpl/create.html',
    })
    .state('bounties', {
      url: '/',
      controller: 'BountiesCtrl',
      templateUrl: '/static/headhunter/js/tpl/bounties.html',
    });

    $urlRouterProvider.otherwise("/");
})

.directive('bounty', function() {
  return {
    scope: {
      bounty: '='
    },
    restrict: 'E',
    templateUrl: '/static/headhunter/js/tpl/components/bounty.html'
  };
})

.directive('bountyList', function() {
  return {
    restrict: 'E',
    scope: {
      bounties: '='
    },
    templateUrl: '/static/headhunter/js/tpl/components/bounty-list.html'
  };
})

.directive('loader', function() {
  return {
    restrict: 'E',
    templateUrl: '/static/headhunter/js/tpl/components/loader.html'
  };
})

.factory('Bounties', function(Restangular) {
  return Restangular.service('bounty');
})

.factory('Regions', function(Restangular) {
  return Restangular.service('regions');
})

.factory('Realms', function(Restangular) {
  return Restangular.service('realms');
})

.factory('User', function(Restangular) {
  return {
    getBattleTag: function() {
      return Restangular.all('player-battletag').one('').get();
    },
    getCharacters: function() {
      return Restangular.all('player-characters').getList();
    }
  };
})

.controller('CreateCtrl', function($scope, User, Regions, Realms, Bounties, Restangular) {

  $scope.currentStep = 1;

  $scope.sCharacter = {};
  $scope.sRegion = {};
  $scope.sRealm = {};
  $scope.sTarget = '';

  // $scope.characters = User.getCharacters().$object;
  $scope.characters = [{"gender": 0, "race": 8, "region": "eu", "name": "Canaflouz", "realm": "Ner'zhul", "battlegroup": "Embuscade / Hinterhalt", "normalized_realm": "nerzhul", "achievementPoints": 0, "thumbnail": "garona/89/65976409-avatar.jpg", "level": 1, "class": 5}, {"race": 5, "guild": "Blight", "realm": "Archimonde", "achievementPoints": 0, "thumbnail": "stonemaul/178/107358386-avatar.jpg", "gender": 0, "battlegroup": "Misery", "region": "eu", "name": "Didyer", "guildRealm": "Archimonde", "normalized_realm": "archimonde", "level": 42, "class": 8}, {"gender": 1, "race": 1, "region": "eu", "name": "Ghaji", "realm": "Cho'gall", "battlegroup": "Vengeance / Rache", "normalized_realm": "chogall", "achievementPoints": 0, "thumbnail": "eldrethalas/245/61643765-avatar.jpg", "level": 10, "class": 8}, {"gender": 0, "race": 5, "region": "eu", "name": "Stickman", "realm": "Ner'zhul", "battlegroup": "Embuscade / Hinterhalt", "normalized_realm": "nerzhul", "achievementPoints": 0, "thumbnail": "garona/48/66248752-avatar.jpg", "level": 14, "class": 4}, {"gender": 1, "race": 5, "region": "eu", "name": "Pikouse", "realm": "Uldaman", "battlegroup": "Embuscade / Hinterhalt", "normalized_realm": "uldaman", "achievementPoints": 460, "thumbnail": "uldaman/162/3590562-avatar.jpg", "level": 41, "class": 5}, {"gender": 0, "race": 5, "region": "eu", "name": "Oldschoolz", "realm": "Ner'zhul", "battlegroup": "Embuscade / Hinterhalt", "normalized_realm": "nerzhul", "achievementPoints": 0, "thumbnail": "garona/214/65887958-avatar.jpg", "level": 38, "class": 1}, {"gender": 1, "race": 10, "region": "eu", "name": "Unilia", "realm": "Scarshield Legion", "battlegroup": "Glutsturm / Emberstorm", "normalized_realm": "scarshield-legion", "achievementPoints": 0, "thumbnail": "scarshield-legion/232/49415144-avatar.jpg", "level": 6, "class": 5}, {"race": 1, "realm": "Conseil des Ombres", "achievementPoints": 2025, "thumbnail": "la-croisade-ecarlate/37/92538661-avatar.jpg", "spec": {"icon": "spell_shadow_shadowwordpain", "role": "DPS", "backgroundImage": "bg-priest-shadow", "name": "Shadow", "order": 2, "description": "Uses sinister Shadow magic, especially damage-over-time spells, to eradicate enemies."}, "gender": 1, "region": "eu", "name": "Umleirria", "battlegroup": "Embuscade / Hinterhalt", "normalized_realm": "conseil-des-ombres", "level": 100, "class": 5}, {"gender": 1, "race": 10, "region": "eu", "name": "Im\u00f6en", "realm": "Ner'zhul", "battlegroup": "Embuscade / Hinterhalt", "normalized_realm": "nerzhul", "achievementPoints": 0, "thumbnail": "garona/215/65964247-avatar.jpg", "level": 21, "class": 9}, {"gender": 0, "race": 2, "region": "eu", "name": "Canap\u00e9", "realm": "Ner'zhul", "battlegroup": "Embuscade / Hinterhalt", "normalized_realm": "nerzhul", "achievementPoints": 0, "thumbnail": "garona/98/65944930-avatar.jpg", "level": 70, "class": 7}, {"gender": 0, "race": 6, "region": "eu", "name": "Didibowser", "realm": "Uldaman", "battlegroup": "Embuscade / Hinterhalt", "normalized_realm": "uldaman", "achievementPoints": 900, "thumbnail": "uldaman/66/12200514-avatar.jpg", "level": 70, "class": 3}, {"gender": 1, "race": 2, "region": "eu", "name": "Umleirria", "realm": "Hyjal", "battlegroup": "Misery", "normalized_realm": "hyjal", "achievementPoints": 0, "thumbnail": "gm-test-realm-2/197/113935813-avatar.jpg", "level": 23, "class": 7}, {"race": 6, "guild": "Arm\u00e9e Des T\u00e9n\u00e8bres", "realm": "Uldaman", "achievementPoints": 860, "thumbnail": "uldaman/30/3513118-avatar.jpg", "gender": 0, "battlegroup": "Embuscade / Hinterhalt", "region": "eu", "name": "Didiroth", "guildRealm": "Uldaman", "normalized_realm": "uldaman", "level": 63, "class": 7}, {"gender": 0, "race": 5, "region": "eu", "name": "Vieumoche", "realm": "Uldaman", "battlegroup": "Embuscade / Hinterhalt", "normalized_realm": "uldaman", "achievementPoints": 250, "thumbnail": "uldaman/173/19406509-avatar.jpg", "level": 30, "class": 5}, {"race": 2, "realm": "Uldaman", "guild": "Holy Beers", "achievementPoints": 1180, "thumbnail": "uldaman/44/57610028-avatar.jpg", "spec": {"icon": "ability_warrior_savageblow", "role": "DPS", "backgroundImage": "bg-warrior-arms", "name": "Arms", "order": 0, "description": "A battle-hardened master of two-handed weapons, using mobility and overpowering attacks to strike his opponents down."}, "gender": 0, "guildRealm": "Uldaman", "region": "eu", "name": "Ragar", "battlegroup": "Embuscade / Hinterhalt", "normalized_realm": "uldaman", "level": 31, "class": 1}];

  // $scope.regions = Regions.getList().$object;
  $scope.regions = [{"slug": "eu", "name": "Europe"}, {"slug": "us", "name": "US"}, {"slug": "kr", "name": "Korea"}, {"slug": "tw", "name": "Taiwan"}];


  $scope.$watch('sRegion.selected', function(region) {
    if (region) {
      // $scope.realms = Realms.getList({region: region.slug}).$object;
      $scope.realms = [{"slug": "aegwynn", "name": "Aegwynn"}, {"slug": "aerie-peak", "name": "Aerie Peak"}, {"slug": "agamaggan", "name": "Agamaggan"}, {"slug": "aggra-portugues", "name": "Aggra (Portugu\u00eas)"}, {"slug": "aggramar", "name": "Aggramar"}, {"slug": "ahnqiraj", "name": "Ahn'Qiraj"}, {"slug": "alakir", "name": "Al'Akir"}, {"slug": "alexstrasza", "name": "Alexstrasza"}, {"slug": "alleria", "name": "Alleria"}, {"slug": "alonsus", "name": "Alonsus"}, {"slug": "amanthul", "name": "Aman'Thul"}, {"slug": "ambossar", "name": "Ambossar"}, {"slug": "anachronos", "name": "Anachronos"}, {"slug": "anetheron", "name": "Anetheron"}, {"slug": "antonidas", "name": "Antonidas"}, {"slug": "anubarak", "name": "Anub'arak"}, {"slug": "arakarahm", "name": "Arak-arahm"}, {"slug": "arathi", "name": "Arathi"}, {"slug": "arathor", "name": "Arathor"}, {"slug": "archimonde", "name": "Archimonde"}, {"slug": "area-52", "name": "Area 52"}, {"slug": "argent-dawn", "name": "Argent Dawn"}, {"slug": "arthas", "name": "Arthas"}, {"slug": "arygos", "name": "Arygos"}, {"slug": "ashenvale", "name": "Ashenvale"}, {"slug": "aszune", "name": "Aszune"}, {"slug": "auchindoun", "name": "Auchindoun"}, {"slug": "azjolnerub", "name": "Azjol-Nerub"}, {"slug": "azshara", "name": "Azshara"}, {"slug": "azuregos", "name": "Azuregos"}, {"slug": "azuremyst", "name": "Azuremyst"}, {"slug": "baelgun", "name": "Baelgun"}, {"slug": "balnazzar", "name": "Balnazzar"}, {"slug": "blackhand", "name": "Blackhand"}, {"slug": "blackmoore", "name": "Blackmoore"}, {"slug": "blackrock", "name": "Blackrock"}, {"slug": "blackscar", "name": "Blackscar"}, {"slug": "blades-edge", "name": "Blade's Edge"}, {"slug": "bladefist", "name": "Bladefist"}, {"slug": "bloodfeather", "name": "Bloodfeather"}, {"slug": "bloodhoof", "name": "Bloodhoof"}, {"slug": "bloodscalp", "name": "Bloodscalp"}, {"slug": "blutkessel", "name": "Blutkessel"}, {"slug": "booty-bay", "name": "Booty Bay"}, {"slug": "borean-tundra", "name": "Borean Tundra"}, {"slug": "boulderfist", "name": "Boulderfist"}, {"slug": "bronze-dragonflight", "name": "Bronze Dragonflight"}, {"slug": "bronzebeard", "name": "Bronzebeard"}, {"slug": "burning-blade", "name": "Burning Blade"}, {"slug": "burning-steppes", "name": "Burning Steppes"}, {"slug": "cthun", "name": "C'Thun"}, {"slug": "chamber-of-aspects", "name": "Chamber of Aspects"}, {"slug": "chants-eternels", "name": "Chants \u00e9ternels"}, {"slug": "chogall", "name": "Cho'gall"}, {"slug": "chromaggus", "name": "Chromaggus"}, {"slug": "colinas-pardas", "name": "Colinas Pardas"}, {"slug": "confrerie-du-thorium", "name": "Confr\u00e9rie du Thorium"}, {"slug": "conseil-des-ombres", "name": "Conseil des Ombres"}, {"slug": "crushridge", "name": "Crushridge"}, {"slug": "culte-de-la-rive-noire", "name": "Culte de la Rive noire"}, {"slug": "daggerspine", "name": "Daggerspine"}, {"slug": "dalaran", "name": "Dalaran"}, {"slug": "dalvengyr", "name": "Dalvengyr"}, {"slug": "darkmoon-faire", "name": "Darkmoon Faire"}, {"slug": "darksorrow", "name": "Darksorrow"}, {"slug": "darkspear", "name": "Darkspear"}, {"slug": "das-konsortium", "name": "Das Konsortium"}, {"slug": "das-syndikat", "name": "Das Syndikat"}, {"slug": "deathguard", "name": "Deathguard"}, {"slug": "deathweaver", "name": "Deathweaver"}, {"slug": "deathwing", "name": "Deathwing"}, {"slug": "deepholm", "name": "Deepholm"}, {"slug": "defias-brotherhood", "name": "Defias Brotherhood"}, {"slug": "dentarg", "name": "Dentarg"}, {"slug": "der-mithrilorden", "name": "Der Mithrilorden"}, {"slug": "der-rat-von-dalaran", "name": "Der Rat von Dalaran"}, {"slug": "der-abyssische-rat", "name": "Der abyssische Rat"}, {"slug": "destromath", "name": "Destromath"}, {"slug": "dethecus", "name": "Dethecus"}, {"slug": "die-aldor", "name": "Die Aldor"}, {"slug": "die-arguswacht", "name": "Die Arguswacht"}, {"slug": "die-nachtwache", "name": "Die Nachtwache"}, {"slug": "die-silberne-hand", "name": "Die Silberne Hand"}, {"slug": "die-todeskrallen", "name": "Die Todeskrallen"}, {"slug": "die-ewige-wacht", "name": "Die ewige Wacht"}, {"slug": "doomhammer", "name": "Doomhammer"}, {"slug": "draenor", "name": "Draenor"}, {"slug": "dragonblight", "name": "Dragonblight"}, {"slug": "dragonmaw", "name": "Dragonmaw"}, {"slug": "drakthul", "name": "Drak'thul"}, {"slug": "drekthar", "name": "Drek'Thar"}, {"slug": "dun-modr", "name": "Dun Modr"}, {"slug": "dun-morogh", "name": "Dun Morogh"}, {"slug": "dunemaul", "name": "Dunemaul"}, {"slug": "durotan", "name": "Durotan"}, {"slug": "earthen-ring", "name": "Earthen Ring"}, {"slug": "echsenkessel", "name": "Echsenkessel"}, {"slug": "eitrigg", "name": "Eitrigg"}, {"slug": "eldrethalas", "name": "Eldre'Thalas"}, {"slug": "elune", "name": "Elune"}, {"slug": "emerald-dream", "name": "Emerald Dream"}, {"slug": "emeriss", "name": "Emeriss"}, {"slug": "eonar", "name": "Eonar"}, {"slug": "eredar", "name": "Eredar"}, {"slug": "eversong", "name": "Eversong"}, {"slug": "executus", "name": "Executus"}, {"slug": "exodar", "name": "Exodar"}, {"slug": "festung-der-sturme", "name": "Festung der St\u00fcrme"}, {"slug": "fordragon", "name": "Fordragon"}, {"slug": "forscherliga", "name": "Forscherliga"}, {"slug": "frostmane", "name": "Frostmane"}, {"slug": "frostmourne", "name": "Frostmourne"}, {"slug": "frostwhisper", "name": "Frostwhisper"}, {"slug": "frostwolf", "name": "Frostwolf"}, {"slug": "galakrond", "name": "Galakrond"}, {"slug": "garona", "name": "Garona"}, {"slug": "garrosh", "name": "Garrosh"}, {"slug": "genjuros", "name": "Genjuros"}, {"slug": "ghostlands", "name": "Ghostlands"}, {"slug": "gilneas", "name": "Gilneas"}, {"slug": "goldrinn", "name": "Goldrinn"}, {"slug": "gordunni", "name": "Gordunni"}, {"slug": "gorgonnash", "name": "Gorgonnash"}, {"slug": "greymane", "name": "Greymane"}, {"slug": "grim-batol", "name": "Grim Batol"}, {"slug": "grom", "name": "Grom"}, {"slug": "guldan", "name": "Gul'dan"}, {"slug": "hakkar", "name": "Hakkar"}, {"slug": "haomarush", "name": "Haomarush"}, {"slug": "hellfire", "name": "Hellfire"}, {"slug": "hellscream", "name": "Hellscream"}, {"slug": "howling-fjord", "name": "Howling Fjord"}, {"slug": "hyjal", "name": "Hyjal"}, {"slug": "illidan", "name": "Illidan"}, {"slug": "jaedenar", "name": "Jaedenar"}, {"slug": "kaelthas", "name": "Kael'thas"}, {"slug": "karazhan", "name": "Karazhan"}, {"slug": "kargath", "name": "Kargath"}, {"slug": "kazzak", "name": "Kazzak"}, {"slug": "kelthuzad", "name": "Kel'Thuzad"}, {"slug": "khadgar", "name": "Khadgar"}, {"slug": "khaz-modan", "name": "Khaz Modan"}, {"slug": "khazgoroth", "name": "Khaz'goroth"}, {"slug": "kiljaeden", "name": "Kil'jaeden"}, {"slug": "kilrogg", "name": "Kilrogg"}, {"slug": "kirin-tor", "name": "Kirin Tor"}, {"slug": "korgall", "name": "Kor'gall"}, {"slug": "kragjin", "name": "Krag'jin"}, {"slug": "krasus", "name": "Krasus"}, {"slug": "kul-tiras", "name": "Kul Tiras"}, {"slug": "kult-der-verdammten", "name": "Kult der Verdammten"}, {"slug": "la-croisade-ecarlate", "name": "La Croisade \u00e9carlate"}, {"slug": "laughing-skull", "name": "Laughing Skull"}, {"slug": "les-clairvoyants", "name": "Les Clairvoyants"}, {"slug": "les-sentinelles", "name": "Les Sentinelles"}, {"slug": "lich-king", "name": "Lich King"}, {"slug": "lightbringer", "name": "Lightbringer"}, {"slug": "lightnings-blade", "name": "Lightning's Blade"}, {"slug": "lordaeron", "name": "Lordaeron"}, {"slug": "los-errantes", "name": "Los Errantes"}, {"slug": "lothar", "name": "Lothar"}, {"slug": "madmortem", "name": "Madmortem"}, {"slug": "magtheridon", "name": "Magtheridon"}, {"slug": "malganis", "name": "Mal'Ganis"}, {"slug": "malfurion", "name": "Malfurion"}, {"slug": "malorne", "name": "Malorne"}, {"slug": "malygos", "name": "Malygos"}, {"slug": "mannoroth", "name": "Mannoroth"}, {"slug": "marecage-de-zangar", "name": "Mar\u00e9cage de Zangar"}, {"slug": "mazrigos", "name": "Mazrigos"}, {"slug": "medivh", "name": "Medivh"}, {"slug": "minahonda", "name": "Minahonda"}, {"slug": "moonglade", "name": "Moonglade"}, {"slug": "mugthol", "name": "Mug'thol"}, {"slug": "nagrand", "name": "Nagrand"}, {"slug": "nathrezim", "name": "Nathrezim"}, {"slug": "naxxramas", "name": "Naxxramas"}, {"slug": "nazjatar", "name": "Nazjatar"}, {"slug": "nefarian", "name": "Nefarian"}, {"slug": "nemesis", "name": "Nemesis"}, {"slug": "neptulon", "name": "Neptulon"}, {"slug": "nerzhul", "name": "Ner'zhul"}, {"slug": "nerathor", "name": "Nera'thor"}, {"slug": "nethersturm", "name": "Nethersturm"}, {"slug": "nordrassil", "name": "Nordrassil"}, {"slug": "norgannon", "name": "Norgannon"}, {"slug": "nozdormu", "name": "Nozdormu"}, {"slug": "onyxia", "name": "Onyxia"}, {"slug": "outland", "name": "Outland"}, {"slug": "perenolde", "name": "Perenolde"}, {"slug": "pozzo-delleternita", "name": "Pozzo dell'Eternit\u00e0"}, {"slug": "proudmoore", "name": "Proudmoore"}, {"slug": "quelthalas", "name": "Quel'Thalas"}, {"slug": "ragnaros", "name": "Ragnaros"}, {"slug": "rajaxx", "name": "Rajaxx"}, {"slug": "rashgarroth", "name": "Rashgarroth"}, {"slug": "ravencrest", "name": "Ravencrest"}, {"slug": "ravenholdt", "name": "Ravenholdt"}, {"slug": "razuvious", "name": "Razuvious"}, {"slug": "rexxar", "name": "Rexxar"}, {"slug": "runetotem", "name": "Runetotem"}, {"slug": "sanguino", "name": "Sanguino"}, {"slug": "sargeras", "name": "Sargeras"}, {"slug": "saurfang", "name": "Saurfang"}, {"slug": "scarshield-legion", "name": "Scarshield Legion"}, {"slug": "senjin", "name": "Sen'jin"}, {"slug": "shadowsong", "name": "Shadowsong"}, {"slug": "shattered-halls", "name": "Shattered Halls"}, {"slug": "shattered-hand", "name": "Shattered Hand"}, {"slug": "shattrath", "name": "Shattrath"}, {"slug": "shendralar", "name": "Shen'dralar"}, {"slug": "silvermoon", "name": "Silvermoon"}, {"slug": "sinstralis", "name": "Sinstralis"}, {"slug": "skullcrusher", "name": "Skullcrusher"}, {"slug": "soulflayer", "name": "Soulflayer"}, {"slug": "spinebreaker", "name": "Spinebreaker"}, {"slug": "sporeggar", "name": "Sporeggar"}, {"slug": "steamwheedle-cartel", "name": "Steamwheedle Cartel"}, {"slug": "stormrage", "name": "Stormrage"}, {"slug": "stormreaver", "name": "Stormreaver"}, {"slug": "stormscale", "name": "Stormscale"}, {"slug": "sunstrider", "name": "Sunstrider"}, {"slug": "sylvanas", "name": "Sylvanas"}, {"slug": "taerar", "name": "Taerar"}, {"slug": "talnivarr", "name": "Talnivarr"}, {"slug": "tarren-mill", "name": "Tarren Mill"}, {"slug": "teldrassil", "name": "Teldrassil"}, {"slug": "temple-noir", "name": "Temple noir"}, {"slug": "terenas", "name": "Terenas"}, {"slug": "terokkar", "name": "Terokkar"}, {"slug": "terrordar", "name": "Terrordar"}, {"slug": "the-maelstrom", "name": "The Maelstrom"}, {"slug": "the-shatar", "name": "The Sha'tar"}, {"slug": "the-venture-co", "name": "The Venture Co"}, {"slug": "theradras", "name": "Theradras"}, {"slug": "thermaplugg", "name": "Thermaplugg"}, {"slug": "thrall", "name": "Thrall"}, {"slug": "throkferoth", "name": "Throk'Feroth"}, {"slug": "thunderhorn", "name": "Thunderhorn"}, {"slug": "tichondrius", "name": "Tichondrius"}, {"slug": "tirion", "name": "Tirion"}, {"slug": "todeswache", "name": "Todeswache"}, {"slug": "trollbane", "name": "Trollbane"}, {"slug": "turalyon", "name": "Turalyon"}, {"slug": "twilights-hammer", "name": "Twilight's Hammer"}, {"slug": "twisting-nether", "name": "Twisting Nether"}, {"slug": "tyrande", "name": "Tyrande"}, {"slug": "uldaman", "name": "Uldaman"}, {"slug": "ulduar", "name": "Ulduar"}, {"slug": "uldum", "name": "Uldum"}, {"slug": "ungoro", "name": "Un'Goro"}, {"slug": "varimathras", "name": "Varimathras"}, {"slug": "vashj", "name": "Vashj"}, {"slug": "veklor", "name": "Vek'lor"}, {"slug": "veknilash", "name": "Vek'nilash"}, {"slug": "voljin", "name": "Vol'jin"}, {"slug": "wildhammer", "name": "Wildhammer"}, {"slug": "wrathbringer", "name": "Wrathbringer"}, {"slug": "xavius", "name": "Xavius"}, {"slug": "ysera", "name": "Ysera"}, {"slug": "ysondre", "name": "Ysondre"}, {"slug": "zenedar", "name": "Zenedar"}, {"slug": "zirkel-des-cenarius", "name": "Zirkel des Cenarius"}, {"slug": "zuljin", "name": "Zul'jin"}, {"slug": "zuluhed", "name": "Zuluhed"}];
    }
  });

  $scope.process = function() {
    var params = {
      region: $scope.sRegion.selected.slug,
      source_realm: $scope.sCharacter.selected.realm,
      source_character: $scope.sCharacter.selected.region,
      destination_realm: $scope.sRealm.selected.slug,
      destination_character: $scope.sTarget,
      reward: $scope.sReward,
      description: $scope.sDescription
    };

    Restangular.all('bounty').customPOST(null, "", params);

    // Bounties.post();
  };
})

.controller('BountiesCtrl', function($scope, Bounties, User) {
  $scope.bounties = Bounties.getList().$object;
});
