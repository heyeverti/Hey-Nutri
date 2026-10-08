import streamlit as st
import pandas as pd
import io
from datetime import datetime

# ==========================================
# CONFIGURAÇÃO DA PÁGINA & ESTILO VISUAL
# ==========================================
st.set_page_config(
    page_title="PlaNutri Web | Sistema de Avaliação Antropométrica",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS para estilo profissional
st.markdown("""
<style>
    /* Estilo do container principal */
    .main {
        background-color: #F8FAFC;
    }
    
    /* Header estilizado */
    .app-header {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
        padding: 24px;
        border-radius: 12px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .app-header h1 {
        color: white !important;
        font-weight: 700;
        margin: 0;
        font-size: 2.2rem;
    }
    .app-header p {
        color: #E2E8F0 !important;
        margin-top: 6px;
        font-size: 1.05rem;
    }
    
    /* Cards de métricas personalizados */
    .metric-card {
        background-color: white;
        border-radius: 10px;
        padding: 18px;
        border-left: 5px solid #3B82F6;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }
    .metric-card-title {
        font-size: 0.85rem;
        color: #64748B;
        text-transform: uppercase;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    .metric-card-value {
        font-size: 1.6rem;
        font-weight: 700;
        color: #0F172A;
        margin: 4px 0;
    }
    .metric-card-badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 600;
    }
    .badge-normal { background-color: #DEF7EC; color: #03543F; }
    .badge-alert { background-color: #FDE8E8; color: #9B1C1C; }
    .badge-warning { background-color: #FEF08A; color: #854D0E; }
    .badge-info { background-color: #E1EFFE; color: #1E429F; }

    /* Estilo dos cards do autor */
    .author-card {
        background-color: #F1F5F9;
        padding: 14px;
        border-radius: 8px;
        border: 1px solid #E2E8F0;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Inicialização do banco de dados na sessão (Session State)
if "historico_pacientes" not in st.session_state:
    st.session_state["historico_pacientes"] = []

# ==========================================
# BARRA LATERAL (SIDEBAR) - AUTOR E NAVEGAÇÃO
# ==========================================
with st.sidebar:
    st.image("https://img.icons8.com/isometric-folders/100/hospital.png", width=70)
    st.title("PlaNutri Pro®")
    st.caption("Suíte Antropométrica Digital")
    st.markdown("---")
    
    st.subheader("👨‍⚕️ Responsável Técnico")
    st.markdown("""
    **Autor:** Everti Alves Pimentel  
    *Nutricionista & Desenvolvedor*  
    
    **Orientação Acadêmica:**  
    Profa. Dra. Margareth Lage Leite de Fornasari  
    *Universidade São Judas Tadeu (USJT)*
    """)
    
    st.markdown("---")
    st.info("💡 **Registro Profissional:** Diagnóstico automatizado em conformidade com as diretrizes da OMS, Lipschitz (1994) e SISVAN (2011).")

# ==========================================
# HEADER PRINCIPAL
# ==========================================
st.markdown("""
<div class="app-header">
    <h1>🩺 PlaNutri Pro — Avaliação & Diagnóstico Antropométrico</h1>
    <p>Sistema Inteligente de Gestão Nutricional para Adultos e Idosos</p>
</div>
""", unsafe_allow_html=True)

# Abas do aplicativo
tab_cadastro, tab_historico, tab_sobre = st.tabs([
    "📝 Nova Avaliação / Paciente", 
    "🗂️ Banco de Dados & Exportação Excel", 
    "ℹ️ Sobre & Referências Teóricas"
])

# ==========================================
# ABA 1: FORMULÁRIO DE AVALIAÇÃO E CÁLCULOS
# ==========================================
with tab_cadastro:
    st.subheader("📋 Preenchimento dos Dados Antropométricos")
    
    with st.form("form_paciente", clear_on_submit=False):
        col_p1, col_p2, col_p3 = st.columns(3)
        with col_p1:
            nome = st.text_input("Nome Completo do Paciente*", value="Maria Silva")
            idade = st.number_input("Idade (anos)*", min_value=18, max_value=115, value=68, step=1)
        with col_p2:
            sexo = st.selectbox("Sexo Biológico*", ["Feminino", "Masculino"])
            data_aval = st.date_input("Data da Avaliação", datetime.now())
        with col_p3:
            prontuario = st.text_input("Nº Prontuário / ID", value="2026-001")
            leito_obs = st.text_input("Observação / Atendimento", value="Consulta Ambulatorial")

        st.markdown("#### 📏 Medidas Corporais Diretas")
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        with col_m1:
            peso = st.number_input("Peso Total (kg)*", min_value=20.0, max_value=250.0, value=58.5, step=0.1)
            estatura = st.number_input("Estatura (m)*", min_value=1.00, max_value=2.20, value=1.58, step=0.01)
        with col_m2:
            ca = st.number_input("Circ. Abdominal (cm)*", min_value=30.0, max_value=200.0, value=84.0, step=0.1)
            quadril = st.number_input("Circ. Quadril (cm)", min_value=0.0, max_value=200.0, value=96.0, step=0.1)
        with col_m3:
            pb = st.number_input("Perímetro Braquial - PB (cm)", min_value=10.0, max_value=60.0, value=26.5, step=0.1)
            dct = st.number_input("Dobra Tricipital - DCT (mm)", min_value=1.0, max_value=60.0, value=14.0, step=0.1)
        with col_m4:
            cp = st.number_input("Circ. Panturrilha - CP (cm)", min_value=0.0, max_value=60.0, value=29.5, step=0.1, help="Obrigatório para Idosos ≥ 60 anos")
            
        submitted = st.form_submit_button("⚡ Processar Avaliação e Salvar Prontuário", use_container_width=True)

    # PROCESSAMENTO E DIAGNÓSTICO
    if submitted or "ultimo_calculo" in st.session_state:
        # Armazena cálculo
        if submitted:
            # 1. Cálculo do IMC com Alternância Etária
            imc = peso / (estatura ** 2)
            if idade >= 60:
                criterio_imc = "Lipschitz (1994) / SISVAN (2011)"
                if imc < 22.0:
                    diag_imc = "Baixo Peso"
                    cls_imc_badge = "badge-alert"
                elif 22.0 <= imc <= 27.0:
                    diag_imc = "Eutrofia (Peso Adequado)"
                    cls_imc_badge = "badge-normal"
                else:
                    diag_imc = "Sobrepeso"
                    cls_imc_badge = "badge-warning"
            else:
                criterio_imc = "OMS (1995/2004)"
                if imc < 18.5:
                    diag_imc = "Baixo Peso"
                    cls_imc_badge = "badge-alert"
                elif 18.5 <= imc <= 24.99:
                    diag_imc = "Eutrofia (Peso Adequado)"
                    cls_imc_badge = "badge-normal"
                elif 25.0 <= imc <= 29.99:
                    diag_imc = "Sobrepeso"
                    cls_imc_badge = "badge-warning"
                else:
                    diag_imc = "Obesidade"
                    cls_imc_badge = "badge-alert"

            # 2. Circunferência Abdominal (Risco Cardiovascular - OMS 1998)
            if sexo == "Feminino":
                if ca < 80.0:
                    diag_ca = "Sem risco aumentado"
                    cls_ca_badge = "badge-normal"
                elif 80.0 <= ca < 88.0:
                    diag_ca = "Risco Aumentado"
                    cls_ca_badge = "badge-warning"
                else:
                    diag_ca = "Risco Muito Aumentado"
                    cls_ca_badge = "badge-alert"
            else:
                if ca < 94.0:
                    diag_ca = "Sem risco aumentado"
                    cls_ca_badge = "badge-normal"
                elif 94.0 <= ca < 102.0:
                    diag_ca = "Risco Aumentado"
                    cls_ca_badge = "badge-warning"
                else:
                    diag_ca = "Risco Muito Aumentado"
                    cls_ca_badge = "badge-alert"

            # 3. Razão Cintura-Quadril (RCQ)
            rcq_val = 0.0
            diag_rcq = "Não calculado"
            if quadril > 0:
                rcq_val = ca / quadril
                if sexo == "Feminino":
                    diag_rcq = "Risco Elevado" if rcq_val >= 0.85 else "Risco Adequado"
                else:
                    diag_rcq = "Risco Elevado" if rcq_val >= 0.90 else "Risco Adequado"

            # 4. Circunferência da Panturrilha (CP) - Sarcopenia
            diag_cp = "Não se aplica (<60 anos)"
            cls_cp_badge = "badge-info"
            if idade >= 60:
                if cp > 0 and cp < 31.0:
                    diag_cp = "Risco de Sarcopenia / Depleção Muscular (< 31 cm)"
                    cls_cp_badge = "badge-alert"
                elif cp >= 31.0:
                    diag_cp = "Massa Muscular Preservada (≥ 31 cm)"
                    cls_cp_badge = "badge-normal"
                else:
                    diag_cp = "Medida não informada"

            # 5. Reserva Proteica e Muscular (CMB e AMBc)
            import math
            cmb_val = 0.0
            ambc_val = 0.0
            diag_muscular = "Medidas incompletas"
            if pb > 0 and dct > 0:
                # CMB = PB (cm) - [pi * DCT (cm)]  (obs: DCT em mm / 10 = cm)
                dct_cm = dct / 10.0
                cmb_val = pb - (math.pi * dct_cm)
                
                # AMB = (CMB)^2 / (4 * pi)
                amb_raw = (cmb_val ** 2) / (4 * math.pi)
                # AMBc = AMB - constante (10.0 p/ homens, 6.5 p/ mulheres) - Heymsfield et al. (1982)
                const_sexo = 10.0 if sexo == "Masculino" else 6.5
                ambc_val = max(0.0, amb_raw - const_sexo)
                
                if ambc_val < 15.0:
                    diag_muscular = "Depleção Muscular Proteica"
                elif 15.0 <= ambc_val <= 40.0:
                    diag_muscular = "Eutrofia / Reserva Preservada"
                else:
                    diag_muscular = "Hipertrofia / Boa Reserva Muscular"

            # Salva objeto nos dados da sessão
            paciente_data = {
                "Data": data_aval.strftime("%d/%m/%Y"),
                "Prontuário": prontuario,
                "Nome": nome,
                "Idade": idade,
                "Sexo": sexo,
                "Peso (kg)": peso,
                "Estatura (m)": estatura,
                "IMC (kg/m²)": round(imc, 2),
                "Diagnóstico IMC": diag_imc,
                "Critério IMC": criterio_imc,
                "Circ. Abdominal (cm)": ca,
                "Risco Cardiovascular (CA)": diag_ca,
                "RCQ": round(rcq_val, 2) if quadril > 0 else "N/A",
                "Diagnóstico RCQ": diag_rcq,
                "Circ. Panturrilha (cm)": cp if idade >= 60 else "N/A",
                "Diagnóstico Sarcopenia": diag_cp,
                "PB (cm)": pb if pb > 0 else "N/A",
                "DCT (mm)": dct if dct > 0 else "N/A",
                "CMB (cm)": round(cmb_val, 2) if cmb_val > 0 else "N/A",
                "AMBc (cm²)": round(ambc_val, 2) if ambc_val > 0 else "N/A",
                "Reserva Muscular": diag_muscular,
                "Observações": leito_obs,
                "Avaliador": "Everti Alves Pimentel"
            }
            
            # Adiciona ao histórico sem duplicar por duplo clique
            st.session_state["historico_pacientes"].append(paciente_data)
            st.session_state["ultimo_calculo"] = paciente_data
            st.success(f"✅ Avaliação de **{nome}** salva no banco de dados com sucesso!")

        p = st.session_state["ultimo_calculo"]

        # EXIBIÇÃO DOS RESULTADOS EM CARDS DE ALTA DEFINIÇÃO
        st.markdown("---")
        st.subheader(f"📊 Diagnóstico Antropométrico Integrado — {p['Nome']}")
        
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-card-title">Índice de Massa Corporal (IMC)</div>
                <div class="metric-card-value">{p['IMC (kg/m²)']} <span style="font-size:1rem;">kg/m²</span></div>
                <span class="metric-card-badge badge-info">{p['Diagnóstico IMC']}</span>
                <p style="font-size:0.75rem; color:#64748B; margin-top:8px;">{p['Critério IMC']}</p>
            </div>
            """, unsafe_allow_html=True)
            
        with c2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-card-title">Risco Cardiovascular (CA)</div>
                <div class="metric-card-value">{p['Circ. Abdominal (cm)']} <span style="font-size:1rem;">cm</span></div>
                <span class="metric-card-badge badge-warning">{p['Risco Cardiovascular (CA)']}</span>
                <p style="font-size:0.75rem; color:#64748B; margin-top:8px;">OMS (1998)</p>
            </div>
            """, unsafe_allow_html=True)

        with c3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-card-title">Triagem de Sarcopenia (CP)</div>
                <div class="metric-card-value">{p['Circ. Panturrilha (cm)']} <span style="font-size:1rem;">cm</span></div>
                <span class="metric-card-badge badge-info">{p['Diagnóstico Sarcopenia']}</span>
                <p style="font-size:0.75rem; color:#64748B; margin-top:8px;">WHO (1995) / SISVAN (2018)</p>
            </div>
            """, unsafe_allow_html=True)

        with c4:
            ambc_str = f"{p['AMBc (cm²)']} cm²" if isinstance(p['AMBc (cm²)'], float) else "N/A"
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-card-title">Reserva Muscular (AMBc)</div>
                <div class="metric-card-value">{ambc_str}</div>
                <span class="metric-card-badge badge-normal">{p['Reserva Muscular']}</span>
                <p style="font-size:0.75rem; color:#64748B; margin-top:8px;">Heymsfield et al. (1982)</p>
            </div>
            """, unsafe_allow_html=True)

        # LAUDO TEXTUAL PRONTO PARA PRONTUÁRIO
        st.markdown("#### 📄 Laudo Síntese (Pronto para copiar para o Prontuário)")
        texto_laudo = f"""====================================================================
LAUDO DE AVALIAÇÃO NUTRICIONAL ANTROPOMÉTRICA - PLANUTRI PRO®
====================================================================
Paciente: {p['Nome']} | Idade: {p['Idade']} anos | Sexo: {p['Sexo']} | Prontuário: {p['Prontuário']}
Data da Avaliação: {p['Data']} | Avaliador: {p['Avaliador']}
--------------------------------------------------------------------
1. DIAGNÓSTICO PONDEROPONDERAL:
   - Peso: {p['Peso (kg)']} kg | Estatura: {p['Estatura (m)']} m
   - IMC: {p['IMC (kg/m²)']} kg/m² -> Classificação: {p['Diagnóstico IMC']} [{p['Critério IMC']}]

2. RISCO CARDIOMETABÓLICO & GORDURA VISCERAL:
   - Circunferência Abdominal: {p['Circ. Abdominal (cm)']} cm -> {p['Risco Cardiovascular (CA)']} (OMS, 1998)
   - Razão Cintura-Quadril (RCQ): {p['RCQ']} -> {p['Diagnóstico RCQ']}

3. COMPOSIÇÃO CORPORAL & MASSA MAGRA:
   - Circunferência da Panturrilha (CP): {p['Circ. Panturrilha (cm)']} cm -> {p['Diagnóstico Sarcopenia']}
   - Perímetro Braquial (PB): {p['PB (cm)']} cm | Dobra Tricipital (DCT): {p['DCT (mm)']} mm
   - Circunferência Muscular do Braço (CMB): {p['CMB (cm)']} cm
   - Área Muscular do Braço Corrigida (AMBc): {p['AMBc (cm²)']} cm² -> {p['Reserva Muscular']}

Observações do Atendimento: {p['Observações']}
===================================================================="""
        st.text_area("Laudo do Prontuário", value=texto_laudo, height=220)

# ==========================================
# ABA 2: BANCO DE DADOS & EXPORTAÇÃO EXCEL
# ==========================================
with tab_historico:
    st.subheader("🗂️ Registro Histórico de Pacientes Avaliados")
    
    if len(st.session_state["historico_pacientes"]) == 0:
        st.info("Nenhum paciente cadastrado até o momento. Preencha o formulário na aba 'Nova Avaliação'.")
    else:
        df_historico = pd.DataFrame(st.session_state["historico_pacientes"])
        
        st.write(f"Total de atendimentos registrados: **{len(df_historico)}**")
        st.dataframe(df_historico, use_container_width=True)
        
        # GERADOR DE PLANILHA EXCEL (.XLSX) PROFISSIONAL
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df_historico.to_excel(writer, index=False, sheet_name='Avaliacoes_Nutricionais')
            
            # Ajuste visual das colunas na planilha
            worksheet = writer.sheets['Avaliacoes_Nutricionais']
            for col in worksheet.columns:
                max_len = max(len(str(cell.value or '')) for cell in col)
                col_letter = col[0].column_letter
                worksheet.column_dimensions[col_letter].width = max(max_len + 3, 12)

        buffer.seek(0)
        
        col_btn1, col_btn2 = st.columns([2, 1])
        with col_btn1:
            st.download_button(
                label="📥 Baixar Relatório Completo em Excel (.xlsx)",
                data=buffer,
                file_name=f"Relatorio_PlaNutri_Atendimentos_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
        with col_btn2:
            if st.button("🗑️ Limpar Banco de Dados", use_container_width=True):
                st.session_state["historico_pacientes"] = []
                if "ultimo_calculo" in st.session_state:
                    del st.session_state["ultimo_calculo"]
                st.rerun()

# ==========================================
# ABA 3: REFERÊNCIAS TEÓRICAS E CRÉDITOS
# ==========================================
with tab_sobre:
    st.markdown("""
    ### 📚 Fundamentação Teórica & Metodológica
    
    Este software antropométrico foi desenvolvido e parametrizado com base no referencial teórico oficial da **Universidade São Judas Tadeu (USJT)**, sob autoria e orientação da **Profa. Dra. Margareth Lage Leite de Fornasari**:
    
    1. **Adultos (< 60 anos):**
       * **IMC:** Classificação do Índice de Massa Corporal segundo a Organização Mundial da Saúde (OMS, 1995/2004).
       * **Risco Cardiovascular:** Pontos de corte de Circunferência Abdominal da OMS (1998).
       * **Composição Corporal:** Matrizes de percentis de Frisancho (1990) e adequação de Blackburn (1979).
       
    2. **Idosos (≥ 60 anos):**
       * **IMC:** Pontos de corte ajustados de Lipschitz (1994), chancelados pelo Ministério da Saúde (SISVAN, 2011).
       * **Sarcopenia & Triagem Muscular:** Circunferência da Panturrilha (CP < 31 cm) conforme recomendações da WHO (1995) e Manual de Atenção à Pessoa Idosa (Brasil, 2018).
       * **Percentis Diretos:** Referenciais do *Third National Health and Nutrition Examination Survey* (NHANES III, 1988–1994).
       
    ---
    ### 👨‍💻 Créditos de Desenvolvimento
    * **Sistema:** PlaNutri Pro® — Suíte Antropométrica
    * **Autor & Programador:** Everti Alves Pimentel
    * **Orientadora:** Profa. Dra. Margareth Lage Leite de Fornasari
    * **Instituição:** Universidade São Judas Tadeu — Curso de Nutrição
    * **Ano de Publicação:** 2026
    """)
