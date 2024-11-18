import streamlit as st
import sqlite3
from datetime import datetime

# 初始化数据库
def init_db():
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS posts
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
         title TEXT NOT NULL,
         content TEXT NOT NULL,
         created_date TEXT NOT NULL)
    ''')
    
    # 插入示例文章
    sample_posts = [
        ("机器人在医疗领域的应用", 
         """医疗机器人正在革新现代医疗保健系统。从手术辅助到病房巡查，机器人技术为医疗服务带来了前所未有的精确性和效率。
         特别是在微创手术方面，机器人辅助系统能够实现人手无法企及的精细操作，大大减少了患者的恢复时间。
         未来，随着AI技术的进步，医疗机器人将在诊断、治疗和康复等多个环节发挥更大作用。""",
         datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        
        ("工业机器人的发展趋势", 
         """工业4.0时代，智能机器人正成为制造业转型升级的核心动力。协作机器人的出现使人机协作更加安全和高效。
         通过深度学习和计算机视觉技术，现代工业机器人具备了更强的环境适应能力和任务处理灵活性。
         未来工业机器人将向着更智能、更灵活、更安全的方向发展。""",
         datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        
        ("服务机器人改变生活方式", 
         """从扫地机器人到送餐机器人，服务型机器人正在悄然改变我们的日常生活。
         在餐厅、酒店、商场等公共场所，服务机器人的身影越来越常见。它们不知疲倦地工作，提供标准化的服务。
         随着技术的发展，服务机器人将具备更强的交互能力，为人类提供更贴心的服务。""",
         datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    ]
    
    c.executemany('INSERT OR IGNORE INTO posts (title, content, created_date) VALUES (?, ?, ?)', sample_posts)
    conn.commit()
    conn.close()

# 获取所有文章
def get_all_posts():
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()
    c.execute('SELECT * FROM posts ORDER BY created_date DESC')
    posts = c.fetchall()
    conn.close()
    return posts

# 获取单篇文章
def get_post(post_id):
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()
    c.execute('SELECT * FROM posts WHERE id = ?', (post_id,))
    post = c.fetchone()
    conn.close()
    return post

# 添加新文章
def add_post(title, content):
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()
    created_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.execute('INSERT INTO posts (title, content, created_date) VALUES (?, ?, ?)',
             (title, content, created_date))
    conn.commit()
    conn.close()

# 初始化数据库并创建示例文章
init_db()

# Streamlit应用界面
st.title('机器人科技博客')

# 侧边栏
st.sidebar.title('博客管理')
page = st.sidebar.radio('选择操作', ['查看文章列表', '发布新文章'])

if page == '查看文章列表':
    posts = get_all_posts()
    for post in posts:
        st.header(post[1])  # 标题
        st.text(f'发布时间: {post[3]}')  # 发布时间
        st.markdown(post[2])  # 内容
        st.markdown('---')

elif page == '发布新文章':
    st.header('发布新文章')
    title = st.text_input('文章标题')
    content = st.text_area('文章内容', height=300)
    if st.button('发布'):
        if title and content:
            add_post(title, content)
            st.success('文章发布成功！')
        else:
            st.error('标题和内容不能为空！')

           