import asyncio
import os
import re
import traceback

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

from data import (
    FOSSIL_POKEMON,
    LABEL_PRIORITY,
    PARADOX_POKEMON,
    PSEUDO_LEGENDARY_POKEMON,
    REGIONAL_FORM_MARKERS,
    REMINDER_MINUTES,
    STARTER_POKEMON,
    SUB_LEGENDARY_POKEMON,
    ULTRA_BEAST_POKEMON,
)
from item_logic import (
    build_item_lines,
    display_item_name,
    get_item_effect_text,
    get_item_type_label,
    get_item_usage_hint,
    search_item_names,
)
from models import ItemDetails, PokemonDetails

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
DEBUG_SPAWN = os.getenv("DEBUG_SPAWN", "false").lower() == "true"
DEBUG_EVENTS = os.getenv("DEBUG_EVENTS", "false").lower() == "true"
POKECORD_AUTHOR_ID = os.getenv("POKECORD_AUTHOR_ID", "").strip()
DISCORD_GUILD_ID = os.getenv("DISCORD_GUILD_ID", "").strip()

if not TOKEN:
    raise ValueError("Chưa tìm thấy DISCORD_TOKEN trong file .env")


class PokemonNotiBot(commands.Bot):
    async def close(self):
        global http_session
        if http_session and not http_session.closed:
            await http_session.close()
        await super().close()


intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.messages = True

bot = PokemonNotiBot(command_prefix="!", intents=intents)
http_session: aiohttp.ClientSession | None = None
pokemon_cache: dict[str, PokemonDetails] = {}
item_cache: dict[str, ItemDetails] = {}
item_name_cache: list[str] = []
processed_spawn_signatures: dict[int, tuple[str, ...]] = {}
pending_spawn_signatures: dict[int, tuple[str, ...]] = {}
spawn_eval_tasks: dict[int, asyncio.Task] = {}
reminder_tasks: dict[tuple[int, int, str], asyncio.Task] = {}

SPAWN_TITLE_PATTERN = re.compile(r"a wild\s+(.+?)\s+appeared", re.IGNORECASE)
NUMBERED_OPTION_PATTERN = re.compile(r"^\s*\d+\.\s+[A-Za-z0-9][A-Za-z0-9\- ':.]*$")


def normalize_name(name: str) -> str:
    value = name.strip().lower()
    value = value.replace("â€™", "'")
    value = re.sub(r"^\d+\.\s*", "", value)
    value = re.sub(r"\s+", "-", value)
    value = value.replace(".", "")
    return value


def display_name(name: str) -> str:
    return name.replace("-", " ").title()


def get_species_lookup_candidates(name: str) -> list[str]:
    candidates = [name]

    for marker in REGIONAL_FORM_MARKERS:
        if name.endswith(marker):
            candidates.append(name[: -len(marker)])

    if name.startswith("mega-"):
        candidates.append(name[len("mega-"):])
    if name.endswith("-mega"):
        candidates.append(name[:-len("-mega")])
    if name.endswith("-gmax"):
        candidates.append(name[:-len("-gmax")])

    unique_candidates: list[str] = []
    for candidate in candidates:
        if candidate and candidate not in unique_candidates:
            unique_candidates.append(candidate)
    return unique_candidates


def classify_pokemon(details: PokemonDetails) -> list[str]:
    name = details.name
    labels: set[str] = set()

    if details.is_baby:
        labels.add("Baby")
    if details.is_mythical:
        labels.add("Mythical")
    elif details.is_legendary:
        labels.add("Legendary")
    if name in SUB_LEGENDARY_POKEMON:
        labels.add("Legendary Trio/Sub-Legendary")
    if name in ULTRA_BEAST_POKEMON:
        labels.add("Ultra Beast")
    if name in PARADOX_POKEMON:
        labels.add("Paradox")
    if name in FOSSIL_POKEMON:
        labels.add("Fossil")
    if name in PSEUDO_LEGENDARY_POKEMON:
        labels.add("Pseudo-Legendary")
    if name in STARTER_POKEMON:
        labels.add("Starter")
    if any(marker in name for marker in REGIONAL_FORM_MARKERS):
        labels.add("Regional Form")
    if name.startswith("mega-") or "-mega" in name:
        labels.add("Mega")

    if not labels:
        labels.add("Thường")

    return sorted(labels, key=lambda label: (LABEL_PRIORITY.get(label, 50), label))


def is_spawn_embed(message: discord.Message) -> bool:
    for embed in message.embeds:
        title = (embed.title or "").lower()
        description = (embed.description or "").lower()
        if "hangmon" in title or "viewing pokemon" in title:
            continue
        if title.startswith("pokemon spawn"):
            return True
        if SPAWN_TITLE_PATTERN.search(title) or SPAWN_TITLE_PATTERN.search(description):
            return True
    return False


def is_hangmon_embed(message: discord.Message) -> bool:
    for embed in message.embeds:
        title = (embed.title or "").lower()
        description = (embed.description or "").lower()
        if "hangmon" in title or "hangmon" in description:
            return True
    return False


def is_spawn_message(message: discord.Message) -> bool:
    return not is_hangmon_embed(message) and is_spawn_embed(message) and bool(
        extract_numbered_pokemon_option_labels(message)
    )


def extract_select_option_labels(message: discord.Message) -> list[str]:
    labels: list[str] = []

    for component in message.components:
        options = getattr(component, "options", None)
        if options:
            for option in options:
                label = getattr(option, "label", None)
                if label:
                    labels.append(str(label))

        children = getattr(component, "children", None)
        if children:
            for child in children:
                child_options = getattr(child, "options", None)
                if child_options:
                    for option in child_options:
                        label = getattr(option, "label", None)
                        if label:
                            labels.append(str(label))

    return labels


def extract_numbered_pokemon_option_labels(message: discord.Message) -> list[str]:
    numbered_labels: list[tuple[int, str]] = []

    for label in extract_select_option_labels(message):
        if not NUMBERED_OPTION_PATTERN.match(label):
            continue

        match = re.match(r"^\s*(\d+)\.\s+(.+?)\s*$", label)
        if not match:
            continue

        numbered_labels.append((int(match.group(1)), match.group(2)))

    numbered_labels.sort(key=lambda item: item[0])
    return [label for _, label in numbered_labels]


def extract_spawn_candidates(message: discord.Message) -> list[str]:
    numbered_labels = extract_numbered_pokemon_option_labels(message)
    if len(numbered_labels) < 5:
        return []
    return [normalize_name(label) for label in numbered_labels[:5]]


async def get_json(url: str, *, suppress_not_found: bool = False):
    global http_session
    if http_session is None or http_session.closed:
        http_session = aiohttp.ClientSession()

    try:
        async with http_session.get(url) as response:
            if response.status == 404 and suppress_not_found:
                return None
            if response.status != 200:
                print(f"HTTP {response.status} when fetching {url}")
                return None
            return await response.json()
    except Exception as exc:
        print(f"Request error for {url}: {exc}")
        traceback.print_exc()
        return None


async def get_pokemon_details(name: str) -> PokemonDetails | None:
    normalized = normalize_name(name)
    if normalized in pokemon_cache:
        return pokemon_cache[normalized]

    pokemon = await get_json(f"https://pokeapi.co/api/v2/pokemon/{normalized}")
    species = None
    for species_name in get_species_lookup_candidates(normalized):
        species = await get_json(
            f"https://pokeapi.co/api/v2/pokemon-species/{species_name}",
            suppress_not_found=True,
        )
        if species:
            break

    if species and not pokemon:
        default_variety = next(
            (variety for variety in species.get("varieties", []) if variety.get("is_default")),
            None,
        )
        if default_variety:
            variety_name = default_variety.get("pokemon", {}).get("name")
            if variety_name:
                pokemon = await get_json(f"https://pokeapi.co/api/v2/pokemon/{variety_name}")

    if not species or not pokemon:
        return None

    details = PokemonDetails(
        name=normalized,
        total_stats=sum(stat["base_stat"] for stat in pokemon.get("stats", [])),
        is_baby=bool(species.get("is_baby")),
        is_legendary=bool(species.get("is_legendary")),
        is_mythical=bool(species.get("is_mythical")),
        types=[entry["type"]["name"] for entry in pokemon.get("types", [])],
        base_experience=pokemon.get("base_experience"),
        height=pokemon.get("height"),
        weight=pokemon.get("weight"),
    )
    pokemon_cache[normalized] = details
    return details


async def get_item_name_choices() -> list[str]:
    global item_name_cache
    if item_name_cache:
        return item_name_cache

    item_list = await get_json("https://pokeapi.co/api/v2/item?limit=2500")
    if not item_list:
        return []

    item_name_cache = sorted(
        {
            entry["name"]
            for entry in item_list.get("results", [])
            if entry.get("name")
        }
    )
    return item_name_cache


async def get_item_details(name: str) -> ItemDetails | None:
    normalized = normalize_name(name)
    if normalized in item_cache:
        return item_cache[normalized]

    item_data = await get_json(
        f"https://pokeapi.co/api/v2/item/{normalized}",
        suppress_not_found=True,
    )
    if not item_data:
        return None

    category_name = item_data.get("category", {}).get("name", "other")
    usage_hint = get_item_usage_hint(item_data)
    details = ItemDetails(
        name=normalized,
        display_name=display_item_name(item_data.get("name", normalized)),
        item=normalized,
        type=get_item_type_label(category_name),
        effect=get_item_effect_text(item_data),
        can_be_used_by=usage_hint["can_be_used_by"],
        good_on=usage_hint["good_on"],
    )
    item_cache[normalized] = details
    return details


async def autocomplete_item_name(
    interaction: discord.Interaction,
    current: str,
) -> list[app_commands.Choice[str]]:
    del interaction

    names = await get_item_name_choices()
    if not names:
        return []

    matches = names[:25] if not current.strip() else search_item_names(names, current, limit=25)
    return [
        app_commands.Choice(name=display_item_name(item_name), value=item_name)
        for item_name in matches
    ]


def build_spawn_line(index: int, details: PokemonDetails) -> str:
    classification = " | ".join(classify_pokemon(details))
    return f"{index}. **{display_name(details.name)}** - BST {details.total_stats} | {classification}"


def build_checkpokemon_lines(details: PokemonDetails) -> list[str]:
    return [
        f"Pokemon: **{display_name(details.name)}**",
        f"Phân loại: {' | '.join(classify_pokemon(details))}",
        f"BST: {details.total_stats}",
        f"Types: {', '.join(type_name.title() for type_name in details.types) or 'Unknown'}",
        f"Base EXP: {details.base_experience}",
        f"Height: {details.height}",
        f"Weight: {details.weight}",
    ]


async def safe_send(channel: discord.abc.Messageable, content: str, **kwargs) -> bool:
    try:
        await channel.send(content, **kwargs)
        return True
    except Exception as exc:
        print(f"Send message error: {exc}")
        traceback.print_exc()
        return False


class SpawnReportView(discord.ui.View):
    def __init__(self, report_text: str):
        super().__init__(timeout=600)
        self.report_text = report_text

    @discord.ui.button(
        label="Xem phân tích",
        style=discord.ButtonStyle.secondary,
        emoji="📊",
    )
    async def show_report(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ):
        del button
        await interaction.response.send_message(self.report_text, ephemeral=True)


def log_message_structure(message: discord.Message):
    print("\n========== SPAWN DEBUG ==========")
    print(f"message_id: {message.id}")
    print(f"author: {message.author} ({message.author.id})")
    print(f"channel_id: {message.channel.id}")
    print(f"content: {message.content!r}")
    print(f"embeds: {len(message.embeds)}")

    for embed_index, embed in enumerate(message.embeds, start=1):
        print(f"[embed {embed_index}] title: {embed.title!r}")
        print(f"[embed {embed_index}] description: {embed.description!r}")
        for field_index, field in enumerate(embed.fields, start=1):
            print(f"[embed {embed_index}][field {field_index}] name: {field.name!r}")
            print(f"[embed {embed_index}][field {field_index}] value: {field.value!r}")

    print(f"components: {len(message.components)}")
    for row_index, component in enumerate(message.components, start=1):
        print(f"[component {row_index}] type: {type(component).__name__}")
        options = getattr(component, "options", None)
        if options:
            for option_index, option in enumerate(options, start=1):
                print(
                    f"[component {row_index}][option {option_index}] "
                    f"label={getattr(option, 'label', None)!r} "
                    f"value={getattr(option, 'value', None)!r} "
                    f"default={getattr(option, 'default', None)!r}"
                )

    print(f"parsed_candidates: {extract_spawn_candidates(message)}")
    print("=================================\n")


def log_event_summary(message: discord.Message, source: str):
    if not DEBUG_EVENTS:
        return
    if not message.embeds and not message.components:
        return

    print(
        f"[{source}] message_id={message.id} author={message.author} "
        f"author_id={message.author.id} embeds={len(message.embeds)} "
        f"components={len(message.components)} content={message.content!r}"
    )


def detect_reminder_type(content: str) -> str | None:
    lowered = (content or "").lower()
    if re.search(r"(?<!\w)(?:[/!.\-]?\w+)?hangmon(?!\w)", lowered):
        return "hangmon"
    if re.search(r"(?<!\w)(?:[/!.\-]?\w+)?spawn(?!\w)", lowered):
        return "spawn"
    return None


async def schedule_reminder(message: discord.Message, reminder_type: str):
    delay_seconds = REMINDER_MINUTES[reminder_type] * 60
    key = (message.channel.id, message.author.id, reminder_type)

    existing_task = reminder_tasks.get(key)
    if existing_task and not existing_task.done():
        existing_task.cancel()

    async def reminder_worker():
        try:
            await asyncio.sleep(delay_seconds)
            await safe_send(
                message.channel,
                f"{message.author.mention} đến giờ `{reminder_type}` rồi.",
            )
        except asyncio.CancelledError:
            return
        finally:
            current_task = reminder_tasks.get(key)
            if current_task is asyncio.current_task():
                reminder_tasks.pop(key, None)

    reminder_tasks[key] = asyncio.create_task(reminder_worker())


async def fetch_latest_message_state(message: discord.Message) -> discord.Message | None:
    try:
        channel = message.channel
        if isinstance(channel, discord.TextChannel | discord.Thread):
            return await channel.fetch_message(message.id)
    except Exception:
        return None
    return None


async def handle_spawn_report(message: discord.Message):
    try:
        if not is_spawn_message(message):
            return

        if DEBUG_SPAWN:
            log_message_structure(message)

        candidates = extract_spawn_candidates(message)
        if len(candidates) < 5:
            return

        signature = tuple(candidates)
        if processed_spawn_signatures.get(message.id) == signature:
            return
        if pending_spawn_signatures.get(message.id) == signature:
            return

        pending_spawn_signatures[message.id] = signature

        lines: list[str] = []
        for index, candidate in enumerate(candidates, start=1):
            details = await get_pokemon_details(candidate)
            if not details:
                continue
            lines.append(build_spawn_line(index, details))

        if len(lines) < 5:
            return

        latest_message = await fetch_latest_message_state(message)
        if latest_message is not None and is_hangmon_embed(latest_message):
            return

        processed_spawn_signatures[message.id] = signature
        await safe_send(
            message.channel,
            "Nhấn nút để xem BST spawn.",
            view=SpawnReportView("Bảng BST các lựa chọn spawn:\n" + "\n".join(lines)),
        )
    except Exception as exc:
        print(f"Spawn report error: {exc}")
        traceback.print_exc()
    finally:
        pending_spawn_signatures.pop(message.id, None)


async def schedule_spawn_evaluation(message: discord.Message):
    if not is_spawn_embed(message):
        return

    existing_task = spawn_eval_tasks.get(message.id)
    if existing_task and not existing_task.done():
        existing_task.cancel()

    async def worker():
        try:
            await asyncio.sleep(0.35)
            latest_message = await fetch_latest_message_state(message)
            if latest_message is None:
                await handle_spawn_report(message)
                return
            await handle_spawn_report(latest_message)
        except asyncio.CancelledError:
            return
        except Exception as exc:
            print(f"Spawn evaluation error: {exc}")
            traceback.print_exc()
        finally:
            current_task = spawn_eval_tasks.get(message.id)
            if current_task is asyncio.current_task():
                spawn_eval_tasks.pop(message.id, None)

    spawn_eval_tasks[message.id] = asyncio.create_task(worker())


async def process_target_message(message: discord.Message):
    log_event_summary(message, "process")
    await schedule_spawn_evaluation(message)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        if DISCORD_GUILD_ID:
            guild = discord.Object(id=int(DISCORD_GUILD_ID))
            bot.tree.copy_global_to(guild=guild)
            synced = await bot.tree.sync(guild=guild)
            print(f"Synced {len(synced)} slash commands to guild {DISCORD_GUILD_ID}")
        else:
            synced = await bot.tree.sync()
            print(f"Synced {len(synced)} global slash commands")
        print("Slash commands:", ", ".join(command.name for command in synced))
    except Exception as exc:
        print("Slash sync error:", exc)
    if POKECORD_AUTHOR_ID:
        print(f"Tracking Pokecord author id: {POKECORD_AUTHOR_ID}")


@bot.event
async def on_message(message: discord.Message):
    log_event_summary(message, "on_message")
    await process_target_message(message)

    if not message.author.bot:
        reminder_type = detect_reminder_type(message.content)
        if reminder_type:
            await schedule_reminder(message, reminder_type)


@bot.event
async def on_message_edit(before: discord.Message, after: discord.Message):
    del before
    log_event_summary(after, "on_message_edit")
    await process_target_message(after)


@bot.event
async def on_raw_message_edit(payload: discord.RawMessageUpdateEvent):
    channel_id = payload.data.get("channel_id")
    message_id = payload.data.get("id")
    if not channel_id or not message_id:
        return

    channel = bot.get_channel(int(channel_id))
    if channel is None:
        try:
            channel = await bot.fetch_channel(int(channel_id))
        except Exception:
            return

    if not isinstance(channel, discord.TextChannel | discord.Thread):
        return

    try:
        message = await channel.fetch_message(int(message_id))
    except Exception:
        return

    log_event_summary(message, "on_raw_message_edit")
    await process_target_message(message)


@bot.tree.command(
    name="check",
    description="Xem thông tin Pokemon và phân loại",
)
@app_commands.describe(name="Tên Pokemon cần kiểm tra")
async def check(interaction: discord.Interaction, name: str):
    details = await get_pokemon_details(name)
    if details is None:
        await interaction.response.send_message(
            f"Không tìm thấy dữ liệu cho '{name}'."
        )
        return

    await interaction.response.send_message("\n".join(build_checkpokemon_lines(details)))


@bot.tree.command(
    name="item",
    description="Xem item dùng để làm gì và hợp với Pokemon nào",
)
@app_commands.describe(name="Tên item cần kiểm tra")
@app_commands.autocomplete(name=autocomplete_item_name)
async def item(interaction: discord.Interaction, name: str):
    item_names = await get_item_name_choices()
    normalized = normalize_name(name)
    if item_names and normalized not in set(item_names):
        suggestions = search_item_names(item_names, name)
        if suggestions:
            suggestion_text = ", ".join(display_item_name(item_name) for item_name in suggestions[:8])
            await interaction.response.send_message(
                f"Không có item chính xác cho '{name}'. Gợi ý: {suggestion_text}"
            )
            return

    details = await get_item_details(name)
    if details is None:
        await interaction.response.send_message(
            f"Không tìm thấy dữ liệu item cho '{name}'."
        )
        return

    await interaction.response.send_message("\n".join(build_item_lines(details)))


bot.run(TOKEN)
