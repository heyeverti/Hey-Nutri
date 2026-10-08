import streamlit as st

# Configuração da página
st.set_page_config(page_title="Calculadora Nutricional Completa - Adultos e Idosos", page_icon="🥗", layout="wide")

st.title("🥗 Calculadora Antropométrica Completa (Adultos e Idosos)")
st.subheader("Avaliação Nutricional Integrada: IMC, Risco Cardiovascular, Dobras e Reserva Muscular/Proteica")
st.markdown("---")

# Tab / Navegação na barra lateral
st.sidebar.header("📋 Dados do Paciente")
nome = st.sidebar.text_input("Nome do Paciente", "Paciente Exemplo")
idade = st.sidebar.number_input("Idade (anos)", min_value=18, max_value=120, value=65)
sexo = st.sidebar.selectbox("Sexo", ["Feminino", "Masculino"])

st.sidebar.markdown("---")
st.sidebar.header("📏 Medidas Globais")
peso = st.sidebar.number_input("Peso (kg)", min_value=20.0, max_value=250.0, value=68.0, step=0.1)
estatura = st.sidebar.number_input("Estatura (m)", min_value=1.00, max_value=2.30, value=1.65, step=0.01)

st.sidebar.markdown("---")
st.sidebar.header("📐 Perímetros e Dobras")
ca = st.sidebar.number_input("Circunferência Abdominal (cm)", min_value=0.0, max_value=180.0, value=82.0, step=0.1)
quadril = st.sidebar.number_input("Circunferência do Quadril (cm)", min_value=0.0, max_value=200.0, value=95.0, step=0.1)
cp = st.sidebar.number_input("Circunferência da Panturrilha (cm - Idosos)", min_value=0.0, max_value=60.0, value=32.0, step=0.1)
pb = st.sidebar.number_input("Perímetro do Braço - PB/CB (cm)", min_value=0.0, max_value=60.0, value=28.5, step=0.1)
dct = st.sidebar.number_input("Dobra Cutânea Tricipital - DCT (mm)", min_value=0.0, max_value=60.0, value=14.0, step=0.1)

# --- 1. CÁLCULO DO IMC ---
imc = peso / (estatura ** 2)
if idade >= 60:
    criterio_imc = "Lipschitz (1994) / SISVAN (2011) [Idosos]"
    if imc < 22.0:
        diag_imc = "Baixo Peso"
    elif 22.0 <= imc <= 27.0:
        diag_imc = "Eutrofia (Peso Adequado)"
    else:
        diag_imc = "Sobrepeso"
else:
    criterio_imc = "OMS (1995/2004) [Adultos]"
    if imc < 18.5:
        diag_imc = "Baixo Peso"
    elif 18.5 <= imc <= 24.99:
        diag_imc = "Eutrofia (Peso Adequado)"
    elif 25.0 <= imc <= 29.99:
        diag_imc = "Sobrepeso"
    else:
        diag_imc = "Obesidade"

# --- 2. RISCO CARDIOVASCULAR (CA) ---
diag_ca = "Não informada"
if ca > 0:
    if sexo == "Feminino":
        if ca < 80.0:
            diag_ca = "Sem Risco Aumentado"
        elif 80.0 <= ca < 88.0:
            diag_ca = "Risco Aumentado"
        else:
            diag_ca = "Risco Muito Aumentado"
    else:
        if ca < 94.0:
            diag_ca = "Sem Risco Aumentado"
        elif 94.0 <= ca < 102.0:
            diag_ca = "Risco Aumentado"
        else:
            diag_ca = "Risco Muito Aumentado"

# --- 3. RAZÃO CINTURA-QUADRIL (RCQ) ---
rcq_val = 0.0
diag_rcq = "Não informada"
if ca > 0 and quadril > 0:
    rcq_val = ca / quadril
    if sexo == "Feminino":
        diag_rcq = "Risco Elevado" if rcq_val >= 0.85 else "Adequado"
    else:
        diag_rcq = "Risco Elevado" if rcq_val >= 0.90 else "Adequado"

# --- 4. SARCOPENIA (PANTURRILHA - IDOSOS) ---
diag_cp = "N/A (Recomendado para Idosos ≥ 60 anos)"
if idade >= 60 and cp > 0:
    if cp < 31.0:
        diag_cp = "Risco de Sarcopenia / Depleção Muscular (< 31 cm)"
    else:
        diag_cp = "Preservação da Massa Muscular (≥ 31 cm)"

# --- 5. COMPOSIÇÃO CORPORAL SEGMENTAR (CMB, AMBc e DCT) ---
# Tabela simplificada P50 de Frisancho (1990) / NHANES III para referência
# Adultos P50 aproximados (Frisancho): Homem PB=32.0, DCT=12.0, CMB=28.2; Mulher PB=28.5, DCT=18.0, CMB=22.8
p50_dct = 18.0 if sexo == "Feminino" else 12.0
p50_cmb = 22.8 if sexo == "Feminino" else 28.2
p50_pb = 28.5 if sexo == "Feminino" else 32.0

# Classificação por Adequação de Blackburn (1979)
def classificar_adeq(adeq):
    if adeq < 70.0:
        return "Desnutrição Grave / Depleção Severa"
    elif 70.0 <= adeq < 80.0:
        return "Desnutrição Moderada / Depleção Moderada"
    elif 80.0 <= adeq < 90.0:
        return "Desnutrição Leve / Depleção Leve"
    elif 90.0 <= adeq <= 110.0:
        return "Eutrofia / Reserva Adequada"
    elif 110.0 < adeq <= 120.0:
        return "Sobrepeso / Reserva Elevada"
    else:
        return "Obesidade / Reserva Muito Elevada"

# Cálculos
cmb_val, ambc_val = 0.0, 0.0
adeq_dct, adeq_cmb, adeq_pb = 0.0, 0.0, 0.0
diag_dct, diag_cmb, diag_pb = "Não informada", "Não informada", "Não informada"

if pb > 0:
    adeq_pb = (pb / p50_pb) * 100
    diag_pb = classificar_adeq(adeq_pb)

if dct > 0:
    adeq_dct = (dct / p50_dct) * 100
    diag_dct = classificar_adeq(adeq_dct)

if pb > 0 and dct > 0:
    # CMB = PB (cm) - [π * (DCT mm / 10)]
    cmb_val = pb - (3.14159 * (dct / 10.0))
    adeq_cmb = (cmb_val / p50_cmb) * 100
    diag_cmb = classificar_adeq(adeq_cmb)
    
    # AMBc = [ (PB - (π * DCT/10))^2 / (4 * π) ] - constante
    # constante: 10.0 para homens, 6.5 para mulheres (Heymsfield et al., 1982)
    constante = 6.5 if sexo == "Feminino" else 10.0
    amb_bruta = ((pb - (3.14159 * (dct / 10.0))) ** 2) / (4 * 3.14159)
    ambc_val = max(0.0, amb_bruta - constante)

# --- APRESENTAÇÃO NA TELA ---
st.header(f"👤 Prontuário Antropométrico: {nome}")
st.write(f"**Perfil:** {idade} anos | Sexo {sexo} | Peso: {peso:.1f} kg | Estatura: {estatura:.2f} m")
st.markdown("---")

# Abas de navegação principal
tab1, tab2, tab3 = st.tabs(["📊 Diagnóstico Geral (IMC & Risco)", "💪 Composição Muscular & Gordura", "📄 Resumo em Laudo"])

with tab1:
    col_a, col_b = st.columns(2)
    with col_a:
        st.metric("Índice de Massa Corporal (IMC)", f"{imc:.2f} kg/m²")
        st.info(f"**Diagnóstico do IMC:** {diag_imc}\n\n*Referência: {criterio_imc}*")
        
    with col_b:
        st.metric("Circunferência Abdominal (CA)", f"{ca:.1f} cm" if ca > 0 else "N/I")
        st.warning(f"**Risco Cardiovascular (CA):** {diag_ca}\n\n*Referência: OMS (1998)*")

    st.markdown("---")
    col_c, col_d = st.columns(2)
    with col_c:
        st.subheader("Razão Cintura-Quadril (RCQ)")
        if rcq_val > 0:
            st.write(f"**Valor:** {rcq_val:.2f}")
            st.write(f"**Classificação:** {diag_rcq}")
        else:
            st.write("Quadril não informado para o cálculo de RCQ.")
            
    with col_d:
        st.subheader("Circunferência da Panturrilha (CP)")
        st.write(f"**Valor:** {cp:.1f} cm" if cp > 0 else "Não informada")
        st.caption(f"**Triagem de Sarcopenia:** {diag_cp}")

with tab2:
    st.subheader("🛡️ Avaliação das Reservas Proteicas e de Adiposidade")
    
    col_e, col_f, col_g = st.columns(3)
    
    with col_e:
        st.markdown("#### Dobra Cutânea Tricipital (DCT)")
        st.metric("DCT Aferida", f"{dct:.1f} mm" if dct > 0 else "N/I")
        if dct > 0:
            st.write(f"**Adequação:** {adeq_dct:.1f}% de P50")
            st.success(f"**Reserva Adiposa:** {diag_dct}")
        else:
            st.caption("Informe a DCT para avaliar a gordura subcutânea.")

    with col_f:
        st.markdown("#### Perímetro do Braço (PB)")
        st.metric("PB Aferido", f"{pb:.1f} cm" if pb > 0 else "N/I")
        if pb > 0:
            st.write(f"**Adequação:** {adeq_pb:.1f}% de P50")
            st.success(f"**Reserva Global:** {diag_pb}")
        else:
            st.caption("Informe o PB para avaliar a reserva global.")

    with col_g:
        st.markdown("#### Tecido Muscular (CMB & AMBc)")
        st.metric("CMB Calculada", f"{cmb_val:.2f} cm" if cmb_val > 0 else "N/I")
        if cmb_val > 0:
            st.write(f"**AMBc Corrigida:** {ambc_val:.2f} cm²")
            st.write(f"**Adequação CMB:** {adeq_cmb:.1f}%")
            st.success(f"**Reserva Proteica:** {diag_cmb}")
        else:
            st.caption("Informe PB e DCT para calcular a massa muscular enxuta.")

with tab3:
    st.subheader("📋 Laudo Antropométrico Sintético")
    laudo_text = f"""
    LAUDO DE AVALIAÇÃO ANTROPOMÉTRICA
    --------------------------------------------------
    Paciente: {nome}
    Idade: {idade} anos | Sexo: {sexo}
    Peso: {peso:.1f} kg | Estatura: {estatura:.2f} m
    --------------------------------------------------
    1. DIAGNÓSTICO NUTRICIONAL GLOBAL:
       - IMC: {imc:.2f} kg/m² -> {diag_imc}
       - Referência: {criterio_imc}

    2. AVALIAÇÃO DE RISCO METABÓLICO E SARCOPENIA:
       - Circunferência Abdominal: {ca:.1f} cm -> {diag_ca} (OMS, 1998)
       - Razão Cintura-Quadril: {rcq_val:.2f} -> {diag_rcq}
       - Circunferência da Panturrilha: {cp:.1f} cm -> {diag_cp}

    3. COMPOSIÇÃO CORPORAL SEGMENTAR (BLACKBURN, 1979 / FRISANCHO, 1990):
       - Dobra Cutânea Tricipital (DCT): {dct:.1f} mm ({adeq_dct:.1f}% adeq.) -> {diag_dct}
       - Perímetro Braquial (PB): {pb:.1f} cm ({adeq_pb:.1f}% adeq.) -> {diag_pb}
       - Circunferência Muscular do Braço (CMB): {cmb_val:.2f} cm ({adeq_cmb:.1f}% adeq.) -> {diag_cmb}
       - Área Muscular do Braço Corrigida (AMBc): {ambc_val:.2f} cm²
    --------------------------------------------------
    Relatório emitido para fins de planejamento e acompanhamento nutricional.
    """
    st.text_area("Texto Formatado para Copiar e Anexar ao Prontuário", laudo_text, height=350)

st.markdown("---")
st.caption("Desenvolvido para apoio à decisão clínica e atendimento em Saúde Coletiva | Universidade São Judas Tadeu (2026)")
