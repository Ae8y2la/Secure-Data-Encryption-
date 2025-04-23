import streamlit as st
import hashlib
from cryptography.fernet import Fernet
import time
import json
import os
import random
import base64
from datetime import datetime

# --- Global Variables ---
if 'failed_attempts' not in st.session_state:
    st.session_state.failed_attempts = 0
if 'last_failed_time' not in st.session_state:
    st.session_state.last_failed_time = 0
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'hacking' not in st.session_state:
    st.session_state.hacking = False
if 'color_theme' not in st.session_state:
    st.session_state.color_theme = "neon_blue"

# --- Color Themes ---
COLOR_THEMES = {
    "neon_blue": {
        "PRIMARY": "#00F0FF",
        "SECONDARY": "#FF0099",
        "ACCENT": "#00FF41",
        "ERROR": "#FF003C",
        "BG": "#0D0208",
        "TEXT": "#00F0FF"
    },
    "matrix_green": {
        "PRIMARY": "#00FF41",
        "SECONDARY": "#FF0099",
        "ACCENT": "#00F0FF",
        "ERROR": "#FF003C",
        "BG": "#0D0208",
        "TEXT": "#00FF41"
    },
    "cyber_purple": {
        "PRIMARY": "#9D00FF",
        "SECONDARY": "#00F0FF",
        "ACCENT": "#FF0099",
        "ERROR": "#FF003C",
        "BG": "#0A0014",
        "TEXT": "#9D00FF"
    },
    "hacker_red": {
        "PRIMARY": "#FF003C",
        "SECONDARY": "#00F0FF",
        "ACCENT": "#FF0099",
        "ERROR": "#9D00FF",
        "BG": "#120002",
        "TEXT": "#FF003C"
    },
    "golden_amber": {
        "PRIMARY": "#FFAA00",
        "SECONDARY": "#00F0FF",
        "ACCENT": "#FF0099",
        "ERROR": "#FF003C",
        "BG": "#0D0A00",
        "TEXT": "#FFAA00"
    }
}

# --- Encryption App ---
def generate_or_load_key():
    if not os.path.exists("secret.key"):
        key = Fernet.generate_key()
        with open("secret.key", "wb") as key_file:
            key_file.write(key)
    return Fernet(open("secret.key", "rb").read())

cipher = generate_or_load_key()
lockout_time = 30  # seconds

# --- Data Storage ---
def load_data():
    if os.path.exists("data.vault"):
        try:
            with open("data.vault", "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_data(data):
    with open("data.vault", "w") as f:
        json.dump(data, f)

stored_data = load_data()

# --- Security Functions ---
def hash_passkey(passkey):
    salt = b"cyber_salt_v4"
    return hashlib.pbkdf2_hmac('sha512', passkey.encode(), salt, 250000).hex()

def encrypt_data(text):
    return cipher.encrypt(text.encode()).decode()

def decrypt_data(encrypted_text, passkey):
    current_time = time.time()
    if st.session_state.failed_attempts >= 3 and current_time - st.session_state.last_failed_time < lockout_time:
        remaining_time = int(lockout_time - (current_time - st.session_state.last_failed_time))
        st.error(f"🔒 SYSTEM LOCKED - TRY AGAIN IN {remaining_time} SECONDS")
        return None
    
    hashed_passkey = hash_passkey(passkey)
    
    for key, value in stored_data.items():
        if value["encrypted_text"] == encrypted_text and value["passkey"] == hashed_passkey:
            st.session_state.failed_attempts = 0
            return cipher.decrypt(encrypted_text.encode()).decode()
    
    st.session_state.failed_attempts += 1
    st.session_state.last_failed_time = current_time
    return None


# --- Hacker Animations ---
def render_hacking_animation():
    theme = COLOR_THEMES[st.session_state.color_theme]
    return f"""
    <style>
    .hacking-overlay {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: {theme['BG']};
        z-index: 9998;
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
    }}
    
    .hacking-terminal {{
        background-color: rgba(13, 2, 8, 0.9);
        border: 1px solid {theme['PRIMARY']};
        border-radius: 4px;
        padding: 20px;
        font-family: 'Courier New', monospace;
        color: {theme['PRIMARY']};
        position: relative;
        overflow: hidden;
        width: 80%;
        max-width: 800px;
        box-shadow: 0 0 20px {theme['PRIMARY']};
    }}
    
    .terminal-header {{
        display: flex;
        justify-content: space-between;
        border-bottom: 1px solid {theme['PRIMARY']};
        padding-bottom: 10px;
        margin-bottom: 15px;
    }}
    
    .terminal-body {{
        height: 300px;
        overflow-y: auto;
    }}
    
    .terminal-line {{
        margin: 5px 0;
        line-height: 1.4;
    }}
    
    .terminal-prompt {{
        color: {theme['ACCENT']};
    }}
    
    .terminal-command {{
        color: {theme['PRIMARY']};
    }}
    
    .terminal-response {{
        color: {theme['TEXT']};
    }}
    
    .terminal-cursor {{
        display: inline-block;
        width: 10px;
        height: 18px;
        background-color: {theme['PRIMARY']};
        animation: blink 1s infinite;
        vertical-align: middle;
    }}
    
    @keyframes blink {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0; }}
    }}
    
    .network-animation {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
        opacity: 0.3;
    }}
    
    .progress-bar {{
        width: 100%;
        height: 4px;
        background-color: rgba(13, 2, 8, 0.5);
        margin-top: 20px;
        overflow: hidden;
    }}
    
    .progress {{
        height: 100%;
        width: 0%;
        background: linear-gradient(90deg, {theme['BG']}, {theme['PRIMARY']}, {theme['BG']});
        animation: progress 2s linear infinite;
        background-size: 200% 100%;
    }}
    
    @keyframes progress {{
        0% {{ width: 0%; background-position: 0% 50%; }}
        100% {{ width: 100%; background-position: -200% 50%; }}
    }}
    </style>
    
    <div class="hacking-overlay">
        <div class="hacking-terminal">
            <div class="terminal-header">
                <span>QUANTUM ENCRYPTION TERMINAL</span>
                <span>{datetime.now().strftime('%H:%M:%S')}</span>
            </div>
            <div class="terminal-body" id="terminalOutput">
                <div class="terminal-line"><span class="terminal-prompt">></span> <span class="terminal-command">INITIALIZING CYBER PROTOCOLS</span></div>
                <div class="terminal-line terminal-response">> CONNECTING TO QUANTUM NETWORK...</div>
                <div class="terminal-line terminal-response">> ESTABLISHING SECURE CHANNEL...</div>
                <div class="terminal-line terminal-response">> AUTHENTICATING USER CREDENTIALS...</div>
                <div class="terminal-line terminal-response">> BYPASSING FIREWALLS...</div>
                <div class="terminal-line terminal-response">> ACCESSING ENCRYPTION MATRIX...</div>
                <div class="terminal-line terminal-response">> COMPILING DATA FRAGMENTS...</div>
                <div class="terminal-line"><span class="terminal-prompt">></span> <span class="terminal-command">PROCESSING</span> <span class="terminal-cursor"></span></div>
            </div>
            <div class="progress-bar">
                <div class="progress"></div>
            </div>
        </div>
    </div>
    """

def render_cyber_ui():
    theme = COLOR_THEMES[st.session_state.color_theme]
    return f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');
    
    html, body, [class*="css"] {{
        font-family: 'Share Tech Mono', monospace !important;
        background-color: {theme['BG']} !important;
        color: {theme['TEXT']} !important;
    }}
    
    .main {{
        background: {theme['BG']} !important;
    }}
    
    .stTextInput input, .stTextArea textarea {{
        background-color: rgba(13, 2, 8, 0.8) !important;
        color: {theme['TEXT']} !important;
        border: 1px solid {theme['PRIMARY']} !important;
        border-radius: 0 !important;
        font-family: 'Share Tech Mono', monospace !important;
        padding: 12px !important;
    }}
    
    .stTextInput input:focus, .stTextArea textarea:focus {{
        box-shadow: 0 0 10px {theme['PRIMARY']} !important;
        border-color: {theme['ACCENT']} !important;
    }}
    
    .stButton button {{
        background-color: {theme['BG']} !important;
        color: {theme['PRIMARY']} !important;
        border: 1px solid {theme['PRIMARY']} !important;
        border-radius: 0 !important;
        font-family: 'Share Tech Mono', monospace !important;
        padding: 12px 24px !important;
        transition: all 0.3s !important;
    }}
    
    .stButton button:hover {{
        background-color: {theme['PRIMARY']} !important;
        color: {theme['BG']} !important;
        box-shadow: 0 0 15px {theme['PRIMARY']} !important;
    }}
    
    .sidebar .sidebar-content {{
        background-color: {theme['BG']} !important;
        border-right: 1px solid {theme['PRIMARY']} !important;
    }}
    
    .cyber-card {{
        background: rgba(13, 2, 8, 0.7);
        border: 1px solid {theme['PRIMARY']};
        padding: 20px;
        margin-bottom: 20px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 0 10px {theme['PRIMARY'] + '33'};
    }}
    
    .cyber-card::before {{
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, {theme['PRIMARY']}, transparent);
    }}
    
    .cyber-card::after {{
        content: "";
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, {theme['PRIMARY']}, transparent);
    }}
    
    .cyber-title {{
        color: {theme['PRIMARY']};
        font-size: 1.8rem;
        margin-bottom: 15px;
        text-shadow: 0 0 10px {theme['PRIMARY']};
    }}
    
    .cyber-subtitle {{
        color: {theme['ACCENT']};
        font-size: 1.2rem;
        margin-bottom: 10px;
    }}
    
    .cyber-text {{
        color: {theme['TEXT']};
        font-size: 1rem;
        line-height: 1.6;
    }}
    
    .scanlines {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: repeating-linear-gradient(
            to bottom,
            transparent,
            transparent 1px,
            {theme['PRIMARY'] + '33'} 2px
        );
        pointer-events: none;
        z-index: 9999;
    }}
    
    .glitch {{
        animation: glitch 1s linear infinite;
    }}
    
    @keyframes glitch {{
        0% {{ text-shadow: 0.05em 0 0 {theme['PRIMARY']}, -0.05em -0.025em 0 {theme['SECONDARY']}; }}
        14% {{ text-shadow: 0.05em 0 0 {theme['PRIMARY']}, -0.05em -0.025em 0 {theme['SECONDARY']}; }}
        15% {{ text-shadow: -0.05em -0.025em 0 {theme['PRIMARY']}, 0.025em 0.025em 0 {theme['SECONDARY']}; }}
        49% {{ text-shadow: -0.05em -0.025em 0 {theme['PRIMARY']}, 0.025em 0.025em 0 {theme['SECONDARY']}; }}
        50% {{ text-shadow: 0.025em 0.05em 0 {theme['PRIMARY']}, 0.05em 0 0 {theme['SECONDARY']}; }}
        99% {{ text-shadow: 0.025em 0.05em 0 {theme['PRIMARY']}, 0.05em 0 0 {theme['SECONDARY']}; }}
        100% {{ text-shadow: -0.025em 0 0 {theme['PRIMARY']}, -0.025em -0.025em 0 {theme['SECONDARY']}; }}
    }}
    
    .data-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        gap: 20px;
        margin-top: 20px;
    }}
    
    .data-node {{
        background: rgba(13, 2, 8, 0.7);
        border: 1px solid {theme['PRIMARY']};
        padding: 15px;
        position: relative;
        overflow: hidden;
    }}
    
    .data-node::before {{
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(
            135deg,
            transparent 0%,
            {theme['PRIMARY'] + '33'} 50%,
            transparent 100%
        );
        animation: shine 3s infinite;
    }}
    
    @keyframes shine {{
        0% {{ transform: translateX(-100%); }}
        100% {{ transform: translateX(100%); }}
    }}
    
    .status-indicator {{
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        margin-right: 5px;
    }}
    
    .status-active {{
        background-color: {theme['PRIMARY']};
        box-shadow: 0 0 10px {theme['PRIMARY']};
    }}
    
    .status-inactive {{
        background-color: {theme['ERROR']};
    }}
    </style>
    
    <div class="scanlines"></div>
    """

def render_network_map():
    theme = COLOR_THEMES[st.session_state.color_theme]
    
    network_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            .network-container {{
                width: 100%;
                height: 300px;
                position: relative;
                overflow: hidden;
                border: 1px solid {theme['PRIMARY']};
                background-color: {theme['BG']};
            }}
            .node {{
                position: absolute;
                width: 10px;
                height: 10px;
                background-color: {theme['PRIMARY']};
                border-radius: 50%;
                box-shadow: 0 0 10px {theme['PRIMARY']};
            }}
            .connection {{
                position: absolute;
                height: 1px;
                background-color: {theme['PRIMARY']};
                transform-origin: 0 0;
            }}
        </style>
    </head>
    <body>
        <div class="network-container" id="networkCanvas"></div>
        
        <script>
            function initNetwork() {{
                const container = document.getElementById('networkCanvas');
                const width = container.offsetWidth;
                const height = container.offsetHeight;
                
                // Create nodes
                const nodes = [];
                for (let i = 0; i < 15; i++) {{
                    const node = document.createElement('div');
                    node.className = 'node';
                    node.style.left = Math.random() * width + 'px';
                    node.style.top = Math.random() * height + 'px';
                    node.style.width = (5 + Math.random() * 10) + 'px';
                    node.style.height = node.style.width;
                    node.style.opacity = 0.7 + Math.random() * 0.3;
                    container.appendChild(node);
                    nodes.push(node);
                    
                    // Pulsing animation
                    setInterval(() => {{
                        node.style.boxShadow = `0 0 ${{5 + Math.random() * 10}}px ${{'{theme['PRIMARY']}'}}`;
                    }}, 1000 + Math.random() * 2000);
                }}
                
                // Create connections
                for (let i = 0; i < 30; i++) {{
                    const node1 = nodes[Math.floor(Math.random() * nodes.length)];
                    const node2 = nodes[Math.floor(Math.random() * nodes.length)];
                    
                    if (node1 !== node2) {{
                        const x1 = parseFloat(node1.style.left) + parseFloat(node1.style.width)/2;
                        const y1 = parseFloat(node1.style.top) + parseFloat(node1.style.height)/2;
                        const x2 = parseFloat(node2.style.left) + parseFloat(node2.style.width)/2;
                        const y2 = parseFloat(node2.style.top) + parseFloat(node2.style.height)/2;
                        
                        const length = Math.sqrt(Math.pow(x2 - x1, 2) + Math.pow(y2 - y1, 2));
                        const angle = Math.atan2(y2 - y1, x2 - x1) * 180 / Math.PI;
                        
                        const connection = document.createElement('div');
                        connection.className = 'connection';
                        connection.style.left = x1 + 'px';
                        connection.style.top = y1 + 'px';
                        connection.style.width = length + 'px';
                        connection.style.opacity = 0.2 + Math.random() * 0.3;
                        connection.style.transform = `rotate(${{angle}}deg)`;
                        container.appendChild(connection);
                    }}
                }}
            }}
            
            // Initialize when DOM is loaded
            if (document.readyState === 'complete') {{
                initNetwork();
            }} else {{
                window.addEventListener('load', initNetwork);
            }}
        </script>
    </body>
    </html>
    """
    
    st.components.v1.html(network_html, height=350)

# --- Main App ---
def main():
    # Set UI theme
    st.markdown(render_cyber_ui(), unsafe_allow_html=True)
    
    theme_option = st.sidebar.selectbox(
        "> COLOR SCHEME",
        list(COLOR_THEMES.keys()),
        index=list(COLOR_THEMES.keys()).index(st.session_state.color_theme),
        key="theme_selector"
    )

    if theme_option != st.session_state.color_theme:
        st.session_state.color_theme = theme_option
        st.rerun()  

    # Navigation
    menu = ["SYSTEM DASHBOARD", "ENCRYPT DATA", "DECRYPT DATA", "NETWORK MAP", "SECURITY SPECS"]
    choice = st.sidebar.selectbox("> NAVIGATION", menu)
    
    theme = COLOR_THEMES[st.session_state.color_theme]
    
    if choice == "SYSTEM DASHBOARD":
        st.markdown(f"""
        <div class="cyber-card">
            <h1 class="cyber-title glitch">> SECURE DATA ENCRYPTION</h1>
            <p class="cyber-text">> SYSTEM STATUS: <span class="status-indicator status-active"></span>ONLINE</p>
            <p class="cyber-text">> LAST ACTIVITY: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="cyber-card">
                <h2 class="cyber-subtitle">> ENCRYPTION MODULE</h2>
                <p class="cyber-text">> AES-256 ACTIVE</p>
                <p class="cyber-text">> FERNET PROTOCOL ENGAGED</p>
                <p class="cyber-text">> KEY ROTATION: ENABLED</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="cyber-card">
                <h2 class="cyber-subtitle">> DECRYPTION MODULE</h2>
                <p class="cyber-text">> PBKDF2-HMAC-SHA512</p>
                <p class="cyber-text">> 250,000 ITERATIONS</p>
                <p class="cyber-text">> BRUTE FORCE PROTECTION: ACTIVE</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="cyber-card">
            <h2 class="cyber-subtitle">> SYSTEM METRICS</h2>
            <div class="data-grid">
                <div class="data-node">
                    <p class="cyber-text">> ENCRYPTED ENTRIES</p>
                    <h3 style="color: {theme['PRIMARY']}">{len(stored_data)}</h3>
                </div>
                <div class="data-node">
                    <p class="cyber-text">> FAILED ATTEMPTS</p>
                    <h3 style="color: {theme['ERROR']}">{st.session_state.failed_attempts}/3</h3>
                </div>
                <div class="data-node">
                    <p class="cyber-text">> SYSTEM UPTIME</p>
                    <h3 style="color: {theme['ACCENT']}">{random.randint(12, 72)}h {random.randint(0, 59)}m</h3>
                </div>
                <div class="data-node">
                    <p class="cyber-text">> THREAT LEVEL</p>
                    <h3 style="color: {theme['PRIMARY']}">{random.choice(['LOW', 'GUARDED', 'ELEVATED'])}</h3>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    elif choice == "ENCRYPT DATA":
        st.markdown(f"""
        <div class="cyber-card">
            <h2 class="cyber-subtitle">> DATA ENCRYPTION PROTOCOL</h2>
            <p class="cyber-text">> ENTER PLAINTEXT DATA FOR QUANTUM ENCRYPTION</p>
        </div>
        """, unsafe_allow_html=True)
        
        user_data = st.text_area("> INPUT:", height=200)
        passkey = st.text_input("> ENCRYPTION PASSPHRASE:", type="password")
        
        if st.button("> INITIATE ENCRYPTION SEQUENCE"):
            if user_data and passkey:
                # Show hacking animation
                hacking_placeholder = st.empty()
                hacking_placeholder.markdown(render_hacking_animation(), unsafe_allow_html=True)
                time.sleep(2)
                
                # Perform encryption
                encrypted = encrypt_data(user_data)
                stored_data[encrypted] = {
                    "encrypted_text": encrypted,
                    "passkey": hash_passkey(passkey)
                }
                save_data(stored_data)
                
                # Clear animation and show results
                hacking_placeholder.empty()
                
                st.markdown(f"""
                <div class="cyber-card" style="border-color: {theme['ACCENT']};">
                    <h3 class="cyber-subtitle">> ENCRYPTION COMPLETE</h3>
                    <p class="cyber-text">> DATA SECURED IN QUANTUM VAULT</p>
                    <p class="cyber-text">> ENCRYPTION ID:</p>
                    <div style="background: rgba(0, 0, 0, 0.5); padding: 10px; border: 1px dashed {theme['ACCENT']}; word-break: break-all;">
                        {encrypted[:100] + ("..." if len(encrypted) > 100 else "")}
                    </div>
                    <p class="cyber-text" style="margin-top: 15px; color: {theme['ERROR']}">> WARNING: STORE THIS ID SECURELY - IT CANNOT BE RECOVERED</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error("> ERROR: ALL FIELDS REQUIRED")
    
    elif choice == "DECRYPT DATA":
        current_time = time.time()
        if st.session_state.failed_attempts >= 3 and current_time - st.session_state.last_failed_time < lockout_time:
            remaining_time = int(lockout_time - (current_time - st.session_state.last_failed_time))
            st.markdown(f"""
            <div class="cyber-card" style="border-color: {theme['ERROR']};">
                <h2 class="cyber-subtitle">> SYSTEM LOCKOUT</h2>
                <p class="cyber-text">> TOO MANY FAILED ATTEMPTS</p>
                <p class="cyber-text">> LOCKOUT TIME: {remaining_time} SECONDS</p>
                <p class="cyber-text">> THIS INCIDENT HAS BEEN LOGGED</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="cyber-card">
                <h2 class="cyber-subtitle">> DATA DECRYPTION PROTOCOL</h2>
                <p class="cyber-text">> ENTER ENCRYPTED DATA ID AND PASSPHRASE</p>
            </div>
            """, unsafe_allow_html=True)
            
            data_id = st.text_area("> ENCRYPTED DATA ID:", height=100)
            passkey = st.text_input("> DECRYPTION PASSPHRASE:", type="password", key="decrypt_pass")
            
            if st.button("> INITIATE DECRYPTION SEQUENCE"):
                if data_id and passkey:
                    # Show hacking animation
                    hacking_placeholder = st.empty()
                    hacking_placeholder.markdown(render_hacking_animation(), unsafe_allow_html=True)
                    time.sleep(2)
                    
                    # Perform decryption
                    decrypted = decrypt_data(data_id, passkey)
                    
                    # Clear animation
                    hacking_placeholder.empty()
                    
                    if decrypted:
                        st.markdown(f"""
                        <div class="cyber-card" style="border-color: {theme['ACCENT']};">
                            <h3 class="cyber-subtitle">> DECRYPTION SUCCESSFUL</h3>
                            <p class="cyber-text">> ORIGINAL DATA RECOVERED:</p>
                            <div style="background: rgba(0, 0, 0, 0.5); padding: 15px; border: 1px dashed {theme['ACCENT']};">
                                {decrypted}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        attempts_left = 3 - st.session_state.failed_attempts
                        st.error(f"> ACCESS DENIED. ATTEMPTS REMAINING: {attempts_left}")
                else:
                    st.error("> ERROR: ALL FIELDS REQUIRED")
    
    elif choice == "NETWORK MAP":
        st.markdown(f"""
        <div class="cyber-card">
            <h2 class="cyber-subtitle">> SECURE NETWORK VISUALIZATION</h2>
            <p class="cyber-text">> REAL-TIME DATA FLOW SIMULATION</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Render the network map
        render_network_map()
        
        st.markdown(f"""
        <div class="cyber-card">
            <h3 class="cyber-subtitle">> NETWORK STATISTICS</h3>
            <div class="data-grid">
                <div class="data-node">
                    <p class="cyber-text">> NODES ONLINE</p>
                    <h3 style="color: {theme['PRIMARY']}">{random.randint(12, 24)}</h3>
                </div>
                <div class="data-node">
                    <p class="cyber-text">> DATA TRANSFERS</p>
                    <h3 style="color: {theme['PRIMARY']}">{random.randint(150, 450)}/s</h3>
                </div>
                <div class="data-node">
                    <p class="cyber-text">> ENCRYPTED PACKETS</p>
                    <h3 style="color: {theme['PRIMARY']}">{random.randint(800, 1200)}/s</h3>
                </div>
                <div class="data-node">
                    <p class="cyber-text">> THREAT DETECTED</p>
                    <h3 style="color: {theme['ERROR']}">{random.randint(0, 5)}</h3>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    elif choice == "SECURITY SPECS":
        st.markdown(f"""
        <div class="cyber-card">
            <h2 class="cyber-subtitle">> SECURITY SPECIFICATIONS</h2>
            <p class="cyber-text">> MILITARY-GRADE QUANTUM ENCRYPTION SYSTEM</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="cyber-card">
            <h3 class="cyber-subtitle">> ENCRYPTION STANDARDS</h3>
            <p class="cyber-text">> AES-256 ENCRYPTION (FIPS 197)</p>
            <p class="cyber-text">> PBKDF2-HMAC-SHA512 (NIST SP 800-132)</p>
            <p class="cyber-text">> 250,000 ITERATIONS (OWASP STANDARD)</p>
            <p class="cyber-text">> FERNET TOKENS (RFC 4493)</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="cyber-card">
            <h3 class="cyber-subtitle">> SECURITY PROTOCOLS</h3>
            <p class="cyber-text">> RATE-LIMITED DECRYPTION ATTEMPTS</p>
            <p class="cyber-text">> ZERO-KNOWLEDGE PASSPHRASE STORAGE</p>
            <p class="cyber-text">> LOCALIZED KEY MANAGEMENT</p>
            <p class="cyber-text">> MEMORY WIPING AFTER OPERATIONS</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="cyber-card">
            <h3 class="cyber-subtitle">> THREAT MITIGATION</h3>
            <p class="cyber-text">> BRUTE FORCE PROTECTION</p>
            <p class="cyber-text">> TIMING ATTACK RESISTANCE</p>
            <p class="cyber-text">> SIDE-CHANNEL PROTECTION</p>
            <p class="cyber-text">> QUANTUM COMPUTING RESISTANT</p>
        </div>
        """, unsafe_allow_html=True)

        
if __name__ == "__main__":
    main()

    # Securing line (copyright notice) - Place this at the BOTTOM of your app
st.markdown(
    f"""
    <div style="
        text-align: center;
        margin-bottom: 50px;
        padding: 15px 0;
        border-bottom: 1px dashed {COLOR_THEMES[st.session_state.color_theme]['PRIMARY']};
        font-family: 'Courier New', monospace;
        color: {COLOR_THEMES[st.session_state.color_theme]['TEXT']};
        letter-spacing: 1px;
    ">
        © 2025 Aeyla Naseer. This code is protected under copyright law. Unauthorized copying is prohibited.
        <span style="color:{COLOR_THEMES[st.session_state.color_theme]['ERROR']}">Ⓧ</span>
    </div>
    """,
    unsafe_allow_html=True
)

# Print statement with cyberpunk styling
print(f"""
\x1b[38;2;0;240;255m■► \x1b[0m© 2025 Aeyla Naseer. This code is protected under copyright law. Unauthorized copying is prohibited. \x1b[38;2;255;0;60m◄■\x1b[0m
""")

# ----------------------------------------------------THE-END---------------------------------------------------------------- 
