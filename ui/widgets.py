import customtkinter as ctk
from PIL import Image
from functools import partial

edit_icon = ctk.CTkImage(dark_image=Image.open("ui/icons/edit_icon.png"), size=(30, 30))
trash_icon = ctk.CTkImage(dark_image=Image.open("ui/icons/trash_icon.png"), size=(30, 30))

NORMAL_COLOR = "#212435"
MAX_TEXT_LEN_SMALL_BTN = 50
MAX_TEXT_LEN_CRITERION = 30

class CustomEntry(ctk.CTkLabel):
    def __init__(self, parent, placeholder = "", font_size=15, bold=False, **kwargs):
        super().__init__(
            parent,
            font=ctk.CTkFont(size=font_size, weight="bold" if bold else "normal"),
            width=350,
            height=35,
            placeholder_text=placeholder,
            border_width=0,
            fg_color="white",
            text_color="black"
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
    def __init__(self, parent, text, command, max_text_len=50, **kwargs):
        text = text[:max_text_len] + '...' if len(text) > max_text_len else text
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