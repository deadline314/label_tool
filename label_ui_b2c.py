import streamlit as st
import pandas as pd
import os
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode

# 如果尚未安裝，請運行：pip install streamlit-aggrid

# 設定頁面佈局
st.set_page_config(layout="wide", page_title="標註工具", page_icon="🛠️")

st.title("🔍 標註工具")
st.subheader("商品匹配的標註界面")

# 讀取數據
@st.cache_data
def load_data():
    return pd.read_csv("./b2c/B2C_Common_250.csv")

data = load_data()

search_terms = data['搜尋詞'].unique()
selected_search_term = st.sidebar.selectbox("選擇搜尋詞", search_terms)

filtered_data = data[data['搜尋詞'] == selected_search_term]

titles_a = filtered_data['商品名稱A'].tolist()
titles_b = filtered_data['商品名稱B'].tolist()

rows = [f"A-{i+1}" for i in range(len(titles_a))]
cols = [f"B-{i+1}" for i in range(len(titles_b))]

annotations_file = f"{selected_search_term}_annotations.csv"

# 初始化標註 DataFrame
if "annotations_df" not in st.session_state or st.session_state.get('search_term') != selected_search_term:
    if os.path.exists(annotations_file):
        st.session_state.annotations_df = pd.read_csv(annotations_file, index_col=0)
    else:
        st.session_state.annotations_df = pd.DataFrame('x', index=rows, columns=cols)
    st.session_state.search_term = selected_search_term

# 如果有圖片欄位，準備圖片數據，否則跳過
if '商品圖片A' in filtered_data.columns and '商品圖片B' in filtered_data.columns:
    images_a = filtered_data['商品圖片A'].tolist()
    images_b = filtered_data['商品圖片B'].tolist()

    st.session_state.row_images = {row: images_a[i] for i, row in enumerate(rows)}
    st.session_state.col_images = {col: images_b[i] for i, col in enumerate(cols)}
else:
    st.session_state.row_images = {}
    st.session_state.col_images = {}

tooltip_df = pd.DataFrame(index=rows, columns=cols)
for i, row in enumerate(rows):
    for j, col in enumerate(cols):
        title_a = titles_a[i]
        title_b = titles_b[j]
        # 如果有圖片，加入圖片資料
        image_a_url = st.session_state.row_images.get(row, "")
        image_b_url = st.session_state.col_images.get(col, "")
        tooltip_df.loc[row, col] = f"{image_a_url}|{image_b_url}|{title_a}|{title_b}"

# 準備數據用於 AgGrid
data_df = st.session_state.annotations_df.copy()
for col in cols:
    data_df[col + "_tooltip"] = tooltip_df[col]
data_df.reset_index(inplace=True)
data_df.rename(columns={'index': '商品A_商品B'}, inplace=True)

gb = GridOptionsBuilder.from_dataframe(data_df)
gb.configure_default_column(resizable=True, suppressMenu=True, minWidth=100)

gb.configure_column('商品A_商品B', pinned='left', cellStyle={'pointer-events': 'none', 'background-color': '#f0f0f0'})

for col in data_df.columns:
    if col.endswith('_tooltip'):
        gb.configure_column(col, hide=True)

gb.configure_grid_options(domLayout='normal')
gridOptions = gb.build()
gridOptions['context'] = {
    'rowImages': st.session_state.row_images,
    'colImages': st.session_state.col_images
}

# JavaScript 代碼處理單元格事件
cell_clicked_js = JsCode("""
function(e) {
    if (e.colDef.field !== '商品A_商品B' && !e.colDef.field.endsWith('_tooltip') && e.rowIndex !== null) {
        var currentValue = e.value;
        var newValue = currentValue === 'x' ? 'o' : 'x';
        e.node.setDataValue(e.colDef.field, newValue);
    }
}
""")

cell_mouse_over_js = JsCode("""
function(e) {
    var imageContainer = document.getElementById('image-preview');
    if (!imageContainer) {
        imageContainer = document.createElement('div');
        imageContainer.id = 'image-preview';
        document.body.appendChild(imageContainer); 
    }

    var field = e.column.userProvidedColDef.field;
    var rowField = e.data['商品A_商品B'];
    var colField = field.replace('_tooltip', '');

    if (e.rowIndex !== null && !field.endsWith('_tooltip')) {
        var tooltip = e.data[field + '_tooltip'].split('|');
        var [imageA, imageB, titleA, titleB] = tooltip;

        if (titleA && titleB) {
            imageContainer.innerHTML = `
                <div>
                    <strong>${titleA}</strong><br>
                    ${imageA ? `<img src="${imageA}" alt="商品A" style="max-width:200px; max-height:150px; margin-right:10px;">` : ''}
                </div>
                <div>
                    <strong>${titleB}</strong><br>
                    ${imageB ? `<img src="${imageB}" alt="商品B" style="max-width:200px; max-height:150px;">` : ''}
                </div>
            `;
        }
    }

    imageContainer.style.display = 'block';
    imageContainer.style.position = 'fixed';
    var mouseEvent = e.event || window.event;

    var topPosition = mouseEvent.clientY + 10;
    var leftPosition = mouseEvent.clientX + 10;

    var viewportWidth = window.innerWidth;
    var viewportHeight = window.innerHeight;
    var containerWidth = imageContainer.offsetWidth;
    var containerHeight = imageContainer.offsetHeight;

    if (mouseEvent.clientY + containerHeight + 20 > viewportHeight) {
        topPosition = mouseEvent.clientY - containerHeight - 10;
    }

    if (mouseEvent.clientX + containerWidth + 20 > viewportWidth) {
        leftPosition = mouseEvent.clientX - containerWidth - 10;
    }

    imageContainer.style.top = `${topPosition}px`;
    imageContainer.style.left = `${leftPosition}px`;
    imageContainer.style.zIndex = '2000';
    imageContainer.style.backgroundColor = 'white';
    imageContainer.style.padding = '10px';
    imageContainer.style.border = '1px solid #ddd';
    imageContainer.style.borderRadius = '5px';
    imageContainer.style.boxShadow = '0 4px 8px rgba(0,0,0,0.2)';
}
""")

cell_mouse_out_js = JsCode("""
function(e) {
    var imageContainer = document.getElementById('image-preview');
    if (imageContainer) {
        imageContainer.style.display = 'none';
        imageContainer.innerHTML = '';
    }
}
""")

gridOptions['onCellClicked'] = cell_clicked_js
gridOptions['onCellMouseOver'] = cell_mouse_over_js
gridOptions['onCellMouseOut'] = cell_mouse_out_js

st.markdown(
    '''
    <style>
    #image-preview {
        display: none;
        position: fixed;
        z-index: 1000;
    }
    </style>
    ''',
    unsafe_allow_html=True
)

response = AgGrid(
    data_df,
    gridOptions=gridOptions,
    enable_enterprise_modules=False,
    fit_columns_on_grid_load=True,
    allow_unsafe_jscode=True,
    reload_data=True,
    height=700,
    width='100%',
    update_mode='MODEL_CHANGED',
)

if st.button("保存標註"):
    updated_data = pd.DataFrame(response['data']).set_index('商品A_商品B')
    st.session_state.annotations_df = updated_data[cols]
    st.session_state.annotations_df.to_csv(annotations_file, index=True)
    st.success("標註已保存！")
