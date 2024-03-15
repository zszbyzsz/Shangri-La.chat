import streamlit as st

from init_role import init_role
from api import get_now_attribute, get_monster_attribute
from system import going_prologue,going_fight,going_conclusion,handle_button_click, FIRST_REMAIN


if 'memory_story' not in st.session_state:
    st.session_state['memory_story'] = []

def main():
    st.title("香格里拉")
    init_role()   # 初始化角色

    latest_response_display = st.empty()
    latest_response_display.text_area("系统提示", value=FIRST_REMAIN, key="latest_response", height=400, disabled=True)
    
    if st.session_state.confirmed == True and st.session_state.prologue_done == False:
        latest_response_display.text_area("系统提示", value="正在开始冒险...", height=400, disabled=True)

        going_prologue()
        st.session_state.condition = "prologue"
        st.success("请点击两次选项")
        value = f"系统面板：\n\n{st.session_state.description}\n\n发生在你面前的：\n\n{st.session_state.move}"
        latest_response_display.text_area("系统面板", value=value, height=400, disabled=True)  
        # life_dice()
        
        st.session_state.prologue_done = True

        
    if st.session_state.fight == True and st.session_state.conclusion ==False:
        # 检查用户是否做出了选择
        if st.session_state.user_choice is not None :
            
            latest_response_display.text_area("系统面板:\n", value="正在执行中...", height=400, disabled=True)
            
            going_fight(st.session_state['memory_story'], st.session_state.user_choice)
            st.success("做出你的选择")

            value= f"系统提示:\n\n {st.session_state.description}\n\n发生在你面前的：\n\n{st.session_state.move}\n\n怪物属性：\n\n{get_monster_attribute()}"
            latest_response_display.text_area("系统面板:\n", value=value, height=400, disabled=True) 
            # st.session_state.message_history.append(value)
            st.session_state.fight == False 
            st.session_state.conclusion ==False
            st.session_state.condition = "fight"


    if st.session_state.fight == False and st.session_state.conclusion ==True:
        if st.session_state.user_choice is not None:
            
            latest_response_display.text_area("系统面板", value="正在执行中...", height=400, disabled=True)
            
            going_conclusion(st.session_state['memory_story'])
            st.success("做出你的选择")

            vule = f"系统面板：\n\n{st.session_state.description}\n\n发生在你面前的：\n\n{st.session_state.move}"
            st.session_state.message_history.append(f"匆忙的记录：{st.session_state.description}\n迅速写下：{st.session_state.move}") 
            
            latest_response_display.text_area("系统面板", value=vule, height=400, disabled=True)  
            st.session_state.fight == False 
            st.session_state.conclusion ==False
            st.session_state.condition = "promote"


    if st.session_state.choice is not None:
        for i, option in enumerate(st.session_state.choice):
            # 使用on_click参数将handle_button_click函数绑定到按钮
            st.button(option, key=f"button_{i}", on_click=handle_button_click, args=(i, option, st.session_state['memory_story']))

    with st.expander("旅行信札", expanded=True):
        # 初始化历史记录内容字符串
        history_content = ""
        # 获取消息总数
        total_messages = len(st.session_state.message_history)
        # 遍历消息历史记录，并添加索引
        for idx, message in enumerate(reversed(st.session_state.message_history), 1):
            # 索引按照逆序显示
            index = total_messages - idx + 1
            # 将索引和历史记录连接在一起，并用分隔符分开
            history_content += f"#{index}\n{message}\n" + "-" * 4 + "\n"
        # # 移除最后一个分隔符
        # if history_content.endswith("-" * 4 + "\n"):
        #     history_content = history_content[:-5]
        # 展示合并后的历史记录
        st.text_area("", value=history_content, height=400, disabled=True)  # height可根据需要调整
            
if __name__ == "__main__":
    main()