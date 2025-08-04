def detect_inefficiencies(df):
    issues = []
    if df['total_energy'].max() > 2000:
        issues.append("⚠️ Sudden spike detected. Check for faulty equipment.")
    if df['appliances_usage'].mean() > 700:
        issues.append("📺 Appliance usage too high. Consider energy-efficient models.")
    return issues

