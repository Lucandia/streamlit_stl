import streamlit as st
from streamlit_stl import stl_from_file, stl_from_text

if __name__ == "__main__":
    st.set_page_config(layout="wide")

    st.title("Streamlit STL Examples")

    st.subheader("Look: a flexi squirrel!")
    cols = st.columns(4)
    with cols[0]:
        color = st.color_picker("Pick a color", "#FF9900", key='color_file')
    with cols[1]:
        material = st.selectbox("Select a material", ["material", "wireframe"], key='material_file')
    with cols[2]:
        st.write('\n'); st.write('\n')
        auto_rotate = st.toggle("Auto rotation", key='auto_rotate_file')
    with cols[3]:
        height = st.slider("Height", min_value=50, max_value=1000, value=500, key='height_file')

    stl_from_file(  file_path='squirrel.stl', 
                    color=color,
                    material=material,
                    auto_rotate=auto_rotate,
                    height=height,
                    key='example1')
    
    file_input = st.file_uploader("Or upload a STL file ", type=["stl"])

    cols = st.columns(4)
    with cols[0]:
        color = st.color_picker("Pick a color", "#0099FF", key='color_text')
    with cols[1]:
        material = st.selectbox("Select a material", ["material", "wireframe"], key='material_text')
    with cols[2]:
        st.write('\n'); st.write('\n')
        auto_rotate = st.toggle("Auto rotation", key='auto_rotate_text')
    with cols[3]:
        height = st.slider("Height", min_value=50, max_value=1000, value=500, key='height_text')
    if file_input:
        stl_from_text(  text=file_input.getvalue(), 
                        color=color,
                        material=material,
                        auto_rotate=auto_rotate,
                        height=height,
                        key='example2')
