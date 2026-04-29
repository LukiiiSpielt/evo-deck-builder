from src import card_loader


def apply_filters(type_filter, realm_filter, level_filter, effect_filter):
    card_list = card_loader.cards
    filtered_list = []
    print("Filtering cards...")

    for card in card_list:
        card_type = card.get("type", None)
        card_realm = card.get("realm", None)
        card_level = card.get("level", None)
        card_effect = card.get("effect_type", None)

        if (type_filter == "any" or card_type == type_filter) and \
            (realm_filter == "any" or card_realm == realm_filter) and \
            (level_filter == "any" or card_level == level_filter) and \
            (effect_filter == "any" or card_effect == effect_filter):
            filtered_list.append(card)
    return filtered_list

if __name__ == "__main__":
    result = apply_filters("evolver", "ocean", "1", "oat")
    print(result)