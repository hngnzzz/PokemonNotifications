import re

from data import ITEM_TYPE_LABELS, ITEM_USAGE_HINTS, MINT_STAT_LABELS
from models import ItemDetails, ItemUsageHint


def display_item_name(name: str) -> str:
    return name.replace("-", " ").title()


def translate_item_effect(effect: str) -> str:
    translated = effect.strip()
    phrase_replacements = [
        ("An item to be held by a Pokémon. ", "Một vật phẩm để Pokémon cầm. "),
        ("If held by a Pokémon, ", "Nếu được Pokémon cầm, "),
        ("If held by the target, ", "Nếu mục tiêu đang cầm vật phẩm này, "),
        ("It raises the power of ", "Nó tăng sức mạnh của "),
        ("It boosts the power of ", "Nó tăng sức mạnh của "),
        ("It weakens ", "Nó giảm sức mạnh của "),
        ("It restores ", "Nó hồi "),
        ("It prevents ", "Nó ngăn "),
        ("It enables ", "Nó cho phép "),
        ("It extends the duration of ", "Nó kéo dài thời gian của "),
        ("It doubles the holder's ", "Nó tăng gấp đôi "),
        ("It halves damage taken from ", "Nó giảm một nửa sát thương nhận từ "),
        ("It makes the holder immune to ", "Nó giúp Pokémon cầm nó miễn nhiễm với "),
        ("The holder", "Pokémon cầm nó"),
        ("holder's", "của Pokémon cầm nó"),
        ("holder", "Pokémon cầm nó"),
        ("super effective", "siêu hiệu quả"),
        ("for five turns", "trong năm lượt"),
        ("for eight turns", "trong tám lượt"),
        ("for one turn", "trong một lượt"),
        ("by 10%", "thêm 10%"),
        ("by 20%", "thêm 20%"),
        ("by 30%", "thêm 30%"),
        ("by 50%", "thêm 50%"),
    ]
    replacements = [
        ("Pokémon's", "của Pokémon"),
        ("Pokemon's", "của Pokémon"),
        ("Ground-type moves", "các đòn hệ Ground"),
        ("Ground-type move", "đòn hệ Ground"),
        ("Ground-type", "hệ Ground"),
        ("Electric-type", "hệ Electric"),
        ("Fire-type", "hệ Fire"),
        ("Water-type", "hệ Water"),
        ("Ice-type", "hệ Ice"),
        ("Rock-type", "hệ Rock"),
        ("Fighting-type", "hệ Fighting"),
        ("Dragon-type", "hệ Dragon"),
        ("Dark-type", "hệ Dark"),
        ("Psychic-type", "hệ Psychic"),
        ("Special Defense", "Phòng Thủ Đặc Biệt"),
        ("Special Attack", "Tấn Công Đặc Biệt"),
        ("Defense", "Phòng Thủ"),
        ("Attack", "Tấn Công"),
        ("Speed", "Tốc Độ"),
        ("accuracy", "độ chính xác"),
        ("critical-hit ratio", "tỉ lệ chí mạng"),
        ("priority", "độ ưu tiên"),
        ("status move", "chiêu trạng thái"),
        ("status moves", "các chiêu trạng thái"),
        ("physical move", "chiêu vật lý"),
        ("physical moves", "các chiêu vật lý"),
        ("special move", "chiêu đặc công"),
        ("special moves", "các chiêu đặc công"),
        ("move", "chiêu"),
        ("moves", "chiêu"),
        ("switching out", "rút ra"),
        ("switch out", "rút ra"),
        ("HP", "HP"),
    ]
    for source, target in phrase_replacements:
        translated = translated.replace(source, target)
    for source, target in replacements:
        translated = translated.replace(source, target)

    translated = re.sub(r"\bIts\b", "Chỉ số của nó", translated)
    translated = re.sub(r"\bits\b", "chỉ số của nó", translated)
    translated = re.sub(r"\bThis item\b", "Vật phẩm này", translated)
    translated = re.sub(r"\bThis\b", "Vật phẩm này", translated)
    translated = re.sub(r"\bWhen hit by\b", "Khi bị đánh bởi", translated)
    translated = re.sub(r"\bWhen struck by\b", "Khi bị trúng", translated)
    translated = re.sub(r"\bWhen\b", "Khi", translated)
    translated = re.sub(r"\bmay\b", "có thể", translated)
    translated = re.sub(r"\bcan\b", "có thể", translated)
    translated = re.sub(r"\bwill\b", "sẽ", translated)
    translated = re.sub(r"\buser\b", "người dùng chiêu", translated)
    translated = re.sub(r"\btarget\b", "mục tiêu", translated)
    translated = re.sub(r"\bturns\b", "lượt", translated)
    translated = re.sub(r"\bturn\b", "lượt", translated)
    translated = re.sub(r"\bused\b", "được dùng", translated)
    translated = re.sub(r"\busing\b", "dùng", translated)
    translated = re.sub(r"\bprevents\b", "ngăn", translated)
    translated = re.sub(r"\bboosts\b", "tăng", translated)
    translated = re.sub(r"\braises\b", "tăng", translated)
    translated = re.sub(r"\brestores\b", "hồi", translated)

    translated = translated.replace("  ", " ")
    translated = translated.replace(" .", ".")
    return translated.strip()


def get_item_type_label(category_name: str) -> str:
    return ITEM_TYPE_LABELS.get(category_name, display_item_name(category_name))


def get_special_item_effect_text(item_name: str, category_name: str) -> str | None:
    if category_name == "nature-mints" and item_name.endswith("-mint"):
        nature_name = item_name[:-len("-mint")]
        stat_pair = MINT_STAT_LABELS.get(nature_name)
        if stat_pair:
            increased_stat, lowered_stat = stat_pair
            return (
                f"Khi dùng mint này, Pokémon sẽ dễ tăng {increased_stat} hơn, "
                f"nhưng {lowered_stat} sẽ tăng chậm hơn."
            )

    special_effects = {
        "air-balloon": (
            "Pokémon cầm nó sẽ miễn nhiễm với đòn hệ Ground cho đến khi bị trúng đòn."
        ),
        "leftovers": (
            "Mỗi lượt, Pokémon cầm nó sẽ hồi một lượng HP nhỏ."
        ),
        "choice-band": (
            "Tăng mạnh Tấn Công, nhưng chỉ được dùng một chiêu cho đến khi rút ra."
        ),
        "choice-specs": (
            "Tăng mạnh Tấn Công Đặc Biệt, nhưng chỉ được dùng một chiêu cho đến khi rút ra."
        ),
        "choice-scarf": (
            "Tăng Tốc Độ, nhưng chỉ được dùng một chiêu cho đến khi rút ra."
        ),
        "focus-sash": (
            "Nếu đang đủ HP và bị hạ trong một đòn, Pokémon sẽ còn lại 1 HP."
        ),
        "life-orb": (
            "Tăng sát thương của đòn tấn công, đổi lại Pokémon sẽ mất một ít HP sau mỗi lần ra chiêu."
        ),
        "heavy-duty-boots": (
            "Giúp Pokémon không bị ảnh hưởng bởi hazard khi vào sân."
        ),
        "rocky-helmet": (
            "Đối thủ dùng đòn tiếp xúc vào Pokémon cầm nó sẽ bị mất máu."
        ),
        "assault-vest": (
            "Tăng Phòng Thủ Đặc Biệt, nhưng không thể dùng các chiêu không gây sát thương."
        ),
        "eviolite": (
            "Tăng Phòng Thủ và Phòng Thủ Đặc Biệt cho Pokémon vẫn còn có thể tiến hóa."
        ),
        "light-clay": (
            "Kéo dài thời gian tồn tại của Reflect và Light Screen."
        ),
        "weakness-policy": (
            "Khi bị đòn siêu hiệu quả đánh trúng, Tấn Công và Tấn Công Đặc Biệt sẽ tăng mạnh."
        ),
        "booster-energy": (
            "Kích hoạt khả năng Protosynthesis hoặc Quark Drive của Paradox Pokémon."
        ),
    }
    return special_effects.get(item_name)


def get_item_effect_text(item_data: dict) -> str:
    item_name = item_data.get("name", "")
    category_name = item_data.get("category", {}).get("name", "")

    special_effect = get_special_item_effect_text(item_name, category_name)
    if special_effect:
        return special_effect

    effect_entries = item_data.get("effect_entries", [])
    english_entry = next(
        (
            entry for entry in effect_entries
            if entry.get("language", {}).get("name") == "en"
        ),
        None,
    )
    short_effect = ""
    if english_entry:
        short_effect = english_entry.get("short_effect") or english_entry.get("effect") or ""

    if not short_effect:
        flavor_entries = item_data.get("flavor_text_entries", [])
        english_flavor = next(
            (
                entry for entry in flavor_entries
                if entry.get("language", {}).get("name") == "en"
            ),
            None,
        )
        if english_flavor:
            short_effect = english_flavor.get("text", "")

    short_effect = short_effect.replace("\n", " ").replace("\f", " ").strip()
    if not short_effect:
        return "Chưa có mô tả hiệu ứng rõ ràng trong PokeAPI."

    translated = translate_item_effect(short_effect)
    return re.sub(r"\s+", " ", translated).strip()


def get_item_usage_hint(item_data: dict) -> ItemUsageHint:
    item_name = item_data["name"]
    if item_name in ITEM_USAGE_HINTS:
        return ITEM_USAGE_HINTS[item_name]

    attributes = {entry["name"] for entry in item_data.get("attributes", [])}
    category_name = item_data.get("category", {}).get("name", "")

    if "holdable" in attributes:
        return {
            "can_be_used_by": "Hầu hết Pokémon có thể cầm, nhưng chỉ hợp nếu build cần hiệu ứng này.",
            "good_on": [],
        }
    if category_name == "medicine":
        return {
            "can_be_used_by": "Dùng trực tiếp từ túi đồ, không phải held item.",
            "good_on": [],
        }
    if category_name == "evolution":
        return {
            "can_be_used_by": "Chỉ dùng cho các Pokémon có liên quan đến tiến hóa bằng item này.",
            "good_on": [],
        }
    return {
        "can_be_used_by": "Tùy item; không phải item nào cũng dùng theo kiểu held item.",
        "good_on": [],
    }


def search_item_names(names: list[str], query: str, limit: int = 10) -> list[str]:
    normalized_query = query.strip().lower().replace(" ", "-").replace(".", "")
    compact_query = normalized_query.replace("-", "")

    starts_with: list[str] = []
    contains: list[str] = []

    for item_name in names:
        compact_name = item_name.replace("-", "")
        if item_name.startswith(normalized_query) or compact_name.startswith(compact_query):
            starts_with.append(item_name)
        elif normalized_query in item_name or compact_query in compact_name:
            contains.append(item_name)

    return (starts_with + contains)[:limit]


def build_item_lines(details: ItemDetails) -> list[str]:
    good_on_text = "Chưa có gợi ý cụ thể cho item này."
    if details.good_on:
        good_on_text = "; ".join(
            f"{entry['pokemon'].replace('-', ' ').title()} ({entry['reason']})"
            for entry in details.good_on[:3]
        )

    return [
        f"Item: **{details.display_name}**",
        f"Loại: {details.type}",
        f"Công dụng: {details.effect}",
        f"Dùng cho: {details.can_be_used_by}",
        f"Hợp với: {good_on_text}",
    ]
