import re

def find_choice_pattern(choice, name):
    # 使用正则表达式来寻找"$<name>"或"<name>$"，其中<name>是传入的参数
    # 要确保name中的特殊字符被正确地转义
    escaped_name = re.escape(name)
    
    pattern = rf'\${escaped_name}|{escaped_name}\$'
    match = re.search(pattern, choice)

    # 如果找到了匹配项，返回匹配项的起始索引，否则返回-1
    return match.start() if match else -1

def find_act_pattern(choice, name):
    # 使用正则表达式来寻找"$<name>"或"<name>$"，其中<name>是传入的参数
    # 要确保name中的特殊字符被正确地转义
    escaped_name = re.escape(name)
    
    pattern = rf'\%{escaped_name}|{escaped_name}\%'
    match = re.search(pattern, choice)

    # 如果找到了匹配项，返回匹配项的起始索引，否则返回-1
    return match.start() if match else -1

def clean(text, name, chars):
    text = text.replace(name, "")
    for char in chars:
        text = text.replace(char, "")
    text = text.replace("*", "")
    text = text.replace("\n", "")
    text = text.replace("'", "")
    text = text.replace('"', "")
    text = text.lstrip()

    return text

def clean_voice(voice):
    r = voice.rfind('"')
    l = voice.find('"')
    voice = voice[l+1:r]
    return voice

def clean_choice(choice):
    
    loc_a = find_choice_pattern(choice, "A")
    loc_b = find_choice_pattern(choice, "B")
    loc_c = find_choice_pattern(choice, "C")
    loc_d = find_choice_pattern(choice, "D")
    choice_a = choice[loc_a: loc_b]
    choice_b = choice[loc_b: loc_c]
    choice_c = choice[loc_c: loc_d]
    choice_d = choice[loc_d:]
    
    choice_a_c = clean(choice_a,"A","$%:')(><|'`")
    choice_b_c = clean(choice_b,"B","$%:')(><|'`")
    choice_c_c = clean(choice_c,"C","$%:')(><|'`")
    choice_d_c = clean(choice_d,"D","$%:')(><|'`")

    return choice_a_c,choice_b_c,choice_c_c,choice_d_c

def clean_act(act):
    loc_a = find_act_pattern(act, "A")
    loc_b = find_act_pattern(act, "B")
    loc_c = find_act_pattern(act, "C")
    loc_d = find_act_pattern(act, "D")
    act_a = act[loc_a: loc_b]
    act_b = act[loc_b: loc_c]
    act_c = act[loc_c: loc_d]
    act_d = act[loc_d:]

    act_a_c = clean_single_act(act_a)
    act_b_c = clean_single_act(act_b)
    act_c_c = clean_single_act(act_c)
    act_d_c = clean_single_act(act_d)

    return act_a_c, act_b_c, act_c_c, act_d_c


def find_signed_number(choice):
    # 使用正则表达式来寻找带有可选前缀“+”或“-”的数字
    pattern = r'[+-]?\d+'
    match = re.search(pattern, choice)

    # 如果找到了带符号的数字，返回这个数字，否则返回0
    return int(match.group()) if match else 0

def clean_single_act(monster_act):
    l = monster_act.find("[")
    r = monster_act.find("]")
    act_slic = monster_act[l:r]
    loc_hp =  act_slic.find("HP")
    loc_mp = act_slic.find("MP")
    loc_phs = act_slic.find("PHYSICAL")
    loc_exps = act_slic.find("EXPERIENCE")
    
    number_hp = find_signed_number(act_slic[loc_hp:loc_mp])
    number_mp = find_signed_number(act_slic[loc_mp:loc_phs])
    number_phs = find_signed_number(act_slic[loc_phs:loc_exps])
    number_exps = find_signed_number(act_slic[loc_exps:])

    
    return {"HP":number_hp,"MP":number_mp,"PHYSICAL":number_phs,"EXPERIENCE":number_exps}

def get_struct_message(monster_message):

    start_1 = monster_message.find("NAME")
    start_2 = monster_message.find("DESCRIPTION")
    start_3 = monster_message.find("MOVE")
    start_4 = monster_message.find("VOICE")
    start_5 = monster_message.find("OPTIONS")
    # start_6 = monster_message.find("ACT")

    monster_name = monster_message[start_1:start_2]
    monster_description = monster_message[start_2: start_3]
    monster_move = monster_message[start_3: start_4]
    # ----
    monster_voice = monster_message[start_4:start_5]

    # ---
    monster_choice = monster_message[start_5: ]
    # monster_act = monster_message[start_6:]
    
    
    monster_name_c = clean(monster_name,"NAME","""<>|':""")
    monster_description_c = clean(monster_description,"DESCRIPTION","""<>|':""")
    monster_move_c = clean(monster_move,"MOVE","""<>|':""")
    monster_voice_c = clean_voice(monster_voice)
    monster_choice_c = clean_choice(monster_choice)
    # monster_act_c = clean_act(monster_act)

    return monster_name_c, monster_description_c, monster_move_c, monster_voice_c, monster_choice_c


def get_struct_prologue(monster_message):

    start_1 = monster_message.find("NAME")
    start_2 = monster_message.find("DESCRIPTION")
    start_3 = monster_message.find("MOVE")
    start_4 = monster_message.find("VOICE")
    start_5 = monster_message.find("OPTIONS")

    monster_name = monster_message[start_1:start_2]
    monster_description = monster_message[start_2: start_3]
    monster_move = monster_message[start_3: start_4]
    # ----
    monster_voice = monster_message[start_4:start_5]

    # ---
    monster_choice = monster_message[start_5: ]
    
    
    monster_name_c = clean(monster_name,"NAME","""<>|':""")
    monster_description_c = clean(monster_description,"DESCRIPTION","""<>|':""")
    monster_move_c = clean(monster_move,"MOVE","""<>|':""")
    monster_voice_c = clean_voice(monster_voice)
    monster_choice_c = clean_choice(monster_choice)

    return monster_name_c, monster_description_c, monster_move_c, monster_voice_c, monster_choice_c

def clean_single_act_7(monster_act):
    l = monster_act.find("[")
    r = monster_act.find("]")
    act_slic = monster_act[l:r]
    loc_hp =  act_slic.find("HP")
    loc_mp = act_slic.find("MP")
    loc_phs = act_slic.find("PHYSICAL")
    loc_exps = act_slic.find("EXPERIENCE")
    loc_aglity =  act_slic.find("AGILITY")
    loc_intelligence = act_slic.find("INTELLIGENCE")
    loc_strength = act_slic.find("STRENGTH")
    loc_luck = act_slic.find("LUCK")
    
    number_hp = find_signed_number(act_slic[loc_hp:loc_mp])
    number_mp = find_signed_number(act_slic[loc_mp:loc_phs])
    number_phs = find_signed_number(act_slic[loc_phs:loc_exps])
    number_exps = find_signed_number(act_slic[loc_exps:loc_aglity])
    
    number_ality = find_signed_number(act_slic[loc_aglity:loc_intelligence])
    number_intenlligence = find_signed_number(act_slic[loc_intelligence:loc_strength])
    number_strength = find_signed_number(act_slic[loc_strength:loc_luck])
    number_luck = find_signed_number(act_slic[loc_luck:])
    
    return {"HP":number_hp,"MP":number_mp,"PHYSICAL":number_phs,"EXPERIENCE":number_exps,
            "AGILITY":number_ality,"INTELLIGENCE":number_intenlligence,"STRENGTH":number_strength,"LUCK":number_luck}


def get_struct_fight(conclusion_message):
    loc_1 = conclusion_message.find("RESULT")
    loc_2 = conclusion_message.find("ACT")
    loc_3 = conclusion_message.find("OPTIONS")

    conclusion_result = conclusion_message[loc_1:loc_2]
    conclusion_act = conclusion_message[loc_2:loc_3]
    conclusion_options = conclusion_message[loc_3:]
    
    conclusion_result_c = clean(conclusion_result,"RESULT","""<>|':""")
    conclusion_act_c = clean_single_act_7(conclusion_act)

    conclusion_options_c = clean_choice(conclusion_options)
    
    return conclusion_result_c,conclusion_act_c,conclusion_options_c


def clean_single_act_promote(prompote):
    l = prompote.find("[")
    r = prompote.find("]")
    act_slic = prompote[l:r]
    loc_hp =  act_slic.find("AGILITY")
    loc_mp = act_slic.find("INTELLIGENCE")
    loc_phs = act_slic.find("STRENGTH")
    loc_exps = act_slic.find("LUCK")
    
    number_hp = find_signed_number(act_slic[loc_hp:loc_mp])
    number_mp = find_signed_number(act_slic[loc_mp:loc_phs])
    number_phs = find_signed_number(act_slic[loc_phs:loc_exps])
    number_exps = find_signed_number(act_slic[loc_exps:])

    
    return {"AGILITY":number_hp,"INTELLIGENCE":number_mp,"STRENGTH":number_phs,"LUCK":number_exps}


def get_struct_promote(conclusion_message):
    loc_1 = conclusion_message.find("RESULT")
    loc_2 = conclusion_message.find("BLESSINGS/CURSES")
    loc_3 = conclusion_message.find("ACT")
    loc_4 = conclusion_message.find("OPTIONS")


    conclusion_result = conclusion_message[loc_1:loc_2]
    conclusion_B_C = conclusion_message[loc_2:loc_3]
    conclusion_act = conclusion_message[loc_3:loc_4]
    conclusion_options = conclusion_message[loc_4:]
    
    
    conclusion_result_c = clean(conclusion_result,"RESULT","""<>|':""")
    conclusion_B_C_c = clean(conclusion_B_C,"BLESSINGS/CURSES","""<>|':""")
    conclusion_act_c = clean_single_act_7(conclusion_act)
    conclusion_options_c = clean_choice(conclusion_options)
    
    return conclusion_result_c,conclusion_B_C_c,conclusion_act_c,conclusion_options_c