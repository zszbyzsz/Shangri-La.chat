import streamlit as st
import random

from api import get_now_attribute


# Density
MAX_HP = 1000
MAX_MP = 1000
MAX_PHYSICAL = 1000
scences = ["Forest","Desert","crust","swamp"]
times= ['Spring','Summer', "Autumn", "Winter"]

scences = ["森林", "沙漠", "地壳", "沼泽", "冻原", "山丘", "山谷"]
times= ['春','夏', "秋", "冬"]
lv_up= random.randint(999999999,9999999999)


def init_role():
    # st.sidebar.image("./pictures/eye.jpg", caption="角色图像")
    
    if 'prologue_done' not in st.session_state:
        st.session_state.prologue_done = False
    
    if "fight" not in st.session_state: 
        st.session_state.fight = False
    
    if "condition" not in st.session_state:
        st.session_state.condition = "prologue"

    if 'user_choice' not in st.session_state:
        st.session_state.user_choice = None
        
    if 'conclusion' not in st.session_state:
        st.session_state.conclusion = False

    if 'choice' not in st.session_state:
        st.session_state.choice = None
        
    if 'message_history' not in st.session_state:
        st.session_state.message_history = []   
        
    if 'act' not in st.session_state:
        st.session_state.act =( {'HP':0, 'MP':0, 'PHYSICAL':0,'EXPERIENCE':0, 'AGILITY':0, 'INTELLIGENCE':0, 'STRENGTH':0, 'LUCK':0})

    # 初始化 session_state 没有被初始化的键
    keys = ['hp', 'mp', 'physical', 'level', 'agility', 'intelligence', 'strength', 'luck', 'confirmed']
    defaults = [78, 65, 72, 1, 14, 9, 17, 8, False]
    for key, default in zip(keys, defaults):
        if key not in st.session_state:
            st.session_state[key] = default
            st.session_state.sence = scences[0]
            st.session_state.time = times[0]
            st.session_state.experience = 0
    with st.sidebar:
        # 如果用户还没有确认，显示“随机生成属性”和“确定”按钮
        if not st.session_state.confirmed:
            col1, col2 = st.columns(2)

            # “随机生成属性”按钮
            if col1.button("随机生成属性"):
                st.session_state.level = random.randint(1, 1)
                st.session_state.hp = random.randint(80, 100)
                st.session_state.mp = random.randint(80, 100)
                st.session_state.physical = random.randint(80, 100)
                st.session_state.agility = random.randint(25, 30)
                st.session_state.intelligence = random.randint(25, 30)
                st.session_state.strength = random.randint(25, 30)
                st.session_state.luck = random.randint(25, 30)
                st.session_state.sence = scences[random.randint(0,len(scences)-1)]
                st.session_state.time = times[random.randint(0,len(times)-1)]
                st.session_state.experience = 0

            # “确定”按钮
            if col2.button("确定"):
                st.session_state.confirmed = True

        # 显示角色属性和进度条
        st.write(f"等级: {st.session_state.level}")
        st.write(f"经验值: {st.session_state.experience}/{lv_up}")

        st.write(f"生命值: {st.session_state.hp}/{MAX_HP}")
        st.progress(st.session_state.hp / MAX_HP)

        st.write(f"魔法值: {st.session_state.mp}/{MAX_MP}")
        st.progress(st.session_state.mp / MAX_MP)

        st.write(f"体力: {st.session_state.physical}/{MAX_PHYSICAL}")
        st.progress(st.session_state.physical / MAX_PHYSICAL)

        col1, col2 = st.columns(2)
        col1.metric("敏捷", f"{st.session_state.agility}")
        col2.metric("智力", f"{st.session_state.intelligence}")

        col3, col4 = st.columns(2)
        col3.metric("力量", f"{st.session_state.strength}")
        col4.metric("幸运", f"{st.session_state.luck}")
        




def prologue():
    user_attribute = get_now_attribute()
    message = f""" 
    ###Answer all questions in English###
    You are now a professional storytelling expert whose sole purpose is to drive the development of the plot.
    The scene in which the story takes place is limited to{st.session_state.sence},the current season is:{st.session_state.time}.
    The User's  attribute is  {user_attribute}
    This is the beginning of the story. The background is other planets in a fantastic parallel universe. Players wake up and find themselves falling into the scene above. Give a specific description and start taking risks. In the above scenario the player is given two choices.
    Reply with a template:
    ```
    DESCRIPTION: "specific scenarios and difficult descriptions"|
    OPTIONS: "give specific options.A&B&C&D"|
    ```
    """
    return message
    


