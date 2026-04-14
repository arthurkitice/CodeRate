import customtkinter as ctk
from PIL import Image

edit_icon = ctk.CTkImage(dark_image=Image.open("ui/icons/edit_icon.png"), size=(30, 30))
trash_icon = ctk.CTkImage(dark_image=Image.open("ui/icons/trash_icon.png"), size=(30, 30))

def create_entry(parent, placeholder, **kwargs):
        return ctk.CTkEntry(
            parent,
            font=ctk.CTkFont(size=15),
            width=350,
            height=35,
            placeholder_text=placeholder,
            border_width=0,
            fg_color="white",
            text_color="black",
            **kwargs
        )

def create_button(parent, text, command, **kwargs):
    return ctk.CTkButton(
        parent,
        font=ctk.CTkFont(size=15),
        width=350,
        height=35,
        text=text,
        cursor="hand2",
        command=command,
        **kwargs
    )

def create_criterion_button(parent, frame, criterion):
        truncated_name = criterion.name[:30] + '...' if len(criterion.name) > 30 else criterion.name
        criterion_button = ctk.CTkButton(
            frame,
            text=truncated_name,
            command=lambda c=criterion: parent.start_evaluation(c.id),
            border_width=0,
            corner_radius=30,
            cursor="hand2",
            font=ctk.CTkFont(size=12),
            anchor="center",
            height=200,
            width=400
        )
        return criterion_button

def create_remove_button(parent, frame, criterion, no_bg_color=True):
    normal_color = "#212435"
    remove_button = ctk.CTkButton(
        frame,
        image=trash_icon,
        text="",
        fg_color=normal_color,
        border_width=0,
        cursor="hand2",
        corner_radius=100,
        command=lambda c_id=criterion.id: parent.delete_criteria(c_id),
        width=15,
        height=15
    )
    
    if no_bg_color:
        remove_button.configure(bg_color=normal_color)

    return remove_button

def create_edit_button(parent, frame, criterion, no_bg_color=True):
    normal_color = "#212435"
    edit_button = ctk.CTkButton(
        frame,
        image=edit_icon,
        text="",
        fg_color=normal_color,
        border_width=0,
        cursor="hand2",
        corner_radius=100,
        command=lambda c_id=criterion.id: parent.edit_criteria(c_id),
        width=15,
        height=15
    )

    if no_bg_color:
        edit_button.configure(bg_color=normal_color)

    return edit_button

def create_small_criterion_button(frame, criterion, command, max_name_len=50):
    truncated_name = criterion.name[:max_name_len] + '...' if len(criterion.name) > max_name_len else criterion.name
    criterion_button = ctk.CTkButton(
        frame,
        text=truncated_name,
        command=command,
        border_width=0,
        corner_radius=10,
        cursor="hand2",
        font=ctk.CTkFont(size=12),
        anchor="w",
        height=40,
    )
    return criterion_button