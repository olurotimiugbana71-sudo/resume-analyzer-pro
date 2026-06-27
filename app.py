import streamlit as st
st.set_page_config(page_title="Resume Analyzer Pro | ApexDynamics", page_icon="📄", layout="wide")

from analyzer import ResumeAnalyzer
from visualizer import Visualizer
from license_gen import LicenseManager
import base64
from fpdf import FPDF
from datetime import datetime

COMPANY = "ApexDynamics Solutions"
DEVELOPER = "Rotimi Ugbana"


def init():
    return ResumeAnalyzer(), Visualizer(), LicenseManager()

analyzer, viz, license_mgr = init()

if 'licensed' not in st.session_state:
    st.session_state.licensed = False

st.sidebar.markdown(f"## {COMPANY}")
st.sidebar.markdown("### Pricing")
st.sidebar.write("Basic: $19 | Standard: $49 | Premium: $149")

st.sidebar.markdown("---")
st.sidebar.markdown("### Activate License")
lic_key = st.sidebar.text_input("License Key", placeholder="ARX-XXXX-XXXX-XXXX")
lic_email = st.sidebar.text_input("Email")
if st.sidebar.button("Activate"):
    valid, msg = license_mgr.validate(lic_key, lic_email)
    if valid:
        st.sidebar.success(msg)
        st.session_state.licensed = True
        st.session_state.buyer_email = lic_email
    else:
        st.sidebar.error(msg)

st.markdown(f"<h1 style='background:linear-gradient(135deg,#667eea,#764ba2);-webkit-background-clip:text;-webkit-text-fill-color:transparent;font-size:3rem;'>📄 Resume Analyzer Pro</h1>", unsafe_allow_html=True)
st.markdown(f"### By {COMPANY}")

industry = st.selectbox("Industry", ["Technology","Finance","Healthcare","Marketing","Sales","General"])
uploaded = st.file_uploader("Upload Resume (PDF/DOCX)", type=['pdf','docx'])

if uploaded:
    with st.spinner("Analyzing..."):
        text = analyzer.extract_text(uploaded)
        analysis = analyzer.analyze(text, industry)
        recs = analyzer.get_recommendations(analysis)
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown(f"<h1 style='text-align:center;font-size:60px;color:#667eea;'>{analysis['total']}</h1>", unsafe_allow_html=True)
            st.markdown("<p style='text-align:center;'>out of 100</p>", unsafe_allow_html=True)
            if analysis['total'] >= 70: st.success("Excellent!")
            elif analysis['total'] >= 50: st.warning("Good")
            else: st.error("Needs Work")
        with col2:
            st.components.v1.html(viz.gauge(analysis['total']), height=300)
        
        tab1, tab2, tab3 = st.tabs(["Breakdown", "Keywords", "Recommendations"])
        with tab1:
            st.components.v1.html(viz.score_breakdown(analysis), height=350)
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Keywords", f"{analysis['keyword_score']}/40")
            c2.metric("Sections", f"{analysis['section_score']}/20")
            c3.metric("Actions", f"{analysis['action_score']}/15")
            c4.metric("Words", analysis['word_count'])
        with tab2:
            st.image(f"data:image/png;base64,{viz.keywords_chart(analysis['found_keywords'], analysis['missing_keywords'])}")
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**Found Keywords**")
                for k in analysis['found_keywords']: st.write(f"✅ {k}")
            with c2:
                st.markdown("**Missing Keywords**")
                for k in analysis['missing_keywords'][:10]: st.write(f"❌ {k}")
        with tab3:
            st.markdown("### Recommendations")
            for r in recs: st.info(r)
        
        if st.session_state.licensed:
            if st.button("Generate PDF Report"):
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font('Arial','B',20)
                pdf.cell(0,15,'Resume Analysis Report',ln=True,align='C')
                pdf.set_font('Arial','',12)
                pdf.cell(0,10,f'Score: {analysis["total"]}/100 | Industry: {industry}',ln=True)
                pdf.cell(0,10,f'Prepared for: {st.session_state.get("buyer_email","N/A")}',ln=True)
                pdf.ln(10)
                pdf.set_font('Arial','B',14)
                pdf.cell(0,10,'Recommendations:',ln=True)
                pdf.set_font('Arial','',11)
                for r in recs:
                    pdf.multi_cell(0,7,f'* {r}')
                pdf.ln(10)
                pdf.set_font('Arial','I',9)
                pdf.cell(0,10,f'© 2026 {COMPANY} | {DEVELOPER}',ln=True,align='C')
                
                pdf_out = pdf.output(dest='S').encode('latin-1')
                pdf_b64 = base64.b64encode(pdf_out).decode()
                st.download_button("Download PDF", pdf_out, "resume_report.pdf", "application/pdf")
                
        else:
            st.info("Activate license for PDF report")

st.markdown("---")
st.caption(f"© 2026 {COMPANY} | Built by {DEVELOPER}")