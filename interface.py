import streamlit as st
import time
from datetime import datetime, timedelta

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CHRONOS-7 // Interface Temporelle",
    page_icon="⏳",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── GLOBAL STYLES ──────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600&display=swap');

:root {
    --cyan: #00ffe7;
    --red: #ff2a2a;
    --yellow: #ffe94d;
    --green: #39ff14;
    --blue: #4da6ff;
    --dark: #020b14;
    --panel: #030f1c;
    --border: #0a3a4a;
}

* { box-sizing: border-box; }

html, body, .stApp {
    background-color: var(--dark) !important;
    color: var(--cyan) !important;
    font-family: 'Share Tech Mono', monospace !important;
}

/* Hide default streamlit elements */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
[data-testid="stSidebar"] { display: none; }
.block-container { padding: 1rem 2rem !important; max-width: 100% !important; }

/* Scanline overlay */
body::before {
    content: '';
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background: repeating-linear-gradient(
        0deg,
        transparent,
        transparent 2px,
        rgba(0,255,231,0.015) 2px,
        rgba(0,255,231,0.015) 4px
    );
    pointer-events: none;
    z-index: 9999;
}

h1, h2, h3 {
    font-family: 'Orbitron', sans-serif !important;
    color: var(--cyan) !important;
    text-shadow: 0 0 20px var(--cyan), 0 0 40px rgba(0,255,231,0.3);
}

/* Inputs */
.stTextInput input, .stNumberInput input {
    background: #020b14 !important;
    border: 1px solid var(--cyan) !important;
    color: var(--cyan) !important;
    font-family: 'Share Tech Mono', monospace !important;
    border-radius: 4px !important;
    caret-color: var(--cyan);
}
.stTextInput input:focus, .stNumberInput input:focus {
    box-shadow: 0 0 15px rgba(0,255,231,0.4) !important;
}

/* Labels */
.stTextInput label, .stNumberInput label, .stSlider label {
    color: var(--cyan) !important;
    font-family: 'Share Tech Mono', monospace !important;
}

/* Buttons */
.stButton > button {
    background: transparent !important;
    border: 1px solid var(--cyan) !important;
    color: var(--cyan) !important;
    font-family: 'Orbitron', monospace !important;
    font-size: 0.85rem !important;
    letter-spacing: 2px !important;
    padding: 0.6rem 1.5rem !important;
    transition: all 0.2s !important;
    border-radius: 3px !important;
}
.stButton > button:hover {
    background: rgba(0,255,231,0.1) !important;
    box-shadow: 0 0 20px rgba(0,255,231,0.5) !important;
}

/* Timer */
.timer-box {
    text-align: center;
    font-family: 'Orbitron', sans-serif;
    font-size: 2.2rem;
    font-weight: 900;
    color: var(--cyan);
    text-shadow: 0 0 30px var(--cyan);
    padding: 0.3rem 1rem;
    border: 1px solid var(--cyan);
    border-radius: 6px;
    background: rgba(0,255,231,0.05);
    display: inline-block;
    letter-spacing: 4px;
}
.timer-warning { color: var(--yellow) !important; text-shadow: 0 0 30px var(--yellow) !important; border-color: var(--yellow) !important; }
.timer-danger  { color: var(--red)    !important; text-shadow: 0 0 30px var(--red)    !important; border-color: var(--red)    !important; animation: blink 0.5s step-end infinite; }

@keyframes blink { 50% { opacity: 0.4; } }

/* Panel cards */
.panel {
    border: 1px solid var(--border);
    background: var(--panel);
    border-radius: 8px;
    padding: 1.2rem;
    position: relative;
    height: 100%;
}
.panel-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 0.85rem;
    color: var(--cyan);
    letter-spacing: 3px;
    text-transform: uppercase;
    border-bottom: 1px solid var(--border);
    padding-bottom: 0.5rem;
    margin-bottom: 1rem;
}
.panel-solved {
    border-color: var(--green) !important;
    background: rgba(57,255,20,0.04) !important;
}
.panel-title-solved {
    color: var(--green) !important;
}

/* Success / Error badges */
.badge-ok  { color: var(--green); font-weight: bold; text-shadow: 0 0 10px var(--green); }
.badge-err { color: var(--red);   font-weight: bold; text-shadow: 0 0 10px var(--red);   }

/* Big red overlay */
.red-overlay {
    position: fixed;
    inset: 0;
    background: rgba(180,0,0,0.92);
    z-index: 10000;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    font-family: 'Orbitron', sans-serif;
    color: white;
    font-size: 2.5rem;
    text-align: center;
    animation: flashIn 0.15s ease-out;
}
@keyframes flashIn { from { opacity: 0; } to { opacity: 1; } }

/* LED dot */
.led {
    display: inline-block;
    width: 18px; height: 18px;
    border-radius: 50%;
    margin: 3px;
    border: 2px solid rgba(255,255,255,0.3);
}
.led-blue   { background: #4da6ff; box-shadow: 0 0 12px #4da6ff; }
.led-green  { background: #39ff14; box-shadow: 0 0 12px #39ff14; }
.led-yellow { background: #ffe94d; box-shadow: 0 0 12px #ffe94d; }
.led-red    { background: #ff2a2a; box-shadow: 0 0 12px #ff2a2a; }
.led-off    { background: #1a2a1a; box-shadow: none; }

/* Suit symbols */
.suit-spade   { color: #aaa; font-size: 2.5rem; }
.suit-heart   { color: #ff4466; font-size: 2.5rem; }
.suit-diamond { color: #ff4466; font-size: 2.5rem; }
.suit-club    { color: #aaa; font-size: 2.5rem; }

/* Typing effect */
.typewriter {
    overflow: hidden;
    border-right: 2px solid var(--cyan);
    white-space: pre-wrap;
    animation: typing-cursor 0.75s step-end infinite;
}
@keyframes typing-cursor { 50% { border-color: transparent; } }

.glitch {
    position: relative;
    animation: glitch 3s infinite;
}
@keyframes glitch {
    0%,95% { text-shadow: 0 0 20px var(--cyan); }
    96% { text-shadow: -3px 0 var(--red), 3px 0 var(--blue); transform: skewX(-5deg); }
    97% { text-shadow: 3px 0 var(--red), -3px 0 var(--blue); transform: skewX(5deg); }
    98% { text-shadow: 0 0 20px var(--cyan); transform: skewX(0); }
}

/* Failure page */
.fail-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 4rem;
    color: var(--red);
    text-shadow: 0 0 40px var(--red), 0 0 80px rgba(255,42,42,0.5);
    text-align: center;
    animation: blink 1s step-end infinite;
}

/* Success page */
.success-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 3rem;
    color: var(--green);
    text-shadow: 0 0 40px var(--green);
    text-align: center;
}

/* Divider */
hr { border-color: var(--border) !important; }

/* Year tags */
.year-tag {
    font-family: 'Orbitron', sans-serif;
    font-size: 0.75rem;
    color: rgba(0,255,231,0.4);
    letter-spacing: 2px;
}

/* Stagger animation for AI text */
.ai-text {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.1rem;
    line-height: 1.8;
    color: rgba(0,255,231,0.9);
    border-left: 2px solid var(--cyan);
    padding-left: 1rem;
    margin: 1rem 0;
}

/* Number input spinner hide */
input[type=number]::-webkit-inner-spin-button,
input[type=number]::-webkit-outer-spin-button { -webkit-appearance: none; margin: 0; }

/* Slider */
.stSlider [data-baseweb="slider"] { padding: 0.5rem 0; }

</style>
""", unsafe_allow_html=True)

# ─── SESSION STATE INIT ──────────────────────────────────────────────────────
defaults = {
    "page": "home",
    "timer_start": None,
    "timer_paused_remaining": None,
    "timer_active": True,
    "roaming_warning": False,
    "roaming_unlocked": False,
    "puzzle1_playing": False,
    "puzzle1_led_step": 0,
    "puzzle1_last_tick": None,
    "puzzle1_solved": False,
    "puzzle2_solved": False,
    "puzzle3_solved": False,
    "puzzle4_solved": False,
    "final_eq_done": False,
    "bus_shown": False,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─── HELPERS ────────────────────────────────────────────────────────────────
LED_SEQ = ["blue","green","green","yellow","blue","red","green","blue","yellow","blue"]
LED_INTERVAL = 1.2  # seconds per step

def get_remaining():
    if st.session_state.timer_paused_remaining is not None:
        return st.session_state.timer_paused_remaining
    if st.session_state.timer_start is None:
        return 3600
    elapsed = time.time() - st.session_state.timer_start
    return max(0, 3600 - elapsed)

def fmt_time(secs):
    s = int(secs)
    m, sc = divmod(s, 60)
    return f"{m:02d}:{sc:02d}"

def render_timer():
    rem = get_remaining()
    t = fmt_time(rem)
    cls = "timer-box"
    if rem < 300: cls += " timer-danger"
    elif rem < 600: cls += " timer-warning"
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        st.markdown(f"<div style='text-align:center'><span class='{cls}'>⏱ {t}</span></div>", unsafe_allow_html=True)
    return rem

def all_puzzles_solved():
    return all([
        st.session_state.puzzle1_solved,
        st.session_state.puzzle2_solved,
        st.session_state.puzzle3_solved,
        st.session_state.puzzle4_solved,
    ])

# ─── ROAMING WARNING OVERLAY ────────────────────────────────────────────────
if st.session_state.roaming_warning:
    st.markdown("""
    <div class="red-overlay" id="rovlay">
        ⚠️ ERREUR CRITIQUE ⚠️<br>
        <span style="font-size:1.3rem; margin-top:1rem; display:block">IL FALLAIT SURTOUT PAS FAIRE ÇA</span>
        <span style="font-size:0.85rem; font-family: monospace; margin-top:0.5rem; display:block; color: #ffaaaa">PERTURBATION TEMPORELLE DÉTECTÉE</span>
    </div>
    """, unsafe_allow_html=True)
    if st.button("⚡ ANNULER L'ACTION", key="dismiss_roaming"):
        st.session_state.roaming_warning = False
        st.session_state.roaming_unlocked = True
        # Force the toggle back to off by clearing its key from session state
        if "roaming_toggle" in st.session_state:
            st.session_state["roaming_toggle"] = False
        st.rerun()
    st.stop()

# ═══════════════════════════════════════════════════════════════════════════
# PAGE: HOME
# ═══════════════════════════════════════════════════════════════════════════
if st.session_state.page == "home":
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align:center'>
        <div style='font-family: Orbitron, sans-serif; font-size: 0.9rem; letter-spacing: 8px; color: rgba(0,255,231,0.5); margin-bottom:1rem'>
            SYSTÈME CHRONOS-7 // INTERFACE DE RÉCUPÉRATION TEMPORELLE
        </div>
        <h1 class='glitch' style='font-size: 3.5rem; margin-bottom: 0.5rem'>FAILLE TEMPORELLE</h1>
        <div style='font-family: Rajdhani, sans-serif; font-size: 1.3rem; color: rgba(0,255,231,0.7); margin: 1rem 0 2rem 0; letter-spacing: 2px'>
            ERREUR SYSTÈME — COORDONNÉES TEMPORELLES CORROMPUES
        </div>
    </div>
    """, unsafe_allow_html=True)

    col = st.columns([1,2,1])
    with col[1]:
        st.markdown("""
        <div style='border: 1px solid #0a3a4a; background: #030f1c; border-radius: 8px; padding: 2rem; text-align: center; margin: 1rem 0'>
            <div style='font-family: Share Tech Mono, monospace; color: rgba(0,255,231,0.6); font-size: 0.9rem; line-height: 2; margin-bottom: 1.5rem'>
                > CONNEXION AU PROTOCOLE DE RÉCUPÉRATION...<br>
                > INTERFACE IA CHRONOS-7 DISPONIBLE<br>
                > EN ATTENTE D'INITIALISATION<br>
                > <span style='color: #ffe94d'>⚠ DURÉE LIMITE : 60 MINUTES</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("▶  LANCER LA MISSION", key="start_game"):
            st.session_state.page = "login"
            st.session_state.timer_start = time.time()
            st.session_state.timer_active = True
            st.rerun()

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align:center; font-family: Share Tech Mono; font-size: 0.7rem; color: rgba(0,255,231,0.2); letter-spacing: 3px'>
        ANTHROPIC TEMPORAL SYSTEMS © 2847  //  CHRONOS-7 v4.2.1
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════
# PAGE: LOGIN
# ═══════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "login":
    rem = render_timer()
    if rem == 0 and st.session_state.timer_active:
        st.session_state.page = "fail"
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    col = st.columns([1,3,1])
    with col[1]:
        st.markdown("""
        <div style='border: 1px solid #0a3a4a; background: #030f1c; border-radius: 8px; padding: 2rem; margin-bottom: 1.5rem'>
            <div style='font-family: Orbitron, sans-serif; font-size: 0.7rem; color: rgba(0,255,231,0.4); letter-spacing: 4px; margin-bottom:1rem'>
                CHRONOS-7 // MESSAGE ENTRANT
            </div>
            <div class='ai-text'>
                Bonjour. Je suis <strong>CHRONOS-7</strong>, l'intelligence artificielle de gestion des corridors temporels.<br><br>
                Votre groupe a été détecté dans une faille spatio-temporelle critique. 
                L'origine de l'incident remonte à une corruption de données survenue entre <strong>1973</strong> et <strong>2003</strong>.<br><br>
                Pour vous libérer et vous rapatrier en <strong>2026</strong>, je dois d'abord 
                <span style='color:#ffe94d'>vérifier l'identité de votre famille</span>.<br><br>
                Merci de vous authentifier ci-dessous. Le protocole de sécurité exige un mot de passe familial.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style='border: 1px solid #0a3a4a; background: #030f1c; border-radius: 8px; padding: 1.5rem'>
            <div style='font-family: Orbitron; font-size: 0.75rem; color: rgba(0,255,231,0.5); letter-spacing: 3px; margin-bottom:1rem'>
                AUTHENTIFICATION REQUISE
            </div>
        """, unsafe_allow_html=True)

        pwd = st.text_input("Mot de passe", type="password", placeholder="••••••••••••", key="login_pwd")
        with st.expander("💡 Indice"):
            st.markdown("<span style='color: #ffe94d; font-family: Share Tech Mono'>Mon prénom</span>", unsafe_allow_html=True)

        if st.button("→ VALIDER", key="login_submit"):
            if pwd == "Lafaoforafa":
                st.session_state.page = "code4"
                st.rerun()
            else:
                st.markdown("<span class='badge-err'>⛔ MOT DE PASSE INCORRECT — ACCÈS REFUSÉ</span>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    time.sleep(1)
    st.rerun()

# ═══════════════════════════════════════════════════════════════════════════
# PAGE: 4-DIGIT CODE
# ═══════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "code4":
    rem = render_timer()
    if rem == 0 and st.session_state.timer_active:
        st.session_state.page = "fail"
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Year tags flanking
    col_left, col_mid, col_right = st.columns([1, 4, 1])
    with col_left:
        st.markdown("<br><br><br><div class='year-tag'>1973</div>", unsafe_allow_html=True)
    with col_right:
        st.markdown("<br><br><br><div class='year-tag' style='text-align:right'>2003</div>", unsafe_allow_html=True)

    with col_mid:
        st.markdown("""
        <div style='border: 1px solid #0a3a4a; background: #030f1c; border-radius: 8px; padding: 2rem; margin-bottom: 1.5rem'>
            <div style='font-family: Orbitron, sans-serif; font-size: 0.7rem; color: var(--green); letter-spacing: 4px; margin-bottom:1rem'>
                ✓ IDENTITÉ FAMILIALE CONFIRMÉE
            </div>
            <div class='ai-text'>
                Bien. L'identité principale est reconnue.<br><br>
                Pour finaliser l'accès au protocole de récupération, j'ai besoin d'un 
                <span style='color:#ffe94d'>code de confirmation à 4 chiffres</span>.<br><br>
                <em style='color: rgba(0,255,231,0.5); font-size: 0.9rem'>
                    [Indice : ici vous mettrez le texte de l'énigme qui mène au code 6435]
                </em>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style='border: 1px solid #0a3a4a; background: #030f1c; border-radius: 8px; padding: 1.5rem'>
            <div style='font-family: Orbitron; font-size: 0.75rem; color: rgba(0,255,231,0.5); letter-spacing: 3px; margin-bottom:1rem'>
                CODE DE CONFIRMATION
            </div>
        """, unsafe_allow_html=True)

        code = st.text_input("Code à 4 chiffres", max_chars=4, placeholder="_ _ _ _", key="code4_input")

        if st.button("→ CONFIRMER", key="code4_submit"):
            if code == "6435":
                st.session_state.page = "menu"
                st.rerun()
            else:
                st.markdown("<span class='badge-err'>⛔ CODE INVALIDE</span>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    time.sleep(1)
    st.rerun()

# ═══════════════════════════════════════════════════════════════════════════
# PAGE: MENU (4 PUZZLES)
# ═══════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "menu":
    rem = render_timer()
    if rem == 0 and st.session_state.timer_active:
        st.session_state.page = "fail"
        st.rerun()

    st.markdown("""
    <div style='text-align:center; margin-bottom:1rem'>
        <div class='ai-text' style='display:inline-block; border-left: none; padding: 0.5rem 1rem; border: 1px solid #0a3a4a; border-radius: 4px; font-size: 0.9rem'>
            ✓ Code de confirmation accepté — Lancement du protocole de vérification multi-systèmes.<br>
            <span style='color: #ffe94d'>4 modules doivent être activés pour valider votre identité familiale complète.</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Row 1 ──
    col1, col2 = st.columns(2)

    # ─ PUZZLE 1: Calibration ─────────────────────────────────────────────
    with col1:
        p1_class = "panel panel-solved" if st.session_state.puzzle1_solved else "panel"
        title_class = "panel-title panel-title-solved" if st.session_state.puzzle1_solved else "panel-title"

        st.markdown(f"<div class='{p1_class}'>", unsafe_allow_html=True)
        st.markdown(f"<div class='{title_class}'>◈ CALIBRATION DE LA MACHINE</div>", unsafe_allow_html=True)

        if st.session_state.puzzle1_solved:
            st.markdown("""
            <div style='color: var(--green); text-align:center; margin: 1rem 0'>
                ♠ &nbsp; ♥ &nbsp; ♦ &nbsp; ♣
            </div>
            <div class='badge-ok' style='text-align:center'>✓ CALIBRATION COMPLÈTE</div>
            """, unsafe_allow_html=True)
        else:
            # Roaming slider
            roaming = st.toggle("📡 Données en itinérance", key="roaming_toggle", value=False)
            if roaming and not st.session_state.roaming_unlocked:
                st.session_state.roaming_warning = True
                st.rerun()

            # Play button — grisé tant que les données en itinérance n'ont pas été activées
            play_unlocked = st.session_state.roaming_unlocked
            play_pressed = st.button(
                "▶ PLAY — Lancer la séquence",
                key="p1_play",
                disabled=not play_unlocked,
                help="Activez d'abord les données en itinérance" if not play_unlocked else None
            )

            if play_pressed and not st.session_state.puzzle1_playing:
                st.session_state.puzzle1_playing = True
                st.session_state.puzzle1_led_step = 0
                st.session_state.puzzle1_last_tick = time.time()

            # LED display
            if st.session_state.puzzle1_playing:
                step = st.session_state.puzzle1_led_step
                leds_html = ""
                for i, color in enumerate(LED_SEQ):
                    if i == step:
                        leds_html += f"<span class='led led-{color}'></span>"
                    else:
                        leds_html += "<span class='led led-off'></span>"
                st.markdown(f"<div style='margin:0.8rem 0'>{leds_html}</div>", unsafe_allow_html=True)

                # Advance step
                now = time.time()
                if st.session_state.puzzle1_last_tick and (now - st.session_state.puzzle1_last_tick) >= LED_INTERVAL:
                    st.session_state.puzzle1_led_step = (step + 1) % len(LED_SEQ)
                    st.session_state.puzzle1_last_tick = now

                color_names = {"blue":"B","green":"V","yellow":"J","red":"R"}
                st.markdown("""
                <div style='font-size:0.75rem; color: rgba(0,255,231,0.5); margin-bottom:0.5rem'>
                Séquence: Bleu, Vert, Vert, Jaune, Bleu, Rouge, Vert, Bleu, Jaune, Bleu
                </div>""", unsafe_allow_html=True)

            p1_code = st.text_input("Code 4 lettres", max_chars=4, placeholder="????", key="p1_code")
            if st.button("→ Valider", key="p1_submit"):
                if p1_code.upper() == "BSJE":
                    st.session_state.puzzle1_solved = True
                    st.rerun()
                else:
                    st.markdown("<span class='badge-err'>Code incorrect</span>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # ─ PUZZLE 2: Test d'identité ──────────────────────────────────────────
    with col2:
        p2_class = "panel panel-solved" if st.session_state.puzzle2_solved else "panel"
        title_class = "panel-title panel-title-solved" if st.session_state.puzzle2_solved else "panel-title"

        st.markdown(f"<div class='{p2_class}'>", unsafe_allow_html=True)
        st.markdown(f"<div class='{title_class}'>◈ TEST D'IDENTITÉ</div>", unsafe_allow_html=True)

        if st.session_state.puzzle2_solved:
            st.markdown("""
            <div class='ai-text' style='font-size:0.9rem'>
                Impression du texte sur la famille…<br>
                <span style='color: rgba(0,255,231,0.5)'>████████████ 100%</span>
            </div>
            <div class='badge-ok'>✓ IDENTITÉ VÉRIFIÉE</div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("<div style='color: rgba(0,255,231,0.6); font-size:0.85rem; margin-bottom:0.8rem'>Entrez le code d'identification à 4 chiffres :</div>", unsafe_allow_html=True)
            p2_code = st.text_input("Code", max_chars=4, placeholder="_ _ _ _", key="p2_code")
            if st.button("→ Valider", key="p2_submit"):
                if p2_code == "6294":
                    st.session_state.puzzle2_solved = True
                    st.rerun()
                else:
                    st.markdown("<span class='badge-err'>Code incorrect</span>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Row 2 ──
    col3, col4 = st.columns(2)

    # ─ PUZZLE 3: Référence de famille ─────────────────────────────────────
    with col3:
        p3_class = "panel panel-solved" if st.session_state.puzzle3_solved else "panel"
        title_class = "panel-title panel-title-solved" if st.session_state.puzzle3_solved else "panel-title"

        st.markdown(f"<div class='{p3_class}'>", unsafe_allow_html=True)
        st.markdown(f"<div class='{title_class}'>◈ RÉFÉRENCE DE FAMILLE</div>", unsafe_allow_html=True)

        if st.session_state.puzzle3_solved:
            st.markdown("""
            <div style='text-align:center; margin:1rem 0'>
                <span style='font-family: Orbitron; font-size: 1.8rem; color: var(--cyan); letter-spacing: 6px; text-shadow: 0 0 20px var(--cyan)'>
                    1…R
                </span>
            </div>
            <div class='badge-ok'>✓ RÉFÉRENCE VALIDÉE</div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("<div style='color: rgba(0,255,231,0.6); font-size:0.85rem; margin-bottom:0.8rem'>Entrez le mot de passe de référence familiale :</div>", unsafe_allow_html=True)
            p3_pwd = st.text_input("Mot de passe", type="password", placeholder="••••••••••••••", key="p3_pwd")
            if st.button("→ Valider", key="p3_submit"):
                if p3_pwd == "Heureusement que papa était là":
                    st.session_state.puzzle3_solved = True
                    st.rerun()
                else:
                    st.markdown("<span class='badge-err'>Mot de passe incorrect</span>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # ─ PUZZLE 4: Lancement moteur ──────────────────────────────────────────
    with col4:
        p4_class = "panel panel-solved" if st.session_state.puzzle4_solved else "panel"
        title_class = "panel-title panel-title-solved" if st.session_state.puzzle4_solved else "panel-title"

        st.markdown(f"<div class='{p4_class}'>", unsafe_allow_html=True)
        st.markdown(f"<div class='{title_class}'>◈ LANCEMENT MOTEUR</div>", unsafe_allow_html=True)

        st.markdown("""
        <div style='text-align:center; font-size:3rem; margin: 0.5rem 0; letter-spacing:8px'>
            🂡 🂮 🂻 🂹
        </div>
        <div style='text-align:center; font-size:0.75rem; color: rgba(0,255,231,0.4); margin-bottom:0.8rem'>
            JEU DE CARTES — RÉFÉRENCE MOTEUR
        </div>
        """, unsafe_allow_html=True)

        if st.session_state.puzzle4_solved:
            st.markdown("<div class='badge-ok' style='text-align:center'>✓ MOTEUR EN LIGNE</div>", unsafe_allow_html=True)
        else:
            p4_code = st.text_input("Code à 4 chiffres", max_chars=4, placeholder="_ _ _ _", key="p4_code")
            if st.button("→ Valider", key="p4_submit"):
                if p4_code == "9576":
                    st.session_state.puzzle4_solved = True
                    st.rerun()
                else:
                    st.markdown("<span class='badge-err'>Code incorrect</span>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # ── Check all solved ──
    if all_puzzles_solved():
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div style='text-align:center; border: 1px solid var(--green); border-radius: 8px; padding: 1rem; background: rgba(57,255,20,0.06)'>
            <div style='color: var(--green); font-family: Orbitron; font-size:1.1rem; letter-spacing:3px'>
                ✓ TOUS LES MODULES VALIDÉS
            </div>
            <div style='color: rgba(0,255,231,0.7); font-size:0.85rem; margin-top:0.5rem'>
                Procédure finale de rapatriement disponible
            </div>
        </div>
        """, unsafe_allow_html=True)
        col_btn = st.columns([1,2,1])
        with col_btn[1]:
            if st.button("▶▶ LANCER LA PROCÉDURE FINALE", key="go_final"):
                st.session_state.page = "final_eq"
                st.rerun()

    time.sleep(1)
    st.rerun()

# ═══════════════════════════════════════════════════════════════════════════
# PAGE: ÉQUATION FINALE
# ═══════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "final_eq":
    rem = render_timer()
    if rem == 0 and st.session_state.timer_active:
        st.session_state.page = "fail"
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    col = st.columns([1,3,1])
    with col[1]:
        st.markdown("""
        <div style='border: 1px solid #0a3a4a; background: #030f1c; border-radius: 8px; padding: 2rem; margin-bottom: 1.5rem'>
            <div style='font-family: Orbitron; font-size:0.7rem; color: rgba(0,255,231,0.4); letter-spacing:4px; margin-bottom:1rem'>
                CHRONOS-7 // CALCUL DE COORDONNÉES TEMPORELLES
            </div>
            <div class='ai-text'>
                Parfait. Tous les modules sont en ligne.<br><br>
                Pour finaliser le rapatriement, le calculateur temporel a besoin d'une dernière valeur. 
                Résolvez l'équation ci-dessous pour obtenir les coordonnées de retour en <strong>2026</strong>.
            </div>
        </div>

        <div style='border: 1px solid var(--cyan); background: #030f1c; border-radius: 8px; padding: 2rem; text-align:center; margin-bottom:1.5rem'>
            <div style='font-family: Orbitron; font-size:0.75rem; color: rgba(0,255,231,0.5); letter-spacing:3px; margin-bottom:1.5rem'>ÉQUATION DE RAPATRIEMENT</div>
            <div style='font-family: Orbitron; font-size: 2rem; color: var(--cyan); text-shadow: 0 0 20px var(--cyan); letter-spacing: 4px'>
                ? × ? + ? = 711
            </div>
            <div style='font-family: Share Tech Mono; font-size: 0.8rem; color: rgba(0,255,231,0.4); margin-top:1rem'>
                [Indice : utilisez les codes trouvés dans les modules]
            </div>
        </div>
        """, unsafe_allow_html=True)

        eq_ans = st.text_input("Votre réponse", max_chars=6, placeholder="???", key="eq_answer")
        if st.button("→ SOUMETTRE LA RÉPONSE", key="eq_submit"):
            try:
                if int(eq_ans) == 711:
                    st.session_state.page = "bus"
                    st.rerun()
                else:
                    st.markdown("<span class='badge-err'>⛔ Valeur incorrecte — recalculez</span>", unsafe_allow_html=True)
            except:
                st.markdown("<span class='badge-err'>⛔ Valeur invalide</span>", unsafe_allow_html=True)

    time.sleep(1)
    st.rerun()

# ═══════════════════════════════════════════════════════════════════════════
# PAGE: BUS JOKE
# ═══════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "bus":
    rem = render_timer()

    st.markdown("<br><br>", unsafe_allow_html=True)
    col = st.columns([1,3,1])
    with col[1]:
        st.markdown("""
        <div style='text-align:center; border: 2px solid #ff2a2a; border-radius: 8px; padding: 2rem; background: rgba(255,42,42,0.08)'>
            <div style='font-family: Orbitron; font-size: 2rem; color: #ff2a2a; text-shadow: 0 0 30px #ff2a2a; margin-bottom: 1rem; animation: blink 0.8s step-end infinite'>
                ⚠ OH NON SURTOUT PAS LE 711 ⚠
            </div>
            <div style='font-size: 5rem; margin: 1rem 0'>🚌</div>
            <div style='font-family: Rajdhani; font-size: 1.1rem; color: rgba(0,255,231,0.7); margin-bottom: 1.5rem'>
                ERREUR FATALE : Le bus 711 de ligne temporelle approche à grande vitesse !<br>
                Perturbation de l'axe espace-temps détectée...
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("→ CONTINUER MALGRÉ TOUT", key="bus_continue"):
            st.session_state.page = "success"
            st.rerun()

    time.sleep(1)
    st.rerun()

# ═══════════════════════════════════════════════════════════════════════════
# PAGE: SUCCESS
# ═══════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "success":
    # Stop timer
    st.session_state.timer_active = False

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Confetti-like particles via CSS
    st.markdown("""
    <style>
    @keyframes floatUp {
        0%   { transform: translateY(0) rotate(0deg); opacity: 1; }
        100% { transform: translateY(-120vh) rotate(720deg); opacity: 0; }
    }
    .particle {
        position: fixed;
        bottom: -20px;
        font-size: 1.5rem;
        animation: floatUp linear infinite;
        pointer-events: none;
        z-index: 100;
    }
    </style>
    <div class="particle" style="left:5%;  animation-duration:4s;  animation-delay:0s">⚡</div>
    <div class="particle" style="left:15%; animation-duration:5s;  animation-delay:0.5s">✦</div>
    <div class="particle" style="left:25%; animation-duration:3.5s;animation-delay:1s">⏱</div>
    <div class="particle" style="left:40%; animation-duration:4.5s;animation-delay:0.2s">✨</div>
    <div class="particle" style="left:55%; animation-duration:3s;  animation-delay:1.5s">⚡</div>
    <div class="particle" style="left:70%; animation-duration:5.5s;animation-delay:0.7s">✦</div>
    <div class="particle" style="left:85%; animation-duration:4s;  animation-delay:0.3s">✨</div>
    <div class="particle" style="left:95%; animation-duration:3.8s;animation-delay:1.2s">⏱</div>
    """, unsafe_allow_html=True)

    col = st.columns([1,3,1])
    with col[1]:
        st.markdown("""
        <div style='text-align:center; margin-bottom: 2rem'>
            <div style='font-family: Orbitron; font-size: 0.8rem; color: rgba(0,255,231,0.4); letter-spacing: 6px; margin-bottom: 1rem'>
                CHRONOS-7 // PROTOCOLE TERMINÉ
            </div>
            <div class='success-title'>✓ MISSION ACCOMPLIE</div>
        </div>

        <div style='border: 1px solid var(--green); background: rgba(57,255,20,0.05); border-radius: 8px; padding: 2rem; text-align:center; margin: 1.5rem 0'>
            <div style='font-size: 3rem; margin-bottom: 1rem'>🌟</div>
            <div class='ai-text' style='border-color: var(--green); text-align:center'>
                <strong style='color: var(--green); font-size:1.3rem'>IDENTITÉ VÉRIFIÉE</strong><br><br>
                Toutes les vérifications ont été effectuées avec succès.<br>
                Le corridor temporel est stabilisé.<br><br>
                <span style='font-family: Orbitron; font-size: 1.1rem; color: var(--cyan); letter-spacing: 3px'>
                    VOUS POUVEZ RENTRER EN 2026
                </span><br><br>
                <span style='color: rgba(0,255,231,0.5); font-size: 0.85rem'>
                    Bon retour à votre époque. CHRONOS-7 vous souhaite un bon voyage.
                </span>
            </div>
        </div>

        <div style='text-align:center; font-family: Share Tech Mono; font-size:0.75rem; color: rgba(0,255,231,0.3); letter-spacing:3px; margin-top: 2rem'>
            CHRONOS-7 // SESSION FERMÉE // MERCI D'AVOIR JOUÉ
        </div>
        """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════
# PAGE: FAIL (timer expired)
# ═══════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "fail":
    st.markdown("""
    <div style='text-align:center; padding: 3rem 0'>
        <div class='fail-title'>TEMPS ÉCOULÉ</div>
        <div style='font-family: Orbitron; font-size:1rem; color: var(--red); letter-spacing:4px; margin: 1rem 0; opacity:0.7'>
            LA FAILLE TEMPORELLE S'EST REFERMÉE
        </div>
        <div style='font-size: 4rem; margin: 1.5rem 0'>💀</div>
        <div style='font-family: Rajdhani; font-size:1.1rem; color: rgba(0,255,231,0.6); max-width:500px; margin:0 auto 2rem auto'>
            Votre groupe est désormais coincé dans la faille temporelle...<br>
            Mais il reste une possibilité de survie.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col = st.columns([1,2,1])
    with col[1]:
        st.markdown("""
        <div style='border: 1px solid #ff2a2a; background: rgba(255,42,42,0.05); border-radius:8px; padding:1.5rem; text-align:center; margin-bottom:1rem'>
            <div style='font-family: Share Tech Mono; font-size:0.85rem; color: rgba(0,255,231,0.6)'>
                Mode de récupération d'urgence disponible.<br>
                Le chronomètre a été désactivé.
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("⚡ CONTINUER SANS CHRONO (mode survie)", key="fail_continue"):
            st.session_state.timer_paused_remaining = 1  # effectively stopped
            st.session_state.timer_active = False
            # Go back to wherever they were
            if st.session_state.puzzle1_solved and st.session_state.puzzle2_solved and \
               st.session_state.puzzle3_solved and st.session_state.puzzle4_solved:
                st.session_state.page = "final_eq"
            elif st.session_state.page not in ["menu","login","code4"]:
                st.session_state.page = "menu"
            else:
                pass  # keep current page
            if st.session_state.page == "fail":
                st.session_state.page = "menu"
            st.rerun()

# ─── AUTO RERUN for timer on active pages ───────────────────────────────────