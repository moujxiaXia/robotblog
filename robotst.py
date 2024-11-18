import streamlit as st
from flask import Flask, render_template
 
# 创建你的 Flask 应用
app = Flask(__name__)
 
@app.route('/')
def hello():
    return "Hello, Flask!"
 
# 运行你的 Flask 应用
if not st.secrets.is_server_running():
    # 只在Streamlit Sharing服务器上运行
    app.run(debug=True)
 
# 在Streamlit应用中的其他部分
st.title('My Streamlit App')
st.write('This is a Streamlit app with a Flask backend.')