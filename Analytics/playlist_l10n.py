# -*- coding: utf-8 -*-
"""재생목록 l10n 배치 (Atelier Miku A Cappella) — review → push → audit.

localize_batch.py 미러 (영상/채널판의 재생목록 대응).
- 9 localizations: ja / ko / es / pt / de / fr / ru / zh-Hant / zh-Hans  (+ en = default snippet)
- **TITLE = 전 로케일 영문 고정** (재생목록명 = 채널 브랜드 라벨로 일관 · 코튼 결단 2026-06-03).
  → localizations 의 title 도 영문 동일. description 만 현지화.
- description 본문의 가수 지칭은 현지 표기 (ru=Мику · zh=初音未來 · latin권=Miku).
- **아카펠라 표기 정합**: 브랜드명(title "A Cappella")만 라틴. 본문은 언어별 자국 문자
  (ja アカペラ · ko 아카펠라 · zh 阿卡貝拉 음역 · ru а капелла 키릴 · 라틴문자권 a cappella). ja/ko 라이브 정본 기준.

번역 cycle: v1 → 3-AI 1차 교차검증 → v3 → 3-AI 2차 교차검증 → **FINAL** (2026-06-03 · 셋 다 "배포 가능" 수렴).
  zh 阿卡貝拉 음역 = ja/ko 정본(アカペラ/아카펠라) 정합 유지 (Claude "규칙대로 OK" · Gemini/ChatGPT 라틴 권고 기각).
  ru voice = 도구격(голосом) 유지 (ChatGPT "flawless"·Claude "정확" · Gemini 2차 исполнении 권고는 소수의견 보류).

워크플로우 (코튼 doctrine = 외부 AI 교차검증을 push 전에):
  python Analytics/playlist_l10n.py review   # _channel_l10n/REVIEW_playlist_l10n_2026-06.txt 생성 → 외부 AI 교차검증
  python Analytics/playlist_l10n.py push [--only <slug>] [--dry-run]   # 교차검증 통과 후에만
  python Analytics/playlist_l10n.py audit [--only <slug>]              # 푸시 후 전수 대조
"""
import sys
import argparse
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, str(Path(__file__).resolve().parent))
from youtube_meta import yt  # noqa: E402
from googleapiclient.errors import HttpError  # noqa: E402

BASE = Path(__file__).resolve().parent.parent
LOC_LANGS = ["ja", "ko", "es", "pt", "de", "fr", "ru", "zh-Hant", "zh-Hans"]  # en = default snippet
# YouTube 가 localizations 키를 정규화: zh-Hant→zh-TW, zh-Hans→zh-CN (push 값은 그대로 보존됨).
LIVE_KEY = {"zh-Hant": "zh-TW", "zh-Hans": "zh-CN"}

# 각 재생목록: title_en = 전 로케일 영문 고정 · desc en = default(snippet), 나머지 = localizations.
PLAYLISTS = [
    {
        "slug": "baroque",
        "pid": "PLYpo6J-CC8YghkggYW208M2_-aRVypQG8",
        "title_en": "Miku in the Baroque Era",
        "desc": {
            "en": "Listen to the dynamic music of the Baroque era, pulsing with dramatic contrasts and ornate embellishments, through Miku's acappella.",
            "ja": "劇的な対比と華やかな装飾音が絶え間なく脈打つ、バロック時代のダイナミックな音楽をミクのアカペラでご堪能ください。",
            "ko": "극적인 대비와 화려한 장식음이 쉴 새 없이 박동하는 바로크 시대의 역동적인 음악을 미쿠의 아카펠라로 감상하세요.",
            "es": "Escucha la dinámica música del Barroco, palpitante de contrastes dramáticos y ornamentación elaborada, en la voz a cappella de Miku.",
            "pt": "Ouça a dinâmica música do Barroco, pulsante de contrastes dramáticos e ornamentações elaboradas, na voz a cappella de Miku.",
            "de": "Erlebe die dynamische Musik des Barock, pulsierend vor dramatischen Kontrasten und kunstvollen Verzierungen, mit Mikus A-cappella-Stimme.",
            "fr": "Écoutez la musique dynamique de l'époque baroque, vibrante de contrastes dramatiques et d'ornements raffinés, à travers la voix a cappella de Miku.",
            "ru": "Слушайте динамичную музыку барокко, пульсирующую драматическими контрастами и изысканной орнаментикой, в исполнении Мику а капелла.",
            "zh-Hant": "聆聽巴洛克時代躍動不息、充滿戲劇性對比與華麗裝飾音的音樂，由初音未來以阿卡貝拉獻聲。",
            "zh-Hans": "聆听巴洛克时代跃动不息、充满戏剧性对比与华丽装饰音的音乐，由初音未来以阿卡贝拉献声。",
        },
    },
    {
        "slug": "classical",
        "pid": "PLYpo6J-CC8YjhbJ4rCEDCD7tZfhtqLYYk",
        "title_en": "Miku in the Classical Era",
        "desc": {
            "en": "Enjoy the music of the Classical era, where strict formal beauty and clear melodies achieve perfect balance, through Miku's transparent voice.",
            "ja": "徹底した形式美と明瞭な旋律が完璧な均衡を保つ、古典派時代の音楽をミクの透明な声でお楽しみください。",
            "ko": "철저한 형식미와 명료한 선율이 완벽한 균형을 이루는 고전주의 시대의 음악을 미쿠의 투명한 목소리로 즐겨보세요.",
            "es": "Disfruta de la música del Clasicismo, donde la rigurosa belleza formal y las melodías nítidas alcanzan un equilibrio perfecto, a través de la voz transparente de Miku.",
            "pt": "Aprecie a música do Classicismo, onde a rigorosa beleza formal e as melodias nítidas alcançam um equilíbrio perfeito, através da voz transparente de Miku.",
            "de": "Genieße die Musik der Klassik, in der strenge formale Schönheit und klare Melodien vollkommene Ausgewogenheit erreichen, mit Mikus transparenter Stimme.",
            "fr": "Savourez la musique de l'époque classique, où une beauté formelle rigoureuse et des mélodies limpides atteignent un équilibre parfait, à travers la voix cristalline de Miku.",
            "ru": "Насладитесь музыкой классицизма, где строгая красота формы и ясность мелодий достигают совершенного равновесия, прозрачным голосом Мику.",
            "zh-Hant": "欣賞古典樂派時期的音樂——嚴謹的形式美與清晰的旋律達到完美的平衡，由初音未來以澄澈的歌聲詮釋。",
            "zh-Hans": "欣赏古典乐派时期的音乐——严谨的形式美与清晰的旋律达到完美的平衡，由初音未来以澄澈的歌声诠释。",
        },
    },
    {
        "slug": "romantic",
        "pid": "PLYpo6J-CC8YhIB5-tQTy_5vAQYC7kShX3",
        "title_en": "Miku in the Romantic Era",
        "desc": {
            "en": "Explore the music of the Romantic era, which broke traditional forms to explode with deep human emotions and dramatic narratives, through Miku's delicate voice.",
            "ja": "形式の枠を越え、人間の濃密な感情と劇的な叙事を爆発させたロマン派時代の音楽を、ミクの繊細な声で探検してみましょう。",
            "ko": "형식의 틀을 벗어나 인간의 짙은 감정과 극적인 서사를 폭발시켰던 낭만주의 시대의 음악을 미쿠의 섬세한 목소리로 탐험하세요.",
            "es": "Explora la música del Romanticismo, que rompió las formas tradicionales para estallar en emociones humanas profundas y narrativas dramáticas, a través de la delicada voz de Miku.",
            "pt": "Explore a música do Romantismo, que rompeu com as formas tradicionais, dando vazão a emoções humanas profundas e narrativas dramáticas, através da delicada voz de Miku.",
            "de": "Erkunde die Musik der Romantik, die traditionelle Formen sprengte und tiefe menschliche Gefühle sowie dramatische Erzählungen entfesselte, mit Mikus zarter Stimme.",
            "fr": "Explorez la musique de l'époque romantique, qui brisa les formes traditionnelles pour faire éclater des émotions humaines profondes et des récits dramatiques, à travers la voix délicate de Miku.",
            "ru": "Откройте для себя музыку романтизма, которая разрушила традиционные формы и дала волю глубоким человеческим чувствам и драматическим повествованиям, нежным голосом Мику.",
            "zh-Hant": "探索浪漫樂派時期的音樂——它打破傳統形式，迸發出深沉的人類情感與戲劇性的敘事，由初音未來以細膩的嗓音演繹。",
            "zh-Hans": "探索浪漫乐派时期的音乐——它打破传统形式，迸发出深沉的人类情感与戏剧性的叙事，由初音未来以细腻的嗓音演绎。",
        },
    },
    {
        "slug": "20th_century",
        "pid": "PLYpo6J-CC8YiSNb8p6FwGvNfpgd_IpUmc",
        "title_en": "Miku in the 20th Century",
        "desc": {
            "en": "Experience the unconventional music of the 20th century, where centuries of rules were deconstructed to welcome diverse rhythms and radical experiments, together with Miku.",
            "ja": "数百年の規則を解体し、多彩なリズムと破格の実験が共存した20世紀の新しい音楽を、ミクと一緒に経験してみてください。",
            "ko": "수백 년의 규칙을 해체하고 다채로운 리듬과 파격적인 실험이 공존했던 20세기의 새로운 음악들을 미쿠와 함께 경험하세요.",
            "es": "Vive la música rompedora del siglo XX, donde siglos de reglas se deconstruyeron para dar paso a ritmos diversos y experimentos radicales, junto a Miku.",
            "pt": "Viva a música inovadora do século XX, onde regras de séculos foram desconstruídas para dar lugar a ritmos diversos e experimentos radicais, ao lado de Miku.",
            "de": "Erlebe die unkonventionelle Musik des 20. Jahrhunderts, in der jahrhundertealte Regeln dekonstruiert wurden, um vielfältigen Rhythmen und radikalen Experimenten Raum zu geben — gemeinsam mit Miku.",
            "fr": "Découvrez la musique non conventionnelle du XXe siècle, où des siècles de règles furent déconstruits pour accueillir des rythmes variés et des expérimentations radicales, aux côtés de Miku.",
            "ru": "Откройте для себя нестандартную музыку XX века, где вековые правила были деконструированы, чтобы впустить разнообразные ритмы и смелые эксперименты, вместе с Мику.",
            "zh-Hant": "與初音未來一同體驗20世紀的不羈音樂——數百年的規則被解構，迎來多元的節奏與大膽的實驗。",
            "zh-Hans": "与初音未来一同体验20世纪的不羁音乐——数百年的规则被解构，迎来多元的节奏与大胆的实验。",
        },
    },
    {
        "slug": "renaissance",
        "pid": "PLYpo6J-CC8YghE4-iwdHlGk6Xm7uXl8LO",
        "title_en": "Miku in the Renaissance Era",
        "desc": {
            "en": "Experience the music of the Renaissance era, where independent melodies intricately intertwine, through Miku's pure voice.",
            "ja": "独立した旋律が交差し、精巧な調和をなすルネサンス時代の音楽を、ミクの純粋な歌声でお楽しみください。",
            "ko": "여러 선율이 독립적으로 교차하며 정교한 조화를 이룩한 르네상스 시대의 음악을 미쿠의 순수한 목소리로 만나보세요.",
            "es": "Descubre la música del Renacimiento, donde melodías independientes se entrelazan con delicadeza, a través de la voz pura de Miku.",
            "pt": "Descubra a música do Renascimento, onde melodias independentes se entrelaçam com delicadeza, através da voz pura de Miku.",
            "de": "Entdecke die Musik der Renaissance, in der eigenständige Melodien sich kunstvoll verflechten, mit Mikus reiner Stimme.",
            "fr": "Plongez dans la musique de la Renaissance, où des mélodies indépendantes s'entrelacent avec finesse, à travers la voix pure de Miku.",
            "ru": "Откройте для себя музыку эпохи Возрождения, где независимые мелодии искусно переплетаются, чистым голосом Мику.",
            "zh-Hant": "探索文藝復興時期的音樂——獨立的旋律交織出精巧的和諧，由初音未來以純淨的歌聲呈現。",
            "zh-Hans": "探索文艺复兴时期的音乐——独立的旋律交织出精巧的和谐，由初音未来以纯净的歌声呈现。",
        },
    },
    {
        "slug": "non_stop",
        "pid": "PLYpo6J-CC8YjNojePlK3VTHGNgGxDdk1t",
        "title_en": "Miku Non-Stop A Cappella",
        "desc": {
            "en": "Experience the complete collection in one non-stop journey across every era, sung purely through Miku's a cappella voice!",
            "ja": "全時代を貫く全コレクションを、ミクのアカペラの歌声でノンストップにお楽しみください！",
            "ko": "모든 시대를 아우르는 전곡 컬렉션을 미쿠의 아카펠라 목소리로 끊김 없이 감상하세요!",
            "es": "¡Vive la colección completa en un viaje sin pausa a través de todas las épocas, cantada enteramente con la voz a cappella de Miku!",
            "pt": "Viva a coleção completa em uma jornada sem pausa por todas as épocas, cantada inteiramente com a voz a cappella de Miku!",
            "de": "Erlebe die komplette Sammlung in einer ununterbrochenen Reise durch alle Epochen, ganz mit Mikus A-cappella-Stimme gesungen!",
            "fr": "Vivez la collection complète en un voyage sans pause à travers toutes les époques, entièrement chantée a cappella par Miku !",
            "ru": "Погрузитесь в полную коллекцию в непрерывном путешествии сквозь все эпохи, целиком исполненную голосом Мику а капелла!",
            "zh-Hant": "在一段不間斷的旅程中，聆聽橫跨所有時代的全套作品，全程由初音未來以阿卡貝拉獻唱！",
            "zh-Hans": "在一段不间断的旅程中，聆听横跨所有时代的全套作品，全程由初音未来以阿卡贝拉献唱！",
        },
    },
]


def render_review():
    lines = [
        "PROJECT MUSE — PLAYLIST LOCALIZATION REVIEW FINAL (2026-06 · 3-AI 2회 교차검증 · 배포 가능 수렴)",
        "playlists: 6 (5 eras + non-stop) · locales: en(default) + ja/ko/es/pt/de/fr/ru/zh-Hant/zh-Hans",
        "정책: TITLE = 전 로케일 영문 고정 · DESCRIPTION 만 현지화 · 본문 가수 지칭은 현지 표기 · 아카펠라=본문은 자국 문자(zh 阿卡貝拉·ru а капелла), 라틴문자권만 a cappella",
        "=" * 70,
        "",
        "### TITLE (전 로케일 영문 고정 — 검토 불필요, 참고용)",
        "",
    ]
    for pl in PLAYLISTS:
        lines.append(f"   {pl['title_en']:30}  [{pl['slug']}]")

    lines += ["", "", "### DESCRIPTION (en/ja/ko = 기존 라이브 정본 · es/pt/de/fr/ru/zh-Hant/zh-Hans = FINAL 번역)", ""]
    for pl in PLAYLISTS:
        lines.append(f"■ {pl['slug']}  ({pl['title_en']})")
        lines.append(f"   {'en':9} {pl['desc']['en']}  (정본)")
        for lang in LOC_LANGS:
            tag = "정본" if lang in ("ja", "ko") else "FINAL"
            lines.append(f"   {lang:9} {pl['desc'][lang]}  ({tag})")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def cmd_review(_):
    out = BASE / "Analytics" / "_channel_l10n" / "REVIEW_playlist_l10n_2026-06.txt"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render_review(), encoding="utf-8")
    print(f"✓ review → {out}")
    print(f"  ({len(PLAYLISTS)} playlists × {1 + len(LOC_LANGS)} locales · title=영문 고정)")


def cmd_push(args):
    svc = yt()
    targets = [pl for pl in PLAYLISTS if not args.only or pl["slug"] == args.only]
    if not targets:
        sys.exit(f"--only 매칭 없음: {args.only}")
    for pl in targets:
        resp = svc.playlists().list(part="snippet,localizations,status", id=pl["pid"]).execute()
        items = resp.get("items", [])
        if not items:
            print(f"✗ {pl['slug']}: playlist 못 찾음 {pl['pid']}")
            continue
        cur = items[0]["snippet"]
        new_snippet = {
            "title": pl["title_en"],
            "description": pl["desc"]["en"],
            "defaultLanguage": "en",
        }
        if cur.get("tags"):
            new_snippet["tags"] = cur["tags"]
        # localizations: title 은 전 로케일 영문 고정, description 만 현지화.
        localizations = {lang: {"title": pl["title_en"], "description": pl["desc"][lang]} for lang in LOC_LANGS}
        body = {"id": pl["pid"], "snippet": new_snippet, "localizations": localizations}
        if args.dry_run:
            print(f"[dry-run] {pl['slug']}  title(고정)={pl['title_en']!r}  +{len(LOC_LANGS)} desc localizations")
            continue
        try:
            svc.playlists().update(part="snippet,localizations", body=body).execute()
            print(f"✓ push {pl['slug']}  (title 영문 고정 + {len(LOC_LANGS)} desc localizations)")
        except HttpError as e:
            print(f"✗ push {pl['slug']} 실패: {e}")


def cmd_audit(args):
    svc = yt()
    targets = [pl for pl in PLAYLISTS if not args.only or pl["slug"] == args.only]
    ok = True
    for pl in targets:
        resp = svc.playlists().list(part="snippet,localizations", id=pl["pid"]).execute()
        items = resp.get("items", [])
        if not items:
            print(f"✗ {pl['slug']}: 못 찾음")
            ok = False
            continue
        live = items[0]
        live_loc = live.get("localizations") or {}
        miss = []
        if live["snippet"].get("title") != pl["title_en"]:
            miss.append("snippet.title")
        for lang in LOC_LANGS:
            lv = live_loc.get(LIVE_KEY.get(lang, lang), {})
            if lv.get("title") != pl["title_en"]:
                miss.append(f"{lang}.title")
            if lv.get("description") != pl["desc"][lang]:
                miss.append(f"{lang}.desc")
        if live["snippet"].get("defaultLanguage") != "en":
            miss.append("defaultLanguage!=en")
        if miss:
            ok = False
            print(f"✗ {pl['slug']}: {', '.join(miss)}")
        else:
            print(f"✓ {pl['slug']}: title 영문 고정 + {len(LOC_LANGS)} desc 정합")
    print("\n=== AUDIT", "PASS ===" if ok else "FAIL ===")
    if not ok:
        sys.exit(1)


def main():
    p = argparse.ArgumentParser(description="재생목록 l10n 배치 (review→push→audit)")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("review", help="교차검증용 REVIEW txt 생성")
    ph = sub.add_parser("push", help="라이브 적용 (교차검증 통과 후)")
    ph.add_argument("--only", help="단일 slug 만")
    ph.add_argument("--dry-run", action="store_true")
    au = sub.add_parser("audit", help="푸시 후 전수 대조")
    au.add_argument("--only", help="단일 slug 만")
    args = p.parse_args()
    {"review": cmd_review, "push": cmd_push, "audit": cmd_audit}[args.cmd](args)


if __name__ == "__main__":
    main()
