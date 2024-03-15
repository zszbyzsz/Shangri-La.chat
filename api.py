import streamlit as st
import random


def get_now_attribute():
    user = f""" 
    LV: {st.session_state.level} /100
    EXPRIENCE:{st.session_state.experience}
    HP: {st.session_state.hp} /1000
    MP: {st.session_state.mp} /1000
    PHYSICAL: {st.session_state.physical} /1000
    AGILITY: {st.session_state.agility} /1000
    INTELLIGENCE:  {st.session_state.intelligence} /1000
    STRENGTHH: {st.session_state.strength} /1000
    LUCK: {st.session_state.luck} /1000
    """
    return user

def get_monster_attribute():
    life_dice()
    monster = f""" 
NAME:{st.session_state.name_monster}
LV: {st.session_state.level_monster} 
HP: {st.session_state.hp_monster} 
MP: {st.session_state.mp_monster} 
PHYSICAL: {st.session_state.physical_monster} 
AGILITY: {st.session_state.agility_monster} 
INTELLIGENCE:  {st.session_state.intelligence_monster} 
STRENGTHH: {st.session_state.strength_monster} 
    """
    return monster
def life_dice():

    
    start = - (1 - st.session_state.luck / 100 )
    end = 1 + st.session_state.luck / 100
    
    if random.uniform(start,end) >99:
        meet_fairy()
    else:
        meet_monster()
    
def meet_fairy():
    return 

def meet_monster():
    if 'user_choice' not in st.session_state:
        st.session_state.name_monster = None
    st.session_state.level_monster = int(st.session_state.level + random.randint(-2,2) )
    st.session_state.hp_monster =     int(st.session_state.hp *(1 + random.uniform(-1.0, +1.0)))
    st.session_state.mp_monster =     int(st.session_state.mp * (1+ random.uniform(-1.0, +1.0)))
    st.session_state.physical_monster =  int(st.session_state.physical*  (1+ random.uniform(-1.0, +1.0)))
    st.session_state.agility_monster =    int(st.session_state.agility * (1+ random.uniform(-1.0, +1.0)))
    st.session_state.intelligence_monster =   int(st.session_state.intelligence * (1+ random.uniform(-1.0, +1.0)))
    st.session_state.strength_monster =     int(st.session_state.strength * (1+ random.uniform(-1.0, +1.0)))



def save_memory(story,move, choice, memory):

    entry = {'story': story, 'move':move,'choice': choice}
    if len(memory) >= 10:
        memory.pop(0)

    memory.append(entry)

    return memory



    
    