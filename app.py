import streamlit as st
import pandas as pd
import numpy as np

# ================= 1. 页面基础配置 =================
st.set_page_config(page_title="5GDHC 实验台数字孪生", layout="wide")

# ================= 2. 主页面头部 =================
st.title("第五代区域供冷供热（5GDHC）实验台数字孪生")

st.markdown("---")

# ================= 3. 标签页分流 =================
tab1, tab2, tab3, tab4 = st.tabs(["⚙️ 系统描述", "📋 实验工况说明", "🎛️ 设备与传感器清单", "🗺️ 系统管网与实时监测"])

# ----------------- 标签页 1：系统描述 -----------------
with tab1:
    st.info("""
    **地理位置：** 本项目位于上海市同济大学嘉定校区的新奥生态园区。建筑设计为办公与学生实验用楼，占地面积 238㎡，总面积 476㎡，其中空调面积 382㎡。
    """)
    st.subheader("🌡️ 核心负荷与参数设定")
    st.markdown("""
    * **夏季工况：** 空调设定温度 26℃，相对湿度 60%。经过校核并考虑管损等因素，系统制冷量为 **66 kW**。
    * **冬季工况：** 空调设定温度 16℃，相对湿度 40%。经过校核并考虑管损等因素，系统制热量为 **25.7 kW**。
    * **核心热源：** 现场共设计有 **21口** 竖直埋管换热井，配备制冷量 105kW、制热量 126kW 的地源热泵主机。
    """)

    st.subheader("🌊 系统冷热源描述")
    st.write("""
    针对上海地区夏季所需冷量高于冬季所需热量的情况，若只采用土壤作为冷热源，可能造成地温场变化。故实验场设置了冷却塔，并采用 **并联** 和 **串联** 两种连接方式。为有效利用资金，系统联合空气源热泵、冷却塔进行组合运行，可利用夜间波谷电价进行蓄冷。
    """)

    st.subheader("💨 空调风系统描述")
    st.write("""
    空气侧采用双风机、一次回风变风量空调系统，机组采用 ZK-12W(42) 型，每层楼设置四个变风量箱，两层共 8 个。在控制策略上采用定静压控制，通过风道静压传感器与设定值对比，变频控制风机转速。
    """)

# ----------------- 标签页 2：最新实验工况 -----------------
with tab2:
    st.subheader("🎛️ 运行工况设定与阀门控制逻辑")

    with st.expander("工况一：ASHP（空气源热泵）供冷供热工况", expanded=True):
        st.info("💡 **工况描述：** 仅依靠空气源热泵为建筑提供冷/热量。适用于过渡季节负荷较小的情况，或作为系统备用模式。")
        st.markdown("""
        * **打开阀门：** 阀门V1、V2、V7、V15、V16开。
        * **关闭阀门：** 阀门V3、V4、V6、V5、V9、V10-V14关。
        """)

    with st.expander("工况二：GSHP（土壤源热泵）单独供冷供热工况"):
        st.info("💡 **工况描述：** 系统的核心基础运行模式。完全利用地下 21 口换热井进行排热或取热。")
        st.markdown("""
        * **打开阀门：** 阀门V5、V7、V10-V14、V8(压差调节)开。
        * **关闭阀门：** 阀门V1、V2、V3、V4、V6、V9(旁通阀)、V15、V16关。
        """)

    with st.expander("工况三：GSHP + 冷却塔 供冷供热工况"):
        st.info("💡 **工况描述：** 针对夏季冷负荷远大于冬季热负荷的特点，引入冷却塔辅助散热，平衡地温场。")
        st.markdown("""
        * **打开阀门：** 阀门V3、V4、V5、V7、V16、V10-V14、V8(压差调节)开。
        * **关闭阀门：** 阀门V1、V2、V6、V15、V9(旁通阀)关。
        """)

# ----------------- 标签页 3：设备清单 -----------------
with tab3:
    st.subheader("全量检测与控制设备名录")
    full_equipment_data = {
        "设备大类": ["流量计", "温湿度", "压力传感器", "水泵/风机调速", "电动两通阀", "电动三通阀", "温度传感器"],
        "编号 / 名称": ["Q1-Q8", "T&RH (2个)", "P1, P2, DP1", "Pump1-3, F1-F3", "V1-V16", "V17-V20", "T1-T15"],
        "位置 / 规格": ["DN50-DN100", "室外", "风道/集水分水器", "冷冻水/冷却塔等", "各类管路", "水环路切换", "PT1000 盲管/贴片"],
        "接口 / 控制类型": ["4-20mA / AI", "4-20mA / AI", "0-10VDC / AI", "0-10V 变频", "二位或0-10V", "二位组合", "TEMP 数据采集"]
    }
    st.dataframe(pd.DataFrame(full_equipment_data), use_container_width=True, hide_index=True)

# ----------------- 标签页 4：高清底图 + 数据看板 -----------------
with tab4:
    st.markdown("下方为复合土壤源热泵系统水系统拓扑图。结合右侧实时监控数据，可全局掌握系统运行工况。")

    # 采用左右分栏设计：左侧2/3放图，右侧1/3放数据
    col_img, col_data = st.columns([2, 1])

    with col_img:
        try:
            # ⚠️ 确保你的文件夹里有导出的 system_map.png
            st.image("system_map.png", caption="5GDHC 实验平台水系统高清拓扑图", use_container_width=True)
        except FileNotFoundError:
            st.error("⚠️ 未找到图片！请将导出的系统图命名为 system_map.png 并放在与 app.py 同一个文件夹下。")

    with col_data:
        st.markdown("### ⚡ 实时测点监控 (模拟)")

        # 模拟生成带有微小波动的实时数据
        sim_temp_out = round(np.random.normal(32.5, 0.5), 1)
        sim_temp_in = round(np.random.normal(27.2, 0.3), 1)
        sim_flow = round(np.random.normal(8.6, 0.2), 2)
        sim_power = round(np.random.normal(15.2, 0.4), 1)

        # 渲染动态指标卡片
        st.metric(label="地埋管总出水温度", value=f"{sim_temp_out} ℃", delta="-0.2 ℃")
        st.metric(label="地埋管总进水温度", value=f"{sim_temp_in} ℃", delta="+0.1 ℃", delta_color="inverse")
        st.metric(label="主管道实时流量", value=f"{sim_flow} m³/h", delta="正常运行区间")
        st.metric(label="系统瞬时总功率", value=f"{sim_power} kW", delta="-0.5 kW")

        st.markdown("---")
        st.markdown("### 🎛️ 核心阀门状态反馈")
        # 模拟工业指示灯状态
        st.success("🟢 V5 (地埋管集分水器间) : 开启状态")
        st.success("🟢 V8 (压差调节阀) : 开启状态")
        st.error("🔴 V9 (旁通阀) : 关闭状态")
        st.error("🔴 V1, V2 (空气源热泵端) : 关闭状态")

    st.markdown("---")
    st.caption("🔄 提示：右侧数据为系统额定参数的动态波动模拟。每次刷新网页或交互时，数据将自动重算以模拟传感器刷新。")