import gradio as gr
import requests
from datetime import datetime, timedelta
from rapidfuzz import process, fuzz

SHEET_URL = "https://api.sheetbest.com/sheets/366fcccd-a48d-493d-8bee-5d9fe3efe795"
DAYS = ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

def get_bg_color(shift: str) -> str:
    """Determine background color based on shift content."""
    shift_lower = shift.lower()
    if any(keyword in shift_lower for keyword in ["off", "leave"]):
        return "#dda0dd"  # Plum
    elif "event" in shift_lower:
        return "#fff3cd"  # Light yellow
    return "#e6e6fa"      # Light purple for regular shifts

def get_schedule(name: str) -> str:
    try:
        response = requests.get(SHEET_URL)
        response.raise_for_status()
        rows = response.json()

        start_date_value = rows[0].get('start date of the week')
        if not start_date_value:
            return "🚫 Start date not found."

        start_date = datetime.strptime(start_date_value, "%m/%d/%Y")

        all_names = [row.get("Name", "").strip().lower() for row in rows if row.get("Name")]
        match, score, _ = process.extractOne(name.strip().lower(), all_names, scorer=fuzz.token_sort_ratio)

        if score < 70:
            return f"❌ No close match found for '{name}'. Please check the spelling."

        # Collect and sort shifts by weekday order
        schedule_blocks = []

        for row in rows:
            employee_name = (row.get("Name") or "").strip().lower()
            location = (row.get("location") or "").strip()

            if employee_name == match:
                for i, day in enumerate(DAYS):
                    shift = (row.get(day) or "").strip()
                    if shift:
                        shift_date = start_date + timedelta(days=i)
                        bg_color = get_bg_color(shift)
                        display_text = f"{shift_date.strftime('%A, %d %b %Y')} - {shift}"
                        if bg_color == "#d4edda":
                            display_text += f" ({location})"

                        block_html = f"""
                        <div style="
                            background-color: {bg_color};
                            padding: 10px;
                            margin-bottom: 5px;
                            border-radius: 5px;
                            font-family: Arial, sans-serif;
                            font-size: 14px;
                        ">
                            {display_text}
                        </div>
                        """
                        schedule_blocks.append((i, block_html))

        if not schedule_blocks:
            return f"❗ No shifts found for {match.title()}."

        schedule_blocks.sort(key=lambda x: x[0])
        sorted_html = "".join([block for _, block in schedule_blocks])

        return f"""
        <div style="font-family: Arial; font-size: 16px;">
            ✅ <strong>Schedule for {match.title()}</strong> (Confidence: {score:.1f}%)
            <br><br>
            {sorted_html}
        </div>
        """

    except Exception as e:
        return f"🚨 Internal Server Error: {str(e)}"

# Gradio Interface
demo = gr.Interface(
    fn=get_schedule,
    inputs=gr.Textbox(label="Enter Your Name"),
    outputs=gr.HTML(label="Your Schedule"),
    title="🗓️ Shift Schedule Assistant",
    description="Type your name to get your weekly shift schedule. Typos? Don't worry — fuzzy matching is enabled ✅",
    theme=gr.themes.Soft(),
)

if __name__ == "__main__":
    demo.launch()
