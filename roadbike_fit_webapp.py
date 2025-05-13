
import tkinter as tk
from tkinter import messagebox

# 雙語資料表
lang_data = {
    "zh": {
        "title": "公路車尺寸購買建議",
        "notice": "此程式為提供新手買車不用再單純只看身高的小幫手，僅供參考",
        "frame_data": "📦 想要購買的車架數據",
        "calculate": "計算建議",
        "result_title": "建議結果",
        "labels": {
            "entry_inseam": "跨下長（Inseam）",
            "entry_trunk": "軀幹長（Trunk）",
            "entry_forearm": "前臂長（Forearm）",
            "entry_arm": "手臂長（Arm）",
            "entry_thigh": "大腿長（Thigh）",
            "entry_lower_leg": "小腿長（Lower leg）",
            "entry_sternal": "胸骨凹口高（Sternal Notch）",
            "entry_height": "身高（Height）",
            "entry_shoulder": "肩寬（Shoulder Width）",
            "entry_ischial": "坐骨寬（Ischial Width）"
        },
        "frame_stack": "車架 Stack",
        "frame_reach": "車架 Reach",
        "stem_length": "龍頭長度",
        "units": {"cm": "cm", "mm": "mm"},
        "spacer": "建議加墊圈",
        "oversize": "⚠️ 車架 Stack / Reach 偏大，建議考慮選擇小一號車架尺寸",
        "ok": "確定"
    },
    "en": {
        "title": "Road Bike Size Recommendation",
        "notice": "This tool helps beginners choose a bike based on body measurements rather than just height. For reference only.",
        "frame_data": "📦 Geometry of Bike You Plan to Purchase",
        "calculate": "Get Recommendation",
        "result_title": "Suggested Fit",
        "labels": {
            "entry_inseam": "Inseam",
            "entry_trunk": "Trunk Length",
            "entry_forearm": "Forearm Length",
            "entry_arm": "Arm Length",
            "entry_thigh": "Thigh Length",
            "entry_lower_leg": "Lower Leg Length",
            "entry_sternal": "Sternal Notch Height",
            "entry_height": "Height",
            "entry_shoulder": "Shoulder Width",
            "entry_ischial": "Ischial Width"
        },
        "frame_stack": "Frame Stack",
        "frame_reach": "Frame Reach",
        "stem_length": "Stem Length",
        "units": {"cm": "cm", "mm": "mm"},
        "spacer": "Spacer Suggestion",
        "oversize": "⚠️ Frame Stack / Reach may be too large. Consider sizing down.",
        "ok": "OK"
    }
}

# 初始語言
current_lang = "zh"

def calculate():
    try:
        lang = lang_data[current_lang]
        # 讀取輸入值
        inseam = float(entry_inseam.get())
        trunk = float(entry_trunk.get())
        forearm = float(entry_forearm.get())
        arm = float(entry_arm.get())
        thigh = float(entry_thigh.get())
        lower_leg = float(entry_lower_leg.get())
        sternal = float(entry_sternal.get())
        height = float(entry_height.get())
        shoulder = float(entry_shoulder.get())
        ischial = float(entry_ischial.get())
        frame_stack = float(entry_frame_stack.get())
        frame_reach = float(entry_frame_reach.get())
        stem_length = int(stem_length_var.get())

        # 計算
        saddle_height = round(inseam * 0.883, 1)
        suggested_stack = round(height * 0.325 * 10, 1)
        reach = round((trunk + arm) * 0.30 * 10, 1)
        saddle_width = f"{ischial + 2.0:.1f}–{ischial + 4.0:.1f} {lang['units']['cm']}"

        # 差值
        stack_diff = round(frame_stack - suggested_stack, 1)
        reach_diff = round(frame_reach - reach, 1)
        stack_match = "✅" if abs(stack_diff) <= 10 else "❌"
        reach_match = "✅" if abs(reach_diff) <= 10 else "❌"

        if stack_diff < -5:
            cm_spacer = round(abs(stack_diff)/10, 1)
            spacer_suggestion = f"（{lang['spacer']}：{cm_spacer} cm）"
        else:
            spacer_suggestion = ""

        warning = ""
        if stack_diff > 15 or reach_diff > 15:
            warning = f"\n{lang['oversize']}"

        result = (
            f"📐 {lang['labels']['entry_inseam']}：{saddle_height} {lang['units']['cm']}\n"
            f"📏 {lang['frame_stack']}：{suggested_stack} mm（差值：{stack_diff} mm，{stack_match}）{spacer_suggestion}\n"
            f"📏 {lang['frame_reach']}：{reach} mm（選用 {stem_length} mm 龍頭）\n"
            f"📏 {lang['frame_reach']} 差值：{reach_diff} mm（{reach_match}）\n"
            f"🪑 建議坐墊寬度：{saddle_width}\n{warning}"
        )
        popup = tk.Toplevel()
        popup.title(lang["result_title"])
        popup.geometry("600x300")
        msg = tk.Message(popup, text=result, width=580, font=("Arial", 12))
        msg.pack(padx=20, pady=20)
        tk.Button(popup, text=lang["ok"], command=popup.destroy).pack(pady=10)
    except:
        messagebox.showerror("錯誤", "請確認所有欄位都正確填寫（數字）")

def switch_language(lang_code):
    global current_lang
    current_lang = lang_code
    lang = lang_data[lang_code]
    window.title(lang["title"])
    notice_label.config(text=lang["notice"])
    frame_label.config(text=lang["frame_data"])
    calc_button.config(text=lang["calculate"])
    for key, widget in label_refs.items():
        widget.config(text=lang["labels"][key])

# 主視窗
window = tk.Tk()
window.title(lang_data["zh"]["title"])
window.geometry("680x620")

# 語言選單
lang_frame = tk.Frame(window)
lang_frame.pack()
tk.Label(lang_frame, text="語言 / Language:").pack(side="left")
tk.Button(lang_frame, text="繁體中文", command=lambda: switch_language("zh")).pack(side="left")
tk.Button(lang_frame, text="English", command=lambda: switch_language("en")).pack(side="left")

# 警示文字
notice_label = tk.Label(window, text=lang_data["zh"]["notice"], fg="red", font=("Arial", 10, "bold"))
notice_label.pack(pady=5)

# 輸入欄位
input_frame = tk.Frame(window)
input_frame.pack(pady=10)

label_refs = {}
entry_refs = {}
fields = [
    "entry_inseam", "entry_trunk", "entry_forearm", "entry_arm", "entry_thigh",
    "entry_lower_leg", "entry_sternal", "entry_height", "entry_shoulder", "entry_ischial"
]

for i, field in enumerate(fields):
    label = tk.Label(input_frame, text=lang_data["zh"]["labels"][field])
    label.grid(row=i // 2, column=(i % 2) * 3, sticky="w", padx=5)
    label_refs[field] = label
    entry = tk.Entry(input_frame, width=10)
    entry.grid(row=i // 2, column=(i % 2) * 3 + 1)
    tk.Label(input_frame, text="cm").grid(row=i // 2, column=(i % 2) * 3 + 2)
    entry_refs[field] = entry

entry_inseam = entry_refs["entry_inseam"]
entry_trunk = entry_refs["entry_trunk"]
entry_forearm = entry_refs["entry_forearm"]
entry_arm = entry_refs["entry_arm"]
entry_thigh = entry_refs["entry_thigh"]
entry_lower_leg = entry_refs["entry_lower_leg"]
entry_sternal = entry_refs["entry_sternal"]
entry_height = entry_refs["entry_height"]
entry_shoulder = entry_refs["entry_shoulder"]
entry_ischial = entry_refs["entry_ischial"]

# 車架資料區塊
frame_label = tk.Label(window, text=lang_data["zh"]["frame_data"], font=("Arial", 11, "bold"))
frame_label.pack(pady=5)
lower_frame = tk.Frame(window)
lower_frame.pack()

entry_frame_stack = tk.Entry(lower_frame, width=10)
entry_frame_reach = tk.Entry(lower_frame, width=10)

tk.Label(lower_frame, text="車架 Stack").grid(row=0, column=0)
entry_frame_stack.grid(row=0, column=1)
tk.Label(lower_frame, text="mm").grid(row=0, column=2)

tk.Label(lower_frame, text="車架 Reach").grid(row=0, column=3)
entry_frame_reach.grid(row=0, column=4)
tk.Label(lower_frame, text="mm").grid(row=0, column=5)

tk.Label(lower_frame, text="龍頭長度").grid(row=1, column=0)
stem_length_var = tk.StringVar(window)
stem_length_var.set("100")
stem_menu = tk.OptionMenu(lower_frame, stem_length_var, "70", "80", "90", "100", "110", "120")
stem_menu.grid(row=1, column=1)


# 加入？提示符號
tooltip_refs = {}
for i, field in enumerate(['entry_inseam', 'entry_trunk', 'entry_forearm', 'entry_arm', 'entry_thigh', 'entry_lower_leg', 'entry_sternal', 'entry_height', 'entry_shoulder', 'entry_ischial']):
    q = tk.Label(input_frame, text="？", fg="blue", cursor="question_arrow")
    q.grid(row=i // 2, column=(i % 2) * 3 + 3)
    tooltip_refs[field] = q
    q.bind("<Enter>", lambda e, t=tooltip_data[current_lang][field]: show_tooltip(e, t))
    q.bind("<Leave>", hide_tooltip)

def switch_language(lang_code):
    global current_lang
    current_lang = lang_code
    lang = lang_data[lang_code]
    window.title(lang["title"])
    notice_label.config(text=lang["notice"])
    frame_label.config(text=lang["frame_data"])
    calc_button.config(text=lang["calculate"])
    for key, widget in label_refs.items():
        widget.config(text=lang["labels"][key])
    for key, widget in tooltip_refs.items():
        widget.unbind("<Enter>")
        widget.bind("<Enter>", lambda e, t=tooltip_data[current_lang][key]: show_tooltip(e, t))
        widget.bind("<Leave>", hide_tooltip)


calc_button = tk.Button(window, text=lang_data["zh"]["calculate"], command=calculate, bg="lightblue")
calc_button.pack(pady=10)

window.mainloop()


# 贊助連結區塊
def open_paypal():
    import webbrowser
    webbrowser.open("https://paypal.me/leopardbikeadvice")

sponsor_frame = tk.Frame(window)
sponsor_frame.pack(pady=10)
sponsor_label = tk.Label(sponsor_frame, text=paypal_text[current_lang], fg="brown", font=("Arial", 11))
sponsor_label.pack(side="left")
tk.Button(sponsor_frame, text="PayPal", command=open_paypal).pack(side="left", padx=8)

# 更新語言時同步替換贊助區塊文字
def switch_language(lang_code):
    global current_lang
    current_lang = lang_code
    lang = lang_data[lang_code]
    window.title(lang["title"])
    notice_label.config(text=lang["notice"])
    frame_label.config(text=lang["frame_data"])
    calc_button.config(text=lang["calculate"])
    sponsor_label.config(text=paypal_text[lang_code])
    for key, widget in label_refs.items():
        widget.config(text=lang["labels"][key])
    for key, widget in tooltip_refs.items():
        widget.unbind("<Enter>")
        widget.bind("<Enter>", lambda e, t=tooltip_data[current_lang][key]: show_tooltip(e, t))
        widget.bind("<Leave>", hide_tooltip)

