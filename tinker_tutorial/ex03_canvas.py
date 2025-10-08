import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Canvas Image (Pillow)")
        self.geometry("320x240")
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        top = tk.Frame(self); top.pack(fill="x")
        tk.Button(top, text="Load Image...", command=self.load_image).pack(side="left", padx=6, pady=6)

        self.canvas = tk.Canvas(self, bg="#fff"); self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", lambda e: self.redraw())

        self._img_pil = None   # 원본 PIL 이미지
        self._img_tk  = None   # 렌더용 Tk 이미지(참조 유지)

    def load_image(self):
        path = filedialog.askopenfilename(
            title="이미지 선택",
            filetypes=[("Images", "*.jpg *.jpeg *.png *.bmp *.gif *.webp *.tif *.tiff"), ("All files", "*.*")]
        )
        if not path:
            return
        try:
            self._img_pil = Image.open(path).convert("RGBA")
            self.redraw()
        except Exception as e:
            messagebox.showerror("로드 실패", str(e))

    def redraw(self):
        if self._img_pil is None:
            return
        cw, ch = max(1, self.canvas.winfo_width()), max(1, self.canvas.winfo_height())
        iw, ih = self._img_pil.size
        scale = min(cw / iw, ch / ih)
        nw, nh = max(1, int(iw * scale)), max(1, int(ih * scale))
        img = self._img_pil.resize((nw, nh), Image.LANCZOS)
        self._img_tk = ImageTk.PhotoImage(img)
        self.canvas.delete("all")
        self.canvas.create_image(cw // 2, ch // 2, image=self._img_tk, anchor="center")

    def on_close(self):
        self.destroy()

if __name__ == "__main__":
    App().mainloop()
