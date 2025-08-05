def generate_recommendations(df):
    avg_usage = df['total_energy'].mean()
    tips = []

    if avg_usage > 500:
        tips.append("🔌 Consider switching off unused appliances during peak hours.")
    if df['hour'].value_counts().idxmax() in [12, 13, 14]:
        tips.append("☀️ High midday usage detected. Consider shifting tasks to morning/evening.")
    if df['lights_usage'].mean() > 100:
        tips.append("💡 Try replacing bulbs with LED for lower lighting costs.")

    if not tips:
        tips.append("✅ Your usage looks efficient! Keep it up!")

    return tips
