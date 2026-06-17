import re, PyPDF2, io
from docx import Document
from collections import Counter

class ResumeAnalyzer:
    def __init__(self):
        self.keywords = {
            "Technology": ["python","java","aws","cloud","agile","sql","git","docker","api","react"],
            "Finance": ["excel","forecasting","budgeting","risk","accounting","audit","quickbooks"],
            "Healthcare": ["patient care","clinical","hipaa","medical","therapy","diagnosis"],
            "Marketing": ["seo","social media","analytics","branding","campaign","content"],
            "Sales": ["crm","salesforce","negotiation","b2b","pipeline","closing"],
            "General": ["leadership","communication","teamwork","project management"]
        }
        self.action_verbs = ["achieved","developed","managed","created","led","increased","reduced","launched"]
    
    def extract_text(self, file):
        if file.name.endswith('.pdf'):
            reader = PyPDF2.PdfReader(file)
            return " ".join(page.extract_text() for page in reader.pages)
        elif file.name.endswith('.docx'):
            doc = Document(file)
            return " ".join(p.text for p in doc.paragraphs)
    
    def analyze(self, text, industry="Technology"):
        text_lower = text.lower()
        kw = self.keywords.get(industry, self.keywords["General"])
        
        found = [k for k in kw if k in text_lower]
        missing = [k for k in kw if k not in text_lower]
        
        kw_score = (len(found) / len(kw)) * 40
        
        sections = ["experience","education","skills","summary","contact"]
        found_sec = [s for s in sections if s in text_lower]
        sec_score = (len(found_sec) / len(sections)) * 20
        
        words = text.split()
        wc = len(words)
        len_score = 10 if 300 <= wc <= 1000 else 5
        
        action_count = sum(1 for v in self.action_verbs if v in text_lower)
        action_score = min((action_count / 5) * 15, 15)
        
        fmt_score = 15
        issues = []
        if wc < 100: issues.append("Too short")
        if not re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', text): issues.append("No email found")
        
        total = min(round(kw_score + sec_score + len_score + action_score + fmt_score), 100)
        
        return {
            "total": total, "keyword_score": round(kw_score,1),
            "section_score": round(sec_score,1), "length_score": len_score,
            "action_score": round(action_score,1), "formatting_score": fmt_score,
            "found_keywords": found, "missing_keywords": missing,
            "found_sections": found_sec, "word_count": wc,
            "issues": issues, "industry": industry
        }
    
    def get_recommendations(self, analysis):
        recs = []
        if analysis["missing_keywords"]:
            recs.append(f"Add: {', '.join(analysis['missing_keywords'][:5])}")
        if analysis["total"] < 70:
            recs.append("Score below 70%. Improve keywords.")
        for sec in ["experience","education","skills","summary"]:
            if sec not in analysis["found_sections"]:
                recs.append(f"Add a '{sec}' section.")
        if analysis["word_count"] < 300:
            recs.append("Resume too short. Aim for 300+ words.")
        return recs