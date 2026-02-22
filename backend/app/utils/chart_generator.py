import io
import matplotlib.pyplot as plt

def generate_score_chart(scores: dict[str, int]) -> io.BytesIO:
    """
    Generates a simple bar chart for module scores.
    Returns: BytesIO containing the PNG image.
    """
    modules = list(scores.keys())
    values = list(scores.values())
    
    # Colors based on score
    colors = []
    for v in values:
        if v >= 90: colors.append('#059669') # Emerald
        elif v >= 70: colors.append('#0284C7') # Sky
        elif v >= 50: colors.append('#D97706') # Amber
        else: colors.append('#DC2626') # Red
    
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(modules, values, color=colors)
    
    ax.set_ylim(0, 100)
    ax.set_ylabel('Score / 100')
    ax.set_title('Performance by Module')
    
    # Hide top/right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png', dpi=150)
    plt.close(fig)
    
    buf.seek(0)
    return buf

def generate_severity_pie(severities: dict[str, int]) -> io.BytesIO | None:
    """
    Generates a pie chart of issue severities.
    Returns: BytesIO containing PNG, or None if no issues.
    """
    labels = []
    sizes = []
    colors = []
    
    color_map = {
        'critical': '#DC2626',
        'high': '#EA580C',
        'medium': '#D97706',
        'low': '#3B82F6',
        'info': '#6B7280'
    }
    
    for sev, count in severities.items():
        if count > 0:
            labels.append(sev.capitalize())
            sizes.append(count)
            colors.append(color_map.get(sev, '#CBD5E1'))
            
    if not sizes:
        return None
        
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', transparent=True, dpi=150)
    plt.close(fig)
    
    buf.seek(0)
    return buf
