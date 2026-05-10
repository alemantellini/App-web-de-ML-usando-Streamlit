import streamlit as st
import pickle
import numpy as np
import pandas as pd
import os

# Configuración
st.set_page_config(
    page_title="Vinoteca · Calidad de vino con IA",
    page_icon="🍷",
    layout="centered",
)

# CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Josefin+Sans:wght@300;400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Josefin Sans', sans-serif;
}

.stApp {
    background: #1a0a0f;
    background-image:
        radial-gradient(ellipse at 20% 20%, rgba(120, 20, 40, 0.15) 0%, transparent 60%),
        radial-gradient(ellipse at 80% 80%, rgba(80, 10, 25, 0.2) 0%, transparent 60%);
}

#MainMenu, footer, header { visibility: hidden; }

/* Hero */
.hero {
    text-align: center;
    padding: 56px 0 40px;
    position: relative;
}
.hero-ornament {
    font-size: 48px;
    margin-bottom: 16px;
    display: block;
    filter: drop-shadow(0 0 20px rgba(180, 120, 60, 0.4));
}
.hero-eyebrow {
    font-family: 'Josefin Sans', sans-serif;
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    color: #b47c3c;
    margin-bottom: 14px;
}
.hero-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: clamp(2.8rem, 6vw, 4.5rem);
    font-weight: 300;
    color: #f5ede0;
    line-height: 1.05;
    letter-spacing: -0.01em;
    margin-bottom: 8px;
}
.hero-title em {
    font-style: italic;
    color: #c8956a;
}
.hero-divider {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
    margin: 20px auto;
    max-width: 320px;
}
.hero-divider::before,
.hero-divider::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(180, 124, 60, 0.4));
}
.hero-divider::after {
    background: linear-gradient(270deg, transparent, rgba(180, 124, 60, 0.4));
}
.hero-diamond {
    width: 6px; height: 6px;
    background: #b47c3c;
    transform: rotate(45deg);
}
.hero-sub {
    font-family: 'Cormorant Garamond', serif;
    font-style: italic;
    font-size: 1.05rem;
    color: #8a7060;
    max-width: 420px;
    margin: 0 auto;
    line-height: 1.7;
}

/* Section label */
.section-label {
    font-family: 'Josefin Sans', sans-serif;
    font-size: 9px;
    font-weight: 600;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    color: #b47c3c;
    margin: 36px 0 20px;
    display: flex;
    align-items: center;
    gap: 14px;
}
.section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: rgba(180, 124, 60, 0.2);
}

/* Streamlit widgets */
div[data-testid="stNumberInput"] label,
div[data-testid="stSlider"] label {
    color: #8a7060 !important;
    font-family: 'Josefin Sans', sans-serif !important;
    font-size: 10px !important;
    font-weight: 600 !important;
    letter-spacing: 0.2em !important;
    text-transform: uppercase !important;
}

div[data-testid="stNumberInput"] input {
    background: rgba(245, 237, 224, 0.04) !important;
    border: 1px solid rgba(180, 124, 60, 0.2) !important;
    border-radius: 8px !important;
    color: #f5ede0 !important;
    font-family: 'Cormorant Garamond', serif !important;
    font-size: 1.1rem !important;
}

div[data-testid="stNumberInput"] input:focus {
    border-color: rgba(180, 124, 60, 0.5) !important;
    box-shadow: 0 0 0 2px rgba(180, 124, 60, 0.1) !important;
}

/* Button */
div[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #7a1e2e, #a0293d) !important;
    color: #f5ede0 !important;
    font-family: 'Josefin Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 11px !important;
    letter-spacing: 0.25em !important;
    text-transform: uppercase !important;
    border: 1px solid rgba(180, 124, 60, 0.3) !important;
    border-radius: 4px !important;
    padding: 16px 0 !important;
    width: 100% !important;
    transition: all 0.3s !important;
}
div[data-testid="stButton"] > button:hover {
    background: linear-gradient(135deg, #8f2335, #b8304a) !important;
    border-color: rgba(180, 124, 60, 0.6) !important;
    box-shadow: 0 4px 24px rgba(120, 30, 46, 0.4) !important;
    transform: translateY(-1px) !important;
}

/* Result */
.result-card {
    border-radius: 4px;
    padding: 36px 40px;
    margin-top: 28px;
    position: relative;
    overflow: hidden;
    text-align: center;
}
.result-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, #b47c3c, transparent);
}
.result-high {
    background: linear-gradient(160deg, rgba(120, 30, 46, 0.25), rgba(80, 15, 25, 0.15));
    border: 1px solid rgba(180, 124, 60, 0.25);
}
.result-mid {
    background: linear-gradient(160deg, rgba(100, 70, 20, 0.2), rgba(60, 40, 10, 0.12));
    border: 1px solid rgba(180, 124, 60, 0.2);
}
.result-low {
    background: linear-gradient(160deg, rgba(40, 40, 60, 0.2), rgba(20, 20, 40, 0.12));
    border: 1px solid rgba(100, 100, 140, 0.2);
}
.result-score {
    font-family: 'Cormorant Garamond', serif;
    font-size: 5rem;
    font-weight: 300;
    line-height: 1;
    margin-bottom: 4px;
}
.result-high .result-score { color: #c8956a; }
.result-mid .result-score { color: #b47c3c; }
.result-low .result-score { color: #6a7080; }

.result-out-of {
    font-family: 'Josefin Sans', sans-serif;
    font-size: 10px;
    letter-spacing: 0.2em;
    color: #6a5a4a;
    margin-bottom: 16px;
}
.result-label {
    font-family: 'Cormorant Garamond', serif;
    font-style: italic;
    font-size: 1.4rem;
    margin-bottom: 20px;
}
.result-high .result-label { color: #f5ede0; }
.result-mid .result-label { color: #d4b896; }
.result-low .result-label { color: #8a8a9a; }

.stars {
    font-size: 1.2rem;
    letter-spacing: 4px;
    margin-bottom: 20px;
}
.result-desc {
    font-family: 'Cormorant Garamond', serif;
    font-style: italic;
    font-size: 0.95rem;
    color: #6a5a4a;
    line-height: 1.7;
    max-width: 360px;
    margin: 0 auto 20px;
}
.disclaimer {
    font-family: 'Josefin Sans', sans-serif;
    font-size: 9px;
    letter-spacing: 0.1em;
    color: #4a3a30;
    line-height: 1.8;
    border-top: 1px solid rgba(180, 124, 60, 0.1);
    padding-top: 16px;
    margin-top: 4px;
}

/* Footer */
.footer {
    text-align: center;
    padding: 48px 0 24px;
    font-family: 'Josefin Sans', sans-serif;
    font-size: 9px;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #3a2a22;
}
.footer a { color: #b47c3c; text-decoration: none; }
</style>
""", unsafe_allow_html=True)

# Cargar el modelo
@st.cache_resource
def load_model():
    model_path = os.path.join(os.path.dirname(__file__), 'models', 'knn_wine.pkl')
    with open(model_path, 'rb') as f:
        return pickle.load(f)
model = load_model()

# Hero
st.markdown("""
<div class="hero">
    <span class="hero-ornament">🍷</span>
    <div class="hero-eyebrow">Inteligencia Artificial · Sommelier digital</div>
    <div class="hero-title"><em>Vinoteca</em></div>
    <div class="hero-divider"><div class="hero-diamond"></div></div>
    <div class="hero-sub">Introduce las propiedades fisicoquímicas de tu vino y este modelo predecirá su calidad como lo haría un sommelier experto.</div>
</div>
""", unsafe_allow_html=True)

# Form
st.markdown('<div class="section-label">Análisis fisicoquímico</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    fixed_acidity = st.number_input("Acidez fija (g/L)", min_value=4.0, max_value=16.0, value=8.0, step=0.1,
                                     help="Ácidos no volátiles del vino")
    volatile_acidity = st.number_input("Acidez volátil (g/L)", min_value=0.1, max_value=1.6, value=0.5, step=0.01,
                                        help="Cantidad de ácido acético; los valores altos dan un sabor avinagrado")
    citric_acid = st.number_input("Ácido cítrico (g/L)", min_value=0.0, max_value=1.0, value=0.3, step=0.01,
                                   help="Aporta frescura y sabor al vino")
    residual_sugar = st.number_input("Azúcar residual (g/L)", min_value=1.0, max_value=16.0, value=2.5, step=0.1,
                                      help="Azúcar restante tras la fermentación")
    chlorides = st.number_input("Cloruros (g/L)", min_value=0.01, max_value=0.62, value=0.08, step=0.001,
                                 format="%.4f", help="Cantidad de sal en el vino")
    free_sulfur_dioxide = st.number_input("SO₂ libre (mg/L)", min_value=1.0, max_value=72.0, value=15.0, step=1.0,
                                           help="Forma libre del SO₂; previene microbios y oxidación")

with col2:
    total_sulfur_dioxide = st.number_input("SO₂ total (mg/L)", min_value=6.0, max_value=289.0, value=46.0, step=1.0,
                                            help="Suma de formas libres y unidas de SO₂")
    density = st.number_input("Densidad (g/cm³)", min_value=0.990, max_value=1.004, value=0.996, step=0.0001,
                               format="%.4f", help="Densidad del vino respecto al agua")
    pH = st.number_input("pH", min_value=2.7, max_value=4.0, value=3.3, step=0.01,
                          help="Escala de acidez del vino")
    sulphates = st.number_input("Sulfatos (g/L)", min_value=0.3, max_value=2.0, value=0.6, step=0.01,
                                 help="Aditivo que contribuye a los niveles de SO₂")
    alcohol = st.number_input("Alcohol (%)", min_value=8.0, max_value=15.0, value=10.5, step=0.1,
                               help="Porcentaje de alcohol por volumen")

st.write("")

# Predicción
if st.button("🍷 Analizar el vino"):
    features = np.array([[fixed_acidity, volatile_acidity, citric_acid, residual_sugar,
                           chlorides, free_sulfur_dioxide, total_sulfur_dioxide,
                           density, pH, sulphates, alcohol]])

    score = int(model.predict(features)[0])

    # Etiqueta y estilo según la puntuación
    if score >= 7:
        card_class = "result-high"
        label = "Vino excelente"
        stars = "★★★★★"
        desc = "Un vino de alta calidad con características excepcionales. Sus propiedades fisicoquímicas reflejan un equilibrio sobresaliente."
    elif score >= 5:
        card_class = "result-mid"
        label = "Vino de buena calidad"
        stars = "★★★☆☆"
        desc = "Un vino agradable al paladar. Presenta unas características sólidas dentro de los parámetros estándar."
    else:
        card_class = "result-low"
        label = "Vino de baja calidad"
        stars = "★★☆☆☆"
        desc = "Este vino presenta algunas características que podrían mejorarse para alcanzar una mayor puntuación."

    st.markdown(f"""
    <div class="result-card {card_class}">
        <div class="result-score">{score}</div>
        <div class="result-out-of">de 10 puntos</div>
        <div class="result-label">{label}</div>
        <div class="stars">{stars}</div>
        <div class="result-desc">{desc}</div>
        <div class="disclaimer">
            Predicción generada por un modelo KNN entrenado con el dataset Red Wine Quality (UCI / Kaggle).<br>
            Este resultado es orientativo y puede diferir de la valoración de un sommelier profesional.
        </div>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    Proyecto de ML · Dataset <a href="https://www.kaggle.com/datasets/uciml/red-wine-quality-cortez-et-al-2009" target="_blank">Red Wine Quality</a> · KNN Classifier
</div>
""", unsafe_allow_html=True)
