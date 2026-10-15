from copy import deepcopy
from datetime import date
from html import escape
from pathlib import Path
from urllib.parse import quote_plus
import base64
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Aura | Centro de Bienestar", page_icon="✦", layout="wide", initial_sidebar_state="collapsed")

LOGO_PATH = Path(__file__).parent / "assets" / "aura-logo.png"
DEFAULT_LOGO = {"mime": "image/png", "data": LOGO_PATH.read_bytes()} if LOGO_PATH.exists() else None

DEFAULT = {
    "business": {
        "name": "AURA",
        "city": "Cali, Colombia",
        "address": "Cali, Colombia",
        "phone": "573102035750",
        "logo": DEFAULT_LOGO,
        "title": "El bienestar también es una forma de volver a ti.",
        "subtitle": "Cuidamos de tu cuerpo y tu calma con tratamientos personalizados para sentirte, verte y vivir mejor.",
        "hero_image": None,
        "gallery": [
            "https://images.unsplash.com/photo-1544161515-4ab6ce6db874?auto=format&fit=crop&w=1000&q=85",
            "https://images.unsplash.com/photo-1519823551278-64ac92734fb1?auto=format&fit=crop&w=1000&q=85",
            "https://images.unsplash.com/photo-1515377905703-c4788e51af15?auto=format&fit=crop&w=1000&q=85",
        ],
    },
    "services": [
        {"id": "fisio", "name": "Fisioterapia", "description": "Movimiento, recuperación y acompañamiento para que vuelvas a sentirte bien.", "minutes": 60, "hours": ["09:00", "10:30", "14:00", "15:30"], "icon": "✦"},
        {"id": "suero", "name": "Sueroterapia", "description": "Una experiencia de bienestar diseñada según tus necesidades.", "minutes": 60, "hours": ["09:00", "11:00", "14:00"], "icon": "✧"},
        {"id": "masaje", "name": "Masajes relajantes", "description": "Una pausa para liberar tensión, reconectar y disfrutar el presente.", "minutes": 60, "hours": ["10:00", "11:30", "15:00", "16:30"], "icon": "◌"},
        {"id": "botox", "name": "Botox", "description": "Armoniza y realza tu expresión con un enfoque natural y profesional.", "minutes": 45, "hours": ["09:00", "10:00", "14:00", "15:00"], "icon": "⌇"},
        {"id": "respira", "name": "Terapia respiratoria", "description": "Cuidado y acompañamiento para respirar mejor y recuperar tu bienestar.", "minutes": 45, "hours": ["09:00", "10:00", "11:00", "14:00"], "icon": "〰"},
    ],
    "bookings": [],
    "blocked": [],
    "blocked_slots": [],
}

if "aura_data" not in st.session_state:
    st.session_state.aura_data = deepcopy(DEFAULT)
st.session_state.aura_data.setdefault("blocked_slots", [])
for business_key, default_value in DEFAULT["business"].items():
    st.session_state.aura_data["business"].setdefault(business_key, deepcopy(default_value))
if "aura_page" not in st.session_state:
    st.session_state.aura_page = "Inicio"
if "aura_admin_ok" not in st.session_state:
    st.session_state.aura_admin_ok = False
if "hero_upload_version" not in st.session_state:
    st.session_state.hero_upload_version = 0
if "gallery_upload_version" not in st.session_state:
    st.session_state.gallery_upload_version = 0
if "logo_upload_version" not in st.session_state:
    st.session_state.logo_upload_version = 0

st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:ital,wght@0,500;0,600;1,500&display=swap');
:root{--ink:#2d332a;--olive:#697258;--sage:#c8cbb6;--cream:#f8f6ef;--sand:#e8e0cf;--gold:#a9925c;--line:rgba(45,51,42,.14)}
#MainMenu,footer,header[data-testid="stHeader"],[data-testid="stToolbar"],[data-testid="stDecoration"],[data-testid="stStatusWidget"],[data-testid="stSidebar"]{display:none!important}
.stApp{background:var(--cream);color:var(--ink);font-family:'DM Sans',sans-serif}.block-container{max-width:1240px;padding:1.2rem 2rem 3.5rem}.stMarkdown p{line-height:1.65}.aura-top{display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid var(--line);padding:4px 0 15px;margin-bottom:17px}.aura-logo{display:flex;align-items:center;gap:10px;color:var(--ink);min-width:0}.aura-seal{width:35px;height:38px;border:1px solid var(--gold);border-radius:55% 0 55% 0;transform:rotate(-25deg);display:grid;place-items:center;color:var(--olive);font:20px Georgia,serif;flex:none}.brand-mark{width:150px;height:58px;object-fit:contain;flex:none}.aura-word{font:600 22px 'Playfair Display',serif;letter-spacing:2px;line-height:1.05;text-transform:uppercase;overflow-wrap:anywhere}.aura-word small{display:block;font:6px 'DM Sans',sans-serif;letter-spacing:2px;text-transform:uppercase;margin-top:6px}.aura-location{font-size:10px;letter-spacing:1.7px;text-transform:uppercase;color:var(--olive)}
.eyebrow{font-size:10px!important;letter-spacing:2px!important;text-transform:uppercase;color:var(--olive)!important;font-weight:700!important;margin:0 0 16px!important}.hero-title{font:500 clamp(44px,5.15vw,68px)/1.04 'Playfair Display',Georgia,serif;letter-spacing:-2px;color:var(--ink);margin:0}.hero-title em,.section-title em,.location-title em{font-weight:500;color:var(--gold)}.hero-copy{font-size:15px;color:#62665b;max-width:460px;margin:22px 0 22px}.hero-art{height:438px;position:relative;overflow:hidden;background:linear-gradient(145deg,#d9d7c8,#b4b59f);background-size:cover;background-position:center}.hero-sun{position:absolute;width:275px;height:275px;border-radius:50%;background:#dfc58c;right:-45px;top:-53px;opacity:.6}.hero-arch{position:absolute;width:265px;height:360px;border:45px solid #f2eedf;border-bottom:0;border-radius:150px 150px 0 0;bottom:0;left:18%}.hero-leaf{position:absolute;right:47px;bottom:47px;width:73px;height:165px;border-radius:100% 0 100% 0;background:#697258;transform:rotate(-37deg);opacity:.9}.hero-leaf.second{right:112px;bottom:17px;width:58px;height:125px;background:#879178;transform:rotate(32deg)}.hero-art-card{position:absolute;left:0;bottom:0;background:#fcfaf3;color:var(--olive);padding:22px 26px;width:56%;font:italic 30px 'Playfair Display',serif}.hero-art-card small{display:block;font:9px 'DM Sans',sans-serif;letter-spacing:1.5px;text-transform:uppercase;margin-top:7px}
.stButton>button,.stLinkButton>a{background:var(--olive)!important;border:1px solid var(--olive)!important;color:#fff!important;border-radius:0!important;min-height:43px;font:500 13px 'DM Sans',sans-serif!important;padding:.55rem 1.15rem!important;transition:all .2s ease}.stButton>button:hover,.stLinkButton>a:hover{background:var(--ink)!important;border-color:var(--ink)!important;transform:translateY(-1px)}.nav-button .stButton>button{background:transparent!important;border-color:transparent!important;color:var(--ink)!important;padding:.35rem .55rem!important;min-height:36px}.nav-button .stButton>button:hover,.nav-active .stButton>button{border-bottom:1px solid var(--olive)!important;background:transparent!important;color:var(--olive)!important;transform:none}.hero-note{font-size:11px;color:#666a60;margin-top:26px}.section-title{font:500 clamp(35px,4vw,54px)/1.07 'Playfair Display',Georgia,serif;letter-spacing:-1.4px;color:var(--ink);margin:0 0 19px}.section-copy{font-size:13px;color:#696d62;max-width:360px}.intro-band{background:#ebe7d9;padding:42px 38px;margin:53px 0}.intro-band h2{font:500 clamp(35px,4vw,52px)/1.06 'Playfair Display',Georgia,serif;margin:0}.intro-band h2 em{color:var(--gold)}.intro-copy{max-width:590px;color:#63675c;font-size:14px;margin:15px 0}.stat{border-left:1px solid var(--line);padding-left:18px}.stat strong{display:block;font:500 21px 'Playfair Display',serif}.stat span{display:block;font-size:9px;letter-spacing:1px;text-transform:uppercase;color:#77796f;margin-top:4px}
.service-card{background:#eff0e8;min-height:278px;padding:23px 22px 20px;display:flex;flex-direction:column}.service-card.warm{background:#e5ddcf}.service-card.olive{background:var(--olive);color:white}.service-number{font-size:9px;letter-spacing:1px;opacity:.7}.service-icon{font:31px 'Playfair Display',serif;color:var(--gold);margin:15px 0 8px}.service-card h3{font:500 23px 'Playfair Display',serif;margin:0 0 9px}.service-card p{font-size:12px;line-height:1.55;color:#63675c;min-height:56px}.service-card.olive p{color:#eef0e7}.service-card .duration{font-size:10px;color:inherit;opacity:.75;margin-top:auto}.service-card .stButton{margin-top:8px}.services-note{font-size:11px;color:#77796f;margin-top:14px}.ritual-band{background:#d3d5c5;padding:0}.ritual-copy{padding:35px 8%}.ritual-copy p{font-size:13px;color:#5f6657;max-width:400px}.ritual-photo{min-height:380px;background-position:center;background-size:cover;position:relative}.ritual-caption{position:absolute;bottom:0;left:0;background:rgba(45,51,42,.7);color:#fff;font:italic 29px 'Playfair Display',serif;padding:18px 25px}.gallery-photo{height:280px;object-fit:cover;width:100%;display:block}.gallery-placeholder{height:280px;background:linear-gradient(145deg,#e4dfd0,#c8cbb6);display:grid;place-items:center;color:var(--olive);font:italic 24px 'Playfair Display',serif}.contact-band{background:var(--olive);color:white;text-align:center;padding:61px 24px}.contact-band h2{font:500 clamp(37px,4.7vw,58px)/1.07 'Playfair Display',serif;max-width:700px;margin:0 auto 16px}.contact-band h2 em{color:#f1dfb9}.contact-band p{font-size:13px;color:#eef0e5}.location-title{font:500 clamp(32px,3.5vw,46px)/1.08 'Playfair Display',serif;margin:0}.map-frame{width:100%;height:345px;border:0;filter:grayscale(.5) saturate(.7)}.aura-footer{display:flex;justify-content:space-between;align-items:center;padding:28px 0;color:#77796e;font-size:10px;border-top:1px solid var(--line);margin-top:28px}.aura-footer a{color:var(--olive)}
.booking-panel,.admin-panel{background:#fffdf8;padding:30px;border:1px solid rgba(45,51,42,.08)}.subtle{font-size:12px;color:#75786e}.stTextInput input,.stTextArea textarea,.stSelectbox div[data-baseweb="select"]>div,.stDateInput input,.stNumberInput input{border-radius:0!important;border-color:#d9d8ce!important;background:#fffdf8!important}.stTabs [data-baseweb="tab-list"]{gap:9px;border-bottom:1px solid var(--line)}.stTabs [data-baseweb="tab"]{font-size:12px;color:#686c62}.stTabs [aria-selected="true"]{color:var(--olive)!important}.admin-heading{font:500 42px 'Playfair Display',serif}.admin-card{background:#fffdf8;padding:20px 22px;border:1px solid #e7e4da;margin-bottom:11px}.admin-card h3{font:500 19px 'Playfair Display',serif;margin:0 0 5px}.admin-card p{font-size:11px;color:#74776d;margin:0}.admin-login{max-width:470px;margin:55px auto;background:#fffdf8;padding:37px}.stFileUploader section{background:#fffdf8;border:1px dashed #b7b9a6;border-radius:0}.stAlert{border-radius:0}
@media(max-width:760px){.block-container{padding:.8rem 1rem 2rem}.aura-top{align-items:flex-start}.aura-location{display:none}.hero-art{height:340px;margin-top:20px}.hero-title{font-size:45px;letter-spacing:-1px}.intro-band{padding:30px 22px;margin:35px 0}.service-card{min-height:245px;padding:18px 15px}.service-card h3{font-size:20px}.service-card p{font-size:11px}.ritual-photo{min-height:290px}.ritual-copy{padding:28px 22px}.gallery-photo,.gallery-placeholder{height:190px}.map-frame{height:285px}.aura-footer{display:block;line-height:1.8}.nav-button .stButton>button{padding:.3rem .25rem!important;font-size:11px!important}}
/* Streamlit widgets stay inside their own blocks, so style their actual blocks. */
div[data-testid="stHorizontalBlock"]:has(>div[data-testid="column"]:nth-child(5)) .stButton>button{background:transparent!important;border:0!important;border-bottom:1px solid transparent!important;color:var(--ink)!important;padding:.3rem .25rem!important;min-height:35px}
div[data-testid="stHorizontalBlock"]:has(>div[data-testid="column"]:nth-child(5)) .stButton>button:hover{border-bottom-color:var(--olive)!important;background:transparent!important;color:var(--olive)!important;transform:none}
.intro-band{display:grid;grid-template-columns:1.1fr 1fr;gap:44px;align-items:center}
.intro-copy{margin:15px 0 23px}.stats-row{display:flex;gap:28px}.stat{padding-left:15px}.stat strong{font-size:19px}
[data-testid="stForm"]{background:#fffdf8;padding:22px 25px;border:1px solid rgba(45,51,42,.08)}[data-testid="stTabsContent"]{padding-top:20px}
@media(max-width:760px){.intro-band{display:block}.stats-row{gap:15px}div[data-testid="stHorizontalBlock"]:has(>div[data-testid="column"]:nth-child(5)) .stButton>button{padding:.3rem .15rem!important;font-size:10px!important}}
.site-header{display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid var(--line);padding:5px 0 16px;margin-bottom:35px}.site-nav{display:flex;align-items:center;gap:28px}.site-nav a{font-size:13px;color:var(--ink);text-decoration:none;padding:9px 0;border-bottom:1px solid transparent}.site-nav a:hover,.site-nav a.active{color:var(--olive);border-bottom-color:var(--olive)}.site-nav a.nav-cta{background:var(--olive);color:white;border:1px solid var(--olive);padding:10px 16px}.site-nav a.nav-cta:hover{background:var(--ink)}.contact-link{display:inline-flex;align-items:center;justify-content:center;margin-top:18px;padding:12px 22px;background:#f4f0e6;color:var(--ink);text-decoration:none;font-size:12px}.contact-link:hover{background:#fff}
@media(max-width:760px){.site-header{align-items:flex-start;gap:15px;flex-direction:column;margin-bottom:24px}.site-nav{gap:15px;flex-wrap:wrap}.site-nav a{font-size:12px}.site-nav a.nav-cta{padding:8px 12px}}
@media(max-width:760px){.brand-mark{width:130px;height:50px}}
.contact-link{display:inline-flex;align-items:center;justify-content:center;margin-top:18px;padding:12px 22px;background:#f4f0e6;color:var(--ink);text-decoration:none;font-size:12px}.contact-link:hover{background:#fff}[data-testid="stImage"] img{width:100%;height:265px;object-fit:cover}
.hero-secondary{display:inline-block;color:var(--ink);font-size:12px;text-decoration:none;border-bottom:1px solid var(--ink);padding:8px 0 5px}.hero-secondary:hover{color:var(--olive);border-color:var(--olive)}
@media(max-width:760px){[data-testid="stImage"] img{height:185px}}
div[data-testid="stRadio"]>label{display:none}div[data-testid="stRadio"] div[role="radiogroup"]{display:flex;justify-content:flex-end;gap:clamp(10px,2vw,28px);flex-wrap:wrap}div[data-testid="stRadio"] div[role="radiogroup"] label{padding:8px 0!important;border-bottom:1px solid transparent;color:var(--ink)!important;background:transparent!important;font-size:12px!important}div[data-testid="stRadio"] div[role="radiogroup"] label>div:first-child{display:none!important}div[data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked){color:var(--olive)!important;border-bottom-color:var(--olive)}
</style>""", unsafe_allow_html=True)


def go_to(page, service_id=None):
    st.session_state.aura_page = page
    if service_id:
        st.session_state.selected_service = service_id
        service = next((item for item in st.session_state.aura_data["services"] if item["id"] == service_id), None)
        if service:
            st.session_state.booking_service = service["name"]


def business():
    return st.session_state.aura_data["business"]


def image_src(image, fallback=""):
    if isinstance(image, dict) and image.get("data"):
        encoded = base64.b64encode(image["data"]).decode("ascii")
        return f"data:{image.get('mime', 'image/jpeg')};base64,{encoded}"
    if isinstance(image, str) and image:
        return image
    return fallback


def title_markup(text):
    safe_text = escape(text)
    target = "volver a ti."
    return safe_text.replace(target, f"<em>{target}</em>")


def normalize_hours(value):
    valid = []
    for item in value.split(","):
        item = item.strip()
        try:
            hour_text, minute_text = item.split(":", 1)
            hour, minute = int(hour_text), int(minute_text)
            if len(hour_text) == 2 and len(minute_text) == 2 and 0 <= hour < 24 and 0 <= minute < 60:
                valid.append(f"{hour:02d}:{minute:02d}")
        except (ValueError, TypeError):
            continue
    return sorted(set(valid))


def minutes_after_midnight(value):
    hour, minute = value.split(":", 1)
    return int(hour) * 60 + int(minute)


def header():
    logo_column, nav_column = st.columns([1.2, 2.8], vertical_alignment="center")
    with logo_column:
        b = business()
        logo = image_src(b.get("logo"))
        if logo:
            mark = f"<img class='brand-mark' src='{logo}' alt='Logo de {escape(b['name'])}'>"
            st.markdown(f"<div class='aura-logo'>{mark}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='aura-logo'><span class='aura-seal'>✦</span><span class='aura-word'>{escape(b['name'])}<small>Centro de bienestar</small></span></div>", unsafe_allow_html=True)
    with nav_column:
        st.radio("Navegación", ["Inicio", "Servicios", "Reservar", "Administrar"], horizontal=True, label_visibility="collapsed", key="aura_page")
    st.markdown("<div class='aura-top'></div>", unsafe_allow_html=True)


def hero_art():
    image = image_src(business().get("hero_image"))
    photo_layer = f"background-image:linear-gradient(145deg,rgba(217,215,200,.42),rgba(180,181,159,.28)),url('{image}');" if image else ""
    return f"""<div class='hero-art' style='{photo_layer}'><div class='hero-sun'></div><div class='hero-arch'></div><div class='hero-leaf'></div><div class='hero-leaf second'></div><div class='hero-art-card'>respira en calma<small>un momento para ti</small></div></div>"""


def public_page():
    data = st.session_state.aura_data
    b = data["business"]
    left, right = st.columns([1.05, .95], gap="large", vertical_alignment="center")
    with left:
        st.markdown(f"<p class='eyebrow'>{escape(b['city'])} · Tu espacio de bienestar</p><h1 class='hero-title'>{title_markup(b['title'])}</h1><p class='hero-copy'>{escape(b['subtitle'])}</p>", unsafe_allow_html=True)
        action, secondary = st.columns([1, 1.25], gap="small")
        with action:
            st.button("Agenda tu cita  ↗", key="hero_book", on_click=go_to, args=("Reservar",), use_container_width=True)
        with secondary:
            st.markdown(f"<a class='hero-secondary' href='https://wa.me/{escape(b['phone'])}?text={quote_plus('Hola Aura, quiero agendar una cita.')}' target='_blank' rel='noreferrer'>Escríbenos por WhatsApp&nbsp; ↗</a>", unsafe_allow_html=True)
        st.markdown("<p class='hero-note'>♡ &nbsp; Atención cercana y personalizada</p>", unsafe_allow_html=True)
    with right:
        st.markdown(hero_art(), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"<div class='intro-band'><div><p class='eyebrow'>Bienvenidos a {escape(b['name'])}</p><h2>Un espacio creado para <em>cuidar de ti.</em></h2></div><div><p class='intro-copy'>Creemos que el bienestar se construye en los pequeños momentos: cuando escuchas tu cuerpo, respiras con tranquilidad y eliges cuidarte.</p><div class='stats-row'><div class='stat'><strong>Atención</strong><span>personalizada</span></div><div class='stat'><strong>Bienestar</strong><span>integral</span></div><div class='stat'><strong>Cali</strong><span>Colombia</span></div></div></div></div>", unsafe_allow_html=True)

    st.markdown("<p class='eyebrow'>Nuestros servicios</p><h2 class='section-title'>Lo que tu cuerpo necesita, <em>en un solo lugar.</em></h2>", unsafe_allow_html=True)
    st.markdown("<p class='section-copy'>Te acompañamos a elegir el servicio más adecuado para tu momento.</p>", unsafe_allow_html=True)
    services = data["services"]
    for start in range(0, len(services), 3):
        visible_services = services[start:start + 3]
        if len(visible_services) == 2:
            all_columns = st.columns([.5, 1, 1, .5], gap="small")
            row = all_columns[1:3]
        else:
            row = st.columns(3, gap="small")
        for index, (col, service) in enumerate(zip(row, visible_services), start=start):
            with col:
                tone = "olive" if index == 0 else ("warm" if index in (1, 4) else "")
                st.markdown(f"<div class='service-card {tone}'><span class='service-number'>0{index+1}</span><span class='service-icon'>{escape(service.get('icon','✦'))}</span><h3>{escape(service['name'])}</h3><p>{escape(service['description'])}</p><span class='duration'>Sesión de {service['minutes']} minutos</span></div>", unsafe_allow_html=True)
                st.button("Conocer y reservar  →", key=f"service_{service['id']}", use_container_width=True, on_click=go_to, args=("Reservar", service["id"]))
    st.markdown("<p class='services-note'>Los tratamientos se realizan previa valoración profesional cuando corresponda.</p><br>", unsafe_allow_html=True)

    ritual_photo = image_src(b.get("gallery", [None, None, None])[0] if b.get("gallery") else None, "https://images.unsplash.com/photo-1540555700478-4be289fbecef?auto=format&fit=crop&w=1200&q=85")
    photo, copy_col = st.columns([1, 1], gap="small", vertical_alignment="center")
    with photo:
        st.markdown(f"<div class='ritual-photo' style=\"background-image:linear-gradient(0deg,rgba(35,42,32,.26),transparent),url('{ritual_photo}')\"><div class='ritual-caption'>Tu bienestar<br>es la prioridad</div></div>", unsafe_allow_html=True)
    with copy_col:
        st.markdown("<div class='ritual-copy'><p class='eyebrow'>Tu momento Aura</p><h2 class='section-title'>Haz de tu cuidado un <em>ritual.</em></h2><p>Cada visita comienza con escuchar lo que necesitas. Estamos aquí para acompañarte con atención, calidez y profesionalismo.</p></div>", unsafe_allow_html=True)
        st.button("Quiero agendar  ↗", key="ritual_book", on_click=go_to, args=("Reservar",))

    st.markdown("<br><p class='eyebrow'>Nuestro espacio</p><h2 class='section-title'>Un lugar pensado para tu <em>bienestar.</em></h2>", unsafe_allow_html=True)
    gallery = b.get("gallery", [])
    gallery_cols = st.columns(3, gap="small")
    for index, col in enumerate(gallery_cols):
        with col:
            if index < len(gallery) and gallery[index]:
                st.image(gallery[index]["data"] if isinstance(gallery[index], dict) else gallery[index], use_container_width=True)
            else:
                st.markdown("<div class='gallery-placeholder'>un momento para ti</div>", unsafe_allow_html=True)

    st.markdown(f"<br><div class='contact-band'><p class='eyebrow' style='color:#e8dbc0'>Hablemos</p><h2>Regálate un momento para <em>sentirte bien.</em></h2><p>Escríbenos para resolver tus preguntas y agendar tu cita.</p><a class='contact-link' href='https://wa.me/{escape(b['phone'])}?text={quote_plus('Hola Aura, quiero agendar una cita.')}' target='_blank' rel='noreferrer'>Hablar por WhatsApp&nbsp; ↗</a></div>", unsafe_allow_html=True)

    st.markdown(f"<br><p class='eyebrow'>Encuéntranos</p><h2 class='location-title'>Estamos en <em>{escape(b['address'])}.</em></h2><p class='section-copy'>Visítanos y regálate un momento para cuidar de ti.</p>", unsafe_allow_html=True)
    map_query = quote_plus(b["address"] or b["city"])
    components.html(f'<iframe title="Ubicación de Aura" width="100%" height="345" style="border:0;filter:grayscale(.5) saturate(.7)" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://www.google.com/maps?q={map_query}&output=embed"></iframe>', height=355, scrolling=False)
    st.markdown(f"<div class='aura-footer'><span>{escape(b['name'])} · Centro de Bienestar</span><span>{escape(b['city'])} · Un espacio para cuidarte</span><span>© {escape(b['name'])}</span></div>", unsafe_allow_html=True)


def booking_page():
    data = st.session_state.aura_data
    st.markdown(f"<p class='eyebrow'>Agenda tu momento {escape(data['business']['name'])}</p><h1 class='section-title'>Elige un servicio y encuentra tu <em>mejor momento.</em></h1><p class='section-copy'>Selecciona el servicio y un horario disponible. Te contactaremos para confirmar.</p>", unsafe_allow_html=True)
    services = data["services"]
    service_names = [service["name"] for service in services]
    preferred = st.session_state.get("selected_service")
    default_index = next((i for i, s in enumerate(services) if s["id"] == preferred), 0)
    selected_name = st.selectbox("¿Qué servicio deseas?", service_names, index=default_index, key="booking_service")
    selected = next(service for service in services if service["name"] == selected_name)
    col_date, col_time = st.columns(2)
    with col_date:
        chosen_date = st.date_input("Fecha", min_value=date.today(), key="booking_date")
    chosen_iso = chosen_date.isoformat()
    is_blocked = chosen_iso in data["blocked"]
    busy_intervals = [(minutes_after_midnight(booking["time"]), minutes_after_midnight(booking["time"]) + int(booking.get("minutes", 45))) for booking in data["bookings"] if booking["date"] == chosen_iso and booking["status"] != "Cancelada"]
    blocked_for_service = {slot["time"] for slot in data["blocked_slots"] if slot["date"] == chosen_iso and slot["service_id"] == selected["id"]}
    available = []
    if not is_blocked:
        for hour in selected["hours"]:
            start = minutes_after_midnight(hour)
            end = start + int(selected["minutes"])
            if hour not in blocked_for_service and all(end <= busy_start or start >= busy_end for busy_start, busy_end in busy_intervals):
                available.append(hour)
    with col_time:
        chosen_time = st.selectbox("Hora", available or (["Día no disponible"] if is_blocked else ["No hay horarios disponibles"]), disabled=not available, key="booking_time")
    if is_blocked:
        st.warning("Ese día no está disponible para reservas.")
    elif not available:
        st.info("No quedan horarios para esa fecha. Prueba otro día.")
    with st.form("client_booking", clear_on_submit=False):
        col_name, col_phone = st.columns(2)
        with col_name:
            client_name = st.text_input("Tu nombre", placeholder="Nombre completo")
        with col_phone:
            client_phone = st.text_input("WhatsApp", placeholder="Ej. 300 000 0000")
        notes = st.text_area("¿Quieres dejarnos un mensaje?", placeholder="Cuéntanos si tienes alguna preferencia", height=90)
        submitted = st.form_submit_button("Solicitar cita  ↗", use_container_width=True)
    if submitted:
        if not client_name.strip() or not client_phone.strip():
            st.error("Por favor escribe tu nombre y WhatsApp para solicitar la cita.")
        elif not available:
            st.error("No hay horarios disponibles para ese día. Elige otra fecha.")
        else:
            booking = {"id": f"{date.today().isoformat()}-{len(data['bookings'])+1}", "service_id": selected["id"], "service": selected["name"], "minutes": int(selected["minutes"]), "date": chosen_iso, "time": chosen_time, "name": client_name.strip(), "phone": client_phone.strip(), "notes": notes.strip(), "status": "Pendiente"}
            data["bookings"].append(booking)
            st.success("¡Recibimos tu solicitud! Aura se comunicará contigo para confirmar la cita.")
            st.link_button("Continuar por WhatsApp", f"https://wa.me/{data['business']['phone']}?text={quote_plus('Hola Aura, solicité una cita para ' + selected['name'] + ' el ' + chosen_iso + ' a las ' + chosen_time + '.')}")


def admin_page():
    if not st.session_state.aura_admin_ok:
        st.markdown("<div class='admin-login'><p class='eyebrow'>Panel privado</p><h1 class='admin-heading'>Bienvenida a tu agenda.</h1><p class='subtle'>Administra los servicios, fotos y solicitudes desde este espacio.</p></div>", unsafe_allow_html=True)
        with st.form("admin_login"):
            password = st.text_input("Contraseña de demostración", type="password")
            login = st.form_submit_button("Entrar al panel", use_container_width=True)
        st.caption("Contraseña de demostración: aura2026")
        if login:
            if password == "aura2026":
                st.session_state.aura_admin_ok = True
                st.rerun()
            else:
                st.error("La contraseña no coincide.")
        return

    st.markdown(f"<p class='eyebrow'>Administración</p><h1 class='admin-heading'>Tu espacio {escape(business()['name'])}.</h1><p class='subtle'>Organiza tus citas, disponibilidad y la información que ven tus clientes.</p>", unsafe_allow_html=True)
    agenda_tab, services_tab, content_tab = st.tabs(["Agenda de citas", "Servicios y horarios", "Página e imágenes"])
    data = st.session_state.aura_data
    with agenda_tab:
        block_col, action_col = st.columns([1, 1], vertical_alignment="bottom")
        with block_col:
            block_date = st.date_input("Bloquear un día", min_value=date.today(), key="admin_block_date")
        with action_col:
            if st.button("Bloquear fecha", key="admin_block_button"):
                if block_date.isoformat() not in data["blocked"]:
                    data["blocked"].append(block_date.isoformat())
                    st.success("Ese día quedó bloqueado para reservas.")
        st.caption("Fechas bloqueadas: " + (" · ".join(sorted(data["blocked"])) or "ninguna"))
        if data["blocked"]:
            unblock_col, unblock_button_col = st.columns([2, 1], vertical_alignment="bottom")
            with unblock_col:
                unblock_day = st.selectbox("Desbloquear fecha", sorted(data["blocked"]), key="unblock_day")
            with unblock_button_col:
                if st.button("Volver a abrir", key="unblock_day_button"):
                    data["blocked"].remove(unblock_day)
                    st.rerun()
        st.markdown("### Bloquear un horario por servicio")
        slot_service_col, slot_date_col, slot_time_col = st.columns([1.2, 1, 1])
        with slot_service_col:
            slot_service_name = st.selectbox("Actividad", [service["name"] for service in data["services"]], key="slot_block_service")
        slot_service = next(service for service in data["services"] if service["name"] == slot_service_name)
        with slot_date_col:
            slot_date = st.date_input("Fecha", min_value=date.today(), key="slot_block_date")
        with slot_time_col:
            slot_time = st.selectbox("Hora", slot_service["hours"] or ["Sin horarios"], key="slot_block_time", disabled=not slot_service["hours"])
        if st.button("Bloquear este horario", key="block_service_slot"):
            entry = {"service_id": slot_service["id"], "service": slot_service["name"], "date": slot_date.isoformat(), "time": slot_time}
            if slot_time != "Sin horarios" and entry not in data["blocked_slots"]:
                data["blocked_slots"].append(entry)
                st.success("Horario bloqueado para esa actividad.")
        if data["blocked_slots"]:
            st.caption("Bloqueos puntuales: " + " · ".join(f"{slot['date']} · {slot['service']} · {slot['time']}" for slot in data["blocked_slots"]))
            remove_slot = st.selectbox("Quitar bloqueo puntual", range(len(data["blocked_slots"])), format_func=lambda index: f"{data['blocked_slots'][index]['date']} · {data['blocked_slots'][index]['service']} · {data['blocked_slots'][index]['time']}", key="remove_slot_select")
            if st.button("Quitar bloqueo", key="remove_slot_button"):
                data["blocked_slots"].pop(remove_slot)
                st.rerun()
        st.markdown("### Vista del calendario")
        agenda_day = st.date_input("Ver disponibilidad de esta fecha", min_value=date.today(), key="agenda_day")
        agenda_iso = agenda_day.isoformat()
        day_appointments = sorted((booking for booking in data["bookings"] if booking["date"] == agenda_iso and booking["status"] != "Cancelada"), key=lambda item: item["time"])
        if agenda_iso in data["blocked"]:
            st.warning("La fecha está bloqueada.")
        elif day_appointments:
            st.markdown("**Citas de ese día**")
            for appointment in day_appointments:
                st.markdown(f"`{escape(appointment['time'])}` · {escape(appointment['service'])} · {escape(appointment['name'])} · {escape(appointment['status'])}")
        else:
            st.info("No hay citas para esa fecha todavía.")
        st.markdown("**Horarios disponibles por actividad**")
        busy_intervals = [(minutes_after_midnight(item["time"]), minutes_after_midnight(item["time"]) + int(item.get("minutes", 45))) for item in day_appointments]
        for service in data["services"]:
            blocked_for_service = {slot["time"] for slot in data["blocked_slots"] if slot["date"] == agenda_iso and slot["service_id"] == service["id"]}
            free_hours = [] if agenda_iso in data["blocked"] else [hour for hour in service["hours"] if hour not in blocked_for_service and all(minutes_after_midnight(hour) + int(service["minutes"]) <= busy_start or minutes_after_midnight(hour) >= busy_end for busy_start, busy_end in busy_intervals)]
            st.caption(f"{service['name']} · {service['minutes']} min · " + (", ".join(free_hours) if free_hours else "sin horarios libres"))
        st.markdown("### Solicitudes recibidas")
        if not data["bookings"]:
            st.info("Todavía no hay citas. Las solicitudes aparecerán aquí.")
        for booking in sorted(data["bookings"], key=lambda item: (item["date"], item["time"])):
            st.markdown(f"<div class='admin-card'><h3>{escape(booking['name'])} · {escape(booking['service'])}</h3><p>{escape(booking['date'])} a las {escape(booking['time'])} · WhatsApp: {escape(booking['phone'])} · Estado: {escape(booking['status'])}</p><p>{escape(booking.get('notes',''))}</p></div>", unsafe_allow_html=True)
            confirm_col, cancel_col, _ = st.columns([1, 1, 5])
            with confirm_col:
                st.button("Confirmar", key=f"confirm_{booking['id']}", on_click=set_booking_status, args=(booking["id"], "Confirmada"))
            with cancel_col:
                st.button("Cancelar", key=f"cancel_{booking['id']}", on_click=set_booking_status, args=(booking["id"], "Cancelada"))

    with services_tab:
        st.markdown("<p class='subtle'>Ajusta cuánto dura cada actividad y en qué horas se puede reservar.</p>", unsafe_allow_html=True)
        names = [service["name"] for service in data["services"]]
        selected_name = st.selectbox("Servicio para editar", names, key="edit_service_select")
        selected = next(service for service in data["services"] if service["name"] == selected_name)
        with st.form("service_edit"):
            service_name = st.text_input("Nombre del servicio", selected["name"], key=f"edit_name_{selected['id']}")
            duration = st.number_input("Duración en minutos", min_value=15, max_value=240, step=15, value=int(selected["minutes"]), key=f"edit_duration_{selected['id']}")
            description = st.text_area("Descripción pública", selected["description"], key=f"edit_description_{selected['id']}")
            hours_text = st.text_input("Horas disponibles", ", ".join(selected["hours"]), help="Escribe horas HH:MM separadas por coma. Se repiten cada día no bloqueado; puedes cerrar fechas u horas puntuales desde la agenda.", key=f"edit_hours_{selected['id']}")
            update_service = st.form_submit_button("Guardar servicio")
        if update_service:
            selected["name"] = service_name.strip()
            selected["minutes"] = int(duration)
            selected["description"] = description.strip()
            selected["hours"] = normalize_hours(hours_text)
            st.success("Servicio actualizado." if selected["hours"] else "Servicio guardado sin horarios. Revisa el formato HH:MM para habilitar reservas.")
        with st.form("new_service"):
            st.markdown("#### Añadir otra actividad")
            new_name = st.text_input("Nombre", key="new_service_name")
            new_description = st.text_input("Descripción", key="new_service_description")
            new_duration = st.number_input("Duración en minutos", min_value=15, max_value=240, step=15, value=60, key="new_service_duration")
            new_hours = st.text_input("Horas disponibles", "09:00, 10:00, 14:00", key="new_service_hours")
            create_service = st.form_submit_button("Añadir servicio")
        if create_service:
            if new_name.strip():
                data["services"].append({"id": f"service-{len(data['services'])+1}", "name": new_name.strip(), "description": new_description.strip(), "minutes": int(new_duration), "hours": normalize_hours(new_hours), "icon": "✦"})
                st.success("Nueva actividad añadida.")
            else:
                st.error("Escribe el nombre del servicio.")

    with content_tab:
        b = data["business"]
        st.markdown("<p class='subtle'>Actualiza el nombre, el logo y los datos que aparecen en la web pública.</p>", unsafe_allow_html=True)
        with st.form("business_content"):
            company_name = st.text_input("Nombre de la empresa", b["name"])
            city = st.text_input("Ciudad", b["city"])
            address = st.text_input("Dirección del centro para el mapa", b["address"])
            phone = st.text_input("WhatsApp con indicativo de país", b["phone"])
            title = st.text_input("Título principal", b["title"])
            subtitle = st.text_area("Texto de presentación", b["subtitle"])
            save_content = st.form_submit_button("Guardar información")
        if save_content:
            if company_name.strip():
                b.update({"name": company_name.strip(), "city": city.strip(), "address": address.strip(), "phone": phone.strip().replace("+", "").replace(" ", ""), "title": title.strip(), "subtitle": subtitle.strip()})
                st.success("Información actualizada.")
            else:
                st.error("El nombre de la empresa no puede quedar vacío.")
        logo_upload = st.file_uploader("Logo de la empresa", type=["png", "jpg", "jpeg", "webp"], key=f"logo_upload_{st.session_state.logo_upload_version}", help="Idealmente usa PNG con fondo transparente o una imagen cuadrada. El logo aparece junto al nombre en la página pública.")
        if logo_upload is not None:
            b["logo"] = {"mime": logo_upload.type, "data": logo_upload.getvalue()}
            st.success("Logo actualizado en esta sesión.")
        if b.get("logo"):
            st.image(b["logo"]["data"], caption="Vista previa del logo", width=260)
            st.button("Quitar logo", key="remove_logo", on_click=clear_logo)
        hero_upload = st.file_uploader("Foto de portada (opcional)", type=["jpg", "jpeg", "png", "webp"], key=f"hero_upload_{st.session_state.hero_upload_version}")
        if hero_upload is not None:
            b["hero_image"] = {"mime": hero_upload.type, "data": hero_upload.getvalue()}
            st.success("Foto de portada cargada para esta sesión.")
        if b.get("hero_image"):
            st.image(b["hero_image"]["data"], caption="Vista previa de portada", width=320)
        if b.get("hero_image"):
            st.button("Quitar foto de portada", key="remove_hero", on_click=clear_hero)
        gallery_uploads = st.file_uploader("Fotos del centro", type=["jpg", "jpeg", "png", "webp"], accept_multiple_files=True, key=f"gallery_uploads_{st.session_state.gallery_upload_version}", help="Selecciona hasta 6 fotos para la galería.")
        if gallery_uploads:
            b["gallery"] = [{"mime": upload.type, "data": upload.getvalue()} for upload in gallery_uploads[:6]]
            st.success(f"{len(b['gallery'])} foto(s) listas para la galería de esta sesión.")
        if b.get("gallery"):
            st.caption("Fotos actuales de la galería")
            preview_columns = st.columns(min(3, len(b["gallery"])))
            for index, image in enumerate(b["gallery"]):
                with preview_columns[index % len(preview_columns)]:
                    st.image(image["data"] if isinstance(image, dict) else image, use_container_width=True)
        if b.get("gallery"):
            st.button("Quitar fotos de la galería", key="clear_gallery", on_click=clear_gallery)
        st.markdown("<p class='subtle'>En esta demo el nombre, el logo, las fotos y las reservas solo viven en la sesión actual. Para que todas las personas vean los mismos cambios y no se pierdan al reiniciar la app, hay que conectar almacenamiento permanente.</p>", unsafe_allow_html=True)


def set_booking_status(booking_id, status):
    for booking in st.session_state.aura_data["bookings"]:
        if booking["id"] == booking_id:
            booking["status"] = status
            break


def clear_hero():
    st.session_state.aura_data["business"]["hero_image"] = None
    st.session_state.hero_upload_version += 1


def clear_gallery():
    st.session_state.aura_data["business"]["gallery"] = []
    st.session_state.gallery_upload_version += 1


def clear_logo():
    st.session_state.aura_data["business"]["logo"] = None
    st.session_state.logo_upload_version += 1


header()
page = st.session_state.aura_page
if page == "Inicio":
    public_page()
elif page == "Servicios":
    st.markdown("<p class='eyebrow'>Cuidado integral</p><h1 class='section-title'>Nuestros servicios</h1>", unsafe_allow_html=True)
    for service in st.session_state.aura_data["services"]:
        with st.container(border=True):
            left, right = st.columns([4, 1], vertical_alignment="center")
            with left:
                st.markdown(f"### {escape(service['name'])}")
                st.write(service["description"])
                st.caption(f"Duración aproximada: {service['minutes']} minutos")
            with right:
                st.button("Agendar", key=f"detail_{service['id']}", on_click=go_to, args=("Reservar", service["id"]))
elif page == "Reservar":
    booking_page()
else:
    admin_page()
