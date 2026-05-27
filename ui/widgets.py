import customtkinter as ctk
from PIL import Image
from functools import partial

edit_icon = ctk.CTkImage(dark_image=Image.open("ui/icons/edit_icon.png"), size=(30, 30))
trash_icon = ctk.CTkImage(dark_image=Image.open("ui/icons/trash_icon.png"), size=(30, 30))

NORMAL_COLOR = "#212435"
MAX_TEXT_LEN_SMALL_BTN = 50
MAX_TEXT_LEN_CRITERION = 30

class CustomEntry(ctk.CTkEntry):
    def __init__(self, parent, placeholder = "", font_size=15, bold=False, **kwargs):
        super().__init__(
            parent,
            font=ctk.CTkFont(size=font_size, weight="bold" if bold else "normal"),
            width=350,
            height=35,
            placeholder_text=placeholder,
            border_width=0
        )

        self.configure(**kwargs)

class CustomButton(ctk.CTkButton):
    def __init__(self, parent, text, command, **kwargs):
        super().__init__(
            parent,
            font=ctk.CTkFont(size=15),
            width=175,
            height=40,
            text=text,
            cursor="hand2",
            command=command,
            corner_radius=10
        )
        self.configure(**kwargs)

class RemoveButton(ctk.CTkButton):
    def __init__(self, parent, command, no_bg_color=True, **kwargs):
        super().__init__(
            parent,
            image=trash_icon,
            text="",
            fg_color=NORMAL_COLOR,
            border_width=0,
            cursor="hand2",
            corner_radius=100,
            command=command,
            width=15,
            height=15
        )
        if no_bg_color:
            self.configure(bg_color=NORMAL_COLOR)
        self.configure(**kwargs)


class EditButton(ctk.CTkButton):
    def __init__(self, parent, command, no_bg_color=True, **kwargs):
        super().__init__(
            parent,
            image=edit_icon,
            text="",
            fg_color=NORMAL_COLOR,
            border_width=0,
            cursor="hand2",
            corner_radius=100,
            command=command,
            width=15,
            height=15
        )
        if no_bg_color:
            self.configure(bg_color=NORMAL_COLOR)
        self.configure(**kwargs)


class SmallButton(ctk.CTkButton):
    def __init__(self, parent, text, command, **kwargs):
        text = text[:MAX_TEXT_LEN_SMALL_BTN] + '...' if len(text) > MAX_TEXT_LEN_SMALL_BTN else text
        super().__init__(
            parent,
            text=text,
            command=command,
            border_width=0,
            corner_radius=10,
            cursor="hand2",
            font=ctk.CTkFont(size=12),
            anchor="w",
            height=40
        )
        self.configure(**kwargs)

class LabelEntry(ctk.CTkFrame):
    def __init__(
        self, 
        parent, 
        label_text = "", 
        label_fontsize = 18,
        label_bold = False,
        placeholder_text = "",
        entry_fontsize = 15,
        entry_bold = False,
        height = 40,
        width = 350
    ):
        super().__init__(parent, fg_color="transparent")

        self.grid_columnconfigure(0, weight=1)

        font = ctk.CTkFont(size=label_fontsize, weight="bold" if label_bold else "normal")
        self.label = ctk.CTkLabel(self, text=label_text, font=font)
        self.label.grid(row=0, column=0, padx=1, sticky="w") # sticky="w" substitui o anchor="w"

        font = ctk.CTkFont(size=entry_fontsize, weight="bold" if entry_bold else "normal")
        self.entry = ctk.CTkEntry(self, placeholder_text=placeholder_text, font=font, height=height, width=width)
        self.entry.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        
    def get(self):
        return self.entry.get()
    
    def set(self, string):
        self.entry.delete(0, "end")
        if string: self.entry.insert(0, string)
    
    def clear(self):
        """Limpa o campo de texto e restaura o placeholder"""
        placeholder = self.entry.cget("placeholder_text")
        self.entry.delete(0, "end")
        self.entry.configure(placeholder_text=placeholder)
    
    def configure_label(self, **kwargs):
        self.label.configure(**kwargs)

    def configure_entry(self, **kwargs):
        self.entry.configure(**kwargs)
    

class ResultButton(ctk.CTkButton):
    def __init__(self, parent, frame, text, submission, **kwargs):
        self.parent = parent
        self.submission = submission
        super().__init__(
            frame,
            text=text,
            # AGORA: Clicar no corpo do botão abre o código do aluno
            command=partial(self.parent.display_code, self.submission), 
            border_width=0,
            corner_radius=30,
            cursor="hand2",
            font=ctk.CTkFont(size=12),
            anchor="w",
            height=40
        )
        
        self.configure(**kwargs)
        self._insert_buttons()

        # Os eventos de hover (passar o mouse) continuam existindo se quiser usar depois
        # self.bind("<Enter>", self._on_criterion_hover_enter)
        # self.bind("<Leave>", self._on_criterion_hover_leave)

    def _insert_buttons(self):
        # Botão "Olho" (Visualizar Feedback) - Fixo em todos os arquivos
        self.eye_button = ctk.CTkButton(
            self, text="👁️", width=30, height=30, fg_color="transparent", hover_color="#171926",
            command=partial(self.parent.display_feedback, self.submission)
        )
        self.eye_button.place(in_=self, relx=0.97, rely=0.1, anchor="ne")
        
        # Botão "!" (Alerta de Similaridade) - Aparece dinamicamente apenas se houver similaridade
        if self.submission.get("similarity"):
            self.alert_button = ctk.CTkButton(
                self, text="!", width=25, height=25, 
                fg_color="#A30000", hover_color="#7A0000", text_color="white",
                font=ctk.CTkFont(size=14, weight="bold"),
                command=partial(self.parent.display_similarity, self.submission)
            )
            # Fica posicionado um pouco antes do olho
            self.alert_button.place(in_=self, relx=0.88, rely=0.12, anchor="ne")
            
    def _on_criterion_hover_enter(self, e):
        hover_color = "#171926"
        self.edit_button.configure(fg_color=hover_color, bg_color=hover_color)
        self.remove_button.configure(fg_color=hover_color, bg_color=hover_color)

    def _on_criterion_hover_leave(self, e):
        normal_color = "#212435"
        self.edit_button.configure(fg_color=normal_color, bg_color=normal_color)
        self.remove_button.configure(fg_color=normal_color, bg_color=normal_color)


class ScoreButton(ctk.CTkFrame):
    def __init__(self, parent, frame, text, submission, **kwargs):
        self.parent = parent
        self.submission = submission
        super().__init__(
            frame,
            border_width=0,
            corner_radius=30,
            fg_color="#212435",
            width=120,
            height=40
        )
        
        self.grid_propagate(False)
        self.grid_columnconfigure(0, weight=1)
        self.text = ctk.CTkLabel(self, text=text, font=ctk.CTkFont(size=14, weight="bold"))
        self.text.grid(row=0, column=0, padx=(17, 5), pady=3, sticky="w")
        self.configure(**kwargs)
        self._insert_edit_button()

    def _insert_edit_button(self):
        # Lápis que permite editar a nota
        self.edit_button = EditButton(
            self,
            command=partial(self.parent.prompt_edit_score, self.submission)
        )
        self.edit_button.grid(row=0, column=1, padx=(5, 15), pady=3, sticky="e")

class CriterionButton(ctk.CTkButton):
    def __init__(self, parent, frame, text, criteria_id, **kwargs):
        text = text[:MAX_TEXT_LEN_CRITERION] + '...' if len(text) > MAX_TEXT_LEN_CRITERION else text
        super().__init__(
            frame,
            text=text,
            command=partial(parent.on_start_evaluation, criteria_id),
            border_width=0,
            corner_radius=30,
            cursor="hand2",
            font=ctk.CTkFont(size=12),
            anchor="center",
            height=200,
            width=400
        )
        self.parent = parent
        self.criteria_id = criteria_id
        self.configure(**kwargs)
        self._insert_edit_button()
        self._insert_remove_button()

        self.bind("<Enter>", self._on_criterion_hover_enter)
        self.bind("<Leave>", self._on_criterion_hover_leave)

    def _insert_edit_button(self):
        self.edit_button = EditButton(
            self,
            command=partial(self.parent.edit_criteria, self.criteria_id)
        )
        self.edit_button.place(in_=self, relx=0.85, rely=0.1, anchor="ne")
    
    def _insert_remove_button(self):
        self.remove_button = RemoveButton(
            self,
            command=partial(self.parent.delete_criteria, self.criteria_id)
        )
        self.remove_button.place(in_=self, relx=0.97, rely=0.1, anchor="ne")

    def _on_criterion_hover_enter(self, e):
        """Quando mouse entra no critério"""
        hover_color = "#171926"
        self.edit_button.configure(fg_color=hover_color, bg_color=hover_color)
        self.remove_button.configure(fg_color=hover_color, bg_color=hover_color)

    def _on_criterion_hover_leave(self, e):
        """Quando mouse sai do critério"""
        normal_color = "#212435"
        self.edit_button.configure(fg_color=normal_color, bg_color=normal_color)
        self.remove_button.configure(fg_color=normal_color, bg_color=normal_color)