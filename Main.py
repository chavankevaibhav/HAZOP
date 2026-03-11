import streamlit as st
import json
import random
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Optional
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="HAZOP.AI — Process Hazard Intelligence",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS to match the original design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Barlow:wght@300;400;500;600;700&family=Barlow+Condensed:wght@400;600;700;900&display=swap');
    
    .main {
        background-color: #0a0d0f;
        color: #c8d8e0;
    }
    
    .stApp {
        background-color: #0a0d0f;
    }
    
    h1, h2, h3 {
        font-family: 'Barlow Condensed', sans-serif !important;
        color: #eaf4f8 !important;
        letter-spacing: 1px;
    }
    
    .stButton>button {
        background-color: #00c8a0 !important;
        color: #050f0d !important;
        font-family: 'Barlow Condensed', sans-serif !important;
        font-weight: 700 !important;
        letter-spacing: 2px !important;
        border: none !important;
        border-radius: 0 !important;
    }
    
    .stButton>button:hover {
        background-color: #00e8b8 !important;
        transform: translateY(-1px);
    }
    
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>select {
        background-color: #151c20 !important;
        color: #eaf4f8 !important;
        border: 1px solid #1e2d36 !important;
        border-radius: 0 !important;
        font-family: 'Barlow', sans-serif !important;
    }
    
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        border-color: #00c8a0 !important;
        box-shadow: 0 0 0 1px rgba(0,200,160,0.15) !important;
    }
    
    .stSelectbox>div>div {
        background-color: #151c20 !important;
        border: 1px solid #1e2d36 !important;
        border-radius: 0 !important;
    }
    
    .risk-badge {
        display: inline-block;
        font-family: 'Share Tech Mono', monospace;
        font-size: 11px;
        letter-spacing: 2px;
        padding: 4px 12px;
        font-weight: 700;
        margin: 4px 0;
    }
    
    .risk-LOW { 
        background: rgba(0,200,160,0.15); 
        color: #00c8a0; 
        border: 1px solid #00c8a0; 
    }
    .risk-MEDIUM { 
        background: rgba(255,209,102,0.15); 
        color: #ffd166; 
        border: 1px solid #ffd166; 
    }
    .risk-HIGH { 
        background: rgba(255,107,43,0.15); 
        color: #ff6b2b; 
        border: 1px solid #ff6b2b; 
    }
    .risk-CRITICAL { 
        background: rgba(255,59,59,0.2); 
        color: #ff3b3b; 
        border: 1px solid #ff3b3b; 
        animation: pulse-red 1.5s ease-in-out infinite;
    }
    
    @keyframes pulse-red {
        0%, 100% { box-shadow: 0 0 0 0 rgba(255,59,59,0.3); }
        50% { box-shadow: 0 0 0 6px rgba(255,59,59,0); }
    }
    
    .panel {
        background: #111820;
        border: 1px solid #1e2d36;
        border-top: 2px solid #00c8a0;
        padding: 24px;
        margin-bottom: 20px;
    }
    
    .panel-title {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 3px;
        color: #5a7a8a;
        text-transform: uppercase;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .section-header {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 3px;
        text-transform: uppercase;
        margin-bottom: 10px;
        padding-bottom: 8px;
        border-bottom: 1px solid #1e2d36;
    }
    
    .causes-h { color: #ffd166 !important; }
    .conseq-h { color: #ff6b2b !important; }
    .safeguard-h { color: #00c8a0 !important; }
    .action-h { color: #a78bfa !important; }
    
    .sil-level {
        display: inline-block;
        width: 50px;
        height: 28px;
        line-height: 28px;
        text-align: center;
        font-family: 'Share Tech Mono', monospace;
        font-size: 12px;
        font-weight: 700;
        border: 1px solid #1e2d36;
        color: #5a7a8a;
        background: #0a0d0f;
        margin-right: 6px;
    }
    
    .sil-level.active {
        background: rgba(255,107,43,0.15);
        border-color: #ff6b2b;
        color: #ff6b2b;
    }
    
    .history-item {
        background: #151c20;
        border: 1px solid #1e2d36;
        padding: 10px 14px;
        margin-bottom: 8px;
        cursor: pointer;
        transition: all 0.15s;
    }
    
    .history-item:hover {
        border-color: #00c8a0;
    }
    
    .mono {
        font-family: 'Share Tech Mono', monospace;
    }
    
    .hero-tag {
        font-family: 'Share Tech Mono', monospace;
        font-size: 11px;
        color: #ff6b2b;
        letter-spacing: 4px;
        text-transform: uppercase;
        margin-bottom: 16px;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background-color: #111820;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #151c20;
        border: 1px solid #1e2d36;
        color: #5a7a8a;
        border-radius: 0;
        font-family: 'Share Tech Mono', monospace;
        font-size: 11px;
        letter-spacing: 1px;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #00c8a0 !important;
        color: #050f0d !important;
        font-weight: 700;
    }
    
    .guideword-btn {
        background: #151c20;
        border: 1px solid #1e2d36;
        color: #5a7a8a;
        padding: 8px 10px;
        font-family: 'Share Tech Mono', monospace;
        font-size: 12px;
        letter-spacing: 1px;
        cursor: pointer;
        transition: all 0.15s;
        text-align: center;
        margin: 2px;
    }
    
    .guideword-btn:hover {
        border-color: #00c8a0;
        color: #00c8a0;
    }
    
    .guideword-btn.active {
        background: rgba(0,200,160,0.1);
        border-color: #00c8a0;
        color: #00c8a0;
    }
    
    .template-chip {
        display: inline-block;
        background: #151c20;
        border: 1px solid #1e2d36;
        color: #5a7a8a;
        font-family: 'Share Tech Mono', monospace;
        font-size: 10px;
        padding: 6px 12px;
        margin: 2px;
        cursor: pointer;
        transition: all 0.15s;
        letter-spacing: 1px;
    }
    
    .template-chip:hover {
        border-color: #ffd166;
        color: #ffd166;
    }
    
    .result-narrative {
        background: #151c20;
        border: 1px solid #1e2d36;
        border-left: 3px solid #00c8a0;
        padding: 16px 20px;
        font-size: 14px;
        line-height: 1.7;
        color: #c8d8e0;
        margin-bottom: 20px;
    }
    
    .risk-matrix {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 4px;
        max-width: 300px;
        margin-bottom: 20px;
    }
    
    .matrix-cell {
        aspect-ratio: 1;
        display: flex;
        align-items: center;
        justify-content: center;
        font-family: 'Share Tech Mono', monospace;
        font-size: 10px;
        border: 1px solid #1e2d36;
        background: #151c20;
        color: #5a7a8a;
    }
    
    .matrix-cell.low { background: rgba(0,200,160,0.2); border-color: #00c8a0; color: #00c8a0; }
    .matrix-cell.medium { background: rgba(255,209,102,0.2); border-color: #ffd166; color: #ffd166; }
    .matrix-cell.high { background: rgba(255,107,43,0.2); border-color: #ff6b2b; color: #ff6b2b; }
    .matrix-cell.critical { background: rgba(255,59,59,0.25); border-color: #ff3b3b; color: #ff3b3b; }
    .matrix-cell.active { box-shadow: 0 0 0 2px #eaf4f8; transform: scale(1.1); z-index: 1; }
    
    div[data-testid="stToolbar"] { display: none !important; }
    div[data-testid="stDecoration"] { display: none !important; }
    div[data-testid="stStatusWidget"] { display: none !important; }
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# Data structures
@dataclass
class HAZOPResult:
    risk_level: str
    sil_recommendation: int
    sil_rationale: str
    narrative: str
    causes: List[str]
    consequences: List[str]
    existing_safeguards: List[str]
    recommended_actions: List[str]

@dataclass
class HAZOPAnalysis:
    node: str
    process_type: str
    parameter: str
    guideword: str
    deviation: str
    context: str
    result: HAZOPResult
    timestamp: str
    notes: str = ""

# Templates
TEMPLATES = {
    'CDU Feed': {'node': 'CDU Feed Preheat Train E-101', 'process': 'Crude Distillation Unit', 'param': 'Temperature', 'gw': 'MORE OF'},
    'Reactor': {'node': 'Hydrotreater Reactor R-101', 'process': 'Hydrotreater / HDS Unit', 'param': 'Pressure', 'gw': 'MORE OF'},
    'Compressor': {'node': 'Recycle Gas Compressor K-101', 'process': 'Hydrotreater / HDS Unit', 'param': 'Flow', 'gw': 'LESS OF'},
    'Storage': {'node': 'Crude Storage Tank T-101', 'process': 'Storage / Loading', 'param': 'Level', 'gw': 'MORE OF'},
    'Column': {'node': 'Debutanizer Column C-201', 'process': 'LPG Fractionation', 'param': 'Pressure', 'gw': 'MORE OF'}
}

GUIDEWORDS = ['NO/NONE', 'MORE OF', 'LESS OF', 'AS WELL AS', 'PART OF', 'REVERSE', 'OTHER THAN', 'EARLY', 'LATE']

PROCESS_TYPES = [
    "Crude Distillation Unit",
    "Hydrotreater / HDS Unit",
    "Catalytic Reformer",
    "Amine Gas Treating",
    "Sour Water Stripper",
    "LPG Fractionation",
    "Hydrogen Plant / SMR",
    "Compressor Train",
    "Storage / Loading",
    "Cooling Water System"
]

PARAMETERS = ["Flow", "Temperature", "Pressure", "Level", "Composition", "Reaction", "Utility"]

# Session state initialization
if 'history' not in st.session_state:
    st.session_state.history = []
if 'current_analysis' not in st.session_state:
    st.session_state.current_analysis = None
if 'selected_guideword' not in st.session_state:
    st.session_state.selected_guideword = None

def generate_mock_result(param: str, gw: str) -> HAZOPResult:
    """Generate mock HAZOP analysis results"""
    risk_levels = ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']
    risk_level = random.choice(risk_levels)
    sil_map = {'LOW': 0, 'MEDIUM': 1, 'HIGH': 2, 'CRITICAL': 3}
    
    return HAZOPResult(
        risk_level=risk_level,
        sil_recommendation=sil_map[risk_level],
        sil_rationale=f"Based on {risk_level} risk classification per IEC 61511",
        narrative=f"Deviation {gw} {param} presents significant process safety concerns requiring immediate evaluation per OSHA PSM standards.",
        causes=[
            f"Control valve failure causing {gw.lower()} {param.lower()}",
            "Instrument malfunction or drift",
            "Operator error during startup/shutdown",
            "Upstream process upset"
        ],
        consequences=[
            f"Equipment damage due to {gw.lower()} {param.lower()}",
            "Potential release of hydrocarbons",
            "Fire and explosion hazard",
            "Environmental violation"
        ],
        existing_safeguards=[
            "High/Low alarms on DCS",
            "Safety Instrumented System (SIS) interlocks",
            "Pressure relief valve",
            "Operator training procedures"
        ],
        recommended_actions=[
            "Verify SIS setpoints per IEC 61511",
            "Conduct SIL verification study",
            "Update operating procedures",
            "Schedule preventive maintenance"
        ]
    )

def render_risk_matrix(risk_level: str):
    """Render the risk matrix visualization"""
    matrix_html = '<div class="risk-matrix">'
    
    # Header row
    matrix_html += '<div class="matrix-cell header"></div>'
    for h in ['A', 'B', 'C', 'D']:
        matrix_html += f'<div class="matrix-cell header">{h}</div>'
    
    # Matrix data
    data = [
        ('1', ['low', 'low', 'medium', 'medium']),
        ('2', ['low', 'medium', 'medium', 'high']),
        ('3', ['medium', 'medium', 'high', 'critical']),
        ('4', ['medium', 'high', 'critical', 'critical'])
    ]
    
    risk_class = risk_level.lower()
    
    for row_num, cells in data:
        matrix_html += f'<div class="matrix-cell header">{row_num}</div>'
        for cell in cells:
            active = 'active' if cell == risk_class else ''
            matrix_html += f'<div class="matrix-cell {cell} {active}">{cell[0].upper()}</div>'
    
    matrix_html += '</div>'
    return matrix_html

def render_sil_bar(sil_level: int):
    """Render SIL requirement bar"""
    html = '<div style="display:flex; align-items:center; gap:16px; flex-wrap:wrap; margin-top:20px;">'
    html += '<span class="mono" style="color:#5a7a8a; font-size:11px; letter-spacing:2px;">SIL REQUIREMENT</span>'
    html += '<div>'
    
    levels = [0, 1, 2, 3]
    labels = {0: 'N/A', 1: 'SIL 1', 2: 'SIL 2', 3: 'SIL 3'}
    
    for level in levels:
        active = 'active' if level == sil_level else ''
        html += f'<div class="sil-level {active}">{labels[level]}</div>'
    
    html += '</div></div>'
    return html

def export_json(data, filename):
    """Export data as JSON file"""
    json_str = json.dumps(data, indent=2, default=lambda o: asdict(o) if hasattr(o, '__dataclass_fields__') else str(o))
    st.download_button(
        label="📥 Download JSON",
        data=json_str,
        file_name=filename,
        mime="application/json"
    )

def main():
    # Header
    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown("""
        <div style="display:flex; align-items:center; gap:12px; margin-bottom:20px;">
            <div style="width:36px; height:36px; background:#00c8a0; clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%); display:flex; align-items:center; justify-content:center; font-size:16px;">⬡</div>
            <div style="font-family:'Barlow Condensed', sans-serif; font-size:28px; font-weight:900; letter-spacing:3px; color:#eaf4f8;">
                HAZOP<span style="color:#00c8a0;">.AI</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="text-align:right; font-family:'Share Tech Mono', monospace; font-size:11px; color:#00c8a0; border:1px solid #00c8a0; padding:4px 10px; display:inline-block; letter-spacing:2px; opacity:0.7; float:right;">
            OIL & GAS // PROCESS SAFETY
        </div>
        """, unsafe_allow_html=True)
    
    # Hero section
    st.markdown('<div class="hero-tag">// AI-Powered Root Cause Analysis</div>', unsafe_allow_html=True)
    st.markdown('<h1 style="font-size:clamp(36px, 6vw, 64px); font-weight:900; line-height:1; margin-bottom:16px;">Process Hazard<br><span style="color:#00c8a0;">Intelligence</span></h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:#5a7a8a; max-width:520px; margin-bottom:30px;">Describe your process node and deviation. AI analyzes causes, consequences, safeguards and recommends protective actions per IEC 61511.</p>', unsafe_allow_html=True)
    
    # Main layout
    col_input, col_history = st.columns([2, 1])
    
    with col_input:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title"><span style="color:#00c8a0; margin-right:8px;">●</span> Node & Deviation Setup</div>', unsafe_allow_html=True)
        
        # Template chips
        st.markdown('<div style="margin-bottom:16px;"><span style="color:#5a7a8a; font-size:10px; font-family:Share Tech Mono; letter-spacing:1px; margin-right:8px;">QUICK:</span>', unsafe_allow_html=True)
        template_cols = st.columns(5)
        for idx, (name, template) in enumerate(TEMPLATES.items()):
            with template_cols[idx]:
                if st.button(name, key=f"tpl_{name}", use_container_width=True):
                    st.session_state.node_input = template['node']
                    st.session_state.process_type = template['process']
                    st.session_state.parameter = template['param']
                    st.session_state.selected_guideword = template['gw']
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Form inputs
        node = st.text_input("Process Node / Equipment", 
                           value=st.session_state.get('node_input', ''),
                           placeholder="e.g. Feed Preheat Train E-101, Distillation Column C-201...",
                           key="node_input")
        
        col_proc, col_param = st.columns(2)
        with col_proc:
            process_type = st.selectbox("Process Type", 
                                      [""] + PROCESS_TYPES,
                                      index=0 if not st.session_state.get('process_type') else PROCESS_TYPES.index(st.session_state.get('process_type', '')) + 1,
                                      key="process_type")
        with col_param:
            parameter = st.selectbox("Parameter", 
                                   [""] + PARAMETERS,
                                   index=0 if not st.session_state.get('parameter') else PARAMETERS.index(st.session_state.get('parameter', '')) + 1,
                                   key="parameter")
        
        # Guideword selection
        st.markdown('<div style="margin-bottom:8px;"><span style="font-family:Share Tech Mono; font-size:11px; color:#5a7a8a; letter-spacing:2px;">GUIDEWORD</span></div>', unsafe_allow_html=True)
        gw_cols = st.columns(3)
        selected_gw = st.session_state.get('selected_guideword')
        for idx, gw in enumerate(GUIDEWORDS):
            with gw_cols[idx % 3]:
                btn_class = "guideword-btn active" if selected_gw == gw else "guideword-btn"
                if st.button(gw, key=f"gw_{gw}", use_container_width=True):
                    st.session_state.selected_guideword = gw if selected_gw != gw else None
                    st.rerun()
        
        context = st.text_area("Additional Context (optional)", 
                             placeholder="Operating conditions, feed composition, previous incidents, nearby equipment, special concerns...",
                             height=100)
        
        # Analyze button
        if st.button("⬡ ANALYZE DEVIATION", use_container_width=True, type="primary"):
            if not node or not process_type or not parameter or not st.session_state.get('selected_guideword'):
                st.error("Please fill in all required fields")
            else:
                with st.spinner("Analyzing..."):
                    import time
                    time.sleep(1.5)  # Simulate API call
                    
                    deviation = f"{st.session_state.selected_guideword} {parameter}"
                    result = generate_mock_result(parameter, st.session_state.selected_guideword)
                    
                    analysis = HAZOPAnalysis(
                        node=node,
                        process_type=process_type,
                        parameter=parameter,
                        guideword=st.session_state.selected_guideword,
                        deviation=deviation,
                        context=context,
                        result=result,
                        timestamp=datetime.now().isoformat()
                    )
                    
                    st.session_state.current_analysis = analysis
                    st.session_state.history.insert(0, analysis)
                    st.rerun()
        
        st.markdown('<div style="text-align:center; margin-top:8px; font-family:Share Tech Mono; font-size:10px; color:#5a7a8a;">Press Ctrl+Enter to analyze</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_history:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title"><span style="color:#00c8a0; margin-right:8px;">●</span> Session History</div>', unsafe_allow_html=True)
        
        search = st.text_input("", placeholder="Search history...", label_visibility="collapsed")
        
        if st.button("Clear All", key="clear_history"):
            st.session_state.history = []
            st.session_state.current_analysis = None
            st.rerun()
        
        # History list
        if not st.session_state.history:
            st.markdown("""
            <div style="text-align:center; padding:40px 20px; color:#5a7a8a;">
                <div style="font-size:32px; margin-bottom:10px; opacity:0.3">📋</div>
                <p style="font-family:Share Tech Mono; font-size:12px; letter-spacing:1px">No analyses yet</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            filtered_history = [h for h in st.session_state.history 
                              if search.lower() in h.node.lower() or 
                                 search.lower() in h.deviation.lower() or
                                 search.lower() in h.process_type.lower()]
            
            for idx, item in enumerate(filtered_history):
                with st.container():
                    st.markdown(f"""
                    <div class="history-item" onclick="window.location.reload()">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <div>
                                <div style="font-size:13px; font-weight:600; color:#eaf4f8; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; max-width:200px;">{item.node[:35]}{'...' if len(item.node) > 35 else ''}</div>
                                <div class="mono" style="font-size:10px; color:#5a7a8a; letter-spacing:1px;">{item.guideword} {item.parameter} · {item.process_type} · {datetime.fromisoformat(item.timestamp).strftime('%Y-%m-%d')}</div>
                            </div>
                            <div class="risk-badge risk-{item.result.risk_level}" style="font-size:9px; padding:2px 8px;">{item.result.risk_level}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button("Load", key=f"load_{idx}", use_container_width=True):
                        st.session_state.current_analysis = item
                        st.session_state.node_input = item.node
                        st.session_state.process_type = item.process_type
                        st.session_state.parameter = item.parameter
                        st.session_state.selected_guideword = item.guideword
                        st.rerun()
                    
                    if st.button("🗑", key=f"del_{idx}"):
                        st.session_state.history.remove(item)
                        if st.session_state.current_analysis == item:
                            st.session_state.current_analysis = None
                        st.rerun()
        
        # Quick reference
        st.markdown('<hr style="border-color:#1e2d36; margin:20px 0;">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title"><span style="color:#ffd166; margin-right:8px;">●</span> Quick Reference</div>', unsafe_allow_html=True)
        
        with st.expander("STANDARDS"):
            st.markdown("IEC 61511 · API RP 14C · API 750 · IEC 61508 · OSHA PSM 29 CFR 1910.119")
        with st.expander("RISK MATRIX"):
            st.markdown("Severity × Likelihood → LOW / MEDIUM / HIGH / CRITICAL")
        with st.expander("SIL LEVELS"):
            st.markdown("SIL 1 (PFD 0.1–0.01) · SIL 2 (0.01–0.001) · SIL 3 (0.001–0.0001)")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Results panel
    st.markdown('<div class="panel" style="border-top-color:#ff6b2b;">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title"><span style="color:#ff6b2b; margin-right:8px;">●</span> HAZOP Analysis Output</div>', unsafe_allow_html=True)
    
    if st.session_state.current_analysis is None:
        st.markdown("""
        <div style="text-align:center; padding:50px 20px; color:#5a7a8a;">
            <div style="font-size:48px; margin-bottom:16px; opacity:0.3;">⬡</div>
            <p class="mono" style="font-size:13px; letter-spacing:1px;">Select a node, parameter, and guideword<br>then click ANALYZE DEVIATION</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        analysis = st.session_state.current_analysis
        
        # Result header
        col_res1, col_res2 = st.columns([3, 1])
        with col_res1:
            st.markdown(f'<div class="mono" style="font-size:10px; color:#5a7a8a; letter-spacing:2px; margin-bottom:4px;">DEVIATION ANALYSIS</div>', unsafe_allow_html=True)
            st.markdown(f'<h2 style="margin:0; font-size:24px;">{analysis.node} — {analysis.deviation}</h2>', unsafe_allow_html=True)
            st.markdown(f'<div class="mono" style="font-size:10px; color:#5a7a8a; margin-top:4px;">{datetime.fromisoformat(analysis.timestamp).strftime("%Y-%m-%d %H:%M:%S")}</div>', unsafe_allow_html=True)
        
        with col_res2:
            st.markdown(f'<div class="risk-badge risk-{analysis.result.risk_level}" style="float:right; margin-top:20px;">⬡ {analysis.result.risk_level}</div>', unsafe_allow_html=True)
        
        # Action buttons
        col_copy, col_save, col_export = st.columns(3)
        with col_copy:
            if st.button("📋 Copy to Clipboard"):
                text = f"""HAZOP ANALYSIS
==============
Node: {analysis.node}
Deviation: {analysis.deviation}
Process: {analysis.process_type}
Risk Level: {analysis.result.risk_level}
SIL: {analysis.result.sil_recommendation if analysis.result.sil_recommendation > 0 else 'N/A'}

NARRATIVE:
{analysis.result.narrative}

CAUSES:
{chr(10).join('• ' + c for c in analysis.result.causes)}

CONSEQUENCES:
{chr(10).join('• ' + c for c in analysis.result.consequences)}

SAFEGUARDS:
{chr(10).join('• ' + s for s in analysis.result.existing_safeguards)}

ACTIONS:
{chr(10).join('• ' + a for a in analysis.result.recommended_actions)}"""
                st.code(text)
                st.success("Copied! (Select and copy the text above)")
        
        with col_save:
            export_json(analysis, f"hazop-{analysis.node.replace(' ', '_')}-{int(datetime.now().timestamp())}.json")
        
        with col_export:
            if st.button("📤 Export Session"):
                session_data = {
                    "exportDate": datetime.now().isoformat(),
                    "version": "1.0",
                    "analyses": st.session_state.history
                }
                export_json(session_data, f"hazop-session-{datetime.now().strftime('%Y-%m-%d')}.json")
        
        st.markdown("<hr style='border-color:#1e2d36; margin:20px 0;'>", unsafe_allow_html=True)
        
        # Risk Matrix
        st.markdown('<div class="mono" style="font-size:10px; color:#5a7a8a; letter-spacing:2px; margin-bottom:8px;">RISK MATRIX VISUALIZATION</div>', unsafe_allow_html=True)
        st.markdown(render_risk_matrix(analysis.result.risk_level), unsafe_allow_html=True)
        
        # Narrative
        st.markdown(f'<div class="result-narrative">{analysis.result.narrative}</div>', unsafe_allow_html=True)
        
        # Result sections
        col_causes, col_conseq = st.columns(2)
        with col_causes:
            with st.expander("⚡ Possible Causes", expanded=True):
                for cause in analysis.result.causes:
                    st.markdown(f"• {cause}")
        
        with col_conseq:
            with st.expander("💥 Consequences", expanded=True):
                for cons in analysis.result.consequences:
                    st.markdown(f"• {cons}")
        
        col_safe, col_action = st.columns(2)
        with col_safe:
            with st.expander("🛡 Existing Safeguards", expanded=True):
                for safeguard in analysis.result.existing_safeguards:
                    st.markdown(f"• {safeguard}")
        
        with col_action:
            with st.expander("📋 Recommended Actions", expanded=True):
                for action in analysis.result.recommended_actions:
                    st.markdown(f"• {action}")
        
        # Notes
        st.markdown("<hr style='border-color:#1e2d36; margin:20px 0;'>", unsafe_allow_html=True)
        notes = st.text_area("📝 Engineer Notes", 
                           value=analysis.notes,
                           placeholder="Add your observations, team discussions, or follow-up actions here...")
        if notes != analysis.notes:
            analysis.notes = notes
            # Update in history
            for h in st.session_state.history:
                if h.timestamp == analysis.timestamp and h.node == analysis.node:
                    h.notes = notes
        
        # SIL Bar
        st.markdown(render_sil_bar(analysis.result.sil_recommendation), unsafe_allow_html=True)
        st.markdown(f'<div style="font-size:12px; color:#5a7a8a; margin-top:8px; font-style:italic;">{analysis.result.sil_rationale}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Import section in sidebar
    with st.sidebar:
        st.markdown("## Import Analysis")
        import_text = st.text_area("Paste JSON data from a previous export:", height=200)
        if st.button("Import Data"):
            try:
                data = json.loads(import_text)
                if 'analyses' in data:
                    st.session_state.history = data['analyses'] + st.session_state.history
                elif 'result' in data:
                    st.session_state.history.insert(0, data)
                st.success("Data imported successfully!")
                st.rerun()
            except:
                st.error("Invalid JSON format")

if __name__ == "__main__":
    main()
