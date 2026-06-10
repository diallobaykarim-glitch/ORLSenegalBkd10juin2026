import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="ORL Sénégal", layout="wide")

# API URL
API_BASE = "http://api:8000"

st.title("🏥 ORL au Sénégal - Dashboard")
st.subheader("Plateforme d'Intelligence Artificielle en ORL Sénégal")

# ============================================
# TABS
# ============================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Vue Générale",
    "🎓 Universités",
    "🏥 Structures",
    "👨‍⚕️ Praticiens",
    "📚 Étudiants"
])

# ============================================
# TAB 1: Vue Générale
# ============================================
with tab1:
    st.header("📊 Vue Générale")
    
    try:
        response = requests.get(f"{API_BASE}/statistics/summary", timeout=5)
        summary = response.json()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Universités", summary.get("universities", 0))
        
        with col2:
            st.metric("Structures", summary.get("structures", 0))
        
        with col3:
            st.metric("Praticiens", summary.get("practitioners", 0))
        
        with col4:
            st.metric("Étudiants", summary.get("students", 0))
        
        st.divider()
        
        # Distribution pie chart
        st.subheader("Distribution par catégorie")
        
        data = {
            "Catégorie": ["Universités", "Structures", "Praticiens", "Étudiants"],
            "Nombre": [
                summary.get("universities", 0),
                summary.get("structures", 0),
                summary.get("practitioners", 0),
                summary.get("students", 0)
            ]
        }
        
        fig = px.pie(
            data,
            values="Nombre",
            names="Catégorie",
            title="Distribution des entités ORL",
            color_discrete_sequence=["#3498db", "#e74c3c", "#2ecc71", "#f39c12"]
        )
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.error(f"Erreur: {str(e)}")

# ============================================
# TAB 2: Universités
# ============================================
with tab2:
    st.header("🎓 Universités ORL")
    
    try:
        response = requests.get(f"{API_BASE}/universities", timeout=5)
        universities = response.json()
        
        df_unis = pd.DataFrame(universities)
        
        st.subheader(f"Total: {len(universities)} universités")
        
        # Secteur pie chart
        col1, col2 = st.columns(2)
        
        with col1:
            sector_counts = df_unis['sector'].value_counts()
            fig = px.pie(
                values=sector_counts.values,
                names=sector_counts.index,
                title="Public vs Privé"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            des_counts = df_unis['has_des'].astype(str).replace({'True': 'Avec DES', 'False': 'Sans DES'}).value_counts()
            fig = px.pie(
                values=des_counts.values,
                names=des_counts.index,
                title="Avec/Sans DES ORL"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("Liste des universités")
        st.dataframe(df_unis, use_container_width=True, hide_index=True)
        
    except Exception as e:
        st.error(f"Erreur: {str(e)}")

# ============================================
# TAB 3: Structures
# ============================================
with tab3:
    st.header("🏥 Structures ORL")
    
    try:
        response = requests.get(f"{API_BASE}/structures", timeout=5)
        structures = response.json()
        
        df_structs = pd.DataFrame(structures)
        
        st.subheader(f"Total: {len(structures)} structures")
        
        # Secteur bar chart
        sector_data = df_structs['sector'].value_counts().reset_index()
        sector_data.columns = ['Secteur', 'Nombre']
        
        fig = px.bar(
            sector_data,
            x='Secteur',
            y='Nombre',
            title="Structures par secteur",
            color='Secteur',
            text='Nombre'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Région bar chart
        region_data = df_structs['region'].value_counts().reset_index()
        region_data.columns = ['Région', 'Nombre']
        
        fig = px.bar(
            region_data,
            x='Région',
            y='Nombre',
            title="Structures par région",
            text='Nombre'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("Liste des structures")
        st.dataframe(df_structs, use_container_width=True, hide_index=True)
        
    except Exception as e:
        st.error(f"Erreur: {str(e)}")

# ============================================
# TAB 4: Praticiens
# ============================================
with tab4:
    st.header("👨‍⚕️ Praticiens ORL")
    
    try:
        response = requests.get(f"{API_BASE}/statistics/practitioners", timeout=5)
        practitioners = response.json()
        
        df_practi = pd.DataFrame(practitioners)
        
        total_practi = df_practi['count'].sum()
        st.metric("Total praticiens", total_practi)
        
        st.divider()
        
        # Secteur
        sector_summary = df_practi.groupby('sector')['count'].sum().reset_index()
        fig = px.bar(
            sector_summary,
            x='sector',
            y='count',
            title="Praticiens par secteur",
            labels={'sector': 'Secteur', 'count': 'Nombre'},
            text='count'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Région
        region_summary = df_practi.groupby('region')['count'].sum().reset_index()
        fig = px.bar(
            region_summary,
            x='region',
            y='count',
            title="Praticiens par région",
            labels={'region': 'Région', 'count': 'Nombre'},
            text='count'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("Détails par secteur et région")
        st.dataframe(df_practi, use_container_width=True, hide_index=True)
        
    except Exception as e:
        st.error(f"Erreur: {str(e)}")

# ============================================
# TAB 5: Étudiants
# ============================================
with tab5:
    st.header("📚 Étudiants (DES ORL)")
    
    try:
        response = requests.get(f"{API_BASE}/statistics/students", timeout=5)
        students = response.json()
        
        df_students = pd.DataFrame(students)
        
        total_students = df_students['count'].sum()
        st.metric("Total étudiants", total_students)
        
        st.divider()
        
        # Distribution par année
        year_summary = df_students.groupby('des_year')['count'].sum().reset_index()
        year_summary.columns = ['Année DES', 'Nombre']
        
        fig = px.bar(
            year_summary,
            x='Année DES',
            y='Nombre',
            title="Étudiants par année (DES 1-4)",
            text='Nombre',
            color='Année DES'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Distribution par région
        region_summary = df_students.groupby('region')['count'].sum().reset_index()
        fig = px.pie(
            values=region_summary['count'],
            names=region_summary['region'],
            title="Étudiants par région"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("Détails complets")
        st.dataframe(df_students, use_container_width=True, hide_index=True)
        
    except Exception as e:
        st.error(f"Erreur: {str(e)}")

# Footer
st.divider()
st.caption("🏥 ORL Sénégal - Dashboard Statistiques | v1.0")
