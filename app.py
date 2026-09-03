"""
Resume Analyzer Pro - Free Preview + Paywall
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
VERSION = "v3.0"
PRICE_NGN = 15000

st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
        text-align: center;
    }
    .keyword-tag {
        display: inline-block;
        background: #e8eaf6;
        padding: 4px 10px;
        margin: 3px;
        border-radius: 12px;
        font-size: 13px;
    }
    .keyword-tag.missing {
        background: #ffcdd2;
        color: #c62828;
    }
    .keyword-tag.found {
        background: #c8e6c9;
        color: #2e7d32;
    }
    .paywall-box {
        background: #16213E;
        border: 2px solid #FFD700;
        border-radius: 15px;
        padding: 25px;
        text-align: center;
        margin: 20px 0;
    }
    .paywall-box h3 {
        color: #FFD700;
        margin-bottom: 10px;
    }
    .locked-content {
        filter: blur(5px);
        pointer-events: none;
        user-select: none;
    }
    .unlock-btn {
        background: linear-gradient(135deg, #FFD700, #FFA500);
        color: #0F0F1A;
        padding: 15px 30px;
        border-radius: 25px;
        font-size: 16px;
        font-weight: 700;
        cursor: pointer;
        border: none;
        text-decoration: none;
        display: inline-block;
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
if 'user_email' not in st.session_state:
    st.session_state.user_email = ""
if 'show_paywall' not in st.session_state:
    st.session_state.show_paywall = False

# Sidebar - License Activation (for returning customers)
with st.sidebar:
    st.markdown(f"## {COMPANY}")
    st.markdown("### Already Purchased?")
    
    lic_key = st.text_input("License Key", placeholder="ARX-XXXX-XXXX-XXXX")
    lic_email = st.text_input("Email", placeholder="you@email.com")
    
    if st.button("Activate License", type="primary"):
        valid, msg = license_mgr.validate(lic_key, lic_email)
        if valid:
            st.success(f"✅ {msg} - Full Access!")
            st.session_state.licensed = True
            st.session_state.user_email = lic_email
        else:
            st.error(f"❌ {msg}")
    
    if st.session_state.licensed:
        st.success("🔓 Full Access Unlocked")
    else:
        st.info("🔒 Free Preview Mode")

# Main Content
st.markdown(f'<h1 class="main-header">📄 Resume Analyzer Pro</h1>', unsafe_allow_html=True)
st.markdown(f"### Get Your ATS Score Free | Unlock AI Rewrite | {COMPANY}")
st.markdown(f"<p style='text-align:center;'>✅ Free ATS Score + Keywords | 🔒 AI Rewrite + PDF - ₦{PRICE_NGN:,} One-Time</p>", unsafe_allow_html=True)

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
            
            # ============ FREE SECTION ============
            st.markdown("---")
            st.markdown("## 🆓 FREE PREVIEW - Your ATS Score")
            
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
                    st.warning("👍 Good - Room for improvement")
                else:
                    st.error("⚠️ Needs work - Unlock recommendations below!")
            
            with col2:
                st.components.v1.html(visualizer.gauge(analysis['total']), height=300)
            
            # ============ FREE BREAKDOWN ============
            st.markdown("---")
            st.markdown("## 📊 Score Breakdown (Free)")
            
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Keywords", f"{analysis['keyword_score']}/40")
            c2.metric("Sections", f"{analysis['section_score']}/20")
            c3.metric("Actions", f"{analysis['action_score']}/15")
            c4.metric("Words", analysis['word_count'])
            
            # ============ FREE KEYWORDS ============
            st.markdown("---")
            st.markdown("## 🔑 Keywords Analysis (Free)")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### ✅ Found Keywords")
                for k in analysis['found_keywords']:
                    st.markdown(f'<span class="keyword-tag found">{k}</span>', unsafe_allow_html=True)
            
            with col2:
                st.markdown("#### ❌ Missing Keywords")
                for k in analysis['missing_keywords'][:10]:
                    st.markdown(f'<span class="keyword-tag missing">{k}</span>', unsafe_allow_html=True)
            
            # ============ LOCKED SECTION ============
            st.markdown("---")
            
            if not st.session_state.licensed:
                # PAYWALL
                st.markdown(f"""
                <div class="paywall-box">
                    <h3>🔒 Unlock Your Full Report + AI Rewrite</h3>
                    <p style="color:#B0B0B0;margin-bottom:15px;">
                        Get personalized recommendations, AI-rewritten bullet points, 
                        and downloadable PDF/DOCX resume.
                    </p>
                    <p style="color:#FFD700;font-size:24px;font-weight:700;margin:15px 0;">
                        ₦{PRICE_NGN:,} One-Time
                    </p>
                    <p style="color:#B0B0B0;font-size:14px;margin-bottom:15px;">
                        ✅ AI Resume Rewriter<br>
                        ✅ Actionable Recommendations<br>
                        ✅ PDF + DOCX Download<br>
                        ✅ 1-Year License<br>
                        ✅ Instant Delivery
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                # Email capture
                st.markdown("### 📧 Where should we send your results?")
                user_email = st.text_input("Your Email Address", placeholder="you@email.com")
                
                if st.button("🔓 Unlock Full Access - ₦15,000", type="primary", use_container_width=True):
                    if user_email and '@' in user_email:
                        st.session_state.user_email = user_email
                        st.success(f"✅ Check your email at {user_email} for payment link!")
                        
                        # Paystack direct link
                        st.markdown(f"""
                        ### Complete Your Payment:
                        
                        [🔗 Click here to pay ₦15,000 via Paystack](https://paystack.com/buy/resume-analyzer-pro---full-access-license-inzyyf)
                        
                        After payment, your license key will be sent to: **{user_email}**
                        
                        *Having trouble? WhatsApp: +234 806 520 9323*
                        """)
                    else:
                        st.error("Please enter a valid email address")
                
                # Show locked content (blurred)
                st.markdown("---")
                st.markdown("## 💡 Recommendations (Locked)")
                st.markdown("""<div class="locked-content">""", unsafe_allow_html=True)
                for r in recs[:3]:
                    st.info(r)
                st.markdown("""</div>""", unsafe_allow_html=True)
                
                st.markdown("## ✍️ AI Rewriter (Locked)")
                st.markdown("""<div class="locked-content">
                    <p>Your AI-rewritten resume will appear here after unlocking...</p>
                    <p>Unlock to get: Action verbs, missing keywords, and optimized summary!</p>
                </div>""", unsafe_allow_html=True)
            
            else:
                # ============ LICENSED FULL ACCESS ============
                st.success("🔓 Full Access Unlocked!")
                
                st.markdown("## 💡 Recommendations (Unlocked)")
                if recs:
                    for r in recs:
                        st.info(r)
                else:
                    st.success("🎉 Your resume is well-optimized!")
                
                st.markdown("---")
                st.markdown("## ✍️ AI Resume Rewriter (Unlocked)")
                
                col1, col2 = st.columns(2)
                with col1:
                    full_name = st.text_input("Full Name", placeholder="John Doe")
                    email = st.text_input("Email", placeholder="john@email.com", value=st.session_state.user_email)
                with col2:
                    phone = st.text_input("Phone", placeholder="080-1234-5678")
                    current_role = st.text_input("Current Job Title", placeholder="Senior Developer")
                
                if st.button("🪄 Rewrite My Resume", type="primary"):
                    with st.spinner("🤖 AI is rewriting..."):
                        rewrite_result = rewriter.rewrite_resume(uploaded_file, analysis_industry)
                        st.session_state.rewrite_result = rewrite_result
                        st.success("✅ Resume optimized!")
                
                if st.session_state.get('rewrite_result'):
                    result = st.session_state.rewrite_result
                    st.markdown("#### 📋 Improved Summary")
                    st.markdown(f'<div style="background:#16213E;padding:20px;border-radius:10px;color:white;">{result["improved_summary"]}</div>', unsafe_allow_html=True)
                    
                    st.markdown("#### 💪 Rewritten Bullets")
                    for bullet in result['improved_bullets'][:5]:
                        st.markdown(f'<div style="background:#f8f9fa;padding:12px;border-radius:8px;margin:8px 0;border-left:4px solid #667EEA;">• {bullet}</div>', unsafe_allow_html=True)
                    
                    if st.button("📥 Download Optimized Resume (DOCX)"):
                        docx_output = rewriter.generate_docx(result, text)
                        st.download_button("📥 Download DOCX", docx_output, "optimized_resume.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        
        except Exception as e:
            st.error(f"Error: {str(e)}")

st.markdown("---")
st.markdown(f"<p style='text-align:center;'>© {YEAR} {COMPANY} | Built by {DEVELOPER} | {VERSION}</p>", unsafe_allow_html=True)