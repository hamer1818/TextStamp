import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os

class ImageEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("TextStamp - Resim Üzerine Metin Ekleme Aracı")
        
        # Pencere boyutunu ayarla
        self.root.geometry("1200x800")
        
        # Ana değişkenler
        self.image = None
        self.photo = None
        self.original_image = None  # Orijinal resmi saklamak için
        self.draw_rect = None
        self.start_x = None
        self.start_y = None
        self.selection = None
        self.is_selection_confirmed = False
        self.text_list = []
        
        # Font yolu
        self.font_path = os.path.join("fonts", "main.ttf")
        if not os.path.exists(self.font_path):
            self.font_path = None
            messagebox.showwarning("Uyarı", "Varsayılan font (fonts/main.ttf) bulunamadı. Sistem fontu kullanılacak.")
        
        # Stil ayarları
        style = ttk.Style()
        style.configure('TButton', padding=5)
        style.configure('TFrame', padding=5)
        
        # Öğretici durumu
        self.tutorial_shown = False
        self.tutorial_steps = [
            ("Hoş Geldiniz!", "Bu uygulama ile resimlerinize metin ekleyebilirsiniz."),
            ("Adım 1", "'Resim Yükle' butonuna tıklayarak bir resim seçin."),
            ("Adım 2", "Resim üzerinde fare ile sürükleyerek metin eklemek istediğiniz alanı seçin."),
            ("Adım 3", "'Bölgeyi Onayla' butonuna tıklayarak seçiminizi onaylayın."),
            ("Adım 4", "Metin kutusuna eklemek istediğiniz metni yazın ve 'Metin Ekle' butonuna tıklayın."),
            ("Adım 5", "Birden fazla metin ekleyebilirsiniz. Metinler listede görünecektir."),
            ("Adım 6", "'Metinleri Uygula ve Çıktı Al' butonuna tıklayarak sonuçları kaydedin."),
            ("İpucu", "Seçili metni silmek için listeden metni seçip 'Seçili Metni Sil' butonunu kullanın.")
        ]
        self.current_tutorial_step = 0
        
        # Ana container
        self.main_container = ttk.PanedWindow(root, orient=tk.HORIZONTAL)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Sol panel - Canvas ve Scrollbar'lar
        self.left_frame = ttk.Frame(self.main_container)
        
        # Canvas için scrollbar'lar
        self.h_scrollbar = ttk.Scrollbar(self.left_frame, orient=tk.HORIZONTAL)
        self.v_scrollbar = ttk.Scrollbar(self.left_frame, orient=tk.VERTICAL)
        self.canvas = tk.Canvas(self.left_frame, bg='#f0f0f0',
                              xscrollcommand=self.h_scrollbar.set,
                              yscrollcommand=self.v_scrollbar.set)
        
        # Scrollbar'ları yapılandır
        self.h_scrollbar.config(command=self.canvas.xview)
        self.v_scrollbar.config(command=self.canvas.yview)
        
        # Grid ile yerleştir
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.h_scrollbar.grid(row=1, column=0, sticky="ew")
        self.v_scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Grid ağırlıklarını ayarla
        self.left_frame.grid_rowconfigure(0, weight=1)
        self.left_frame.grid_columnconfigure(0, weight=1)
        
        self.main_container.add(self.left_frame, weight=3)  # Sol panel daha geniş
        
        # Sağ panel - Kontroller
        self.right_frame = ttk.Frame(self.main_container)
        self.main_container.add(self.right_frame)
        
        # Kontrol elemanları
        self.setup_controls()
        
        # Canvas olayları
        self.canvas.bind('<ButtonPress-1>', self.on_press)
        self.canvas.bind('<B1-Motion>', self.on_drag)
        self.canvas.bind('<ButtonRelease-1>', self.on_release)
        
        # Menü oluştur
        self.create_menu()
        
        # İlk açılışta öğreticiyi göster
        self.root.after(1000, self.show_tutorial)
        
    def setup_controls(self):
        """Sağ panel kontrol elemanlarının oluşturulması"""
        control_frame = ttk.Frame(self.right_frame)
        control_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Başlık
        title_label = ttk.Label(control_frame, text="Kontrol Paneli", 
                              font=('Helvetica', 12, 'bold'))
        title_label.pack(pady=10)
        
        # Gruplandırma için frame'ler
        image_frame = ttk.LabelFrame(control_frame, text="Resim İşlemleri", padding=5)
        image_frame.pack(fill=tk.X, pady=5)
        
        selection_frame = ttk.LabelFrame(control_frame, text="Seçim İşlemleri", padding=5)
        selection_frame.pack(fill=tk.X, pady=5)
        
        text_frame = ttk.LabelFrame(control_frame, text="Metin İşlemleri", padding=5)
        text_frame.pack(fill=tk.X, pady=5)
        
        # Resim yükleme butonu
        ttk.Button(image_frame, text="Resim Yükle", 
                  command=self.load_image).pack(pady=5, fill=tk.X)
        
        # Koordinat bilgileri
        self.coord_label = ttk.Label(selection_frame, text="Seçilen Alan: (-,-) - (-,-)")
        self.coord_label.pack(pady=5)
        
        # Bölge onaylama butonu
        self.confirm_btn = ttk.Button(selection_frame, text="Bölgeyi Onayla",
                                    command=self.confirm_selection, state=tk.DISABLED)
        self.confirm_btn.pack(pady=5, fill=tk.X)
        
        # Metin işlemleri
        ttk.Label(text_frame, text="Metin:").pack(pady=2)
        self.text_entry = ttk.Entry(text_frame)
        self.text_entry.pack(pady=2, fill=tk.X)
        
        ttk.Button(text_frame, text="Metin Ekle",
                  command=self.add_text).pack(pady=5, fill=tk.X)
        
        # Metin listesi
        self.text_listbox = tk.Listbox(text_frame, height=5)
        self.text_listbox.pack(pady=5, fill=tk.BOTH)
        
        ttk.Button(text_frame, text="Seçili Metni Sil",
                  command=self.remove_text).pack(pady=5, fill=tk.X)
        
        # Çıktı alma butonu
        ttk.Button(control_frame, text="Metinleri Uygula ve Çıktı Al",
                  command=self.generate_outputs).pack(pady=20, fill=tk.X)
    
    def load_image(self):
        """Resim yükleme işlemi"""
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.ppm *.pgm")])
        
        if file_path:
            self.original_image = Image.open(file_path)
            self.image = self.original_image.copy()
            self.resize_image()
            self.photo = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
            
            # Seçim alanını sıfırla
            self.reset_selection()

        # Pencere yeniden boyutlandırıldığında resmi yeniden boyutlandır
        self.root.bind('<Configure>', lambda e: self.resize_image())
    
    def resize_image(self):
        """Resmi canvas boyutuna göre yeniden boyutlandır"""
        if not self.image:
            return
            
        # Orijinal resmi sakla
        if not self.original_image:
            self.original_image = self.image.copy()
        
        # Canvas boyutlarını al
        canvas_width = self.canvas.winfo_width() or 800
        canvas_height = self.canvas.winfo_height() or 600
        
        # Resim boyutlarını al
        img_width, img_height = self.original_image.size
        
        # En-boy oranını koru
        ratio = min(canvas_width/img_width, canvas_height/img_height)
        
        # Yeni boyutları hesapla
        new_width = int(img_width * ratio)
        new_height = int(img_height * ratio)
        
        # Resmi yeniden boyutlandır
        self.image = self.original_image.resize((new_width, new_height), 
                                              Image.Resampling.LANCZOS)
        
        # Canvas scroll bölgesini ayarla
        self.canvas.config(scrollregion=(0, 0, new_width, new_height))
    
    def on_press(self, event):
        """Fare tıklama olayı"""
        if not self.is_selection_confirmed and self.image:
            self.start_x = event.x
            self.start_y = event.y
            if self.draw_rect:
                self.canvas.delete(self.draw_rect)
    
    def on_drag(self, event):
        """Fare sürükleme olayı"""
        if not self.is_selection_confirmed and self.image:
            if self.draw_rect:
                self.canvas.delete(self.draw_rect)
            self.draw_rect = self.canvas.create_rectangle(
                self.start_x, self.start_y, event.x, event.y,
                outline='red', width=2)
    
    def on_release(self, event):
        """Fare bırakma olayı"""
        if not self.is_selection_confirmed and self.image:
            self.selection = (min(self.start_x, event.x), 
                            min(self.start_y, event.y),
                            max(self.start_x, event.x), 
                            max(self.start_y, event.y))
            self.coord_label.config(
                text=f"Seçilen Alan: ({self.selection[0]}, {self.selection[1]}) ({self.selection[2]}, {self.selection[3]})")
            self.confirm_btn.config(state=tk.NORMAL)
    
    def confirm_selection(self):
        """Seçim alanını onayla"""
        if self.selection:
            self.is_selection_confirmed = True
            self.confirm_btn.config(state=tk.DISABLED)
            messagebox.showinfo("Bilgi", "Bölge seçimi onaylandı!")
    
    def add_text(self):
        """Metin listesine yeni metin ekle"""
        text = self.text_entry.get().strip()
        if text:
            self.text_list.append(text)
            self.text_listbox.insert(tk.END, text)
            self.text_entry.delete(0, tk.END)
    
    def remove_text(self):
        """Seçili metni listeden kaldır"""
        selection = self.text_listbox.curselection()
        if selection:
            index = selection[0]
            self.text_list.pop(index)
            self.text_listbox.delete(index)
    
    def reset_selection(self):
        """Seçim alanını sıfırla"""
        if self.draw_rect:
            self.canvas.delete(self.draw_rect)
        self.selection = None
        self.is_selection_confirmed = False
        self.confirm_btn.config(state=tk.DISABLED)
        self.coord_label.config(text="Seçilen Alan: (-,-) - (-,-)")
    
    def generate_outputs(self):
        """Metinleri uygula ve çıktı al"""
        if not all([self.image, self.selection, self.is_selection_confirmed, self.text_list]):
            messagebox.showerror("Hata", 
                "Lütfen resim yükleyin, bir alan seçip onaylayın ve en az bir metin ekleyin!")
            return
        
        # Çıktı klasörü seç
        output_dir = filedialog.askdirectory()
        if not output_dir:
            return
        
        try:
            # Her metin için ayrı çıktı oluştur
            for i, text in enumerate(self.text_list, 1):
                # Orijinal resmin kopyasını al
                output_image = self.image.copy()
                draw = ImageDraw.Draw(output_image)
                
                # Seçili alanın boyutlarını hesapla
                box_width = self.selection[2] - self.selection[0]
                box_height = self.selection[3] - self.selection[1]
                
                # Başlangıç font boyutu
                font_size = 12
                max_font_size = 100  # Maksimum font boyutu
                best_font_size = font_size
                
                # Font boyutunu optimize et
                while font_size < max_font_size:
                    try:
                        # Önce belirlenen fontu kullan, yoksa sistem fontunu dene
                        if self.font_path:
                            font = ImageFont.truetype(self.font_path, font_size)
                        else:
                            font = ImageFont.truetype("arial.ttf", font_size)
                    except:
                        font = ImageFont.load_default()
                    
                    # Metnin boyutlarını hesapla
                    text_bbox = draw.textbbox((0, 0), text, font=font)
                    text_width = text_bbox[2] - text_bbox[0]
                    text_height = text_bbox[3] - text_bbox[1]
                    
                    # Metin kutunun içine sığıyor mu kontrol et
                    if text_width <= box_width * 0.9 and text_height <= box_height * 0.9:
                        best_font_size = font_size
                        font_size += 1
                    else:
                        break
                
                # En uygun font boyutunu kullan
                try:
                    if self.font_path:
                        final_font = ImageFont.truetype(self.font_path, best_font_size)
                    else:
                        final_font = ImageFont.truetype("arial.ttf", best_font_size)
                except:
                    final_font = ImageFont.load_default()
                
                # Metnin son boyutlarını hesapla
                text_bbox = draw.textbbox((0, 0), text, font=final_font)
                text_width = text_bbox[2] - text_bbox[0]
                text_height = text_bbox[3] - text_bbox[1]
                
                # Metni ortalayarak yerleştir
                x = self.selection[0] + (box_width - text_width) / 2
                y = self.selection[1] + (box_height - text_height) / 2
                
                # Metni ekle
                draw.text((x, y), text, fill='black', font=final_font)
                
                # Çıktıyı kaydet
                output_path = os.path.join(output_dir, f"output_{i}.png")
                output_image.save(output_path)
            
            messagebox.showinfo("Başarılı", 
                              "Metinler uygulandı ve çıktılar kaydedildi!")
            
        except Exception as e:
            messagebox.showerror("Hata", f"Çıktı oluşturulurken hata: {str(e)}")

    def create_menu(self):
        """Menü oluştur"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Yardım menüsü
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Yardım", menu=help_menu)
        help_menu.add_command(label="Öğretici", command=self.restart_tutorial)
        help_menu.add_command(label="Hakkında", command=self.show_about)

    def show_about(self):
        """Hakkında penceresini göster"""
        messagebox.showinfo("Hakkında", 
            "TextStamp v1.0\n\n"
            "Resimleriniz üzerine özelleştirilmiş metin damgaları ekleyin.\n"
            "Menüden 'Öğretici'yi seçerek kullanım adımlarını görebilirsiniz.\n\n"
            "Hamza ORTATEPE tarafından geliştirildi. \n"
            "Github: https://github.com/hamer1818/TextStamp \n"
            "© 2024 TextStamp")



    def show_tutorial(self):
        """Öğretici adımını göster"""
        if not self.tutorial_shown and self.current_tutorial_step < len(self.tutorial_steps):
            title, message = self.tutorial_steps[self.current_tutorial_step]
            
            # Özel öğretici penceresi oluştur
            tutorial_window = tk.Toplevel(self.root)
            tutorial_window.title(title)
            tutorial_window.geometry("400x150")
            tutorial_window.transient(self.root)
            tutorial_window.grab_set()
            
            # Pencereyi ortala
            tutorial_window.geometry("+%d+%d" % (
                self.root.winfo_rootx() + self.root.winfo_width()//2 - 200,
                self.root.winfo_rooty() + self.root.winfo_height()//2 - 75))
            
            # İçerik
            ttk.Label(tutorial_window, text=message, 
                     wraplength=350, justify="center").pack(pady=20)
            
            # Butonlar
            button_frame = ttk.Frame(tutorial_window)
            button_frame.pack(pady=10)
            
            if self.current_tutorial_step > 0:
                ttk.Button(button_frame, text="Önceki", 
                          command=lambda: self.navigate_tutorial(-1, tutorial_window)).pack(side=tk.LEFT, padx=5)
            
            if self.current_tutorial_step < len(self.tutorial_steps) - 1:
                ttk.Button(button_frame, text="Sonraki", 
                          command=lambda: self.navigate_tutorial(1, tutorial_window)).pack(side=tk.LEFT, padx=5)
            else:
                ttk.Button(button_frame, text="Bitir", 
                          command=lambda: self.end_tutorial(tutorial_window)).pack(side=tk.LEFT, padx=5)
            
            ttk.Button(button_frame, text="Kapat", 
                      command=lambda: self.skip_tutorial(tutorial_window)).pack(side=tk.LEFT, padx=5)

    def navigate_tutorial(self, direction, window):
        """Öğreticide ileri veya geri git"""
        window.destroy()
        self.current_tutorial_step += direction
        self.show_tutorial()

    def end_tutorial(self, window):
        """Öğreticiyi bitir"""
        window.destroy()
        self.tutorial_shown = True
        messagebox.showinfo("Öğretici", "Öğretici tamamlandı! Artık uygulamayı kullanmaya başlayabilirsiniz.")

    def skip_tutorial(self, window):
        """Öğreticiyi atla"""
        window.destroy()
        self.tutorial_shown = True
        messagebox.showinfo("Öğretici", "Öğretici kapatıldı. İstediğiniz zaman Yardım menüsünden tekrar açabilirsiniz.")

    def restart_tutorial(self):
        """Öğreticiyi yeniden başlat"""
        self.current_tutorial_step = 0
        self.tutorial_shown = False
        self.show_tutorial()

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEditor(root)
    root.mainloop()