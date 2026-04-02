REMINDER_MINUTES = {
    "spawn": 4,
    "hangmon": 8,
}

STARTER_POKEMON = {
    "bulbasaur", "ivysaur", "venusaur", "charmander", "charmeleon", "charizard",
    "squirtle", "wartortle", "blastoise", "chikorita", "bayleef", "meganium",
    "cyndaquil", "quilava", "typhlosion", "totodile", "croconaw", "feraligatr",
    "treecko", "grovyle", "sceptile", "torchic", "combusken", "blaziken",
    "mudkip", "marshtomp", "swampert", "turtwig", "grotle", "torterra",
    "chimchar", "monferno", "infernape", "piplup", "prinplup", "empoleon",
    "snivy", "servine", "serperior", "tepig", "pignite", "emboar",
    "oshawott", "dewott", "samurott", "chespin", "quilladin", "chesnaught",
    "fennekin", "braixen", "delphox", "froakie", "frogadier", "greninja",
    "rowlet", "dartrix", "decidueye", "litten", "torracat", "incineroar",
    "popplio", "brionne", "primarina", "grookey", "thwackey", "rillaboom",
    "scorbunny", "raboot", "cinderace", "sobble", "drizzile", "inteleon",
    "sprigatito", "floragato", "meowscarada", "fuecoco", "crocalor", "skeledirge",
    "quaxly", "quaxwell", "quaquaval",
}

PSEUDO_LEGENDARY_POKEMON = {
    "dragonite", "tyranitar", "salamence", "metagross", "garchomp", "hydreigon",
    "goodra", "kommo-o", "dragapult", "baxcalibur", "archaludon",
}

ULTRA_BEAST_POKEMON = {
    "nihilego", "buzzwole", "pheromosa", "xurkitree", "celesteela", "kartana",
    "guzzlord", "poipole", "naganadel", "stakataka", "blacephalon",
}

PARADOX_POKEMON = {
    "great-tusk", "scream-tail", "brute-bonnet", "flutter-mane", "slither-wing",
    "sandy-shocks", "roaring-moon", "walking-wake", "gouging-fire", "raging-bolt",
    "iron-treads", "iron-bundle", "iron-hands", "iron-jugulis", "iron-moth",
    "iron-thorns", "iron-valiant", "iron-leaves", "iron-boulder", "iron-crown",
}

FOSSIL_POKEMON = {
    "omanyte", "omastar", "kabuto", "kabutops", "aerodactyl", "lileep", "cradily",
    "anorith", "armaldo", "cranidos", "rampardos", "shieldon", "bastiodon",
    "tirtouga", "carracosta", "archen", "archeops", "tyrunt", "tyrantrum",
    "amaura", "aurorus", "dracozolt", "arctozolt", "dracovish", "arctovish",
}

SUB_LEGENDARY_POKEMON = {
    "articuno", "zapdos", "moltres", "raikou", "entei", "suicune", "regirock",
    "regice", "registeel", "latias", "latios", "uxie", "mesprit", "azelf",
    "heatran", "cresselia", "cobalion", "terrakion", "virizion", "tornadus",
    "thundurus", "landorus", "type-null", "silvally", "tapu-koko", "tapu-lele",
    "tapu-bulu", "tapu-fini", "nihilego", "buzzwole", "pheromosa", "xurkitree",
    "celesteela", "kartana", "guzzlord", "poipole", "naganadel", "stakataka",
    "blacephalon", "kubfu", "urshifu", "regieleki", "regidrago", "glastrier",
    "spectrier", "enamorus", "wo-chien", "chien-pao", "ting-lu", "chi-yu",
    "okidogi", "munkidori", "fezandipiti",
}

REGIONAL_FORM_MARKERS = (
    "-alola", "-galar", "-hisui", "-paldea",
)

LABEL_PRIORITY = {
    "Mythical": 0,
    "Legendary": 1,
    "Legendary Trio/Sub-Legendary": 2,
    "Ultra Beast": 3,
    "Paradox": 4,
    "Pseudo-Legendary": 5,
    "Starter": 6,
    "Baby": 7,
    "Mega": 8,
    "Regional Form": 9,
    "Fossil": 10,
    "Thường": 99,
}

ITEM_TYPE_LABELS = {
    "held-items": "Vật phẩm cầm",
    "healing": "Hồi máu",
    "pp-recovery": "Hồi PP",
    "revival": "Hồi sinh",
    "status-cures": "Chữa trạng thái",
    "bad-held-items": "Vật phẩm cầm bất lợi",
    "choice": "Vật phẩm Choice",
    "effort-training": "Vật phẩm EV",
    "evolution": "Tiến hóa",
    "plates": "Tấm Plate",
    "species-specific": "Item theo loài",
    "type-protection": "Giảm sát thương theo hệ",
    "stat-boosts": "Tăng chỉ số",
    "medicine": "Thuốc",
    "nature-mints": "Kẹo bạc hà Nature",
    "other": "Khác",
}

MINT_STAT_LABELS = {
    "adamant": ("Tấn Công", "Tấn Công Đặc Biệt"),
    "bold": ("Phòng Thủ", "Tấn Công"),
    "brave": ("Tấn Công", "Tốc Độ"),
    "calm": ("Phòng Thủ Đặc Biệt", "Tấn Công"),
    "careful": ("Phòng Thủ Đặc Biệt", "Tấn Công Đặc Biệt"),
    "gentle": ("Phòng Thủ Đặc Biệt", "Phòng Thủ"),
    "hasty": ("Tốc Độ", "Phòng Thủ"),
    "impish": ("Phòng Thủ", "Tấn Công Đặc Biệt"),
    "jolly": ("Tốc Độ", "Tấn Công Đặc Biệt"),
    "lax": ("Phòng Thủ", "Phòng Thủ Đặc Biệt"),
    "lonely": ("Tấn Công", "Phòng Thủ"),
    "mild": ("Tấn Công Đặc Biệt", "Phòng Thủ"),
    "modest": ("Tấn Công Đặc Biệt", "Tấn Công"),
    "naive": ("Tốc Độ", "Phòng Thủ Đặc Biệt"),
    "naughty": ("Tấn Công", "Phòng Thủ Đặc Biệt"),
    "quiet": ("Tấn Công Đặc Biệt", "Tốc Độ"),
    "rash": ("Tấn Công Đặc Biệt", "Phòng Thủ Đặc Biệt"),
    "relaxed": ("Phòng Thủ", "Tốc Độ"),
    "sassy": ("Phòng Thủ Đặc Biệt", "Tốc Độ"),
    "timid": ("Tốc Độ", "Tấn Công"),
}

ITEM_USAGE_HINTS = {
    "air-balloon": {
        "can_be_used_by": "Hầu hết Pokémon có thể cầm",
        "good_on": [
            {"pokemon": "dialga", "reason": "giảm áp lực từ Ground moves"},
            {"pokemon": "magnezone", "reason": "4x sợ Ground"},
            {"pokemon": "heatran", "reason": "cần một lượt miễn nhiễm Ground để xoay vòng"},
        ],
    },
    "choice-band": {
        "can_be_used_by": "Phù hợp nhất với sweeper vật lý",
        "good_on": [
            {"pokemon": "dragonite", "reason": "tăng sức ép Extreme Speed và Outrage"},
            {"pokemon": "azumarill", "reason": "Aqua Jet và Play Rough gây áp lực mạnh"},
            {"pokemon": "garchomp", "reason": "wallbreak tốt hơn với Earthquake"},
        ],
    },
    "choice-specs": {
        "can_be_used_by": "Phù hợp nhất với sweeper đặc công",
        "good_on": [
            {"pokemon": "dragapult", "reason": "Shadow Ball và Draco Meteor rất khó đỡ"},
            {"pokemon": "walking-wake", "reason": "Hydro Steam và Draco Meteor gây sức ép lớn"},
            {"pokemon": "flutter-mane", "reason": "Moonblast và Shadow Ball đều nguy hiểm"},
        ],
    },
    "choice-scarf": {
        "can_be_used_by": "Phù hợp với revenge killer cần tốc độ",
        "good_on": [
            {"pokemon": "landorus-therian", "reason": "pivot nhanh, dễ revenge kill"},
            {"pokemon": "gholdengo", "reason": "vượt speed nhiều mối đe dọa"},
            {"pokemon": "chi-yu", "reason": "tốc độ cao hơn giúp dọn sân"},
        ],
    },
    "focus-sash": {
        "can_be_used_by": "Tốt cho lead mỏng hoặc setup sweeper",
        "good_on": [
            {"pokemon": "alakazam", "reason": "cần sống qua một hit để phản công"},
            {"pokemon": "breloom", "reason": "giữ một lượt để Spore hoặc setup"},
            {"pokemon": "glimmora", "reason": "lead hazard rất hợp với sash"},
        ],
    },
    "life-orb": {
        "can_be_used_by": "Hợp với sweeper muốn đổi lâu lượt lấy sức mạnh",
        "good_on": [
            {"pokemon": "greninja", "reason": "cần sát thương linh hoạt khi đổi chiêu"},
            {"pokemon": "mamoswine", "reason": "tăng áp lực tấn công ngay lập tức"},
            {"pokemon": "infernape", "reason": "mixed attacker tận dụng tốt"},
        ],
    },
    "leftovers": {
        "can_be_used_by": "Phù hợp với tank, wall và setup bulky",
        "good_on": [
            {"pokemon": "toxapex", "reason": "rất cần hồi máu mỗi lượt"},
            {"pokemon": "corviknight", "reason": "tăng độ bền khi pivot"},
            {"pokemon": "ting-lu", "reason": "bulk cao, càng hợp item hồi máu"},
        ],
    },
    "assault-vest": {
        "can_be_used_by": "Phù hợp Pokémon chỉ muốn tấn công và cần bulk đặc biệt",
        "good_on": [
            {"pokemon": "goodra", "reason": "special bulk rất cao khi cầm vest"},
            {"pokemon": "iron-hands", "reason": "trâu hơn rất nhiều khi ăn hit đặc công"},
            {"pokemon": "slowking-galar", "reason": "pivot đặc công rất khó chết"},
        ],
    },
    "eviolite": {
        "can_be_used_by": "Chỉ dùng tốt cho Pokémon chưa tiến hóa hết",
        "good_on": [
            {"pokemon": "chansey", "reason": "bulk đặc biệt cực cao"},
            {"pokemon": "porygon2", "reason": "vừa trâu vừa utility tốt"},
            {"pokemon": "dusclops", "reason": "tăng bulk rất mạnh cho vai trò support"},
        ],
    },
    "light-clay": {
        "can_be_used_by": "Tốt cho screen setter có Reflect và Light Screen",
        "good_on": [
            {"pokemon": "grimmsnarl", "reason": "screen setter rất phổ biến"},
            {"pokemon": "regieleki", "reason": "dựng screen nhanh rồi rút"},
            {"pokemon": "klefki", "reason": "Prankster giúp bật screen ổn định"},
        ],
    },
    "rocky-helmet": {
        "can_be_used_by": "Hợp với wall chịu đòn tiếp xúc",
        "good_on": [
            {"pokemon": "skarmory", "reason": "punish contact move rất tốt"},
            {"pokemon": "garchomp", "reason": "kết hợp Rough Skin để bào máu đối thủ"},
            {"pokemon": "tangrowth", "reason": "vào đòn vật lý nhiều lần"},
        ],
    },
    "weakness-policy": {
        "can_be_used_by": "Phù hợp Pokémon bulky có thể sống qua đòn siêu hiệu quả",
        "good_on": [
            {"pokemon": "dragonite", "reason": "Multiscale giúp kích hoạt item an toàn hơn"},
            {"pokemon": "necrozma-dusk", "reason": "bulk tốt, sau boost rất nguy hiểm"},
            {"pokemon": "coalossal", "reason": "có thể snowball sau khi bị đánh đúng kèo combo"},
        ],
    },
    "heavy-duty-boots": {
        "can_be_used_by": "Rất tốt cho Pokémon yếu Stealth Rock hoặc cần vào ra liên tục",
        "good_on": [
            {"pokemon": "volcarona", "reason": "rất ngại Stealth Rock"},
            {"pokemon": "charizard", "reason": "4x sợ Rock hazard"},
            {"pokemon": "dragonite", "reason": "giữ HP để tận dụng Multiscale"},
        ],
    },
    "booster-energy": {
        "can_be_used_by": "Dành cho Paradox Pokémon",
        "good_on": [
            {"pokemon": "flutter-mane", "reason": "kích hoạt Protosynthesis ngay lập tức"},
            {"pokemon": "iron-valiant", "reason": "tăng sức ép tấn công hoặc tốc độ"},
            {"pokemon": "roaring-moon", "reason": "setup sweep dễ hơn sau boost"},
        ],
    },
}
