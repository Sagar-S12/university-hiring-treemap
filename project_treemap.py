import matplotlib.pyplot as plt
import numpy as np
import squarify

# University data with additional details
universities = [
    "University of Phoenix", "University of Washington", "Georgia Tech", "Stanford",
    "UC Berkeley", "USC", "University of Texas", "Arizona State", "Cornell",
    "Penn State", "Strayer University", "University of Arkansas", "MIT",
    "San Jose State", "Northeastern", "UIUC", "Harvard", "Purdue", "UPenn"
]

graduates = [
    15924, 14264, 5292, 4639, 4302, 4213, 3938, 3820, 3680,
    3214, 3025, 2845, 2692, 2661, 2302, 2251, 2220, 2195, 2022
]

us_ranking = [200, 20, 10, 3, 4, 15, 9, 30, 7, 25, 300, 100, 1, 40, 50, 14, 2, 35, 6]
intl_ratio = [5, 18, 20, 23, 22, 25, 10, 12, 28, 15, 3, 7, 30, 10, 25, 20, 26, 12, 24]  # Percentage
acceptance_rate = [90, 56, 21, 5, 14, 13, 33, 85, 11, 50, 95, 77, 7, 67, 18, 60, 4, 59, 9]  # Percentage

# Companies hiring from each university
companies = [
    ["AT&T", "Walmart", "Amazon", "Verizon"],
    ["Microsoft", "Amazon", "Apple", "AT&T"],
    ["Google", "Boeing", "Lockheed", "Intel"],
    ["Google", "Apple", "Tesla", "Facebook"],
    ["Apple", "Google", "Tesla", "Intel"],
    ["Disney", "Amazon", "SpaceX", "Google"],
    ["Dell", "Apple", "Amazon", "Exxon"],
    ["Intel", "Amazon", "Honeywell", "Raytheon"],
    ["Goldman", "Amazon", "Google", "JPMorgan"],
    ["Boeing", "Lockheed", "Amazon", "IBM"],
    ["Amazon", "Verizon", "AT&T", "Microsoft"],
    ["Walmart", "Tyson", "J.B. Hunt", "Amazon"],
    ["Google", "Microsoft", "Apple", "SpaceX"],
    ["Apple", "Google", "Cisco", "Intel"],
    ["Amazon", "Google", "Wayfair", "Deloitte"],
    ["Microsoft", "Amazon", "Intel", "Caterpillar"],
    ["Goldman", "JPMorgan", "Google", "McKinsey"],
    ["Caterpillar", "Lockheed", "GM", "Boeing"],
    ["Goldman", "JPMorgan", "BCG", "Morgan Stanley"]
]

# Industry-based color coding
industry_colors = {
    "Tech": "#1f77b4",  # Blue
    "Finance": "#2ca02c",  # Green
    "Aerospace": "#ff7f0e",  # Orange
    "Retail": "#d62728",  # Red
    "Automotive": "#9467bd",  # Purple
    "Consulting": "#8c564b"  # Brown
}


# Function to get industry color
def get_company_color(company):
    tech_companies = {"Google", "Amazon", "Microsoft", "Apple", "Intel", "Cisco", "Facebook"}
    finance_companies = {"Goldman Sachs", "JPMorgan", "Morgan Stanley"}
    aerospace_companies = {"Boeing", "Lockheed", "SpaceX", "Raytheon"}
    retail_companies = {"Walmart", "AT&T", "Verizon", "Disney"}
    automotive_companies = {"Tesla", "GM", "Caterpillar"}
    consulting_companies = {"McKinsey", "BCG", "Deloitte"}

    if company in tech_companies:
        return industry_colors["Tech"]
    elif company in finance_companies:
        return industry_colors["Finance"]
    elif company in aerospace_companies:
        return industry_colors["Aerospace"]
    elif company in retail_companies:
        return industry_colors["Retail"]
    elif company in automotive_companies:
        return industry_colors["Automotive"]
    elif company in consulting_companies:
        return industry_colors["Consulting"]
    else:
        return "#7f7f7f"  # Default gray for unknown companies


# Normalize company hires to split among university hires
company_proportions = np.array([0.4, 0.3, 0.2, 0.1])  # Relative sizes

# Define colors for universities
university_colors = plt.cm.Paired.colors

# Create figure
fig, ax = plt.subplots(figsize=(14, 9))

# Create university-level treemap
univ_rects = squarify.normalize_sizes(graduates, 100, 100)
univ_positions = squarify.squarify(univ_rects, 0, 0, 100, 100)

for i, (pos, uni, grad, rank, intl, accept) in enumerate(
        zip(univ_positions, universities, graduates, us_ranking, intl_ratio, acceptance_rate)):
    x, y, dx, dy = pos['x'], pos['y'], pos['dx'], pos['dy']

    # Draw university tile with thick border
    ax.add_patch(
        plt.Rectangle((x, y), dx, dy, color=university_colors[i % len(university_colors)], alpha=0.5, edgecolor="black",
                      linewidth=3))

    # University Text (Placed at the Top)
    text_y = y + dy - 3  # Offset downward to avoid overlap
    ax.text(x + dx / 2, text_y, f"{uni}", ha="center", va="top", fontsize=9, color="black", fontweight="bold")

    # Additional University Info (Placed Below University Name)
    info_text = f"Rank: {rank}\nInt'l: {intl}%\nAcceptance: {accept}%"
    ax.text(x + dx / 2, text_y - 4, info_text, ha="center", va="top", fontsize=7, color="black")

    # Create company tiles inside university tile with padding
    padding = 1  # Small padding for better separation
    comp_sizes = company_proportions * grad
    comp_positions = squarify.squarify(squarify.normalize_sizes(comp_sizes, dx - 2 * padding, dy - 12), x + padding,
                                       y + padding, dx - 2 * padding, dy - 12)

    for j, (comp_pos, comp) in enumerate(zip(comp_positions, companies[i])):
        cx, cy, cdx, cdy = comp_pos['x'], comp_pos['y'], comp_pos['dx'], comp_pos['dy']

        # Draw company tile inside university tile
        company_color = get_company_color(comp)
        ax.add_patch(
            plt.Rectangle((cx, cy), cdx, cdy, color=company_color, alpha=0.9, edgecolor="white", linewidth=1.5))
        ax.text(cx + cdx / 2, cy + cdy / 2, comp, ha="center", va="center", fontsize=7, color="white",
                fontweight="bold")

# Remove axes
ax.set_xticks([])
ax.set_yticks([])
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.set_title("Treemap: US Universities & Their Top Hiring Companies (Industry-Based Colors)", fontsize=14)

plt.show()
