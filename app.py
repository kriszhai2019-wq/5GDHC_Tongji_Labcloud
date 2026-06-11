import streamlit as st
import pandas as pd

# 1. 页面基础配置（开启宽屏）
st.set_page_config(page_title="复合土壤源热泵系统", layout="wide")

# ================= 侧边栏 =================
st.sidebar.title("🌿 新奥生态园区项目")
st.sidebar.markdown("---")
st.sidebar.subheader("👨‍🔬 团队成员")
st.sidebar.write("马嘉诚, 熊婉仪")
st.sidebar.write("于海晨, Christoph Schuppin")

st.sidebar.subheader("📍 地理概况")
st.sidebar.info("本项目位于上海市同济大学嘉定校区的新奥生态园区。建筑占地面积238㎡，总面积476㎡，其中空调面积382㎡。")

# ================= 主页面 =================
st.title("复合土壤源热泵系统实验数据看板")
st.markdown("以土壤源热泵相关影响参数为主导研究方向，联合空气源热泵与冷却塔组合运行。")

# --- 核心数据指标卡片 ---
st.markdown("### 📊 核心设计负荷")
col1, col2, col3, col4 = st.columns(4)
col1.metric(label="夏季制冷负荷 (含管损)", value="66 kW", delta="设定温度: 26℃")
col2.metric(label="冬季制热负荷 (含管损)", value="25.7 kW", delta="设定温度: 16℃", delta_color="normal")
col3.metric(label="地源热泵制冷/热量", value="105 / 126 kW")
col4.metric(label="换热井数量", value="21 口")

st.markdown("---")

# --- 使用标签页组织大段内容 ---
tab1, tab2, tab3 = st.tabs(["⚙️ 系统架构描述", "📋 实验工况说明", "🎛️ 设备与传感器清单"])

# 标签页 1：系统架构
with tab1:
    st.subheader("系统冷热源描述")
    st.write("""
    针对上海地区夏季所需冷量高于冬季所需热量的情况，若只采用土壤作为冷热源，将导致土壤蓄热，地层温度升高。
    故实验场设置了冷却塔，并采用**并联**和**串联**两种连接方式。为节约成本，联合空气源热泵、冷却塔进行组合运行，可利用夜间波谷电价进行蓄冷。
    """)
    st.info("💡 提示：这里未来可以插入 【图1 空调水系统图】 的高清图片，代码：st.image('你的图片路径.png')")

    st.subheader("空调风系统描述")
    st.write("空气侧采用双风机、一次回风变风量空调系统，每层楼设置四个变风量箱。在控制策略上，采用定静压控制。")

# 标签页 2：四种实验工况
with tab2:
    st.subheader("运行工况设定")

    # 用 Expander (折叠面板) 让排版更整洁
    with st.expander("工况一：只使用土壤源热泵", expanded=True):
        st.write("**核心动作：** 关闭连通空气源热泵和冷却塔的两通阀V1-V4。打开地埋管集分水器间的两通阀V5。")
        st.write("**水环路：** GSHP水环路切换三通阀门V17-V20根据工况切换，1制冷，2制热。")

    with st.expander("工况二：只使用空气源热泵"):
        st.write("**核心动作：** 打开连通空气源热泵的两通阀V1，V2。关闭冷却塔的两通阀V3，V4及地埋管V5。")

    with st.expander("工况三：土壤源热泵 + 冷却塔"):
        st.write("**核心动作：** 关闭V1，V2，打开V3，V4。通过冷却塔承担建筑物部分冷负荷，缓解土壤热平衡问题。")

    with st.expander("工况四：土壤源热泵 + 空气源热泵"):
        st.write("**核心动作：** 打开V1，V2，关闭V3，V4。联合运行。")

# 标签页 3：设备清单（用表格展示）
with tab3:
    st.subheader("检测与控制设备 (部分展示)")
    # 使用 Pandas DataFrame 让表格非常美观
    sensor_data = {
        "名称": ["涡轮流量 Q1", "涡轮流量 Q5", "室外温湿度", "风道静压 P1", "温度传感器 T1"],
        "位置": ["出地端", "板换 + 旁通前", "室外", "一层", "出地端5"],
        "接口协议": ["4-20mA", "4-20mA", "4-20mA", "0-10VDC", "PT1000"],
        "模块类型": ["AI", "AI", "AI*4", "AI", "TEMP"]
    }
    df = pd.DataFrame(sensor_data)
    st.dataframe(df, use_container_width=True)

    st.caption("完整设备参数请参考原始文档附录。")