import tkinter as tk
import json
import os

# اسم ملف الـ JSON الخاص بك
DATA_FILE = "data.json"


class FloatingDashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("لوحة الاختصارات الذكية")
        self.geometry("200x540+1165+150")  # مقاساتك الأصلية الثابتة بالبكسل تماماً
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.attributes("-alpha", 0.94)
        self.configure(bg="#1e1e2e")
        try:
            self.iconbitmap("my_icon.ico")
        except Exception:
            pass

        self.withdraw()
        self.deiconify()

        top_frame = tk.Frame(self, bg="#252538", height=50)
        top_frame.pack(fill="x", side="top")

        close_btn = tk.Button(top_frame, text="X", fg="red", bg="#252538", bd=0, activebackground="#f38ba8",
                              activeforeground="#1e1e2e", width=3, font=("Segoe UI", 10, "bold"), command=self.destroy)
        close_btn.pack(side="left", fill="y")

        lab = tk.Label(top_frame, text="مدير الصوتيات المتقدم", bg="#252538", bd=0, activebackground="#f38ba8",
                       activeforeground="#1e1e2e", font=("Segoe UI", 10, "bold"))
        lab.pack(side="right", fill="y")

        # حاوية ثابتة لعرض الأزرار على نفس تصميمك الأصلي
        self.presets_frame = tk.Frame(self, bg="#1e1e2e")
        self.presets_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # تحميل البيانات من الملف (وإذا كان فارغاً سيضع أزرارك الافتراضية فوراً)
        self.audio_presets = self.load_presets()
        self.refresh_ui_buttons()

        # زر الإضافة الخاص بك بنفس مكانه وأبعاده وشكله
        add_btn = tk.Button(self, text="اضافة اختصار صوتي", fg="#11111b", bg="#a6e3a1", font=("Segoe UI", 11, "bold"),
                            bd=0, cursor="hand2", pady=4, command=self.add)
        add_btn.pack(pady=10)

    def load_presets(self):
        """جلب القائمة من ملف data.json أو وضع أزرارك الافتراضية إذا كان الملف فارغاً"""
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    if data:  # تأكيد أن الملف يحتوي على أزرار فعلاً
                        return data
            except Exception:
                pass

        # أزرارك الافتراضية التي وضعتها لك لكي لا تظهر الشاشة فارغة أبداً عند أول تشغيل
        default_buttons = [
            {"input_one": "📚 وضع الدراسة", "input_two": "20"},
            {"input_one": "🎮 وضع الألعاب", "input_two": "80"},
            {"input_one": "🎬 وضع الأفلام", "input_two": "50"}
        ]
        # حفظ الأزرار الافتراضية في الملف لكي تصبح جاهزة دائماً
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(default_buttons, file, indent=4, ensure_ascii=False)
        return default_buttons

    def save_presets(self):
        """حفظ القائمة الحالية داخل ملف data.json"""
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(self.audio_presets, file, indent=4, ensure_ascii=False)

    def refresh_ui_buttons(self):
        """إعادة رسم أزرارك مع ميزة الحذف وتغيير الصوت عند النقر (الفقس)"""
        for widget in self.presets_frame.winfo_children():
            widget.destroy()

        for index, item in enumerate(self.audio_presets):
            name = item["input_one"]
            volume = item["input_two"]

            row_frame = tk.Frame(self.presets_frame, bg="#1e1e2e")
            row_frame.pack(fill="x", pady=4, padx=5)

            # زر X صغير بجانب زر الاختصار لحذفه برمجياً
            delete_btn = tk.Button(
                row_frame, text="✕", fg="#1e1e2e", bg="#f38ba8", font=("Segoe UI", 8, "bold"),
                bd=0, cursor="hand2", width=2, command=lambda i=index: self.delete_preset(i)
            )
            delete_btn.pack(side="left", padx=(0, 4))

            # الزر المخصص لك يعرض الاسم والنسبة بشكل أنيق ويتفاعل عند الفقس
            display_text = f"{name} ({volume}%)"
            btn = tk.Button(
                row_frame, text=display_text, fg="#cdd6f4", bg="#313244",
                font=("Segoe UI", 10, "bold"), bd=0, cursor="hand2", pady=6,
                anchor="e", padx=10, command=lambda v=volume: self.change_system_volume(v)
            )
            btn.pack(side="right", fill="x", expand=True)

    def change_system_volume(self, volume_level):
        """تغيير مستوى صوت الويندوز الحقيقي فوراً عند الضغط على الزر"""
        try:
            os.system(f"nircmd.exe setsysvolume {int(float(volume_level) * 655.35)}")
            print(f"🎵 تم تغيير شدة الصوت بنجاح إلى: {volume_level}%")
        except Exception:
            pass

    def delete_preset(self, index):
        """حذف الزر وإعادة رص باقي الأزرار تلقائياً للأعلى لملء الفراغ"""
        del self.audio_presets[index]
        self.save_presets()
        self.refresh_ui_buttons()

    def add(self):
        """نافذة الإضافة الخاصة بك بدون أي تغيير في التصميم أو الأبعاد"""
        root = tk.Tk()
        root.attributes("-topmost", True)
        root.overrideredirect(True)
        root.geometry("150x100+1200+400")

        frame = tk.Frame(root, width=50)
        frame.pack(fill="x", side="top")
        label = tk.Label(frame, text="اسم الاختصار", font=("Segoe UI", 10, "bold"))
        label.pack(side="right")
        ety = tk.Entry(frame, width=150, bd=0)
        ety.pack(side="left")

        frame = tk.Frame(root, width=50)
        frame.pack(fill="x", side="top", pady=5)
        label1 = tk.Label(frame, text="شدة الصوت", font=("Segoe UI", 10, "bold"))
        label1.pack(side="right")
        ety1 = tk.Entry(frame, width=150, bd=0)
        ety1.pack(side="left")

        frame = tk.Frame(root, width=50)
        frame.pack(fill="x", side="top")

        def ok():
            ety_g = ety.get()
            ety_g1 = ety1.get()

            if not ety_g.strip() or not ety_g1.strip():
                return

            new_preset = {
                "input_one": ety_g.strip(),
                "input_two": ety_g1.strip()
            }

            self.audio_presets.append(new_preset)
            self.save_presets()
            self.refresh_ui_buttons()
            root.destroy()

        ok_btn = tk.Button(frame, text="ok", width=5, font=("Segoe UI", 10, "bold"), command=ok)
        ok_btn.pack(side="right")

        exit_btn = tk.Button(frame, text="cancel", width=5, font=("Segoe UI", 10, "bold"), command=root.destroy)
        exit_btn.pack(side="right", padx=1)
        root.mainloop()


if __name__ == "__main__":
    app = FloatingDashboard()
    app.mainloop()
