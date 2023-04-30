import json

# Завантаження даних з налаштувань
with open("configs/settings.json", encoding="utf-8") as f:
    settings = json.load(f)
    print(settings)

#Завантаження перекладу до вибраної мови
    for params in settings.items():
        if settings['language'] == #

        for lang_code in current_language.values():
            if lang_code == list(current_language.values())[0]:
                try:
                    with open(f'lang/{lang_code}.json', "r", encoding="utf-8") as g:
                        translation_text = json.load(g)
                        break
                except:
                    with open(f'lang/enUS.json', "r", encoding="utf-8") as g:
                        translation_text = json.load(g)
                        break

            if self.combobox_language.currentText() == list(lang_list.keys())[0]:
                new_language = {'language': f'{list(lang_list.values())[0]}'}
            elif self.combobox_language.currentText() == list(lang_list.keys())[1]:
                new_language = {'language': f'{list(lang_list.values())[1]}'}
            elif self.combobox_language.currentText() == list(lang_list.keys())[2]:
                new_language = {'language': f'{list(lang_list.values())[2]}'}