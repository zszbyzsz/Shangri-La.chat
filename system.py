
import random
import streamlit as st

from connect import call_with_messages
from prompts_z import (use_system_prompt_prologue,use_message_prompt_prologue,
                       use_system_prompt_fight_consequence ,use_message_prompt_fight_consequence,
                       use_system_prompt_fight,use_message_prompt_fight,
                     use_message_prompt_normal_consequence, use_system_prompt_normal_consequence, )
from api import get_now_attribute, get_monster_attribute,save_memory
from utils import get_struct_prologue, get_struct_fight, get_struct_promote, get_struct_message

FIRST_REMAIN = f""" 
【开始游戏】：随机好属性角色，点击【两次】确定 即可开始游戏

【当心】：当左侧属性在某次选择后，小于等于0，则角色死亡。

【加载】：右上角runing的小人，即是在加载游戏，请耐心等候

如果选项没有文字，随便选择要给依然可以推动剧情发展
如果你刷新页面，一切将会重新来过（重生，同时所有剧情将会消失）。

如果角色没有死亡，这款游戏可以一直玩下去，希望您【享受游戏本身】

而不是想办法把等级升到2级

）
"""


def going_prologue():
    system_prompt = use_system_prompt_prologue(st.session_state.sence,st.session_state.time)
    message_prompt = use_message_prompt_prologue(st.session_state.sence,st.session_state.time,get_now_attribute())
    
    # print(system_prompt,message_prompt)
    response = call_with_messages(system_prompt, message_prompt)

    # response =raw_response['output']['choices'][0]["message"]['content']

    name, description, move, voice, choice = get_struct_prologue(response)
    st.session_state.description = description
    st.session_state.move = move
    st.session_state.name_monster = name
    st.session_state.choice = choice
    
    # st.session_state.message_history.append(f"匆忙的记录：{description}\n 迅速写下的：{move}")            

def going_fight(memory_story, choice):

    system_prompt = use_system_prompt_fight(st.session_state.sence,st.session_state.time, memory_story, choice)
    message_prompt = use_message_prompt_fight(memory_story, choice, get_now_attribute(),get_monster_attribute())
    # print("2"*100)

    # print(system_prompt,message_prompt)
    response = call_with_messages(system_prompt, message_prompt)

    # response =raw_response['output']['choices'][0]["message"]['content']

    name, description, move, voice, choice = get_struct_message(response)
    
    st.session_state.description = description
    st.session_state.move = move
    st.session_state.name_monster = name
    st.session_state.choice = choice
    st.session_state.message_history.append(f"匆忙的记录：{description}\n 迅速写下的：{move}")            

    
def going_conclusion(memory_story):
    if st.session_state.condition == "fight":
        system_prompt = use_system_prompt_fight_consequence(memory_story, st.session_state.user_choice,st.session_state.user_choice)
        message_prompt = use_message_prompt_fight_consequence(memory_story, st.session_state.user_choice,st.session_state.user_choice)
        
        response = call_with_messages(system_prompt, message_prompt)

        # response =raw_response['output']['choices'][0]["message"]['content']

        conclusion_result,conclusion_act, conclusion_options = get_struct_fight(response)
        
        st.session_state.description = conclusion_result
        st.session_state.choice = conclusion_options
        st.session_state.act = conclusion_act
        
    if st.session_state.condition == "promote":
        system_prompt = use_system_prompt_normal_consequence(memory_story)
        message_prompt = use_message_prompt_normal_consequence(memory_story, st.session_state.user_choice)
        
        response = call_with_messages(system_prompt, message_prompt)

        # response =raw_response['output']['choices'][0]["message"]['content']

        conclusion_result,conclusion_B_C,conclusion_act,conclusion_options = get_struct_promote(response)
        
        st.session_state.description = conclusion_result
        st.session_state.move = conclusion_B_C
        st.session_state.choice = conclusion_options
        st.session_state.act = conclusion_act

    
def life_dice():
    start = - (1 - st.session_state.luck / 100 )
    end = 1 + st.session_state.luck / 100
    if random.uniform(0,1) > 0.9:
        st.session_state.fight = True
        st.session_state.conclusion = False
    else:
        st.session_state.fight = False
        st.session_state.conclusion = True

# 定义按钮点击时调用的函数
def handle_button_click(i, option, memory_story):
    # print("!"*100)
    st.session_state.user_choice = option
    save_memory(st.session_state.description,st.session_state.move ,option, memory_story)
    # print(memory_story)
    # print("promote",st.session_state.act)
    st.session_state.agility = min(st.session_state.agility + st.session_state.act["AGILITY"],1000)
    st.session_state.intelligence = min(st.session_state.intelligence + st.session_state.act["INTELLIGENCE"],1000)
    st.session_state.strength = min(st.session_state.strength + st.session_state.act["STRENGTH"],1000)
    st.session_state.luck = min(st.session_state.luck + st.session_state.act["LUCK"],1000)
    st.session_state.hp = min(st.session_state.hp + st.session_state.act["HP"], 1000)
    st.session_state.mp = min(st.session_state.mp + st.session_state.act["MP"],1000)
    st.session_state.physical = min(st.session_state.physical + st.session_state.act["PHYSICAL"],1000)
    st.session_state.experience = st.session_state.experience + st.session_state.act["EXPERIENCE"]
    life_dice()
        