# -*- coding: utf-8 -*-
"""Localization-expansion batch (2026-06): 7 new locales for live videos + channel.

Single source of truth for the es / pt / zh-Hant / zh-Hans / ru / de / fr expansion.
- `python Analytics/localize_batch.py gate`   → 검토용 표 (제목 · 큐레이터 보이스 · 작곡가/곡명)
- `python Analytics/localize_batch.py write`  → 각 work video/release/ 에 description.<lang>.txt 생성 + titles.<lang> 출력
- `python Analytics/localize_batch.py channel` → 채널 description sidecar (Analytics/_channel_l10n/) 생성

정책 (JA/KO 선례 정합):
- 네이티브 스크립트로 완전 현지화 (작곡가명 키릴/중국어 음역, 곡명 시장 canonical).
- 화가명: ru/zh 음역, latin 4종은 라틴 유지. **명화 제목은 영어 원제 유지** (검증 가능성 보수 선택).
- "The Entertainer" = 고유 영문 제목 유지 (음역 X). 독일어 Köchel = KV (K. 아님).
- title badge "【初音ミク A Cappella】" = 전 로케일 불변 (브랜드 · s402 · 긴 곡 = 【A Cappella】 fallback).
"""
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE = Path(__file__).resolve().parent.parent
LANGS = ["es", "pt", "de", "fr", "ru", "zh-Hant", "zh-Hans"]
CHANNEL_CODE = {"es": "es_ES", "pt": "pt_BR", "de": "de_DE", "fr": "fr_FR",
                "ru": "ru_RU", "zh-Hant": "zh_TW", "zh-Hans": "zh_CN"}
SUFFIX = " (feat. 初音ミク)"          # legacy (pre-s402) — kept for reference
BADGE = " 【初音ミク A Cappella】"       # s402 title badge (코튼 2026-06-06 LOCK · title_naming_guide)
BADGE_ABBR = " 【A Cappella】"          # long-title fallback (per-work "badge_abbrev": True · e.g. Mozart K.265)
CC = "CC BY-NC 3.0 https://creativecommons.org/licenses/by-nc/3.0/"

# ── shared localized tokens ────────────────────────────────────────────────
MIKU = {"es": "Hatsune Miku", "pt": "Hatsune Miku", "de": "Hatsune Miku", "fr": "Hatsune Miku",
        "ru": "Хацунэ Мику", "zh-Hant": "初音未來", "zh-Hans": "初音未来"}
PROD = {"es": "Herramienta de producción", "pt": "Ferramenta de produção",
        "de": "Produktionswerkzeug", "fr": "Outil de production",
        "ru": "Программа", "zh-Hant": "製作工具", "zh-Hans": "制作工具"}
VOICE = {"es": "Banco de voz", "pt": "Banco de voz", "de": "Stimmbank", "fr": "Banque vocale",
         "ru": "Голосовой банк", "zh-Hant": "聲庫", "zh-Hans": "声库"}
CHAPTERS_LBL = {"es": "Capítulos:", "pt": "Capítulos:", "de": "Kapitel:", "fr": "Chapitres :",
                "ru": "Главы:", "zh-Hant": "章節：", "zh-Hans": "章节："}

def sing(lang, n):
    """'{N} Mikus sing it now' — 목적어 생략으로 성(性) 일치 함정 회피."""
    word = NUM[lang][n]
    return {
        "es": f"Ahora cantan {word} Mikus",
        "pt": f"Agora cantam {word} Mikus",
        "de": f"Jetzt singen {word} Mikus",
        "fr": f"À présent, {word} Mikus chantent",
        "ru": f"Теперь поют {word} Мику",
        "zh-Hant": f"如今由{word}位初音未來獻唱",
        "zh-Hans": f"如今由{word}位初音未来献唱",
    }[lang]

NUM = {
    "es": {6: "seis", 7: "siete", 9: "nueve", 11: "once"},
    "pt": {6: "seis", 7: "sete", 9: "nove", 11: "onze"},
    "de": {6: "sechs", 7: "sieben", 9: "neun", 11: "elf"},
    "fr": {6: "six", 7: "sept", 9: "neuf", 11: "onze"},
    "ru": {6: "шесть", 7: "семь", 9: "девять", 11: "одиннадцать"},
    "zh-Hant": {6: "六", 7: "七", 9: "九", 11: "十一"},
    "zh-Hans": {6: "六", 7: "七", 9: "九", 11: "十一"},
}

WELCOME = {  # Satie 전용 (구작 Welcome 블록)
    "es": "¡Te damos la bienvenida a Atelier Miku A Cappella!\n\nEste es un proyecto de fans: música clásica, arreglada para la voz de Hatsune Miku, una pieza a la vez.\nEspero que encuentres algo que amar aquí ♪",
    "pt": "Boas-vindas ao Atelier Miku A Cappella!\n\nEste é um projeto de fãs: música clássica, arranjada para a voz da Hatsune Miku, uma peça de cada vez.\nEspero que você encontre algo para amar por aqui ♪",
    "de": "Willkommen im Atelier Miku A Cappella!\n\nDies ist ein Fanprojekt: klassische Musik, arrangiert für Hatsune Mikus Stimme, ein Stück nach dem anderen.\nIch hoffe, du findest hier etwas, das du liebgewinnst ♪",
    "fr": "Bienvenue à l'Atelier Miku A Cappella !\n\nCeci est un projet de fans : de la musique classique, arrangée pour la voix de Hatsune Miku, une pièce à la fois.\nJ'espère que vous trouverez ici quelque chose à aimer ♪",
    "ru": "Добро пожаловать в Atelier Miku A Cappella!\n\nЭто фанатский проект: классическая музыка в аранжировке для голоса Хацунэ Мику, по одной пьесе за раз.\nНадеюсь, вы найдёте здесь что-то, что полюбите ♪",
    "zh-Hant": "歡迎來到 Atelier Miku A Cappella！\n\n這是一個同人企劃：將古典名曲改編給初音未來的歌聲，一次一首，細細打磨。\n願你在這裡遇見值得珍愛的一曲 ♪",
    "zh-Hans": "欢迎来到 Atelier Miku A Cappella！\n\n这是一个同人企划：将古典名曲改编给初音未来的歌声，一次一首，细细打磨。\n愿你在这里遇见值得珍爱的一曲 ♪",
}
SUBSCRIBE = {  # Satie/Vivaldi/Joplin (구작 CTA 유지)
    "es": "¡Suscríbete para unirte al Atelier y descubrir un nuevo lado de la música clásica!",
    "pt": "Inscreva-se para entrar no Atelier e descobrir um novo lado da música clássica!",
    "de": "Abonniere, um dem Atelier beizutreten und eine neue Seite der klassischen Musik zu entdecken!",
    "fr": "Abonnez-vous pour rejoindre l'Atelier et découvrir un nouveau visage de la musique classique !",
    "ru": "Подпишитесь, чтобы присоединиться к Ателье и открыть для себя новую сторону классической музыки!",
    "zh-Hant": "訂閱以加入這間工坊，一同發現古典音樂的另一種面貌！",
    "zh-Hans": "订阅以加入这间工坊，一同发现古典音乐的另一种面貌！",
}

def cover_line(lang, painter, painting, year):
    return {
        "es": f"Portada, a partir de {painter}, '{painting}' ({year}).",
        "pt": f"Capa, a partir de {painter}, '{painting}' ({year}).",
        "de": f"Coverbild, nach {painter}, „{painting}“ ({year}).",
        "fr": f"Illustration, d'après {painter}, « {painting} » ({year}).",
        "ru": f"Обложка по картине {painter} «{painting}» ({year}).",
        "zh-Hant": f"封面取材自{painter}的畫作〈{painting}〉（{year}）。",
        "zh-Hans": f"封面取材自{painter}的画作〈{painting}〉（{year}）。",
    }[lang]

def date_for(lang, year):
    """Locale-aware circa notation, with shortened ranges expanded for clarity."""
    if year.startswith("c."):
        base = year[2:].strip()
        base = base.replace("1680–90", "1680–1690").replace("1670–72", "1670–1672")
        prefix = {
            "es": "c. ", "pt": "c. ", "de": "ca. ", "fr": "v. ",
            "ru": "ок. ", "zh-Hant": "約 ", "zh-Hans": "约 ",
        }[lang]
        return prefix + base
    return year

def year_parens(lang, year):
    y = date_for(lang, year)
    if lang.startswith("zh-"):
        return f"（{y}）"
    return f"({y})"

def label_colon(lang):
    if lang == "fr":
        return " : "
    if lang.startswith("zh-"):
        return "："
    return ": "

PAINTER = {
    "Whistler": {"ru": "Уистлера", "zh-Hant": "惠斯勒", "zh-Hans": "惠斯勒"},
    "Botticelli": {"ru": "Боттичелли", "zh-Hant": "波提切利", "zh-Hans": "波提切利"},
    "Glackens": {"ru": "Глакенса", "zh-Hant": "格拉肯斯", "zh-Hans": "格拉肯斯"},
    "Waterhouse": {"ru": "Уотерхауса", "zh-Hant": "沃特豪斯", "zh-Hans": "沃特豪斯"},
    "van Gogh": {"ru": "Ван Гога", "zh-Hant": "梵谷", "zh-Hans": "梵高"},
    "Vermeer": {"ru": "Вермеера", "zh-Hant": "維米爾", "zh-Hans": "维米尔"},
    "Renoir": {"ru": "Ренуара", "zh-Hant": "雷諾瓦", "zh-Hans": "雷诺阿"},
}
def painter_name(lang, en):
    return PAINTER.get(en, {}).get(lang, en)

# ── Mozart chapter labels ──────────────────────────────────────────────────
CH_THEME = {"es": "Tema", "pt": "Tema", "de": "Thema", "fr": "Thème", "ru": "Тема",
            "zh-Hant": "主題", "zh-Hans": "主题"}
CH_VAR = {"es": "Var.", "pt": "Var.", "de": "Var.", "fr": "Var.", "ru": "Вар.",
          "zh-Hant": "變奏", "zh-Hans": "变奏"}
# 12 descriptor sets (idx 1..12). Italian tempo/dynamic terms kept universal.
CH_DESC = {
    1: {"es": "Figuración mano derecha", "pt": "Figuração mão direita", "de": "Figuration rechte Hand", "fr": "Figuration main droite", "ru": "Фигурация правой руки", "zh-Hant": "右手音型", "zh-Hans": "右手音型"},
    2: {"es": "Figuración mano izquierda", "pt": "Figuração mão esquerda", "de": "Figuration linke Hand", "fr": "Figuration main gauche", "ru": "Фигурация левой руки", "zh-Hant": "左手音型", "zh-Hans": "左手音型"},
    3: {"es": "Arpegios en tresillos", "pt": "Arpejos em tercinas", "de": "Triolen-Arpeggien", "fr": "Arpèges en triolets", "ru": "Триольные арпеджио", "zh-Hant": "三連音琶音", "zh-Hans": "三连音琶音"},
    4: {"es": "Tresillos mano izquierda", "pt": "Tercinas mão esquerda", "de": "Triolen linke Hand", "fr": "Triolets main gauche", "ru": "Триоли левой руки", "zh-Hant": "左手三連音", "zh-Hans": "左手三连音"},
    5: {"es": "Síncopa", "pt": "Síncope", "de": "Synkopen", "fr": "Syncope", "ru": "Синкопа", "zh-Hant": "切分音", "zh-Hans": "切分音"},
    6: {"es": "Ambas manos activas", "pt": "Ambas as mãos ativas", "de": "Beide Hände aktiv", "fr": "Les deux mains actives", "ru": "Обе руки активны", "zh-Hant": "雙手齊奏", "zh-Hans": "双手齐奏"},
    7: {"es": "Escalas rápidas", "pt": "Escalas rápidas", "de": "Schnelle Tonleitern", "fr": "Gammes rapides", "ru": "Быстрые гаммы", "zh-Hant": "快速音階", "zh-Hans": "快速音阶"},
    8: {"es": "Do menor · imitación", "pt": "Dó menor · imitação", "de": "c-Moll · Imitation", "fr": "Ut mineur · imitation", "ru": "До минор · имитация", "zh-Hant": "c小調·模仿", "zh-Hans": "c小调·模仿"},
    9: {"es": "Staccato ligero · dolce", "pt": "Staccato leve · dolce", "de": "Leichtes Staccato · dolce", "fr": "Staccato léger · dolce", "ru": "Лёгкое staccato · dolce", "zh-Hant": "輕巧斷奏·dolce", "zh-Hans": "轻巧断奏·dolce"},
    10: {"es": "Cruce de manos", "pt": "Cruzamento de mãos", "de": "Handkreuzung", "fr": "Croisement de mains", "ru": "Перекрещивание рук", "zh-Hant": "交叉手", "zh-Hans": "交叉手"},
    11: {"es": "Adagio · ornamentado", "pt": "Adagio · ornamentado", "de": "Adagio · verziert", "fr": "Adagio · orné", "ru": "Adagio · орнаментика", "zh-Hant": "Adagio·裝飾", "zh-Hans": "Adagio·装饰"},
    12: {"es": "Allegro · final", "pt": "Allegro · final", "de": "Allegro · Finale", "fr": "Allegro · finale", "ru": "Allegro · финал", "zh-Hant": "Allegro·終曲", "zh-Hans": "Allegro·终曲"},
}
MOZART_TIMES = ["0:00", "0:28", "0:53", "1:19", "1:44", "2:09", "2:35", "3:00", "3:25", "3:51", "4:16", "4:41", "5:09"]
MOZART_THEME_DESC = {"es": "Andante grazioso", "pt": "Andante grazioso", "de": "Andante grazioso", "fr": "Andante grazioso", "ru": "Andante grazioso", "zh-Hant": "Andante grazioso", "zh-Hans": "Andante grazioso"}

def mozart_chapters(lang):
    lines = [CHAPTERS_LBL[lang]]
    lines.append(f"{MOZART_TIMES[0]} {CH_THEME[lang]} — {MOZART_THEME_DESC[lang]}")
    for i in range(1, 13):
        lines.append(f"{MOZART_TIMES[i]} {CH_VAR[lang]} {i} — {CH_DESC[i][lang]}")
    return "\n".join(lines)

# ── per-work data ──────────────────────────────────────────────────────────
# surname/full/piece keyed by lang; latin 4종 동일하면 "_latin" 공유 키 사용.
def L(latin, ru, hant, hans):
    return {"es": latin, "pt": latin, "de": latin, "fr": latin, "ru": ru, "zh-Hant": hant, "zh-Hans": hans}

WORKS = [
    {
        "vid": "rRnl8RZ3EjY", "slug": "gymnopedie_1_first_proof", "count": 7, "year": "1888",
        "style": "welcome_inline", "welcome": True, "subscribe": True, "era": "romantic",
        "surname": L("Satie", "Сати", "薩蒂", "萨蒂"),
        "full": L("Erik Satie", "Эрик Сати", "艾瑞克·薩蒂", "埃里克·萨蒂"),
        "piece": {"es": "Gymnopédie n.º 1", "pt": "Gymnopédie n.º 1", "de": "Gymnopédie Nr. 1",
                  "fr": "Gymnopédie n° 1", "ru": "Гимнопедия № 1", "zh-Hant": "《吉諾佩第》第1號", "zh-Hans": "《吉诺佩第》第1号"},
        "painter": "Whistler", "painting": "Nocturne in Blue and Gold: Old Battersea Bridge", "p_year": "1872–75",
        "cover_url": "https://www.tate.org.uk/art/artworks/whistler-nocturne-blue-and-gold-old-battersea-bridge-n01959",
        "curator": None,
        "tag_piece": {"es": "#Gymnopedie", "pt": "#Gymnopedie", "de": "#Gymnopedie", "fr": "#Gymnopedie", "ru": "#Гимнопедия", "zh-Hant": "#吉諾佩第", "zh-Hans": "#吉诺佩第"},
    },
    {
        "vid": "0qXLYmZXAx0", "slug": "vivaldi_spring_1_allegro", "count": 6, "year": "1725",
        "style": "vivaldi", "welcome": False, "subscribe": True, "era": "baroque",
        "surname": L("Vivaldi", "Вивальди", "韋瓦第", "维瓦尔第"),
        "full": L("Antonio Vivaldi", "Антонио Вивальди", "安東尼奧·韋瓦第", "安东尼奥·维瓦尔第"),
        "piece": {"es": "La primavera, 1.er mov.", "pt": "Primavera, 1.º mov.", "de": "Der Frühling, 1. Satz",
                  "fr": "Le Printemps, 1er mouvement", "ru": "«Весна», часть I", "zh-Hant": "《春》第一樂章", "zh-Hans": "《春》第一乐章"},
        "painter": "Botticelli", "painting": "Primavera", "p_year": "c. 1482",
        "cover_url": "https://commons.wikimedia.org/wiki/File:Botticelli-primavera.jpg",
        "curator": {
            "es": "Elegida con la nostalgia de la fresca brisa de la primavera—",
            "pt": "Escolhida com a saudade da brisa fresca da primavera—",
            "de": "Gewählt aus Sehnsucht nach der kühlen Frühlingsbrise—",
            "fr": "Choisie dans le désir de la fraîche brise du printemps—",
            "ru": "Выбрана с тоской по прохладному дыханию весны—",
            "zh-Hant": "懷著對春日清風的思念而選——",
            "zh-Hans": "怀着对春日清风的思念而选——",
        },
        "tag_piece": {"es": "#LasCuatroEstaciones", "pt": "#AsQuatroEstações", "de": "#DieVierJahreszeiten", "fr": "#LesQuatreSaisons", "ru": "#ВременаГода", "zh-Hant": "#四季", "zh-Hans": "#四季"},
    },
    {
        "vid": "DVIYl09zX-w", "slug": "joplin_the_entertainer", "count": 9, "year": "1902",
        "style": "inline", "welcome": False, "subscribe": True, "era": "ragtime",
        "surname": L("Joplin", "Джоплин", "喬普林", "乔普林"),
        "full": L("Scott Joplin", "Скотт Джоплин", "史考特·喬普林", "斯科特·乔普林"),
        "piece": L("The Entertainer", "The Entertainer", "The Entertainer", "The Entertainer"),
        "painter": "Glackens", "painting": "Hammerstein's Roof Garden", "p_year": "c. 1901",
        "cover_url": "https://commons.wikimedia.org/wiki/File:Hammerstein%27s_Roof_Garden,_by_William_Glackens.jpg",
        "curator": {
            "es": "Una melodía familiar que se volvió un clásico.",
            "pt": "Uma melodia familiar que virou um clássico.",
            "de": "Eine vertraute Melodie, die zum Klassiker wurde.",
            "fr": "Une mélodie familière devenue un classique.",
            "ru": "Знакомая мелодия, ставшая классикой.",
            "zh-Hant": "一段耳熟能詳、終成經典的旋律。",
            "zh-Hans": "一段耳熟能详、终成经典的旋律。",
        },
        "tag_piece": L("#TheEntertainer", "#TheEntertainer", "#TheEntertainer", "#TheEntertainer"),
    },
    {
        "vid": "zshjmBhus2I", "slug": "elgar_salut_damour", "count": 9, "year": "1888",
        "style": "inline", "welcome": False, "subscribe": False, "era": "romantic",
        "surname": L("Elgar", "Элгар", "艾爾加", "埃尔加"),
        "full": L("Edward Elgar", "Эдуард Элгар", "愛德華·艾爾加", "爱德华·埃尔加"),
        "piece": {"es": "Salut d'Amour", "pt": "Salut d'Amour", "de": "Salut d'Amour", "fr": "Salut d'Amour",
                  "ru": "Salut d’Amour («Приветствие любви»)", "zh-Hant": "《愛的禮讚》", "zh-Hans": "《爱的礼赞》"},
        "painter": "Waterhouse", "painting": "The Soul of the Rose", "p_year": "1903",
        "cover_url": "https://commons.wikimedia.org/wiki/File:John_William_Waterhouse_-_The_Soul_of_the_Rose%2C_1903.jpg",
        "curator": {
            "es": "Un amor tierno que habita en una melodía sencilla.",
            "pt": "Um amor terno que habita numa melodia simples.",
            "de": "Eine zärtliche Liebe, die in einer schlichten Melodie wohnt.",
            "fr": "Un amour tendre niché dans une mélodie toute simple.",
            "ru": "Нежная любовь, живущая в простой мелодии.",
            "zh-Hant": "棲息於樸素旋律中的，一份溫柔的愛。",
            "zh-Hans": "栖息于朴素旋律中的，一份温柔的爱。",
        },
        "tag_piece": {"es": "#SalutDamour", "pt": "#SalutDamour", "de": "#SalutDamour", "fr": "#SalutDamour", "ru": "#ПриветствиеЛюбви", "zh-Hant": "#愛的禮讚", "zh-Hans": "#爱的礼赞"},
    },
    {
        "vid": "PiR9hy6xmGQ", "slug": "mozart_twinkle_variations_k265", "count": 9, "year": "1781–82",
        "style": "inline", "welcome": False, "subscribe": False, "era": "classical", "chapters": True,
        "surname": L("Mozart", "Моцарт", "莫札特", "莫扎特"),
        "full": L("Wolfgang Amadeus Mozart", "Вольфганг Амадей Моцарт", "沃夫岡·阿瑪迪斯·莫札特", "沃尔夫冈·阿马德乌斯·莫扎特"),
        "piece": {
            "es": "Doce variaciones sobre «Ah, vous dirai-je, maman» K. 265",
            "pt": "Doze variações sobre «Ah, vous dirai-je, maman» K. 265",
            "de": "Zwölf Variationen über „Ah, vous dirai-je, maman“ KV 265",
            "fr": "Douze Variations sur « Ah, vous dirai-je, maman » K. 265",
            "ru": "12 вариаций на тему «Ah, vous dirai-je, maman» K. 265",
            "zh-Hant": "《小星星變奏曲》K. 265",
            "zh-Hans": "《小星星变奏曲》K. 265",
        },
        "painter": "van Gogh", "painting": "Starry Night Over the Rhône", "p_year": "1888",
        "cover_url": "https://www.musee-orsay.fr/en/artworks/la-nuit-etoilee-87780",
        "curator": {
            "es": "La melodía familiar de la infancia.",
            "pt": "A melodia familiar da infância.",
            "de": "Die vertraute Melodie aus Kindertagen.",
            "fr": "La mélodie familière de l'enfance.",
            "ru": "Знакомая с детства мелодия.",
            "zh-Hant": "童年裡熟悉的那段旋律。",
            "zh-Hans": "童年里熟悉的那段旋律。",
        },
        "tag_piece": {"es": "#VariacionesTwinkle", "pt": "#VariaçõesTwinkle", "de": "#TwinkleVariationen", "fr": "#VariationsTwinkle", "ru": "#ВариацииМоцарта", "zh-Hant": "#小星星變奏曲", "zh-Hans": "#小星星变奏曲"},
    },
    {
        "vid": "9EvpHXE3D1s", "slug": "chopin_nocturne_op9_2", "count": 7, "year": "1830–32",
        "style": "lead", "welcome": False, "subscribe": False, "era": "romantic",
        "surname": L("Chopin", "Шопен", "蕭邦", "肖邦"),
        "full": L("Frédéric Chopin", "Фредерик Шопен", "弗雷德里克·蕭邦", "弗里德里克·肖邦"),
        "piece": {"es": "Nocturno op. 9 n.º 2", "pt": "Noturno op. 9 n.º 2", "de": "Nocturne op. 9 Nr. 2",
                  "fr": "Nocturne op. 9 n° 2", "ru": "Ноктюрн соч. 9 № 2", "zh-Hant": "夜曲 作品9之2", "zh-Hans": "夜曲 作品9之2"},
        "painter": "Whistler", "painting": "Nocturne: Blue and Silver — Chelsea", "p_year": "1871",
        "cover_url": "https://commons.wikimedia.org/wiki/File:James_Abbott_McNeill_Whistler_-_Nocturne-_Blue_and_Silver_-_Chelsea_-_Google_Art_Project.jpg",
        "curator": {
            "es": "Un nocturno profundo para la hora de la medianoche",
            "pt": "Um noturno profundo para a hora da meia-noite",
            "de": "Eine tiefe Nocturne für die Mitternachtsstunde",
            "fr": "Un nocturne profond pour l'heure de minuit",
            "ru": "Глубокий ноктюрн для полуночного часа",
            "zh-Hant": "獻給午夜時分的深邃夜曲",
            "zh-Hans": "献给午夜时分的深邃夜曲",
        },
        "tag_piece": {"es": "#Nocturno", "pt": "#Noturno", "de": "#Nocturne", "fr": "#Nocturne", "ru": "#Ноктюрн", "zh-Hant": "#夜曲", "zh-Hans": "#夜曲"},
    },
    {
        "vid": "B9ENEwjgAhc", "slug": "pachelbel_canon_in_d", "count": 11, "year": "c.1680–90",
        "style": "lead", "welcome": False, "subscribe": False, "era": "baroque",
        "surname": L("Pachelbel", "Пахельбель", "帕海貝爾", "帕赫贝尔"),
        "full": L("Johann Pachelbel", "Иоганн Пахельбель", "約翰·帕海貝爾", "约翰·帕赫贝尔"),
        "piece": {"es": "Canon en re mayor", "pt": "Cânone em ré maior", "de": "Kanon in D-Dur",
                  "fr": "Canon en ré majeur", "ru": "Канон в ре мажоре", "zh-Hant": "D大調卡農", "zh-Hans": "D大调卡农"},
        "painter": "Vermeer", "painting": "A Young Woman seated at a Virginal", "p_year": "c.1670–72",
        "cover_url": "https://commons.wikimedia.org/wiki/File:Jan_Vermeer_van_Delft_-_Jonge_vrouw_aan_een_virginaal_(ca._1670-72).jpg",
        "curator": {
            "es": "Un canon atemporal, voz sobre voz",
            "pt": "Um cânone atemporal, voz sobre voz",
            "de": "Ein zeitloser Kanon, Stimme über Stimme",
            "fr": "Un canon hors du temps, voix sur voix",
            "ru": "Вечный канон, голос за голосом",
            "zh-Hant": "聲疊著聲，超越時間的卡農",
            "zh-Hans": "声叠着声，超越时间的卡农",
        },
        "tag_piece": {"es": "#Canon", "pt": "#Cânone", "de": "#Kanon", "fr": "#Canon", "ru": "#Канон", "zh-Hant": "#卡農", "zh-Hans": "#卡农"},
    },
    {
        "vid": "759VCWOtC2w", "slug": "tchaikovsky_sugar_plum_fairy", "count": 32, "year": "1892",
        "style": "lead", "welcome": False, "subscribe": False, "era": "romantic",
        "surname": L("Tchaikovsky", "Чайковский", "柴可夫斯基", "柴可夫斯基"),
        "full": L("Pyotr Ilyich Tchaikovsky", "Пётр Ильич Чайковский", "彼得·伊里奇·柴可夫斯基", "彼得·伊里奇·柴可夫斯基"),
        # s411 enrich: 부모작 발레명 병기 (검색량 압도 · 정식 발레 타이틀)
        "piece": {"es": "Danza del Hada de Azúcar (El Cascanueces)", "pt": "Dança da Fada Açucarada (O Quebra-Nozes)", "de": "Tanz der Zuckerfee (Der Nussknacker)",
                  "fr": "Danse de la Fée Dragée (Casse-Noisette)", "ru": "Танец Феи Драже (Щелкунчик)", "zh-Hant": "糖梅仙子之舞（胡桃鉗）", "zh-Hans": "糖梅仙子之舞（胡桃夹子）"},
        "painter": "Renoir", "painting": "The Dancer", "p_year": "1874",
        "cover_url": "https://commons.wikimedia.org/wiki/File:Renoir_-_Danseuse_NGA.jpg",
        "curator": None,
        # bespoke hook (코튼 LOCK 2026-06-06 · 첫 풀 관현악 편곡 + N=32 혹사 코미디). EN/KO/JA = release/ hand-sidecar 정본.
        "custom_hook": {
            "es": "Nuestro primer arreglo orquestal completo, y una Miku muy sobrecargada de trabajo.\nTreinta y dos Mikus cantan cada parte, hasta la última nota.\nPyotr Ilyich Tchaikovsky - Danza del Hada de Azúcar (1892)",
            "pt": "Nosso primeiro arranjo orquestral completo, e uma Miku muito sobrecarregada.\nTrinta e duas Mikus cantam cada parte, até a última nota.\nPyotr Ilyich Tchaikovsky - Dança da Fada Açucarada (1892)",
            "de": "Unser erstes vollständiges Orchesterarrangement — und eine völlig überlastete Miku.\nZweiunddreißig Mikus singen jede Stimme, bis zur letzten Note.\nPyotr Ilyich Tchaikovsky - Tanz der Zuckerfee (1892)",
            "fr": "Notre premier arrangement orchestral complet, et une Miku bien surmenée.\nTrente-deux Mikus chantent chaque voix, jusqu'à la dernière note.\nPyotr Ilyich Tchaikovsky - Danse de la Fée Dragée (1892)",
            "ru": "Наша первая полная оркестровая аранжировка — и одна совершенно загнанная Мику.\nТридцать две Мику поют каждую партию, до последней строчки.\nПётр Ильич Чайковский - Танец Феи Драже (1892)",
            "zh-Hant": "我們的第一首完整管弦樂編曲——還有一位被使喚到不行的初音未來。\n三十二位初音未來唱遍每一個聲部，一句都不漏。\n彼得·伊里奇·柴可夫斯基 - 糖梅仙子之舞 (1892)",
            "zh-Hans": "我们的第一首完整管弦乐编曲——还有一位被使唤到不行的初音未来。\n三十二位初音未来唱遍每一个声部，一句都不落。\n彼得·伊里奇·柴可夫斯基 - 糖梅仙子之舞 (1892)",
        },
        "tag_piece": {"es": "#HadaDeAzúcar", "pt": "#FadaAçucarada", "de": "#Zuckerfee", "fr": "#FéeDragée", "ru": "#ФеяДраже", "zh-Hant": "#糖梅仙子", "zh-Hans": "#糖梅仙子"},
    },
    {
        "vid": "X9xxOeqi2Sk", "slug": "boccherini_minuet", "count": 9, "year": "1771",
        "style": "lead", "welcome": False, "subscribe": False, "era": "classical",
        "surname": L("Boccherini", "Боккерини", "鮑凱利尼", "博凯里尼"),
        "full": L("Luigi Boccherini", "Луиджи Боккерини", "路易吉·鮑凱利尼", "路易吉·博凯里尼"),
        "piece": {"es": "Minueto", "pt": "Minueto", "de": "Menuett", "fr": "Menuet",
                  "ru": "Менуэт", "zh-Hant": "小步舞曲", "zh-Hans": "小步舞曲"},
        "painter": "Longhi", "painting": "The Dancing Lesson", "p_year": "c.1741",
        "cover_url": "https://www.wga.hu/html/l/longhi/pietro/1/01dancin.html",
        "curator": None,
        # custom_hook (코튼 LOCK 2026-06-08 · "토막상식+미뉴엣 어원[menu=작다]" 형식 · 표준 "{N} Mikus" 템플릿 벗어남).
        # EN/KO/JA = release/ hand-sidecar 정본. 7언어 번역 = 외부 QA subagent 게이트 (l10n cross-verification).
        "custom_hook": {
            "es": "¿Sabías que el minueto es una elegante danza cortesana francesa en compás ternario? Su nombre viene de los pasos pequeños (menu) y gráciles con que se bailaba.\nNueve Mikus cantan las cinco voces del quinteto de cuerda.\nLuigi Boccherini - Minueto (1771)",
            "pt": "Você sabia que o minueto é uma elegante dança da corte francesa em compasso ternário? O nome vem dos passos pequenos (menu) e graciosos com que era dançado.\nNove Mikus cantam as cinco vozes do quinteto de cordas.\nLuigi Boccherini - Minueto (1771)",
            "de": "Schon gewusst? Das Menuett ist ein eleganter französischer Hoftanz im Dreiertakt, benannt nach den kleinen (menu), anmutigen Schritten, mit denen es getanzt wurde.\nNeun Mikus singen alle fünf Stimmen des Streichquintetts.\nLuigi Boccherini - Menuett (1771)",
            "fr": "Le saviez-vous ? Le menuet est une élégante danse de cour française à trois temps, qui doit son nom aux petits pas menus et gracieux que l'on y dansait.\nNeuf Mikus chantent les cinq voix du quintette à cordes.\nLuigi Boccherini - Menuet (1771)",
            "ru": "А вы знали? Менуэт — изящный французский придворный танец в трёхдольном размере, названный так за маленькие (menu), грациозные шаги, которыми его танцевали.\nДевять Мику поют все пять голосов струнного квинтета.\nЛуиджи Боккерини - Менуэт (1771)",
            "zh-Hant": "你知道嗎？小步舞曲是一種優雅的三拍子法國宮廷舞曲，名稱源自跳舞時那細小（menu）而優雅的步伐。\n九位初音未來唱出弦樂五重奏的五個聲部。\n路易吉·鮑凱利尼 - 小步舞曲 (1771)",
            "zh-Hans": "你知道吗？小步舞曲是一种优雅的三拍子法国宫廷舞曲，名称源自跳舞时那细小（menu）而优雅的步伐。\n九位初音未来唱出弦乐五重奏的五个声部。\n路易吉·博凯里尼 - 小步舞曲 (1771)",
        },
        "tag_piece": {"es": "#Minueto", "pt": "#Minueto", "de": "#Menuett", "fr": "#Menuet", "ru": "#Менуэт", "zh-Hant": "#小步舞曲", "zh-Hans": "#小步舞曲"},
    },
]

# ── hashtags ───────────────────────────────────────────────────────────────
TAG_MIKU = {"es": "#HatsuneMiku", "pt": "#HatsuneMiku", "de": "#HatsuneMiku", "fr": "#HatsuneMiku", "ru": "#ХацунэМику", "zh-Hant": "#初音未來", "zh-Hans": "#初音未来"}
TAG_ACA = {"es": "#Acappella", "pt": "#Acappella", "de": "#ACappella", "fr": "#ACappella", "ru": "#Акапелла", "zh-Hant": "#阿卡貝拉", "zh-Hans": "#阿卡贝拉"}
TAG_VOCALOID = {"es": "#VOCALOID", "pt": "#VOCALOID", "de": "#VOCALOID", "fr": "#VOCALOID", "ru": "#Вокалоид", "zh-Hant": "#VOCALOID", "zh-Hans": "#VOCALOID"}
TAG_CLASSICAL = {"es": "#MúsicaClásica", "pt": "#MúsicaClássica", "de": "#KlassischeMusik", "fr": "#MusiqueClassique", "ru": "#КлассическаяМузыка", "zh-Hant": "#古典音樂", "zh-Hans": "#古典音乐"}
TAG_ERA = {
    "romantic": {"es": "#Romanticismo", "pt": "#Romantismo", "de": "#Romantik", "fr": "#Romantisme", "ru": "#Романтизм", "zh-Hant": "#浪漫樂派", "zh-Hans": "#浪漫乐派"},
    "baroque": {"es": "#Barroco", "pt": "#Barroco", "de": "#Barock", "fr": "#Baroque", "ru": "#Барокко", "zh-Hant": "#巴洛克", "zh-Hans": "#巴洛克"},
    "classical": {"es": "#Clasicismo", "pt": "#Classicismo", "de": "#Klassik", "fr": "#Classicisme", "ru": "#Классицизм", "zh-Hant": "#古典樂派", "zh-Hans": "#古典乐派"},
    "ragtime": {"es": "#Ragtime", "pt": "#Ragtime", "de": "#Ragtime", "fr": "#Ragtime", "ru": "#Рэгтайм", "zh-Hant": "#拉格泰姆", "zh-Hans": "#拉格泰姆"},
}
TAG_COMPOSER = {  # composer hashtag (no space) per lang
    "Satie": {"ru": "#Сати", "zh-Hant": "#薩蒂", "zh-Hans": "#萨蒂"},
    "Vivaldi": {"ru": "#Вивальди", "zh-Hant": "#韋瓦第", "zh-Hans": "#维瓦尔第"},
    "Joplin": {"ru": "#Джоплин", "zh-Hant": "#喬普林", "zh-Hans": "#乔普林"},
    "Elgar": {"ru": "#Элгар", "zh-Hant": "#艾爾加", "zh-Hans": "#埃尔加"},
    "Mozart": {"ru": "#Моцарт", "zh-Hant": "#莫札特", "zh-Hans": "#莫扎特"},
    "Chopin": {"ru": "#Шопен", "zh-Hant": "#蕭邦", "zh-Hans": "#肖邦"},
    "Pachelbel": {"ru": "#Пахельбель", "zh-Hant": "#帕海貝爾", "zh-Hans": "#帕赫贝尔"},
    "Tchaikovsky": {"ru": "#Чайковский", "zh-Hant": "#柴可夫斯基", "zh-Hans": "#柴可夫斯基"},
}
def composer_tag(lang, surname_en):
    return TAG_COMPOSER.get(surname_en, {}).get(lang, "#" + surname_en.replace(" ", ""))

def hashtags(w, lang):
    tags = [
        TAG_MIKU[lang], TAG_ACA[lang], w["tag_piece"][lang], "#初音ミク",
        TAG_VOCALOID[lang], TAG_CLASSICAL[lang], TAG_ERA[w["era"]][lang],
        composer_tag(lang, w["surname"]["es"]),  # es key holds latin surname
        "#AtelierMikuAcappella",
    ]
    return " ".join(tags)

# ── assembly ───────────────────────────────────────────────────────────────
def title(w, lang):
    badge = BADGE_ABBR if w.get("badge_abbrev") else BADGE
    return f"{w['surname'][lang]} - {w['piece'][lang]}{badge}"

def dedication(w, lang):
    full = w["full"][lang]
    piece = w["piece"][lang]
    yr = year_parens(lang, w["year"])
    s = sing(lang, w["count"])
    if lang.startswith("zh-"):
        if w["style"] == "lead":
            return f"{s} —\n{full} - {piece}{yr}。"
        return f"{full} - {piece}{yr}。{s}。"
    if w["style"] == "lead":
        return f"{s} —\n{full} - {piece} {yr}."
    # inline / welcome_inline / vivaldi
    return f"{full} - {piece} {yr}. {s}."

def credit(w, lang):
    sep = label_colon(lang)
    return (f"{PROD[lang]}{sep}VOCALOID6 / {VOICE[lang]}{sep}{MIKU[lang]} V6\n"
            f"{MIKU[lang]}, © Crypton Future Media, Inc. — {CC}")

def cover(w, lang):
    return (cover_line(lang, painter_name(lang, w["painter"]), w["painting"], date_for(lang, w["p_year"]))
            + "\n" + w["cover_url"])

def build_description(w, lang):
    """주요 블록은 '—' 로 구분 · 해시태그는 크레딧 블록에 빈 줄로 부착 (live EN 정합)."""
    major = []
    if w.get("welcome"):
        major.append(WELCOME[lang])
        block = dedication(w, lang) + "\n\n" + cover(w, lang)
    elif w.get("custom_hook"):
        # bespoke hook (표준 "{N} Mikus sing it now" 템플릿 벗어남 · 차이콥스키 사탕요정 s398).
        # curator+dedication 대신 per-work 3줄 블록 통째 사용 (count/sing/NUM 미사용).
        head = w["custom_hook"][lang]
        block = head + "\n\n" + cover(w, lang)
    else:
        cur = w["curator"][lang]
        ded = dedication(w, lang)
        head = (cur + "\n\n" + ded) if w["style"] == "lead" else (cur + "\n" + ded)
        block = head + "\n\n" + cover(w, lang)
    if w.get("subscribe"):
        block += "\n\n" + SUBSCRIBE[lang]
    major.append(block)
    if w.get("chapters"):
        major.append(mozart_chapters(lang))
    major.append(credit(w, lang) + "\n\n" + hashtags(w, lang))  # 해시태그 = 크레딧과 같은 블록
    return "\n\n—\n\n".join(major)

# ── channel ────────────────────────────────────────────────────────────────
CHANNEL = {
    "es": "¿Y si Hatsune Miku cantara música clásica?\nUn pequeño atelier donde Miku y los viejos maestros se encuentran.\n\nEste es un canal de fans de Hatsune Miku.\nAmo la música clásica y también amo a Miku, por eso hago esto.",
    "pt": "E se a Hatsune Miku cantasse música clássica?\nUm pequeno atelier onde a Miku e os velhos mestres se encontram.\n\nEste é um canal de fãs da Hatsune Miku.\nEu amo música clássica e também amo a Miku, por isso faço isso.",
    "de": "Was wäre, wenn Hatsune Miku klassische Musik sänge?\nEin kleines Atelier, in dem Miku und die alten Meister einander begegnen.\n\nDies ist ein Hatsune-Miku-Fankanal.\nIch liebe klassische Musik und ich liebe Miku — darum mache ich das.",
    "fr": "Et si Hatsune Miku chantait de la musique classique ?\nUn petit atelier où Miku et les maîtres anciens se rencontrent.\n\nCeci est une chaîne de fans de Hatsune Miku.\nJ'aime la musique classique et j'aime aussi Miku, alors je fais ceci.",
    "ru": "Что, если бы Хацунэ Мику пела классическую музыку?\nМаленькое ателье, где Мику встречается со старыми мастерами.\n\nЭто фанатский канал Хацунэ Мику.\nЯ люблю классическую музыку и люблю Мику — поэтому я делаю это.",
    "zh-Hant": "如果初音未來歌唱古典音樂，會是什麼模樣？\n一間小小的工坊，讓初音未來與古典大師在此相遇。\n\n這是初音未來的同人頻道。\n因為深愛古典音樂，也深愛著初音未來，於是有了這個頻道。",
    "zh-Hans": "如果初音未来歌唱古典音乐，会是什么模样？\n一间小小的工坊，让初音未来与古典大师在此相遇。\n\n这是初音未来的同人频道。\n因为深爱古典音乐，也深爱着初音未来，于是有了这个频道。",
}

# ── commands ───────────────────────────────────────────────────────────────
def cmd_gate(_):
    print("### 제목 (Title) — {surname} - {piece} 【初音ミク A Cappella】\n")
    for w in WORKS:
        print(f"■ {w['slug']}  [{w['vid']}]")
        for lang in LANGS:
            print(f"   {lang:8} {title(w, lang)}")
        print()
    print("\n### 큐레이터 보이스 (Curator voice)\n")
    for w in WORKS:
        print(f"■ {w['slug']}")
        if w["curator"] is None:
            print("   (Welcome 블록형 — epithet 없음)")
        else:
            for lang in LANGS:
                print(f"   {lang:8} {w['curator'][lang]}")
        print()

def _select(only):
    """--only <vid|slug-prefix> → 단일 작품만 (신곡 발행 시 기존 작품 재푸시 회피). 없으면 전체."""
    if not only:
        return WORKS
    sel = [w for w in WORKS if w["vid"] == only or w["slug"].startswith(only)]
    if not sel:
        sys.exit(f"--only '{only}' 매칭 work 없음. 후보 = {[w['slug'] for w in WORKS]}")
    return sel

def cmd_write(args):
    for w in _select(getattr(args, "only", None)):
        rel = BASE / "works" / w["slug"] / "video" / "release"
        rel.mkdir(parents=True, exist_ok=True)
        for lang in LANGS:
            (rel / f"description.{lang}.txt").write_text(build_description(w, lang) + "\n", encoding="utf-8")
            (rel / f"title.{lang}.txt").write_text(title(w, lang) + "\n", encoding="utf-8")
        print(f"✓ {w['slug']}: {len(LANGS)} locale sidecars + titles")

def cmd_channel(_):
    out = BASE / "Analytics" / "_channel_l10n"
    out.mkdir(parents=True, exist_ok=True)
    for lang in LANGS:
        (out / f"channel.{lang}.txt").write_text(CHANNEL[lang] + "\n", encoding="utf-8")
    print(f"✓ channel sidecars → {out} ({len(LANGS)} locales · codes {CHANNEL_CODE})")

def render_review():
    lines = [
        "PROJECT MUSE — LOCALIZATION EXPANSION REVIEW (2026-06)",
        "locales: es / pt / de / fr / ru / zh-Hant / zh-Hans",
        "============================================================",
        "",
        "### 제목 (Title) — {surname} - {piece} 【初音ミク A Cappella】",
        "",
    ]
    for w in WORKS:
        lines.append(f"■ {w['slug']}  [{w['vid']}]")
        for lang in LANGS:
            lines.append(f"   {lang:8} {title(w, lang)}")
        lines.append("")

    lines += ["", "### 큐레이터 보이스 (Curator voice)", ""]
    for w in WORKS:
        lines.append(f"■ {w['slug']}")
        if w["curator"] is None:
            lines.append("   (Welcome 블록형 — epithet 없음)")
        else:
            for lang in LANGS:
                lines.append(f"   {lang:8} {w['curator'][lang]}")
        lines.append("")

    lines += ["", "############ FULL RENDERED DESCRIPTIONS ############"]
    for w in WORKS:
        for lang in LANGS:
            lines.append(f"========== [{lang}] {title(w, lang)} ==========")
            lines.append(build_description(w, lang))
            lines.append("")

    lines += ["############ CHANNEL ############"]
    for lang in LANGS:
        lines.append(f"----- [{lang}] -----")
        lines.append(CHANNEL[lang])
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"

def cmd_review(_):
    out = BASE / "Analytics" / "_channel_l10n" / "REVIEW_l10n_2026-06.txt"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render_review(), encoding="utf-8")
    print(f"✓ review → {out}")

def cmd_push(args):
    """라이브 푸시: 7 신규 로케일을 영상 localizations + 채널 localizations 에 read-modify-write.
    기존 en/ja/ko + 기본 snippet 전부 보존. --dry-run 으로 미적용 미리보기."""
    import youtube_meta as ym
    svc = ym.yt()
    sel = _select(getattr(args, "only", None))

    # ── videos ──
    for w in sel:
        vid = w["vid"]
        v = svc.videos().list(part="snippet,localizations", id=vid).execute()["items"][0]
        sn = v["snippet"]
        locs = dict(v.get("localizations") or {})
        before = sorted(locs.keys())
        for lang in LANGS:
            locs[lang] = {"title": title(w, lang), "description": build_description(w, lang)}
        new_snippet = {
            "title": sn.get("title"),
            "categoryId": sn.get("categoryId"),
            "description": sn.get("description", ""),
        }
        if sn.get("tags"):
            new_snippet["tags"] = sn["tags"]
        if sn.get("defaultLanguage"):
            new_snippet["defaultLanguage"] = sn["defaultLanguage"]
        if sn.get("defaultAudioLanguage"):
            new_snippet["defaultAudioLanguage"] = sn["defaultAudioLanguage"]
        if args.dry_run:
            print(f"[dry] {vid} {w['slug']}: {before} → +{len(LANGS)} ({LANGS})")
            continue
        svc.videos().update(
            part="snippet,localizations",
            body={"id": vid, "snippet": new_snippet, "localizations": locs},
        ).execute()
        print(f"✓ {vid} {w['slug']}: +{len(LANGS)} locales (보존 {before})")

    # ── channel ── (전체 실행에서만 · --only 신곡 푸시 땐 채널 불변이라 skip)
    if getattr(args, "only", None):
        return
    # 채널 defaultLanguage(en) 이미 설정됨 → part="localizations" 단독 write 로 persist 확인됨.
    # ('brandingSettings cannot be used with other parts' → 동봉 불가 · 동봉 불필요.)
    # 코드 = region 형(es_ES…) 으로 기존 en_US/ja_JP/ko_KR 스타일 정합. 쓰기 후 propagation lag 있음.
    ch = svc.channels().list(part="snippet,localizations", mine=True).execute()["items"][0]
    cid = ch["id"]
    brand = ch["snippet"].get("title")
    clocs = dict(ch.get("localizations") or {})
    cbefore = sorted(clocs.keys())
    for lang in LANGS:
        clocs[CHANNEL_CODE[lang]] = {"title": brand, "description": CHANNEL[lang]}
    if args.dry_run:
        print(f"[dry] channel {cid}: {cbefore} → +{[CHANNEL_CODE[l] for l in LANGS]} (title 고정 {brand!r})")
        return
    svc.channels().update(part="localizations", body={"id": cid, "localizations": clocs}).execute()
    print(f"✓ channel {cid}: +{len(LANGS)} locales (보존 {cbefore})")


def cmd_audit(args):
    """푸시 후 전수 검증: 영상 + 채널에 7 신규 로케일이 정확히 박혔는지 re-get 대조 (--only 단일 작품)."""
    import youtube_meta as ym
    svc = ym.yt()
    ok = True
    sel = _select(getattr(args, "only", None))
    for w in sel:
        v = svc.videos().list(part="snippet,localizations", id=w["vid"]).execute()["items"][0]
        locs = v.get("localizations") or {}
        miss = [l for l in LANGS if l not in locs]
        bad = [l for l in LANGS if l in locs and locs[l].get("title") != title(w, l)]
        status = "✓" if not miss and not bad else "✗"
        if miss or bad:
            ok = False
        extra = f" MISSING={miss}" if miss else ""
        extra += f" TITLE-MISMATCH={bad}" if bad else ""
        print(f"{status} {w['vid']} {w['slug']}: locales={sorted(locs.keys())}{extra}")
    if not getattr(args, "only", None):  # 채널은 전체 audit 에서만
        ch = svc.channels().list(part="localizations", mine=True).execute()["items"][0]
        clocs = ch.get("localizations") or {}
        cmiss = [CHANNEL_CODE[l] for l in LANGS if CHANNEL_CODE[l] not in clocs]
        cstatus = "✓" if not cmiss else "✗"
        if cmiss:
            ok = False
        print(f"{cstatus} channel: locales={sorted(clocs.keys())}" + (f" MISSING={cmiss}" if cmiss else ""))
    print("\n=== AUDIT", "PASS ===" if ok else "FAIL ===")
    if not ok:
        sys.exit(1)


def cmd_preview(args):
    w = next((x for x in WORKS if x["slug"].startswith(args.slug) or x["vid"] == args.slug), None)
    if not w:
        sys.exit(f"work 못 찾음: {args.slug}")
    for lang in (args.langs.split(",") if args.langs else LANGS):
        print(f"========== [{lang}] {title(w, lang)} ==========")
        print(build_description(w, lang))
        print()

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("gate")
    wr = sub.add_parser("write")
    wr.add_argument("--only", help="단일 작품만 (vid 또는 slug 접두)")
    sub.add_parser("channel")
    sub.add_parser("review")
    ph = sub.add_parser("push")
    ph.add_argument("--dry-run", action="store_true")
    ph.add_argument("--only", help="단일 작품만 (신곡 발행 시 · 채널 skip)")
    au = sub.add_parser("audit")
    au.add_argument("--only", help="단일 작품만 (신곡 발행 시 · 채널 skip)")
    pv = sub.add_parser("preview")
    pv.add_argument("slug")
    pv.add_argument("--langs")
    a = p.parse_args()
    {"gate": cmd_gate, "write": cmd_write, "channel": cmd_channel, "review": cmd_review,
     "push": cmd_push, "audit": cmd_audit, "preview": cmd_preview}[a.cmd](a)
