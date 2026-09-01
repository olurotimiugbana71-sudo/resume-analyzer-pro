"""
Resume Analyzer Pro - Main Application
Copyright 2026 ApexDynamics Solutions | Built by Rotimi Ugbana
"""
import streamlit as st

st.set_page_config(
    page_title="Resume Analyzer Pro | ApexDynamics Solutions",
    page_icon="📄",
    layout="wide"
)

import pandas as pd
import numpy as np
from analyzer import ResumeAnalyzer
from visualizer import Visualizer
from license_gen import LicenseManager
from rewriter import ResumeRewriter
import base64
from fpdf import FPDF
from datetime import datetime
import io

COMPANY = "ApexDynamics Solutions"
DEVELOPER = "Rotimi Ugbana"
YEAR = "2026"
VERSION = "v2.2"

st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
    }
    .keyword-tag {
        display: inline-block;
        background: #e8eaf6;
        padding: 4px 10px;
        margin: 3px;
        border-radius: 12px;
        font-size: 13px;
    }
    .preview-banner {
        background: #fff3cd;
        border: 2px solid #ffc107;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        margin: 15px 0;
    }
    .summary-box {
        background: #16213E;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #667EEA;
        color: #FFFFFF;
        font-size: 16px;
        line-height: 1.6;
    }
    .bullet-box {
        background: #f8f9fa;
        padding: 12px;
        border-radius: 8px;
        margin: 8px 0;
        border-left: 4px solid #667EEA;
        color: #333;
    }
</style>
""", unsafe_allow_html=True)

def init_components():
    return ResumeAnalyzer(), Visualizer(), LicenseManager(), ResumeRewriter()

analyzer, visualizer, license_mgr, rewriter = init_components()

if 'licensed' not in st.session_state:
    st.session_state.licensed = False
if 'rewrite_result' not in st.session_state:
    st.session_state.rewrite_result = None

# Sidebar
with st.sidebar:
    st.markdown(f"## {COMPANY}")
    st.markdown("### 💰 Pricing")
    
    with st.expander("Full Access License - N15,000", expanded=True):
        st.write("✓ ATS Score Analysis")
        st.write("✓ AI Resume Rewriter")
        st.write("✓ Keyword Check")
        st.write("✓ PDF + DOCX Download")
        st.write("✓ 1-Year License")
    
    st.markdown("---")
    st.markdown("### 🔑 License Activation")
    
    lic_key = st.text_input("License Key", placeholder="ARX-XXXX-XXXX-XXXX")
    lic_email = st.text_input("Email", placeholder="you@email.com")
    
    if st.button("Activate License", type="primary"):
        valid, msg = license_mgr.validate(lic_key, lic_email)
        if valid:
            st.success(f"✅ {msg} - Full Access!")
            st.session_state.licensed = True
            st.session_state.buyer_email = lic_email
        else:
            st.error(f"❌ {msg}")
    
    if st.session_state.licensed:
        st.success("🔓 Licensed - Full Access")
    else:
        st.info("🔒 Preview Mode")

# Main Content
st.markdown(f'<h1 class="main-header">📄 Resume Analyzer Pro</h1>', unsafe_allow_html=True)
st.markdown(f"### AI-Powered Resume Analysis & Rewriting | {COMPANY}")

if not st.session_state.licensed:
    st.markdown("""
    <div class="preview-banner">
        <h3>🔒 PREVIEW MODE</h3>
        <p>Upload your resume for basic analysis. <strong>Activate license</strong> to unlock 
        the AI Resume Rewriter, PDF reports, and complete optimization.</p>
        <p style="font-size:14px;">💰 Full Access: N15,000 (1-Year License)</p>
    </div>
    """, unsafe_allow_html=True)

industry = st.selectbox(
    "🎯 Select Your Target Industry",
    ["Auto-Detect", "Technology", "Finance", "Healthcare", "Marketing", "Sales", "General"]
)

uploaded_file = st.file_uploader(
    "📁 Upload Your Resume (PDF or DOCX)",
    type=['pdf', 'docx']
)

if uploaded_file is not None:
    with st.spinner("🔍 Analyzing your resume..."):
        try:
            text = analyzer.extract_text(uploaded_file)
            
            if industry == "Auto-Detect":
                analysis_industry = rewriter.identify_industry(text) if hasattr(rewriter, 'identify_industry') else "General"
            else:
                analysis_industry = industry
            
            analysis = analyzer.analyze(text, analysis_industry)
            recs = analyzer.get_recommendations(analysis)
            
            st.success(f"✅ Analysis complete!")
            
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.markdown(f"""
                <div style="text-align:center;background:#16213E;padding:30px;border-radius:20px;border:1px solid #667EEA;">
                    <h1 style="font-size:80px;color:#667EEA;margin:0;">{analysis['total']}</h1>
                    <p style="color:#B0B0B0;font-size:18px;">out of 100</p>
                    <p style="color:#FFD700;font-size:14px;">Industry: {analysis['industry']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if analysis['total'] >= 70:
                    st.success("🌟 Excellent!")
                elif analysis['total'] >= 50:
                    st.warning("👍 Good")
                else:
                    st.error("⚠️ Needs work")
            
            with col2:
                st.components.v1.html(visualizer.gauge(analysis['total']), height=300)
            
            tab1, tab2, tab3, tab4 = st.tabs([
                "📊 Breakdown", "🔑 Keywords", "💡 Recommendations", "✍️ AI Rewriter"
            ])
            
            with tab1:
                st.markdown("### Score Breakdown")
                st.components.v1.html(visualizer.score_breakdown(analysis), height=350)
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Keywords", f"{analysis['keyword_score']}/40")
                c2.metric("Sections", f"{analysis['section_score']}/20")
                c3.metric("Actions", f"{analysis['action_score']}/15")
                c4.metric("Words", analysis['word_count'])
            
            with tab2:
                st.markdown("### Keywords Analysis")
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("#### ✅ Found Keywords")
                    for k in analysis['found_keywords']:
                        st.markdown(f'<span class="keyword-tag" style="background:#c8e6c9;">{k}</span>', unsafe_allow_html=True)
                with col2:
                    st.markdown("#### ❌ Missing Keywords")
                    for k in analysis['missing_keywords'][:10]:
                        st.markdown(f'<span class="keyword-tag" style="background:#ffcdd2;">{k}</span>', unsafe_allow_html=True)
            
            with tab3:
                st.markdown("### Actionable Recommendations")
                if recs:
                    for r in recs:
                        st.info(r)
                else:
                    st.success("🎉 Your resume is well-optimized!")
            
            with tab4:
                st.markdown("### ✍️ AI Resume Rewriter")
                
                if not st.session_state.licensed:
                    st.warning("🔒 Activate license (N15,000) to unlock the full AI Rewriter")
                
                st.markdown("#### 📋 Your Personal Information")
                col1, col2 = st.columns(2)
                with col1:
                    full_name = st.text_input("👤 Full Name", placeholder="John Doe")
                    email = st.text_input("📧 Email", placeholder="john@email.com")
                    phone = st.text_input("📱 Phone", placeholder="080-1234-5678")
                with col2:
                    location = st.text_input("📍 Location", placeholder="Lagos, Nigeria")
                    linkedin = st.text_input("💼 LinkedIn URL", placeholder="linkedin.com/in/johndoe")
                    current_role = st.text_input("💼 Current Job Title", placeholder="Senior Developer")
                
                if st.button("🪄 Rewrite My Resume", type="primary"):
                    with st.spinner("🤖 AI is rewriting your resume..."):
                        rewrite_result = rewriter.rewrite_resume(uploaded_file, analysis_industry)
                        st.session_state.rewrite_result = rewrite_result
                        st.success("✅ Resume optimized!")
                
                if st.session_state.get('rewrite_result'):
                    result = st.session_state.rewrite_result
                    st.markdown("#### 📋 Improved Summary")
                    st.markdown(f'<div class="summary-box">{result["improved_summary"]}</div>', unsafe_allow_html=True)
                    st.markdown("#### 💪 Rewritten Bullets")
                    for bullet in result['improved_bullets'][:5]:
                        st.markdown(f'<div class="bullet-box">• {bullet}</div>', unsafe_allow_html=True)
                    
                    if st.session_state.licensed:
                        if st.button("📥 Download Optimized Resume (DOCX)"):
                            docx_output = rewriter.generate_docx(result, text)
                            st.download_button("📥 Download DOCX", docx_output, "optimized_resume.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        
        except Exception as e:
            st.error(f"Error: {str(e)}")

st.markdown("---")
st.markdown(f"<p style='text-align:center;'>© {YEAR} {COMPANY} | Built by {DEVELOPER} | {VERSION}</p>", unsafe_allow_html=True)
