import json
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import card_loader
import filter_cards

current_card = None
card_list = None
name_to_id = {card["name"]: card["id"] for card in card_loader.cards}

def card_selected(evt):
    w = evt.widget
    if w == card_list and w.curselection():
        get_card_image(w.get(w.curselection()))


def get_card_image(card_name):
    card_id = name_to_id[card_name]
    image_path = card_loader.card_images[card_id]
    image = Image.open(image_path)
    photo = ImageTk.PhotoImage(image)
    current_card.config(image=photo)
    current_card.image = photo

def start_gui():
    global current_card, card_list

    bg_color = "#999999"
    window = Tk()
    window.geometry("1200x800")
    window.resizable(False, False)

    card_list = Listbox(window, bg=bg_color, font=("Arial", 20))
    card_list.pack(side="left", fill="y")
    card_list.bind("<<ListboxSelect>>", card_selected)

    for n in card_loader.cards:
        card_list.insert(END, n["name"])

    dummy_img = PhotoImage(file=card_loader.dummy_path)
    current_card = Label(window, image=dummy_img)
    current_card.place(x=600, y=800, anchor="s")

    deck_frame = Frame(window, bg="pink")
    deck_frame.pack(side="right", fill="y")

    deck_list = Listbox(deck_frame, bg=bg_color, font=("Arial", 20))
    deck_list.pack(side="top", expand=True, fill="y")

    evo_deck_list = Listbox(deck_frame, bg=bg_color, font=("Arial", 20), height=5)
    evo_deck_list.pack(side="bottom")

    add_frame = Frame(window, pady= 20)
    add_frame.pack(side="top")

    options = ["1", "2", "3"]
    selected_option = StringVar(value=options[0])
    opt = OptionMenu(add_frame, selected_option, *options)
    opt.pack(side="left")


    def add_to_deck():
        if card_list.curselection() == ():
            print("Nothing selected")
        else:
            if card_loader.cards[name_to_id[card_list.get(card_list.curselection())]]["type"] == "evolver":
                evo_deck_list.insert(END, f"{selected_option.get()} {card_list.get(card_list.curselection())}")
            else:
                deck_list.insert(END, f"{selected_option.get()} {card_list.get(card_list.curselection())}")

    add_button = Button(add_frame, text= "Add to Deck", font=("Arial", 15), bg=bg_color, command=add_to_deck)
    add_button.pack(side="right")

    def remove_from_deck():
        if not deck_list.curselection() == ():
            deck_list.delete(deck_list.curselection())
        if not evo_deck_list.curselection() == ():
            evo_deck_list.delete(evo_deck_list.curselection())


    remove_button = Button(window, text="Remove from Deck", font=("Arial", 15), bg=bg_color,command=remove_from_deck)
    remove_button.pack(side="top")

    menubar = Menu(window, bg=bg_color, font=("Arial", 15))
    window.config(menu=menubar)

    file_menu = Menu(menubar, tearoff=False)
    menubar.add_cascade(label="File", menu=file_menu)

    export_menu = Menu(file_menu, tearoff=False)
    file_menu.add_cascade(label="Export", menu=export_menu)

    def export_untap():
        file = filedialog.asksaveasfile(defaultextension=".txt",
                                        filetypes=[("Text file:", ".txt")])
        suffix = " - Sample"
        modified_card_names = [line + suffix for line in deck_list.get(0, END)]
        modified_evo_names = [line + suffix for line in evo_deck_list.get(0, END)]
        filetext = f"//deck-1\n{"\n".join(modified_card_names)}\n\n//deck-2\n{"\n".join(modified_evo_names)}"
        file.write(filetext)
        file.close()

    export_menu.add_command(label="Export to Untap", command=export_untap)

    def export_json():
        file = filedialog.asksaveasfile(defaultextension=".json",
                                       filetypes=[("JSON file:", ".json")])
        data = {"main_deck": [], "evo_deck": []}
        for card in deck_list.get(0, END):
            quantaty, *name_parts = card.split()
            card_name = " ".join(name_parts)
            data["main_deck"].append({
                "card_id": name_to_id[card_name],
                "card_name": card_name,
                "quantaty": int(quantaty)
            })
        for card in evo_deck_list.get(0, END):
            quantaty, *name_parts = card.split()
            card_name = " ".join(name_parts)
            data["evo_deck"].append({
                "card_id": name_to_id[card_name],
                "card_name": card_name,
                "quantaty": int(quantaty)
            })
        json_data = json.dumps(data, indent=4)
        file.write(json_data)
        file.close()

    export_menu.add_command(label="Export as json", command=export_json)

    filter_menu = Menu(menubar, tearoff=False)
    menubar.add_cascade(label="Filter", menu=filter_menu)

    type_filter = Menu(filter_menu, tearoff=False)
    filter_menu.add_cascade(label="Type", menu=type_filter)
    card_types = ["any","evolver", "defender", "effector"]
    selected_type = StringVar(value=card_types[0])
    for card_type in card_types:
        type_filter.add_radiobutton(
            label=card_type.capitalize(),
            variable=selected_type,
            value=card_type
        )

    realm_filter = Menu(filter_menu, tearoff=False)
    filter_menu.add_cascade(label="Realm", menu=realm_filter)
    card_realms = ["any", "ocean", "desert", "fire", "forest", "sky", "dark"]
    selected_realm = StringVar(value=card_realms[0])
    for card_realm in card_realms:
        realm_filter.add_radiobutton(
            label=card_realm.capitalize(),
            variable=selected_realm,
            value=card_realm
        )

    level_filter = Menu(filter_menu, tearoff=False)
    filter_menu.add_cascade(label="Level", menu=level_filter)
    card_levels = ["any", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]
    selected_level = StringVar(value=card_levels[0])
    for card_level in card_levels:
        level_filter.add_radiobutton(
            label=card_level.capitalize(),
            variable=selected_level,
            value=card_level
        )

    effect_filter = Menu(filter_menu, tearoff=False)
    filter_menu.add_cascade(label="Effect", menu=effect_filter)
    card_effects = ["any", "void", "play", "oat", "permanent", "vanilla"]
    selected_effect = StringVar(value=card_effects[0])
    for card_effect in card_effects:
        effect_filter.add_radiobutton(
            label=card_effect.capitalize(),
            variable=selected_effect,
            value=card_effect
        )

    def apply_filters():
        filtered_cards = filter_cards.apply_filters(selected_type.get(),
                                                    selected_realm.get(),
                                                    selected_level.get(),
                                                    selected_effect.get())
        card_list.delete(0, END)
        if not filtered_cards:
            if all(var == "any" for var in [selected_type.get(),
                                            selected_realm.get(),
                                            selected_level.get(),
                                            selected_effect.get()]):
                for card in card_loader.cards:
                    card_list.insert(END, card["name"])
        else:
            for card in filtered_cards:
                card_list.insert(END, card["name"])

    menubar.add_command(label="Apply filters", command=apply_filters)

    window.mainloop()

if __name__ == "__main__":
    start_gui()