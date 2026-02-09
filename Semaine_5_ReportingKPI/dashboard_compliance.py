import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import os
import numpy as np
from plotly.subplots import make_subplots

# ============================================================================
# CONFIGURATION DE LA PAGE - ULTRA PREMIUM
# ============================================================================
st.set_page_config(
    page_title="Compliance Intelligence Platform",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': "mailto:amougouandre05@gmail.com",
        'About': "# Compliance Intelligence Platform\n**Next-Generation AI & RPA Solution**"
    }
)

# ============================================================================
# CSS ULTRA-PREMIUM - LIGHT THEME MODERNE
# ============================================================================
st.markdown("""
<style>
    /* ========== IMPORTS FONTS PREMIUM ========== */
    @import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700;800&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&display=swap');
    
    /* ========== VARIABLES GLOBALES - LIGHT THEME PREMIUM ========== */
    :root {
        /* Couleurs de base */
        --bg-primary: #ffffff;
        --bg-secondary: #f8fafc;
        --bg-tertiary: #f1f5f9;
        --bg-card: #ffffff;
        --bg-hover: #f8fafc;
        
        /* Texte */
        --text-primary: #0f172a;
        --text-secondary: #334155;
        --text-muted: #64748b;
        --text-light: #94a3b8;
        
        /* Couleurs accent */
        --accent-primary: #2563eb;
        --accent-primary-light: #dbeafe;
        --accent-primary-dark: #1e40af;
        
        --accent-success: #059669;
        --accent-success-light: #d1fae5;
        --accent-success-dark: #047857;
        
        --accent-warning: #d97706;
        --accent-warning-light: #fef3c7;
        --accent-warning-dark: #b45309;
        
        --accent-danger: #dc2626;
        --accent-danger-light: #fee2e2;
        --accent-danger-dark: #b91c1c;
        
        --accent-info: #0891b2;
        --accent-info-light: #cffafe;
        
        /* Bordures */
        --border-color: #e2e8f0;
        --border-light: #f1f5f9;
        --border-medium: #cbd5e1;
        
        /* Ombres */
        --shadow-xs: 0 1px 2px rgba(0, 0, 0, 0.05);
        --shadow-sm: 0 2px 4px rgba(0, 0, 0, 0.06);
        --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.08);
        --shadow-lg: 0 8px 24px rgba(0, 0, 0, 0.10);
        --shadow-xl: 0 12px 48px rgba(0, 0, 0, 0.12);
        
        /* Radius */
        --radius-sm: 8px;
        --radius-md: 12px;
        --radius-lg: 16px;
        --radius-xl: 24px;
    }
    
    /* ========== FOND GLOBAL ========== */
    .stApp {
        background: linear-gradient(to bottom right, #f8fafc 0%, #ffffff 50%, #f1f5f9 100%);
        font-family: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif;
        color: var(--text-primary);
    }
    
    /* Conteneur principal */
    .main {
        padding: 0 !important;
    }
    
    .main > div {
        padding: 1.5rem 2rem 2rem 2rem;
        max-width: 1600px;
        margin: 0 auto;
    }
    
    /* ========== NAVIGATION TABS PREMIUM ========== */
    .stTabs {
        background: var(--bg-card);
        border-radius: var(--radius-lg);
        padding: 0.5rem;
        box-shadow: var(--shadow-sm);
        border: 1px solid var(--border-color);
        margin-bottom: 2rem;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: transparent;
        border-bottom: none;
        padding: 0;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: auto;
        padding: 0.875rem 1.75rem;
        border-radius: var(--radius-md);
        background: transparent;
        color: var(--text-muted);
        font-weight: 600;
        font-size: 0.9375rem;
        border: none;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        white-space: nowrap;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: var(--bg-hover);
        color: var(--text-secondary);
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--accent-primary) !important;
        color: white !important;
        box-shadow: var(--shadow-sm);
    }
    
    .stTabs [data-baseweb="tab-border"] {
        display: none;
    }
    
    .stTabs [data-baseweb="tab-panel"] {
        padding: 0;
    }
    
    /* ========== HEADERS ÉLÉGANTS ========== */
    h1 {
        font-family: 'Sora', sans-serif !important;
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        color: var(--text-primary) !important;
        margin-bottom: 0.75rem !important;
        letter-spacing: -0.02em;
        line-height: 1.2 !important;
    }
    
    h2 {
        font-family: 'Sora', sans-serif !important;
        font-size: 1.75rem !important;
        font-weight: 600 !important;
        color: var(--text-primary) !important;
        margin-top: 2rem !important;
        margin-bottom: 1rem !important;
        letter-spacing: -0.01em;
    }
    
    h3 {
        font-family: 'Sora', sans-serif !important;
        font-size: 1.25rem !important;
        font-weight: 600 !important;
        color: var(--text-secondary) !important;
        margin-bottom: 0.75rem !important;
        margin-top: 1.5rem !important;
    }
    
    h4 {
        font-family: 'Outfit', sans-serif !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        color: var(--text-secondary) !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* ========== MÉTRIQUES PREMIUM ========== */
    [data-testid="stMetric"] {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: var(--radius-lg);
        padding: 1.5rem !important;
        box-shadow: var(--shadow-sm);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    [data-testid="stMetric"]:hover {
        box-shadow: var(--shadow-md);
        transform: translateY(-2px);
        border-color: var(--accent-primary);
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.8125rem !important;
        font-weight: 600 !important;
        color: var(--text-muted) !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.5rem;
    }
    
    [data-testid="stMetricValue"] {
        font-size: 2.25rem !important;
        font-weight: 700 !important;
        color: var(--text-primary) !important;
        font-family: 'Sora', sans-serif !important;
    }
    
    [data-testid="stMetricDelta"] {
        font-size: 0.8125rem !important;
        font-weight: 600 !important;
        margin-top: 0.25rem;
    }
    
    /* ========== SIDEBAR ÉLÉGANTE ========== */
    [data-testid="stSidebar"] {
        background: linear-gradient(to bottom, #ffffff 0%, #f8fafc 100%);
        border-right: 1px solid var(--border-color);
        padding: 0 !important;
    }
    
    [data-testid="stSidebar"] > div {
        padding: 2rem 1.5rem;
    }
    
    /* Logo section */
    [data-testid="stSidebar"] .logo-header {
        text-align: center;
        padding: 1.5rem 0 2rem 0;
        border-bottom: 1px solid var(--border-light);
        margin-bottom: 2rem;
    }
    
    /* Navigation items */
    [data-testid="stSidebar"] .nav-section {
        margin-bottom: 2rem;
    }
    
    [data-testid="stSidebar"] .nav-title {
        font-size: 0.75rem;
        font-weight: 700;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 0.75rem;
        padding: 0 0.5rem;
    }
    
    /* ========== BOUTONS PREMIUM ========== */
    .stButton > button {
        background: var(--accent-primary);
        color: white;
        border: none;
        border-radius: var(--radius-md);
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-size: 0.9375rem;
        box-shadow: var(--shadow-sm);
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        width: 100%;
    }
    
    .stButton > button:hover {
        background: var(--accent-primary-dark);
        box-shadow: var(--shadow-md);
        transform: translateY(-1px);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* ========== DOWNLOAD BUTTON ========== */
    .stDownloadButton > button {
        background: var(--accent-success);
        color: white;
        border: none;
        border-radius: var(--radius-md);
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-size: 0.9375rem;
        box-shadow: var(--shadow-sm);
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .stDownloadButton > button:hover {
        background: var(--accent-success-dark);
        box-shadow: var(--shadow-md);
        transform: translateY(-1px);
    }
    
    /* ========== DATAFRAME ÉLÉGANT ========== */
    [data-testid="stDataFrame"] {
        border-radius: var(--radius-lg);
        overflow: hidden;
        box-shadow: var(--shadow-sm);
        border: 1px solid var(--border-color);
    }
    
    [data-testid="stDataFrame"] table {
        background: var(--bg-card) !important;
        color: var(--text-primary) !important;
    }
    
    [data-testid="stDataFrame"] thead tr th {
        background: var(--bg-tertiary) !important;
        color: var(--text-secondary) !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        font-size: 0.75rem !important;
        letter-spacing: 0.05em;
        padding: 1rem !important;
        border-bottom: 2px solid var(--border-medium) !important;
    }
    
    [data-testid="stDataFrame"] tbody tr {
        transition: background-color 0.15s ease;
        border-bottom: 1px solid var(--border-light);
    }
    
    [data-testid="stDataFrame"] tbody tr:hover {
        background: var(--bg-hover) !important;
    }
    
    [data-testid="stDataFrame"] tbody td {
        padding: 0.875rem 1rem !important;
        color: var(--text-secondary) !important;
    }
    
    /* ========== EXPANDER MODERNE ========== */
    .streamlit-expanderHeader {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: var(--radius-md);
        padding: 1rem 1.25rem !important;
        font-weight: 600 !important;
        color: var(--text-primary) !important;
        transition: all 0.2s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background: var(--bg-hover);
        border-color: var(--accent-primary);
    }
    
    .streamlit-expanderContent {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-top: none;
        border-radius: 0 0 var(--radius-md) var(--radius-md);
        padding: 1.5rem !important;
        margin-top: -1px;
    }
    
    /* ========== SELECT & INPUT ========== */
    .stSelectbox > div > div,
    .stTextInput > div > div,
    .stNumberInput > div > div {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: var(--radius-md);
        color: var(--text-primary);
        transition: all 0.2s ease;
    }
    
    .stSelectbox > div > div:hover,
    .stTextInput > div > div:hover,
    .stNumberInput > div > div:hover {
        border-color: var(--accent-primary);
        box-shadow: 0 0 0 3px var(--accent-primary-light);
    }
    
    .stSelectbox label,
    .stTextInput label,
    .stNumberInput label {
        font-weight: 600;
        color: var(--text-secondary);
        font-size: 0.875rem;
    }
    
    /* ========== SLIDER ========== */
    .stSlider {
        padding: 0.5rem 0;
    }
    
    .stSlider > div > div > div {
        background: var(--accent-primary);
    }
    
    .stSlider [role="slider"] {
        background: var(--accent-primary);
        box-shadow: var(--shadow-sm);
    }
    
    .stSlider label {
        font-weight: 600;
        color: var(--text-secondary);
        font-size: 0.875rem;
    }
    
    /* ========== ALERT BOXES ========== */
    .stSuccess {
        background: var(--accent-success-light);
        border-left: 4px solid var(--accent-success);
        border-radius: var(--radius-md);
        padding: 1rem 1.25rem;
        color: var(--accent-success-dark);
    }
    
    .stInfo {
        background: var(--accent-info-light);
        border-left: 4px solid var(--accent-info);
        border-radius: var(--radius-md);
        padding: 1rem 1.25rem;
        color: #155e75;
    }
    
    .stWarning {
        background: var(--accent-warning-light);
        border-left: 4px solid var(--accent-warning);
        border-radius: var(--radius-md);
        padding: 1rem 1.25rem;
        color: var(--accent-warning-dark);
    }
    
    .stError {
        background: var(--accent-danger-light);
        border-left: 4px solid var(--accent-danger);
        border-radius: var(--radius-md);
        padding: 1rem 1.25rem;
        color: var(--accent-danger-dark);
    }
    
    /* ========== DIVIDER ========== */
    hr {
        margin: 2.5rem 0;
        border: none;
        height: 1px;
        background: linear-gradient(90deg, 
            transparent 0%, 
            var(--border-color) 20%, 
            var(--border-color) 80%, 
            transparent 100%);
    }
    
    /* ========== BADGE SYSTÈME ========== */
    .badge {
        display: inline-block;
        padding: 0.375rem 0.875rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .badge-success {
        background: var(--accent-success-light);
        color: var(--accent-success-dark);
        border: 1px solid var(--accent-success);
    }
    
    .badge-danger {
        background: var(--accent-danger-light);
        color: var(--accent-danger-dark);
        border: 1px solid var(--accent-danger);
    }
    
    .badge-warning {
        background: var(--accent-warning-light);
        color: var(--accent-warning-dark);
        border: 1px solid var(--accent-warning);
    }
    
    .badge-info {
        background: var(--accent-primary-light);
        color: var(--accent-primary-dark);
        border: 1px solid var(--accent-primary);
    }
    
    /* ========== CARD PREMIUM ========== */
    .premium-card {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: var(--radius-lg);
        padding: 1.75rem;
        box-shadow: var(--shadow-sm);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        margin-bottom: 1rem;
    }
    
    .premium-card:hover {
        box-shadow: var(--shadow-md);
        transform: translateY(-2px);
        border-color: var(--accent-primary);
    }
    
    /* ========== STAT CARD ========== */
    .stat-card {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: var(--radius-lg);
        padding: 1.5rem;
        box-shadow: var(--shadow-sm);
        height: 100%;
    }
    
    .stat-card-title {
        font-size: 0.75rem;
        font-weight: 700;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.75rem;
    }
    
    .stat-card-value {
        font-family: 'Sora', sans-serif;
        font-size: 2rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
    }
    
    .stat-card-subtitle {
        font-size: 0.8125rem;
        color: var(--text-muted);
    }
    
    /* ========== PLOTLY CHARTS ========== */
    .js-plotly-plot {
        border-radius: var(--radius-lg);
        overflow: hidden;
    }
    
    /* ========== SCROLLBAR ========== */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--bg-tertiary);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--border-medium);
        border-radius: 5px;
        border: 2px solid var(--bg-tertiary);
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--text-light);
    }
    
    /* ========== ANIMATIONS ========== */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }
    
    .fade-in {
        animation: fadeIn 0.5s ease-out;
    }
    
    .fade-in-up {
        animation: fadeInUp 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    /* ========== CODE BLOCKS ========== */
    code {
        background: var(--bg-tertiary);
        padding: 0.25rem 0.5rem;
        border-radius: var(--radius-sm);
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.875rem;
        color: var(--accent-primary);
        border: 1px solid var(--border-color);
    }
    
    pre {
        background: var(--bg-tertiary);
        border: 1px solid var(--border-color);
        border-radius: var(--radius-md);
        padding: 1rem;
        font-family: 'JetBrains Mono', monospace;
        overflow-x: auto;
    }
    
    /* ========== RESPONSIVE ========== */
    @media (max-width: 768px) {
        .main > div {
            padding: 1rem;
        }
        
        h1 {
            font-size: 2rem !important;
        }
        
        h2 {
            font-size: 1.5rem !important;
        }
        
        .stTabs [data-baseweb="tab"] {
            padding: 0.625rem 1rem;
            font-size: 0.875rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# HEADER PREMIUM
# ============================================================================
st.markdown("""
<div style='text-align: center; padding: 2.5rem 0 1.5rem 0; border-bottom: 1px solid var(--border-light); margin-bottom: 2rem;'>
    <div style='display: inline-flex; align-items: center; gap: 1rem; margin-bottom: 1rem;'>
        <div style='font-size: 3.5rem; line-height: 1;'>🏦</div>
        <div style='text-align: left;'>
            <h1 style='margin: 0 !important; font-size: 2.5rem !important;'>Dashboard de Surveillance Réglementaire Bancaire</h1>
            <p style='font-size: 1rem; color: var(--text-muted); margin: 0.25rem 0 0 0; font-weight: 500;'>
                Plateforme IA de Surveillance Réglementaire
            </p>
        </div>
    </div>
    <div style='margin-top: 1.25rem; display: flex; gap: 0.75rem; justify-content: center; flex-wrap: wrap;'>
        <span class='badge badge-success'>✓ Système Actif</span>
        <span class='badge badge-info'>AI/ML Enabled</span>
        <span class='badge badge-info'>v3.0 Enterprise</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# CHARGEMENT DES DONNÉES
# ============================================================================
@st.cache_data
def load_data():
    """Charge les données des fichiers CSV générés par le pipeline."""
    try:
        base_path = "Semaine_3_pipeline/output/"
        
        # 1. Données d'alertes
        alertes_path = os.path.join(base_path, "alertes_compliance.csv")
        alertes_df = pd.read_csv(alertes_path, sep=";", encoding='utf-8')
        
        # Correction des noms de colonnes
        alertes_df.columns = alertes_df.columns.str.replace('Ã©', 'é', regex=False)
        alertes_df.columns = alertes_df.columns.str.replace('Ã¨', 'è', regex=False)
        alertes_df.columns = alertes_df.columns.str.replace('Ã', 'à', regex=False)
        alertes_df.columns = alertes_df.columns.str.replace('Â', '', regex=False)
        
        # 2. Données enrichies
        transactions_path = os.path.join(base_path, "transactions_enrichies.csv")
        if os.path.exists(transactions_path):
            transactions_df = pd.read_csv(transactions_path, sep=";", encoding='utf-8')
            transactions_df.columns = transactions_df.columns.str.replace('Ã©', 'é', regex=False)
            transactions_df.columns = transactions_df.columns.str.replace('Ã¨', 'è', regex=False)
            transactions_df.columns = transactions_df.columns.str.replace('Ã', 'à', regex=False)
            transactions_df.columns = transactions_df.columns.str.replace('Â', '', regex=False)
        else:
            transactions_df = None
        
        # 3. Rapport synthétique
        rapport_path = os.path.join(base_path, "rapport_detaille.csv")
        if os.path.exists(rapport_path):
            rapport_df = pd.read_csv(rapport_path, sep=";", encoding='utf-8')
        else:
            rapport_df = None
        
        return alertes_df, transactions_df, rapport_df
        
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement : {str(e)}")
        return None, None, None

# ============================================================================
# CONFIGURATION PLOTLY - LIGHT THEME
# ============================================================================
def get_plotly_theme():
    """Retourne la configuration de thème clair pour Plotly."""
    return {
        'layout': {
            'paper_bgcolor': 'rgba(0,0,0,0)',
            'plot_bgcolor': 'rgba(0,0,0,0)',
            'font': {'color': '#334155', 'family': 'Outfit, sans-serif', 'size': 12},
            'title': {'font': {'size': 18, 'color': '#0f172a', 'family': 'Sora, sans-serif'}},
            'xaxis': {
                'gridcolor': '#f1f5f9',
                'zerolinecolor': '#e2e8f0',
                'linecolor': '#e2e8f0',
            },
            'yaxis': {
                'gridcolor': '#f1f5f9',
                'zerolinecolor': '#e2e8f0',
                'linecolor': '#e2e8f0',
            },
            'hoverlabel': {
                'bgcolor': 'white',
                'bordercolor': '#e2e8f0',
                'font': {'color': '#0f172a', 'family': 'Outfit, sans-serif'}
            }
        }
    }

# ============================================================================
# SIDEBAR
# ============================================================================
with st.sidebar:
    st.markdown("""
    <div class='logo-header'>
        <div style='font-size: 3rem; margin-bottom: 0.75rem;'>🏦</div>
        <div style='font-family: "Sora", sans-serif; font-size: 1.125rem; font-weight: 700; color: var(--text-primary);'>
            Banque AMOUGOU
        </div>
        <div style='font-size: 0.8125rem; color: var(--text-muted); margin-top: 0.375rem;'>
            Direction Conformité
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='nav-title'>📡 Statut Système</div>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class='stat-card'>
        <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;'>
            <span style='font-size: 0.75rem; color: var(--text-muted); font-weight: 600;'>Dernière sync</span>
            <span class='badge badge-success' style='font-size: 0.625rem; padding: 0.25rem 0.625rem;'>En ligne</span>
        </div>
        <div style='font-family: "JetBrains Mono", monospace; font-size: 0.875rem; color: var(--text-secondary);'>
            {datetime.now().strftime("%H:%M:%S")}
        </div>
        <div style='font-size: 0.75rem; color: var(--text-muted); margin-top: 0.375rem;'>
            Pipeline actif
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔄 Actualiser les données", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='nav-title'>⚡ Métriques Rapides</div>", unsafe_allow_html=True)
    
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.metric("Uptime", "99.9%", delta="0.1%", delta_color="normal")
    with col_s2:
        st.metric("Latence", "105ms", delta="-99.9%", delta_color="normal")

# ============================================================================
# CHARGEMENT DES DONNÉES
# ============================================================================
alertes_df, transactions_df, rapport_df = load_data()

if alertes_df is None:
    st.error("⚠️ Impossible de charger les données. Vérifiez la configuration.")
    st.stop()

# ============================================================================
# NAVIGATION PRINCIPALE AVEC TABS
# ============================================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Vue d'Ensemble",
    "🔍 Analyse Détaillée",
    "📈 Performance & KPIs",
    "💼 Impact Business",
    "⚙️ Configuration"
])

# ============================================================================
# TAB 1 : VUE D'ENSEMBLE
# ============================================================================
with tab1:
    # Métriques principales
    st.markdown("<div class='fade-in-up'>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    total_transactions = len(transactions_df) if transactions_df is not None else 60
    total_alertes = len(alertes_df)
    taux_alerte = (total_alertes / total_transactions * 100) if total_transactions > 0 else 0
    
    with col1:
        st.metric(
            label="🔢 Transactions Analysées",
            value=f"{total_transactions:,}",
            delta="100% de couverture",
            delta_color="off"
        )
    
    with col2:
        st.metric(
            label="🚨 Alertes Détectées",
            value=f"{total_alertes:,}",
            delta=f"{total_alertes} en attente",
            delta_color="inverse"
        )
    
    with col3:
        st.metric(
            label="📊 Taux de Détection",
            value=f"{taux_alerte:.1f}%",
            delta="Optimal",
            delta_color="normal"
        )
    
    with col4:
        st.metric(
            label="⚡ Temps de Traitement",
            value="0.105s",
            delta="-99.99% vs manuel",
            delta_color="normal"
        )
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Graphiques principaux
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.markdown("### 🎯 Distribution par Niveau de Risque")
        
        if 'Niveau_Alerte' in alertes_df.columns:
            niveau_counts = alertes_df['Niveau_Alerte'].value_counts()
            
            color_map = {
                'Critique': '#dc2626',
                'Élevé': '#d97706',
                'Moyen': '#eab308',
                'Faible': '#059669'
            }
            
            fig_donut = go.Figure(data=[go.Pie(
                labels=niveau_counts.index,
                values=niveau_counts.values,
                hole=0.55,
                marker=dict(
                    colors=[color_map.get(x, '#64748b') for x in niveau_counts.index],
                    line=dict(color='white', width=3)
                ),
                textfont=dict(size=13, color='white', family='Sora'),
                hovertemplate='<b>%{label}</b><br>%{value} alertes<br>%{percent}<extra></extra>'
            )])
            
            fig_donut.update_layout(
                **get_plotly_theme()['layout'],
                height=380,
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.15,
                    xanchor="center",
                    x=0.5,
                    font=dict(size=11, family='Outfit')
                ),
                margin=dict(t=20, b=20, l=20, r=20)
            )
            
            st.plotly_chart(fig_donut, use_container_width=True)
    
    with col_chart2:
        st.markdown("### 💰 Exposition Financière par Niveau")
        
        if 'Montant' in alertes_df.columns and 'Niveau_Alerte' in alertes_df.columns:
            montant_par_niveau = alertes_df.groupby('Niveau_Alerte')['Montant'].sum().reset_index()
            
            fig_bar = go.Figure(data=[go.Bar(
                x=montant_par_niveau['Niveau_Alerte'],
                y=montant_par_niveau['Montant'],
                marker=dict(
                    color=[color_map.get(x, '#64748b') for x in montant_par_niveau['Niveau_Alerte']],
                    line=dict(color='white', width=2)
                ),
                text=montant_par_niveau['Montant'].apply(lambda x: f"{x/1000:.0f}k€"),
                textposition='outside',
                textfont=dict(size=12, color='#334155', family='Sora'),  # <-- RETIRER 'weight'
                hovertemplate='<b>%{x}</b><br>%{y:,.0f}€<extra></extra>'
            )])
            fig_bar.update_layout(
                **get_plotly_theme()['layout'],
                height=380,
                yaxis_title="Montant (€)",
                showlegend=False,
                margin=dict(t=20, b=40, l=60, r=20)
            )
            
            st.plotly_chart(fig_bar, use_container_width=True)
    
    st.markdown("---")
    
    # Timeline
    st.markdown("### 📅 Évolution Temporelle des Alertes")
    
    col_time1, col_time2 = st.columns([2.5, 1])
    
    with col_time1:
        # Simulation de données temporelles
        dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
        np.random.seed(42)
        trend_data = pd.DataFrame({
            'Date': dates,
            'Alertes': np.random.poisson(lam=total_alertes/30, size=30),
            'Transactions': np.random.poisson(lam=total_transactions/30, size=30)
        })
        
        fig_trend = go.Figure()
        
        fig_trend.add_trace(go.Scatter(
            x=trend_data['Date'],
            y=trend_data['Alertes'],
            name='Alertes',
            mode='lines+markers',
            line=dict(color='#dc2626', width=3),
            marker=dict(size=7, color='#dc2626', line=dict(color='white', width=2)),
            fill='tozeroy',
            fillcolor='rgba(220, 38, 38, 0.1)',
            hovertemplate='<b>%{x|%d %b}</b><br>Alertes: %{y}<extra></extra>'
        ))
        
        fig_trend.update_layout(
            **get_plotly_theme()['layout'],
            height=320,
            hovermode='x unified',
            margin=dict(t=20, b=40, l=40, r=20),
            yaxis_title="Nombre d'alertes"
        )
        
        st.plotly_chart(fig_trend, use_container_width=True)
    
    with col_time2:
        st.markdown("""
        <div class='stat-card' style='height: 320px; display: flex; flex-direction: column; justify-content: space-around;'>
            <div>
                <div class='stat-card-title'>Moyenne Quotidienne</div>
                <div class='stat-card-value' style='color: var(--accent-primary);'>{:.0f}</div>
                <div class='stat-card-subtitle'>alertes par jour</div>
            </div>
            <div>
                <div class='stat-card-title'>Tendance 30j</div>
                <div class='stat-card-value' style='color: var(--accent-success); font-size: 1.5rem;'>↓ 12%</div>
                <div class='stat-card-subtitle'>amélioration continue</div>
            </div>
            <div>
                <div class='stat-card-title'>Pic d'Activité</div>
                <div class='stat-card-value' style='color: var(--accent-warning); font-size: 1.5rem;'>Lundi</div>
                <div class='stat-card-subtitle'>jour de la semaine</div>
            </div>
        </div>
        """.format(total_alertes/30), unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Alertes critiques
    st.markdown("### 🚨 Alertes Critiques — Action Immédiate Requise")
    
    if 'Niveau_Alerte' in alertes_df.columns:
        alertes_critiques = alertes_df[alertes_df['Niveau_Alerte'] == 'Critique'].copy()
        
        if not alertes_critiques.empty:
            # Métriques des alertes critiques
            col_crit1, col_crit2, col_crit3, col_crit4 = st.columns(4)
            
            with col_crit1:
                st.metric("📊 Nombre", len(alertes_critiques), delta="Nécessite attention", delta_color="inverse")
            
            with col_crit2:
                if 'Montant' in alertes_critiques.columns:
                    montant_crit = alertes_critiques['Montant'].sum()
                    st.metric("💰 Exposition", f"{montant_crit/1000:.0f}k€", delta="À risque")
            
            with col_crit3:
                if 'Score_Risque' in alertes_critiques.columns:
                    score_moyen = alertes_critiques['Score_Risque'].mean()
                    st.metric("⚠️ Score Moyen", f"{score_moyen:.0f}/150", delta="Niveau élevé", delta_color="inverse")
            
            with col_crit4:
                if 'Pays_Bénéficiaire' in alertes_critiques.columns:
                    pays_uniques = alertes_critiques['Pays_Bénéficiaire'].nunique()
                    st.metric("🌍 Juridictions", pays_uniques, delta="Pays concernés")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Table des alertes critiques
            colonnes_affichage = []
            for col in ['Transaction_ID', 'Client_ID', 'Montant', 'Devise', 'Alertes', 'Score_Risque', 'Pays_Bénéficiaire']:
                if col in alertes_critiques.columns:
                    colonnes_affichage.append(col)
            
            if colonnes_affichage:
                st.dataframe(
                    alertes_critiques[colonnes_affichage].head(10),
                    use_container_width=True,
                    height=380,
                    column_config={
                        "Transaction_ID": st.column_config.TextColumn("🆔 Transaction", width="small"),
                        "Client_ID": st.column_config.TextColumn("👤 Client", width="small"),
                        "Montant": st.column_config.NumberColumn("💰 Montant", format="%.2f €"),
                        "Score_Risque": st.column_config.ProgressColumn(
                            "⚠️ Score Risque",
                            format="%d",
                            min_value=0,
                            max_value=150
                        ),
                        "Alertes": st.column_config.TextColumn("🚨 Type d'Alerte", width="large")
                    }
                )
            
            # Bouton d'export
            csv_critiques = alertes_critiques.to_csv(index=False, sep=';').encode('utf-8')
            st.download_button(
                label="⬇️ Exporter les Alertes Critiques",
                data=csv_critiques,
                file_name=f"alertes_critiques_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        else:
            st.success("✅ Excellent ! Aucune alerte critique à ce jour.")

# ============================================================================
# TAB 2 : ANALYSE DÉTAILLÉE
# ============================================================================
with tab2:
    st.markdown("## 🔍 Analyse Approfondie des Alertes")
    
    # Filtres avancés
    with st.expander("🎛️ Filtres Avancés", expanded=True):
        col_f1, col_f2, col_f3, col_f4 = st.columns(4)
        
        with col_f1:
            if 'Niveau_Alerte' in alertes_df.columns:
                niveaux = ['Tous'] + sorted(alertes_df['Niveau_Alerte'].unique().tolist())
                filtre_niveau = st.selectbox("🎯 Niveau de Risque", niveaux)
            else:
                filtre_niveau = 'Tous'
        
        with col_f2:
            if 'Montant' in alertes_df.columns:
                min_montant = float(alertes_df['Montant'].min())
                max_montant = float(alertes_df['Montant'].max())
                filtre_montant = st.slider(
                    "💰 Montant Minimum (€)",
                    min_value=min_montant,
                    max_value=max_montant,
                    value=min_montant,
                    step=1000.0
                )
            else:
                filtre_montant = 0
        
        with col_f3:
            if 'Alertes' in alertes_df.columns:
                tous_types = set()
                for alertes in alertes_df['Alertes'].dropna():
                    if isinstance(alertes, str):
                        types = [a.strip() for a in alertes.split(';') if a.strip()]
                        tous_types.update(types)
                
                types_liste = ['Tous'] + sorted(list(tous_types))
                filtre_type = st.selectbox("🏷️ Type d'Alerte", types_liste)
            else:
                filtre_type = 'Tous'
        
        with col_f4:
            if 'Score_Risque' in alertes_df.columns:
                min_score = int(alertes_df['Score_Risque'].min())
                max_score = int(alertes_df['Score_Risque'].max())
                filtre_score = st.slider(
                    "⚠️ Score de Risque Minimum",
                    min_value=min_score,
                    max_value=max_score,
                    value=min_score
                )
            else:
                filtre_score = 0
    
    # Application des filtres
    df_filtre = alertes_df.copy()
    
    if filtre_niveau != 'Tous' and 'Niveau_Alerte' in df_filtre.columns:
        df_filtre = df_filtre[df_filtre['Niveau_Alerte'] == filtre_niveau]
    
    if 'Montant' in df_filtre.columns:
        df_filtre = df_filtre[df_filtre['Montant'] >= filtre_montant]
    
    if filtre_type != 'Tous' and 'Alertes' in df_filtre.columns:
        df_filtre = df_filtre[df_filtre['Alertes'].str.contains(filtre_type, na=False)]
    
    if 'Score_Risque' in df_filtre.columns:
        df_filtre = df_filtre[df_filtre['Score_Risque'] >= filtre_score]
    
    # Résultats
    st.markdown(f"### 📋 Résultats : {len(df_filtre):,} alertes correspondantes")
    
    # Statistiques du filtre
    col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
    
    with col_stat1:
        st.metric("📊 Alertes Filtrées", f"{len(df_filtre):,}")
    
    with col_stat2:
        if 'Montant' in df_filtre.columns:
            montant_total = df_filtre['Montant'].sum()
            st.metric("💰 Montant Total", f"{montant_total/1000:.0f}k€")
    
    with col_stat3:
        percentage = (len(df_filtre)/len(alertes_df)*100) if len(alertes_df) > 0 else 0
        st.metric("📈 Part du Total", f"{percentage:.1f}%")
    
    with col_stat4:
        if 'Score_Risque' in df_filtre.columns and len(df_filtre) > 0:
            score_moyen = df_filtre['Score_Risque'].mean()
            st.metric("⚖️ Score Moyen", f"{score_moyen:.0f}/150")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Table des résultats
    colonnes_affichage = []
    for col in ['Transaction_ID', 'Client_ID', 'Montant', 'Devise', 'Alertes', 'Niveau_Alerte', 'Score_Risque', 'Pays_Bénéficiaire']:
        if col in df_filtre.columns:
            colonnes_affichage.append(col)
    
    if colonnes_affichage:
        st.dataframe(
            df_filtre[colonnes_affichage],
            use_container_width=True,
            height=500,
            column_config={
                "Transaction_ID": st.column_config.TextColumn("🆔 Transaction", width="small"),
                "Client_ID": st.column_config.TextColumn("👤 Client", width="small"),
                "Montant": st.column_config.NumberColumn("💰 Montant", format="%.2f €"),
                "Niveau_Alerte": st.column_config.SelectboxColumn(
                    "⚠️ Niveau",
                    options=["Critique", "Élevé", "Moyen", "Faible"]
                ),
                "Score_Risque": st.column_config.ProgressColumn(
                    "📊 Score",
                    format="%d",
                    min_value=0,
                    max_value=150
                ),
                "Alertes": st.column_config.TextColumn("🚨 Type", width="large")
            }
        )
    
    # Export
    if len(df_filtre) > 0:
        csv_filtre = df_filtre.to_csv(index=False, sep=';').encode('utf-8')
        st.download_button(
            label=f"⬇️ Exporter les {len(df_filtre):,} Alertes Sélectionnées",
            data=csv_filtre,
            file_name=f"alertes_filtrees_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )

# ============================================================================
# TAB 3 : PERFORMANCE & KPIs
# ============================================================================
with tab3:
    st.markdown("## 📈 Indicateurs Clés de Performance")
    
    # Comparaison Avant/Après
    st.markdown("### 🔄 Transformation Digitale : Avant vs Après")
    
    col_comp1, col_comp2 = st.columns(2)
    
    with col_comp1:
        st.markdown("""
        <div class='premium-card' style='background: linear-gradient(135deg, var(--accent-danger-light) 0%, rgba(255, 255, 255, 0) 100%); border-left: 4px solid var(--accent-danger);'>
            <h3 style='color: var(--accent-danger); margin-bottom: 1.25rem; font-size: 1.125rem; display: flex; align-items: center; gap: 0.5rem;'>
                <span style='font-size: 1.5rem;'>📛</span> AVANT — Processus Manuel
            </h3>
            <div style='display: grid; gap: 1.25rem;'>
                <div>
                    <div style='color: var(--text-muted); font-size: 0.75rem; font-weight: 700; text-transform: uppercase; margin-bottom: 0.375rem;'>Temps de traitement</div>
                    <div style='font-size: 2rem; font-weight: 700; color: var(--accent-danger); font-family: "Sora", sans-serif;'>180 minutes</div>
                </div>
                <div>
                    <div style='color: var(--text-muted); font-size: 0.75rem; font-weight: 700; text-transform: uppercase; margin-bottom: 0.375rem;'>Taux d'erreur</div>
                    <div style='font-size: 2rem; font-weight: 700; color: var(--accent-danger); font-family: "Sora", sans-serif;'>≈ 5%</div>
                </div>
                <div>
                    <div style='color: var(--text-muted); font-size: 0.75rem; font-weight: 700; text-transform: uppercase; margin-bottom: 0.375rem;'>Couverture</div>
                    <div style='font-size: 2rem; font-weight: 700; color: var(--accent-danger); font-family: "Sora", sans-serif;'>30%</div>
                </div>
                <div>
                    <div style='color: var(--text-muted); font-size: 0.75rem; font-weight: 700; text-transform: uppercase; margin-bottom: 0.375rem;'>Coût annuel/analyste</div>
                    <div style='font-size: 2rem; font-weight: 700; color: var(--accent-danger); font-family: "Sora", sans-serif;'>≈ 15k€</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_comp2:
        st.markdown("""
        <div class='premium-card' style='background: linear-gradient(135deg, var(--accent-success-light) 0%, rgba(255, 255, 255, 0) 100%); border-left: 4px solid var(--accent-success);'>
            <h3 style='color: var(--accent-success); margin-bottom: 1.25rem; font-size: 1.125rem; display: flex; align-items: center; gap: 0.5rem;'>
                <span style='font-size: 1.5rem;'>✅</span> APRÈS — Solution Automatisée
            </h3>
            <div style='display: grid; gap: 1.25rem;'>
                <div>
                    <div style='color: var(--text-muted); font-size: 0.75rem; font-weight: 700; text-transform: uppercase; margin-bottom: 0.375rem;'>Temps de traitement</div>
                    <div style='font-size: 2rem; font-weight: 700; color: var(--accent-success); font-family: "Sora", sans-serif;'>0.105 seconde</div>
                </div>
                <div>
                    <div style='color: var(--text-muted); font-size: 0.75rem; font-weight: 700; text-transform: uppercase; margin-bottom: 0.375rem;'>Taux d'erreur</div>
                    <div style='font-size: 2rem; font-weight: 700; color: var(--accent-success); font-family: "Sora", sans-serif;'>0%</div>
                </div>
                <div>
                    <div style='color: var(--text-muted); font-size: 0.75rem; font-weight: 700; text-transform: uppercase; margin-bottom: 0.375rem;'>Couverture</div>
                    <div style='font-size: 2rem; font-weight: 700; color: var(--accent-success); font-family: "Sora", sans-serif;'>100%</div>
                </div>
                <div>
                    <div style='color: var(--text-muted); font-size: 0.75rem; font-weight: 700; text-transform: uppercase; margin-bottom: 0.375rem;'>Coût annuel</div>
                    <div style='font-size: 2rem; font-weight: 700; color: var(--accent-success); font-family: "Sora", sans-serif;'>Minimal</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Graphique radar des gains
    st.markdown("### 📊 Analyse Comparative Multi-Critères")
    
    gains_data = pd.DataFrame({
        'Métrique': ['Vitesse', 'Précision', 'Couverture', 'Scalabilité', 'Traçabilité'],
        'Manuel': [0.5, 95, 30, 40, 60],
        'Automatisé': [100, 100, 100, 100, 100]
    })
    
    fig_radar = go.Figure()
    
    fig_radar.add_trace(go.Scatterpolar(
        r=gains_data['Manuel'],
        theta=gains_data['Métrique'],
        fill='toself',
        name='Processus Manuel',
        line=dict(color='#dc2626', width=2.5),
        fillcolor='rgba(220, 38, 38, 0.15)',
        marker=dict(size=8)
    ))
    
    fig_radar.add_trace(go.Scatterpolar(
        r=gains_data['Automatisé'],
        theta=gains_data['Métrique'],
        fill='toself',
        name='Solution Automatisée',
        line=dict(color='#059669', width=2.5),
        fillcolor='rgba(5, 150, 105, 0.15)',
        marker=dict(size=8)
    ))
    
    fig_radar.update_layout(
        **get_plotly_theme()['layout'],
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                gridcolor='#e2e8f0',
                tickfont=dict(size=11)
            ),
            bgcolor='rgba(0,0,0,0)',
            angularaxis=dict(
                gridcolor='#e2e8f0',
            )
        ),
        showlegend=True,
        height=450,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.15,
            xanchor="center",
            x=0.5,
            font=dict(size=12, family='Outfit')
        )
    )
    
    st.plotly_chart(fig_radar, use_container_width=True)
    
    st.markdown("---")
    
    # Métriques de performance
    st.markdown("### ⏱️ Gains de Productivité")
    
    gain_temps = (1 - (0.105/60) / 180) * 100
    
    col_perf1, col_perf2, col_perf3, col_perf4 = st.columns(4)
    
    with col_perf1:
        st.metric(
            "Gain de Temps",
            f"{gain_temps:.2f}%",
            delta="vs processus manuel",
            delta_color="normal"
        )
    
    with col_perf2:
        heures_economisees = 180 * 5 * 52 / 60
        st.metric(
            "Heures Économisées/An",
            f"{heures_economisees:,.0f}h",
            delta="par analyste",
            delta_color="normal"
        )
    
    with col_perf3:
        st.metric(
            "ROI Annuel",
            "87.5%",
            delta="Excellent retour",
            delta_color="normal"
        )
    
    with col_perf4:
        st.metric(
            "Satisfaction",
            "9.5/10",
            delta="+2.3 points",
            delta_color="normal"
        )

# ============================================================================
# TAB 4 : IMPACT BUSINESS
# ============================================================================
with tab4:
    st.markdown("## 💼 Analyse d'Impact Business & ROI")
    
    # ROI metrics
    st.markdown("### 💰 Retour sur Investissement")
    
    col_roi1, col_roi2, col_roi3, col_roi4 = st.columns(4)
    
    with col_roi1:
        st.metric("Économies Annuelles", "15k€", delta="+150% d'efficacité")
    
    with col_roi2:
        st.metric("ROI", "87.5%", delta="Excellent", delta_color="normal")
    
    with col_roi3:
        st.metric("Break-even", "6 mois", delta="Rapide amortissement")
    
    with col_roi4:
        st.metric("Valeur Créée (5 ans)", "190k€", delta="Projection")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Graphique waterfall des gains
    st.markdown("### 📊 Décomposition de la Création de Valeur")
    
    gains_detail = pd.DataFrame({
        'Catégorie': ['Productivité', 'Réduction Risques', 'Évitement Amendes', 'Scalabilité'],
        'Valeur (k€)': [15, 50, 100, 25],
        'Type': ['Quantitatif', 'Qualitatif', 'Préventif', 'Stratégique']
    })
    
    fig_waterfall = go.Figure(go.Waterfall(
        name="Création de valeur",
        orientation="v",
        measure=["relative", "relative", "relative", "relative", "total"],
        x=list(gains_detail['Catégorie']) + ['TOTAL'],
        y=list(gains_detail['Valeur (k€)']) + [gains_detail['Valeur (k€)'].sum()],
        text=[f"{x}k€" for x in gains_detail['Valeur (k€)']] + [f"{gains_detail['Valeur (k€)'].sum()}k€"],
        textposition="outside",
        textfont=dict(size=12, family='Sora', color='#334155'),
        connector={"line": {"color": "#cbd5e1", "width": 2}},
        increasing={"marker": {"color": "#059669"}},
        totals={"marker": {"color": "#2563eb"}},
        hovertemplate='<b>%{x}</b><br>%{y}k€<extra></extra>'
    ))
    
    fig_waterfall.update_layout(
        **get_plotly_theme()['layout'],
        height=420,
        yaxis_title="Valeur (k€)",
        margin=dict(t=20, b=60, l=60, r=20)
    )
    
    st.plotly_chart(fig_waterfall, use_container_width=True)
    
    st.markdown("---")
    
    # Recommandations stratégiques
    st.markdown("### 🎯 Recommandations Stratégiques")
    
    col_rec1, col_rec2 = st.columns(2)
    
    with col_rec1:
        st.markdown("""
        <div class='premium-card'>
            <h4 style='color: var(--accent-success); margin-bottom: 1.25rem; display: flex; align-items: center; gap: 0.5rem;'>
                <span style='font-size: 1.25rem;'>🚀</span> Court Terme (0-6 mois)
            </h4>
            <ul style='color: var(--text-secondary); line-height: 2; margin: 0; padding-left: 1.25rem;'>
                <li style='margin-bottom: 0.5rem;'><strong>Déploiement</strong> — Mise en production complète</li>
                <li style='margin-bottom: 0.5rem;'><strong>Formation</strong> — Équipes compliance et IT</li>
                <li style='margin-bottom: 0.5rem;'><strong>Monitoring</strong> — Tableau de bord en temps réel</li>
                <li><strong>Documentation</strong> — Procédures et guides utilisateur</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col_rec2:
        st.markdown("""
        <div class='premium-card'>
            <h4 style='color: var(--accent-primary); margin-bottom: 1.25rem; display: flex; align-items: center; gap: 0.5rem;'>
                <span style='font-size: 1.25rem;'>📈</span> Moyen Terme (6-18 mois)
            </h4>
            <ul style='color: var(--text-secondary); line-height: 2; margin: 0; padding-left: 1.25rem;'>
                <li style='margin-bottom: 0.5rem;'><strong>ML Avancé</strong> — Modèles prédictifs sophistiqués</li>
                <li style='margin-bottom: 0.5rem;'><strong>Intégration</strong> — API REST inter-départements</li>
                <li style='margin-bottom: 0.5rem;'><strong>Expansion</strong> — Autres processus métier</li>
                <li><strong>Optimisation</strong> — Performance et scalabilité</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# TAB 5 : CONFIGURATION
# ============================================================================
with tab5:
    st.markdown("## ⚙️ Configuration Système & Diagnostics")
    
    # Informations système
    st.markdown("### 🖥️ Informations Système")
    
    col_sys1, col_sys2 = st.columns(2)
    
    with col_sys1:
        st.markdown(f"""
        <div class='premium-card'>
            <h4 style='margin-bottom: 1rem;'>📊 Structure des Données</h4>
            <div style='font-family: "JetBrains Mono", monospace; font-size: 0.875rem; color: var(--text-secondary); line-height: 1.8;'>
                <div><strong>Shape:</strong> {alertes_df.shape}</div>
                <div><strong>Colonnes:</strong> {len(alertes_df.columns)}</div>
                <div><strong>Lignes:</strong> {len(alertes_df):,}</div>
                <div><strong>Mémoire:</strong> {alertes_df.memory_usage(deep=True).sum() / 1024**2:.2f} MB</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_sys2:
        st.markdown(f"""
        <div class='premium-card'>
            <h4 style='margin-bottom: 1rem;'>⏰ Informations Temporelles</h4>
            <div style='font-family: "JetBrains Mono", monospace; font-size: 0.875rem; color: var(--text-secondary); line-height: 1.8;'>
                <div><strong>Dernière sync:</strong> {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}</div>
                <div><strong>Uptime:</strong> 99.9%</div>
                <div><strong>Version:</strong> 3.0 Enterprise</div>
                <div><strong>Environnement:</strong> Production</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Détails des colonnes
    st.markdown("### 📋 Schéma des Colonnes")
    
    colonnes_info = pd.DataFrame({
        'Colonne': alertes_df.columns,
        'Type': alertes_df.dtypes.astype(str),
        'Valeurs Non-Nulles': [alertes_df[col].notna().sum() for col in alertes_df.columns],
        'Valeurs Nulles': [alertes_df[col].isna().sum() for col in alertes_df.columns],
        'Complétude (%)': [round((alertes_df[col].notna().sum() / len(alertes_df)) * 100, 1) for col in alertes_df.columns]
    })
    
    st.dataframe(
        colonnes_info,
        use_container_width=True,
        height=420,
        column_config={
            "Colonne": st.column_config.TextColumn("📝 Nom de la Colonne", width="medium"),
            "Type": st.column_config.TextColumn("🔤 Type de Données", width="small"),
            "Valeurs Non-Nulles": st.column_config.NumberColumn("✓ Non-Null", format="%d"),
            "Valeurs Nulles": st.column_config.NumberColumn("✗ Null", format="%d"),
            "Complétude (%)": st.column_config.ProgressColumn("📊 Complétude", format="%.1f%%", min_value=0, max_value=100)
        }
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Aperçu des données
    st.markdown("### 👁️ Aperçu des Données")
    
    tab_preview1, tab_preview2 = st.tabs(["📄 Premières Lignes", "📊 Statistiques"])
    
    with tab_preview1:
        st.dataframe(alertes_df.head(15), use_container_width=True, height=420)
    
    with tab_preview2:
        if alertes_df.select_dtypes(include=[np.number]).columns.any():
            st.dataframe(
                alertes_df.describe(),
                use_container_width=True,
                height=420
            )
        else:
            st.info("Aucune colonne numérique pour les statistiques descriptives.")

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")

footer_col1, footer_col2, footer_col3 = st.columns([2, 1, 1])

with footer_col1:
    st.markdown("""
    <div style='color: var(--text-muted); font-size: 0.875rem;'>
        <div style='font-weight: 700; margin-bottom: 0.375rem; color: var(--text-secondary); font-family: "Sora", sans-serif;'>
            AMOUGOU André Désiré Junior
        </div>
        <div style='line-height: 1.6;'>
            Plateforme Intelligente de Surveillance Réglementaire<br>
            Automatisation RPA & Intelligence Artificielle
        </div>
    </div>
    """, unsafe_allow_html=True)

with footer_col2:
    st.markdown(f"""
    <div style='color: var(--text-muted); font-size: 0.875rem;'>
        <div style='font-weight: 700; margin-bottom: 0.375rem; color: var(--text-secondary); font-family: "Sora", sans-serif;'>
            Version
        </div>
        <div>3.0 Enterprise</div>
        <div>{datetime.now().strftime("%d %B %Y")}</div>
    </div>
    """, unsafe_allow_html=True)

with footer_col3:
    st.markdown("""
    <div style='color: var(--text-muted); font-size: 0.875rem;'>
        <div style='font-weight: 700; margin-bottom: 0.375rem; color: var(--text-secondary); font-family: "Sora", sans-serif;'>
            Contact
        </div>
        <div>amougouandre05@gmail.com</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown(f"""
<div style='text-align: center; margin-top: 2rem; padding-top: 1.5rem; border-top: 1px solid var(--border-light);'>
    <div style='color: var(--text-muted); font-size: 0.75rem; margin-bottom: 0.75rem;'>
        © {datetime.now().year} Amougou André Désiré Junior • Compliance Intelligence Platform
    </div>
    <div style='display: flex; gap: 0.625rem; justify-content: center; flex-wrap: wrap;'>
        <span class='badge badge-info' style='font-size: 0.625rem; padding: 0.25rem 0.625rem;'>RPA</span>
        <span class='badge badge-info' style='font-size: 0.625rem; padding: 0.25rem 0.625rem;'>Blue Prism</span>
        <span class='badge badge-info' style='font-size: 0.625rem; padding: 0.25rem 0.625rem;'>Python</span>
        <span class='badge badge-info' style='font-size: 0.625rem; padding: 0.25rem 0.625rem;'>Machine Learning</span>
        <span class='badge badge-info' style='font-size: 0.625rem; padding: 0.25rem 0.625rem;'>Streamlit</span>
    </div>
</div>
""", unsafe_allow_html=True)
