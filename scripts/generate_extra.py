import os
langs = ["de", "it", "pt", "nl", "pl", "sv", "cs", "hu", "ro", "da", "fi", "sk", "bg", "hr", "lt", "sl", "lv", "et", "ga", "mt", "el", "hi", "zh", "ms", "id", "ko", "ja", "ar", "he"]
topics = ["Amygdala", "Mismatch", "Chemistry", "Hijack", "Plasticity", "Gut-Brain", "Worry", "Memory", "Breathing", "Retraining"]
slugs = ["amygdala", "evolution", "chemistry", "hijack", "plasticity", "gut_brain", "worry_loop", "memory_trauma", "breathwork_regulation", "reconstructing_calm"]
def get_c(l, i):
    return f"**Juan Moises de la Serna**\nUNIR | ORCID: 0000-0002-8401-8018\n\n# {topics[i]} ({l.upper()})\n\nMeta-analysis on {topics[i]} in {l} following PRISMA guidelines."
for l in langs:
    d = f"meta_analysis_neuroscience_{l}"
    os.makedirs(d, exist_ok=True)
    for i in range(10):
        with open(f"{d}/{slugs[i]}.md", "w", encoding="utf-8") as f: f.write(get_c(l, i))
