# 🍷 Vinoteca: Predicción de la calidad de un vino con IA

Esta es una aplicación web que predice la calidad de un vino tinto (con una puntuación del 1 al 10) usando un modelo de Machine Learning (KNN) entrenado con el dataset **Red Wine Quality**.

🔗 **Demo en vivo**: [enlace-a-render-aqui]

---

## 📁 Estructura del proyecto

```
App-web-de-ML-usando-Streamlit/
└── models/
    └── knn_wine_quality.pkl # Modelo KNN entrenado
├── .gitattributes
├── .python-version
├── app.py # Aplicación Streamlit
├── Procfile # Configuración para Render
├── README.md
├── requirements.txt # Dependencias Python
```

---

## 🚀 Instalación local

```bash
pip install -r requirements.txt
streamlit run app.py
```

Abrir Localhost

---

## 🤖 Modelo

- **Algoritmo**: K-Nearest Neighbours (KNN)
- **Dataset**: Red Wine Quality (UCI / Kaggle)
- **Features**: Fixed acidity, Volatile acidity, Citric acid, Residual sugar, Chlorides, Free sulfur dioxide, Total sulfur dioxide, Density, pH, Sulphates, Alcohol
- **Target**: Puntuación de calidad del vino (0-10)

---

## ☁️ Deploy en Render

1. Subir este proyecto a un **nuevo repositorio** en GitHub
2. Ir a [render.com](https://render.com) --> New --> Web Service
3. Conectar el repositorio
4. Configurar:
   - **Build command**: `pip install -r requirements.txt`
   - **Start command**: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
   - **Plan**: Free
5. Hacer click en **Deploy**

---

## ⚠️ Aviso

Este modelo es orientativo. La calidad del vino puede variar según el gusto del consumidor.
