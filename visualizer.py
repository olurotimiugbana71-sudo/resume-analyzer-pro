import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from io import BytesIO
import base64

class Visualizer:
    def __init__(self):
        plt.style.use('seaborn-v0_8-darkgrid')
    
    def _to_b64(self, fig):
        buf = BytesIO()
        fig.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        buf.seek(0)
        img = base64.b64encode(buf.read()).decode()
        plt.close(fig)
        return img
    
    def gauge(self, score):
        color = "#6bcf7f" if score >= 70 else "#ffd93d" if score >= 50 else "#ff6b6b"
        fig = go.Figure(go.Indicator(
            mode="gauge+number", value=score,
            title={'text': "ATS Score"},
            gauge={'axis': {'range': [0, 100]}, 'bar': {'color': color},
                   'steps': [{'range': [0,50], 'color': "#ffebee"},
                            {'range': [50,70], 'color': "#fff9c4"},
                            {'range': [70,100], 'color': "#c8e6c9"}]}
        ))
        fig.update_layout(height=280)
        return fig.to_html(full_html=False)
    
    def score_breakdown(self, analysis):
        cats = ['Keywords', 'Sections', 'Length', 'Actions', 'Format']
        vals = [analysis['keyword_score'], analysis['section_score'],
                analysis['length_score'], analysis['action_score'], analysis['formatting_score']]
        fig = go.Figure(data=[go.Bar(x=cats, y=vals, marker_color='#667eea')])
        fig.update_layout(height=300, yaxis_range=[0,40])
        return fig.to_html(full_html=False)
    
    def keywords_chart(self, found, missing):
        fig, ax = plt.subplots(figsize=(8, 3))
        ax.barh(['Found', 'Missing'], [len(found), len(missing)], color=['#6bcf7f', '#ff6b6b'])
        ax.set_title('Keywords')
        plt.tight_layout()
        return self._to_b64(fig)