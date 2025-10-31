import json
import re
import time
from typing import Iterable, List, Optional
from urllib.parse import urlparse
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError


URL_LIST = """https://jobs.ashbyhq.com/1password
https://jobs.ashbyhq.com/9fin
https://jobs.ashbyhq.com/A1%20Garage%20Door%20Service
https://jobs.ashbyhq.com/Acorns
https://jobs.ashbyhq.com/Adtucon
https://jobs.ashbyhq.com/AlephAlpha
https://jobs.ashbyhq.com/Anon
https://jobs.ashbyhq.com/basis-ai
https://jobs.ashbyhq.com/BranchInsurance
https://jobs.ashbyhq.com/Cambly
https://jobs.ashbyhq.com/Clicklease
https://jobs.ashbyhq.com/Commure-Athelas
https://jobs.ashbyhq.com/credal
https://jobs.ashbyhq.com/Crusoe
https://jobs.ashbyhq.com/CylinderHealth
https://jobs.ashbyhq.com/Dashworks
https://jobs.ashbyhq.com/DatologyAI
https://jobs.ashbyhq.com/Deel
https://jobs.ashbyhq.com/DeepL
https://jobs.ashbyhq.com/Deepgram
https://jobs.ashbyhq.com/Distyl
https://jobs.ashbyhq.com/Doowii
https://jobs.ashbyhq.com/DoseSpot
https://jobs.ashbyhq.com/FURTHER
https://jobs.ashbyhq.com/FlutterFlow
https://jobs.ashbyhq.com/Fourier
https://jobs.ashbyhq.com/GPTZero
https://jobs.ashbyhq.com/GoHenry
https://jobs.ashbyhq.com/GradientNetwork
https://jobs.ashbyhq.com/InscribeAI
https://jobs.ashbyhq.com/Jerry
https://jobs.ashbyhq.com/Juicebox
https://jobs.ashbyhq.com/LeanTech
https://jobs.ashbyhq.com/OpenSea
https://jobs.ashbyhq.com/Parkade
https://jobs.ashbyhq.com/Roam
https://jobs.ashbyhq.com/Secoda
https://jobs.ashbyhq.com/Siro
https://jobs.ashbyhq.com/Sonio
https://jobs.ashbyhq.com/Speakeasy
https://jobs.ashbyhq.com/StandardBots
https://jobs.ashbyhq.com/Stepful
https://jobs.ashbyhq.com/Tabs
https://jobs.ashbyhq.com/The-Flex
https://jobs.ashbyhq.com/Vultron
https://jobs.ashbyhq.com/aescape
https://jobs.ashbyhq.com/airapps
https://jobs.ashbyhq.com/airwallex
https://jobs.ashbyhq.com/alan
https://jobs.ashbyhq.com/almedia
https://jobs.ashbyhq.com/altimate
https://jobs.ashbyhq.com/altura
https://jobs.ashbyhq.com/amper
https://jobs.ashbyhq.com/anglehealth
https://jobs.ashbyhq.com/anima
https://jobs.ashbyhq.com/ankorstore
https://jobs.ashbyhq.com/anrok
https://jobs.ashbyhq.com/apify
https://jobs.ashbyhq.com/aptosfoundation
https://jobs.ashbyhq.com/arcade
https://jobs.ashbyhq.com/articul8
https://jobs.ashbyhq.com/artsy
https://jobs.ashbyhq.com/ashby
https://jobs.ashbyhq.com/assembledhq
https://jobs.ashbyhq.com/astera
https://jobs.ashbyhq.com/atob
https://jobs.ashbyhq.com/atroposhealth
https://jobs.ashbyhq.com/auger
https://jobs.ashbyhq.com/august-health
https://jobs.ashbyhq.com/axiom
https://jobs.ashbyhq.com/bankjoy
https://jobs.ashbyhq.com/beam
https://jobs.ashbyhq.com/bedrockocean
https://jobs.ashbyhq.com/benepass
https://jobs.ashbyhq.com/bestow
https://jobs.ashbyhq.com/bettermile
https://jobs.ashbyhq.com/bifrost
https://jobs.ashbyhq.com/blockhouse
https://jobs.ashbyhq.com/blockworks
https://jobs.ashbyhq.com/blueberrypediatrics
https://jobs.ashbyhq.com/boon
https://jobs.ashbyhq.com/botanictonics
https://jobs.ashbyhq.com/brainco
https://jobs.ashbyhq.com/brainly
https://jobs.ashbyhq.com/bratte
https://jobs.ashbyhq.com/bridge
https://jobs.ashbyhq.com/brigit
https://jobs.ashbyhq.com/bunch
https://jobs.ashbyhq.com/cantina
https://jobs.ashbyhq.com/capimoney
https://jobs.ashbyhq.com/captions
https://jobs.ashbyhq.com/carry
https://jobs.ashbyhq.com/casca
https://jobs.ashbyhq.com/centari
https://jobs.ashbyhq.com/character
https://jobs.ashbyhq.com/chronospherejobs
https://jobs.ashbyhq.com/cinder
https://jobs.ashbyhq.com/claylabs
https://jobs.ashbyhq.com/cluely
https://jobs.ashbyhq.com/cohere
https://jobs.ashbyhq.com/cointracker
https://jobs.ashbyhq.com/column
https://jobs.ashbyhq.com/comind
https://jobs.ashbyhq.com/compa
https://jobs.ashbyhq.com/comulate
https://jobs.ashbyhq.com/comun
https://jobs.ashbyhq.com/corti
https://jobs.ashbyhq.com/counsel
https://jobs.ashbyhq.com/count
https://jobs.ashbyhq.com/dakota
https://jobs.ashbyhq.com/dandy
https://jobs.ashbyhq.com/dave
https://jobs.ashbyhq.com/davidenergy
https://jobs.ashbyhq.com/decagon
https://jobs.ashbyhq.com/dedale
https://jobs.ashbyhq.com/deductive
https://jobs.ashbyhq.com/deel
https://jobs.ashbyhq.com/deepwalk
https://jobs.ashbyhq.com/delian
https://jobs.ashbyhq.com/devsavant
https://jobs.ashbyhq.com/dolarapp
https://jobs.ashbyhq.com/doppel
https://jobs.ashbyhq.com/dust
https://jobs.ashbyhq.com/earnedwealth
https://jobs.ashbyhq.com/ekumenlabs
https://jobs.ashbyhq.com/elevenlabs
https://jobs.ashbyhq.com/ema
https://jobs.ashbyhq.com/empora
https://jobs.ashbyhq.com/endex
https://jobs.ashbyhq.com/enode
https://jobs.ashbyhq.com/eotlabs
https://jobs.ashbyhq.com/equi
https://jobs.ashbyhq.com/equip
https://jobs.ashbyhq.com/everai
https://jobs.ashbyhq.com/evertune
https://jobs.ashbyhq.com/fable
https://jobs.ashbyhq.com/farmraise
https://jobs.ashbyhq.com/feathr
https://jobs.ashbyhq.com/fermat
https://jobs.ashbyhq.com/finalis
https://jobs.ashbyhq.com/finary
https://jobs.ashbyhq.com/finch
https://jobs.ashbyhq.com/finvest
https://jobs.ashbyhq.com/fleetpulse
https://jobs.ashbyhq.com/franki
https://jobs.ashbyhq.com/freshpaint
https://jobs.ashbyhq.com/fullstory
https://jobs.ashbyhq.com/g2i
https://jobs.ashbyhq.com/growthtroops
https://jobs.ashbyhq.com/guaranteed
https://jobs.ashbyhq.com/handshake
https://jobs.ashbyhq.com/handspring
https://jobs.ashbyhq.com/harvey
https://jobs.ashbyhq.com/hawk
https://jobs.ashbyhq.com/hcompany
https://jobs.ashbyhq.com/heyjobs
https://jobs.ashbyhq.com/hiive
https://jobs.ashbyhq.com/hims-and-hers
https://jobs.ashbyhq.com/horizon3ai
https://jobs.ashbyhq.com/hotplate
https://jobs.ashbyhq.com/humaans
https://jobs.ashbyhq.com/ideogram
https://jobs.ashbyhq.com/immersivelabs
https://jobs.ashbyhq.com/improbable
https://jobs.ashbyhq.com/integrationapp
https://jobs.ashbyhq.com/invert
https://jobs.ashbyhq.com/january
https://jobs.ashbyhq.com/jigsaw
https://jobs.ashbyhq.com/join9am
https://jobs.ashbyhq.com/joko
https://jobs.ashbyhq.com/julius
https://jobs.ashbyhq.com/junipersquare
https://jobs.ashbyhq.com/keeper
https://jobs.ashbyhq.com/keyrock
https://jobs.ashbyhq.com/kindred
https://jobs.ashbyhq.com/kovo
https://jobs.ashbyhq.com/kraken.com
https://jobs.ashbyhq.com/krea
https://jobs.ashbyhq.com/kustomer
https://jobs.ashbyhq.com/landbase
https://jobs.ashbyhq.com/latitude
https://jobs.ashbyhq.com/leland
https://jobs.ashbyhq.com/letta
https://jobs.ashbyhq.com/lightning
https://jobs.ashbyhq.com/lightspark
https://jobs.ashbyhq.com/lilt
https://jobs.ashbyhq.com/limble
https://jobs.ashbyhq.com/lindushealth
https://jobs.ashbyhq.com/listenlabs
https://jobs.ashbyhq.com/liveflow
https://jobs.ashbyhq.com/lmarena
https://jobs.ashbyhq.com/lucidlink
https://jobs.ashbyhq.com/luma-ai
https://jobs.ashbyhq.com/lunar
https://jobs.ashbyhq.com/mach
https://jobs.ashbyhq.com/mach9
https://jobs.ashbyhq.com/magiceden
https://jobs.ashbyhq.com/magicschool
https://jobs.ashbyhq.com/mainshares
https://jobs.ashbyhq.com/mandolin
https://jobs.ashbyhq.com/mangomint
https://jobs.ashbyhq.com/masabi
https://jobs.ashbyhq.com/mazehq
https://jobs.ashbyhq.com/menlosecurity
https://jobs.ashbyhq.com/metalenz
https://jobs.ashbyhq.com/middesk
https://jobs.ashbyhq.com/mintlify
https://jobs.ashbyhq.com/modernfi
https://jobs.ashbyhq.com/moderntreasury
https://jobs.ashbyhq.com/moego
https://jobs.ashbyhq.com/monarchmoney
https://jobs.ashbyhq.com/mondoo
https://jobs.ashbyhq.com/montecarlodata
https://jobs.ashbyhq.com/mosey
https://jobs.ashbyhq.com/mystenlabs
https://jobs.ashbyhq.com/n8n
https://jobs.ashbyhq.com/netboxlabs
https://jobs.ashbyhq.com/netic
https://jobs.ashbyhq.com/neworbit
https://jobs.ashbyhq.com/niramedical
https://jobs.ashbyhq.com/nomic
https://jobs.ashbyhq.com/notable
https://jobs.ashbyhq.com/numeric
https://jobs.ashbyhq.com/olive
https://jobs.ashbyhq.com/omnea
https://jobs.ashbyhq.com/omniscient
https://jobs.ashbyhq.com/oneapp
https://jobs.ashbyhq.com/onebrief
https://jobs.ashbyhq.com/openai
https://jobs.ashbyhq.com/opengov
https://jobs.ashbyhq.com/oplabs
https://jobs.ashbyhq.com/optery
https://jobs.ashbyhq.com/opusclip
https://jobs.ashbyhq.com/orbitalmaterials
https://jobs.ashbyhq.com/oumi
https://jobs.ashbyhq.com/outliant
https://jobs.ashbyhq.com/pacificfusion
https://jobs.ashbyhq.com/parabola-io
https://jobs.ashbyhq.com/parallel
https://jobs.ashbyhq.com/partiful
https://jobs.ashbyhq.com/partisiablockchain
https://jobs.ashbyhq.com/passage
https://jobs.ashbyhq.com/patreon
https://jobs.ashbyhq.com/peek
https://jobs.ashbyhq.com/phylax
https://jobs.ashbyhq.com/plain
https://jobs.ashbyhq.com/plasmidsaurus
https://jobs.ashbyhq.com/playai
https://jobs.ashbyhq.com/polygon-labs
https://jobs.ashbyhq.com/posthog
https://jobs.ashbyhq.com/primer
https://jobs.ashbyhq.com/privy
https://jobs.ashbyhq.com/projectgrowth
https://jobs.ashbyhq.com/proofofplay
https://jobs.ashbyhq.com/propelus
https://jobs.ashbyhq.com/protege
https://jobs.ashbyhq.com/pylon-labs
https://jobs.ashbyhq.com/quicknode
https://jobs.ashbyhq.com/qventus
https://jobs.ashbyhq.com/raiku
https://jobs.ashbyhq.com/ramp
https://jobs.ashbyhq.com/ravio
https://jobs.ashbyhq.com/reddit
https://jobs.ashbyhq.com/reflectionai
https://jobs.ashbyhq.com/reka
https://jobs.ashbyhq.com/remberg
https://jobs.ashbyhq.com/replit
https://jobs.ashbyhq.com/replo
https://jobs.ashbyhq.com/rilla
https://jobs.ashbyhq.com/rockerbox
https://jobs.ashbyhq.com/rocketsciencegg
https://jobs.ashbyhq.com/rogo
https://jobs.ashbyhq.com/rooser
https://jobs.ashbyhq.com/rula
https://jobs.ashbyhq.com/sardine
https://jobs.ashbyhq.com/scaler
https://jobs.ashbyhq.com/scrollmark
https://jobs.ashbyhq.com/seconddinner
https://jobs.ashbyhq.com/sensmore
https://jobs.ashbyhq.com/sentilink
https://jobs.ashbyhq.com/sesame
https://jobs.ashbyhq.com/siena
https://jobs.ashbyhq.com/silver
https://jobs.ashbyhq.com/skydropx
https://jobs.ashbyhq.com/sleeper
https://jobs.ashbyhq.com/slingshotai
https://jobs.ashbyhq.com/slope
https://jobs.ashbyhq.com/smalls
https://jobs.ashbyhq.com/solace
https://jobs.ashbyhq.com/sona
https://jobs.ashbyhq.com/speak
https://jobs.ashbyhq.com/sprig
https://jobs.ashbyhq.com/stainlessapi
https://jobs.ashbyhq.com/statsig
https://jobs.ashbyhq.com/stealthventurecapitalfirm
https://jobs.ashbyhq.com/stedi
https://jobs.ashbyhq.com/stickermule
https://jobs.ashbyhq.com/stream
https://jobs.ashbyhq.com/suno
https://jobs.ashbyhq.com/supabase
https://jobs.ashbyhq.com/superdial
https://jobs.ashbyhq.com/superduper
https://jobs.ashbyhq.com/surreal
https://jobs.ashbyhq.com/suzy
https://jobs.ashbyhq.com/svix
https://jobs.ashbyhq.com/symbiotic
https://jobs.ashbyhq.com/syndr
https://jobs.ashbyhq.com/synthflow
https://jobs.ashbyhq.com/system2
https://jobs.ashbyhq.com/talentful
https://jobs.ashbyhq.com/tandem
https://jobs.ashbyhq.com/tapcart
https://jobs.ashbyhq.com/taptapsend
https://jobs.ashbyhq.com/tarro
https://jobs.ashbyhq.com/tenex
https://jobs.ashbyhq.com/thatgamecompany
https://jobs.ashbyhq.com/thirstysprout
https://jobs.ashbyhq.com/tonal
https://jobs.ashbyhq.com/traba
https://jobs.ashbyhq.com/tryvital
https://jobs.ashbyhq.com/turnstile
https://jobs.ashbyhq.com/twelve
https://jobs.ashbyhq.com/udisc
https://jobs.ashbyhq.com/uipath
https://jobs.ashbyhq.com/valeriehealth
https://jobs.ashbyhq.com/vanta
https://jobs.ashbyhq.com/vapi
https://jobs.ashbyhq.com/virtahealth
https://jobs.ashbyhq.com/virtuous
https://jobs.ashbyhq.com/vitalize
https://jobs.ashbyhq.com/voladynamics
https://jobs.ashbyhq.com/vooma
https://jobs.ashbyhq.com/wander
https://jobs.ashbyhq.com/warp
https://jobs.ashbyhq.com/waterplan
https://jobs.ashbyhq.com/wayflyer
https://jobs.ashbyhq.com/weave
https://jobs.ashbyhq.com/welltech
https://jobs.ashbyhq.com/winona
https://jobs.ashbyhq.com/withclutch
https://jobs.ashbyhq.com/withpulley
https://jobs.ashbyhq.com/worldlabs
https://jobs.ashbyhq.com/writer
https://jobs.ashbyhq.com/xbowcareers
https://jobs.ashbyhq.com/xoul
https://jobs.ashbyhq.com/yondr
https://jobs.ashbyhq.com/yutori
https://jobs.ashbyhq.com/zapier
https://jobs.ashbyhq.com/zefir
https://jobs.ashbyhq.com/zefr
https://jobs.ashbyhq.com/zencastr
https://jobs.ashbyhq.com/zyphra"""


GLOBAL_KEYWORDS = ['global', 'worldwide', 'anywhere', 'international', 'all locations', 'any location', 'any country']
EMEA_PHRASES = [
    'middle east', 'north africa', 'south africa', 'sub-saharan africa', 'sub saharan africa',
    'united kingdom', 'great britain', 'british isles', 'czech republic', 'saudi arabia',
    'united arab emirates', 'abu dhabi', 'san marino', 'bosnia and herzegovina', 'holy see', 'vatican city', 'isle of man',
    'ivory coast', "cote d'ivoire", 'cape verde', 'equatorial guinea', 'sierra leone',
    'sao tome', 'sao tomé', 'sao tomè', 'sao tome and principe', 'faroe islands', 'channel islands',
    'north macedonia', 'czechia', 'western balkans', 'eastern europe', 'northern europe', 'southern europe', 'central europe',
]

EMEA_SINGLE_TOKENS = {
    'emea','europe','european','eu','eea','schengen','europ','mena','uk','ireland','irish','england','scotland','wales','cymru',
    'london','britain','british','germany','deutschland','france','french','spain','spanish','portugal','portuguese','andorra',
    'iceland','norway','norwegian','sweden','swedish','finland','finnish','denmark','danish','netherlands','dutch','belgium','belgian',
    'luxembourg','luxemburg','switzerland','swiss','liechtenstein','austria','italy','italian','greece','greek','malta','cyprus','turkey','turkiye',
    'poland','polish','czech','slovakia','slovak','hungary','hungarian','romania','romanian','bulgaria','bulgarian','estonia','estonian','latvia','latvian','lithuania','lithuanian',
    'slovenia','slovenian','croatia','croatian','serbia','serbian','bosnia','montenegro','macedonia','kosovo','albania','georgia','georgian','armenia','armenian','azerbaijan','azerbaijani',
    'ukraine','ukrainian','belarus','belarusian','moldova','moldovan','russia','russian','kazakhstan','kazakh','uzbekistan','uzbek',
    'israel','israeli','palestine','palestinian','jordan','jordanian','lebanon','lebanese','qatar','qatari','kuwait','kuwaiti',
    'bahrain','bahraini','oman','omani','uae','dubai','riyadh','jeddah','saudi','mena','egypt','egyptian','morocco','moroccan','tunisia','tunisian','algeria','algerian','libya','libyan',
    'sudan','sudanese','ethiopia','ethiopian','kenya','kenyan','uganda','ugandan','tanzania','tanzanian','rwanda','rwandan','burundi','burundian','ghana','ghanaian','nigeria','nigerian','cameroon','cameroonian',
    'senegal','senegalese','gabon','gabonese','angola','angolan','namibia','namibian','botswana','botswanan','zambia','zambian','zimbabwe','zimbabwean',
    'malawi','malawian','mozambique','mozambican','madagascar','mauritius','mauritian','seychelles','seychellois','lesotho','swazi','eswatini','somalia','somali','djibouti','djiboutian','eritrea','eritrean',
    'benin','beninese','togo','togolese','mali','malian','niger','nigerien','burkina','ivory','ivoire','sierra','leone','gambia','gambian','guinea','guinean','liberia','liberian','mauritania','mauritanian',
    'sahara','saharan','reunion','réunion','comoros','comorian','southafrica','south-africa','southafrican'
}


TOKEN_SPLIT_RE = re.compile(r'[^a-z0-9]+')
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0 Safari/537.36'


def deduplicate_slugs(urls: Iterable[str]) -> List[str]:
    seen = {}
    ordered = []
    for url in urls:
        parsed = urlparse(url)
        slug = parsed.path.strip('/')
        if not slug:
            continue
        key = slug.lower()
        if key not in seen:
            seen[key] = slug
            ordered.append(slug)
    return ordered


def tokenize(text: str) -> set[str]:
    return set(filter(None, TOKEN_SPLIT_RE.split(text.lower())))


def normalize_locations(values: Optional[Iterable]) -> List[str]:
    normalized: List[str] = []
    if not values:
        return normalized
    for item in values:
        if isinstance(item, str):
            normalized.append(item)
        elif isinstance(item, dict):
            for key in ('locationName', 'name', 'displayName', 'label'):
                if item.get(key):
                    normalized.append(item[key])
                    break
    return normalized


def is_remote_location(location: str) -> bool:
    if not location:
        return False
    text = location.lower()
    if 'remote' not in text:
        return False
    tokens = tokenize(location)
    if 'remote' not in tokens and 'remote-' not in text and ' remote' not in text and not text.startswith('remote'):
        return False
    if any(term in text for term in (term.lower() for term in GLOBAL_KEYWORDS)):
        return True
    if any(phrase in text for phrase in (phrase.lower() for phrase in EMEA_PHRASES)):
        return True
    if tokens & EMEA_SINGLE_TOKENS:
        return True
    return False


def extract_app_data(html: str) -> Optional[dict]:
    marker = 'window.__appData = '
    start = html.find(marker)
    if start == -1:
        return None
    start += len(marker)
    depth = 0
    in_string = False
    escape = False
    for idx in range(start, len(html)):
        ch = html[idx]
        if in_string:
            if escape:
                escape = False
            elif ch == '\\':
                escape = True
            elif ch == '"':
                in_string = False
        else:
            if ch == '"':
                in_string = True
            elif ch == '{':
                depth += 1
            elif ch == '}':
                depth -= 1
                if depth == 0:
                    json_str = html[start:idx+1]
                    return json.loads(json_str)
    return None


def fetch_job_board(slug: str) -> Optional[dict]:
    url = f'https://jobs.ashbyhq.com/{slug}'
    try:
        req = Request(url, headers={'User-Agent': USER_AGENT})
        with urlopen(req, timeout=30) as resp:
            html = resp.read().decode('utf-8', errors='replace')
    except (HTTPError, URLError):
        return None
    return extract_app_data(html)


def main() -> None:
    urls = [line.strip() for line in URL_LIST.splitlines() if line.strip()]
    slugs = deduplicate_slugs(urls)
    results = []
    errors = []

    for idx, slug in enumerate(slugs, start=1):
        data = fetch_job_board(slug)
        if not data:
            errors.append({'slug': slug, 'error': 'fetch_failed'})
            continue

        org = data.get('organization') or {}
        org_name = org.get('name') or slug
        job_board = data.get('jobBoard') or {}
        postings = job_board.get('jobPostings') or []
        for posting in postings:
            if not posting.get('isListed', True):
                continue
            primary = posting.get('locationName')
            secondary = normalize_locations(posting.get('secondaryLocations'))
            candidates = [primary] + secondary
            matches = []
            seen_locations = set()
            for loc in candidates:
                if not loc:
                    continue
                key_loc = loc.strip()
                if key_loc in seen_locations:
                    continue
                seen_locations.add(key_loc)
                if is_remote_location(loc):
                    matches.append(loc)
            if matches:
                job_id = posting.get('id')
                results.append({
                    'company_slug': slug,
                    'company_name': org_name,
                    'job_id': job_id,
                    'job_url': f'https://jobs.ashbyhq.com/{slug}/job/{job_id}' if job_id else None,
                    'title': posting.get('title'),
                    'primary_location': primary,
                    'secondary_locations': secondary,
                    'matched_locations': matches,
                    'workplace_type': posting.get('workplaceType'),
                    'employment_type': posting.get('employmentType'),
                    'team_name': posting.get('teamName'),
                    'updated_at': posting.get('updatedAt'),
                })

        if idx % 20 == 0:
            print(f'Processed {idx}/{len(slugs)} company boards...')
        time.sleep(0.15)

    output = {
        'results': results,
        'errors': errors,
        'meta': {
            'total_boards': len(slugs),
            'boards_with_matches': len({item['company_slug'] for item in results}),
            'total_remote_postings': len(results),
        }
    }

    with open('remote_jobs.json', 'w', encoding='utf-8') as fh:
        json.dump(output, fh, ensure_ascii=False, indent=2)

    print(f"Saved {len(results)} postings (errors: {len(errors)}) to remote_jobs.json")


if __name__ == '__main__':
    main()
