import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

DATA_PATH = 'RTA Dataset.csv'
ACCIDENT_SEVERITY_ORDER = ['轻微伤害', '严重伤害', '致命伤害']
CRITICAL_SEVERITY = ['严重伤害', '致命伤害']

st.set_page_config(
    page_title="RTA 仪表板：精细多维度事故分析",
    layout="wide",
    initial_sidebar_state="expanded"
)


@st.cache_data(show_spinner="正在加载和准备数据...")
def load_data(path: str) -> pd.DataFrame:
    """加载原始数据集，清理列名并设置数据类型。"""
    df = pd.read_csv(path)

    df.columns = df.columns.str.replace('[^A-Za-z0-9_]+', '', regex=True).str.lower()
    df = df.replace(['Unknown', 'unknown', 'na', '-1', 'Other'], np.nan)
    df['time'] = pd.to_datetime(df['time'], format='%H:%M:%S', errors='coerce').dt.time
    
    df['day_of_week'] = pd.Categorical(
        df['day_of_week'], 
        categories=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], 
        ordered=True
    )

    severity_mapping = {
        'Slight Injury': '轻微伤害',
        'Serious Injury': '严重伤害',
        'Fatal Injury': '致命伤害'
    }
    df['accident_severity'] = df['accident_severity'].map(severity_mapping)
    df['accident_severity'] = pd.Categorical(
        df['accident_severity'], 
        categories=ACCIDENT_SEVERITY_ORDER, 
        ordered=True
    )

    df['hour'] = df['time'].apply(lambda x: x.hour if pd.notna(x) else np.nan)
    df['casualty_count'] = pd.to_numeric(df['number_of_casualties'], errors='coerce')

    AGE_BANDS = ['Under 18', '18-30', '31-50', 'Over 51']
    df['age_band_of_driver'] = pd.Categorical(df['age_band_of_driver'], categories=AGE_BANDS, ordered=True)
    
    EDU_LEVELS = ['Illiterate', 'Elementary school', 'Junior high school', 'High school graduate', 'Above high school', 'College & above']
    df['educational_level'] = pd.Categorical(df['educational_level'], categories=EDU_LEVELS, ordered=True)
    
    return df

def draw_chart(chart, title):
    """用于显示具有一致样式图表的实用函数。"""
    chart = chart.interactive()
    st.altair_chart(chart, use_container_width=True)

df_data = load_data(DATA_PATH)

with st.sidebar:
    st.image("微信图片_20251123203603_26_25.jpg", width=100) 
    st.image("微信图片_20251123203604_27_25.jpg", width=100) 
    st.markdown("---")
  
    st.title("数据筛选器")
    
    st.header("1. 事故严重程度")
    selected_severity = st.multiselect(
        "要关注的严重程度级别：",
        options=ACCIDENT_SEVERITY_ORDER,
        default=ACCIDENT_SEVERITY_ORDER,
        help="选择要包含在图表和关键绩效指标 (KPI) 中的严重程度级别。"
    )
    
    st.header("2. 地理筛选")
    areas = df_data['area_accident_occured'].dropna().unique().tolist()
    selected_areas = st.multiselect(
        "按事故发生区域筛选：",
        options=areas,
        default=areas
    )
    
    st.markdown("---")
    st.markdown(
        """
        #EFREIDataStoriesWUT2025  
        **Kangmin Yu** | kangmin.yu@efrei.net
        """
    )

df_filtered = df_data[
    (df_data['accident_severity'].isin(selected_severity)) &
    (df_data['area_accident_occured'].isin(selected_areas))
].copy()

st.title("RTA 仪表板：道路交通事故多维度分析")
st.caption("项目概览：对埃塞俄比亚道路交通事故 (RTA) 数据进行可视化和分析，涵盖五个定制的分析主题。")
st.markdown("---")

st.header("1. 🚨 项目叙述：从问题到分析框架")
st.markdown("---")

st.subheader("问题：埃塞俄比亚道路上的沉默危机")
st.error(
    """
    道路交通事故（RTAs）在全球范围内，尤其是在发展中国家，构成了一个重大的公共卫生和经济挑战。埃塞俄比亚正面临着惊人的严重事故和致命事故发生率。传统的事故报告往往只关注总体计数，未能提供制定有效政策干预所需的精细、多维度的见解。**核心问题是缺乏可操作的智能**——政策制定者需要了解最危险的事故是*谁*、*何时*、*何地*、*为何*发生的。
    """
)

st.subheader("数据解决方案：为什么选择这个数据集？")
st.info(
    """
    选择该**埃塞俄比亚道路交通事故数据集**是因为其丰富且相互关联的变量，它超越了简单的时间/位置数据。它包含关键的**驾驶员特征**（年龄、教育、经验）、**环境因素**（天气、路面）、**行为原因**（`Cause_of_accident`）和详细的**严重程度**结果。这使得分析能够从简单的计数转向**因果和预测性分析**。

    本项目采用五个分析维度将原始数据转化为有针对性的见解（分析阶段）：
    
    * **地理风险:** 高风险区域在哪里？
    * **时间模式:** 高风险时段/日期是何时？
    * **因果因素:** 哪些驾驶员行为和条件导致事故？
    * **碰撞机制:** 哪些碰撞类型最致命？
    * **驾驶员人口统计:** 哪些驾驶员群体最脆弱或最危险？
    """
)
st.markdown("---")

col1, col2, col3 = st.columns(3)
col1.metric("事故总数（已筛选）", f"{len(df_filtered):,}")
col2.metric("每次事故平均伤亡人数", f"{df_filtered['casualty_count'].mean():.2f}")
critical_rate = (len(df_filtered[df_filtered['accident_severity'].isin(CRITICAL_SEVERITY)]) / len(df_filtered) * 100) if len(df_filtered) > 0 else 0
col3.metric("严重/致命事故发生率", f"{critical_rate:.1f}%")

st.markdown("---")

st.header("2. 🗺️ 地理事故比较 ")
st.info("目标：识别高风险地理区域，并分析其主要的碰撞特征。")
col1, col2 = st.columns(2)

with col1:
    st.subheader("按严重程度划分的事故地理分布")
    area_agg_severity = df_filtered.groupby(['area_accident_occured', 'accident_severity'], observed=True).size().reset_index(name='count')
    
    chart = alt.Chart(area_agg_severity).mark_circle(opacity=0.8).encode(
        x=alt.X('accident_severity', title='事故严重程度', sort=ACCIDENT_SEVERITY_ORDER),
        y=alt.Y('area_accident_occured', title='事故发生区域', sort=alt.EncodingSortField(field='count', op='sum', order='descending')),
        size=alt.Size('count', title='事故数量', scale=alt.Scale(range=[50, 600])),
        color=alt.Color('accident_severity', scale=alt.Scale(domain=ACCIDENT_SEVERITY_ORDER, range=['#4C78A8', '#E34C31', '#943E2C']), title='严重程度'),
        tooltip=['area_accident_occured', 'accident_severity', alt.Tooltip('count', title='事故数量')]
    ).properties(title="区域事故严重程度分布")
    draw_chart(chart, "区域事故严重程度分布")
with col2:
    st.subheader("按区域划分的主要碰撞类型分布")
    area_collision_agg = df_filtered.groupby(['area_accident_occured', 'type_of_collision'], observed=True).size().reset_index(name='count')
    
    chart = alt.Chart(area_collision_agg).mark_bar().encode(
        x=alt.X('count', stack="normalize", title='碰撞类型比例'),
        y=alt.Y('area_accident_occured', title='事故发生区域', sort=alt.EncodingSortField(field='count', op='sum', order='descending')),
        color=alt.Color('type_of_collision', title='碰撞类型', scale=alt.Scale(scheme='category10')),
        tooltip=['area_accident_occured', 'type_of_collision', alt.Tooltip('count', format=',', title='事故数量')]
    ).properties(title="区域碰撞类型比例")
    draw_chart(chart, "按区域划分的主要碰撞类型分布")

st.markdown("---")

st.header("3. ⏱️ 时间事故分析")
st.info("目标：确定一天中的高风险时间窗口，并观察碰撞类型随时间的变化。")
col1, col2 = st.columns(2)

with col1:
    st.subheader("每小时事故数量和严重程度趋势")
    time_severity_agg = df_filtered.groupby(['hour', 'accident_severity'], observed=True).size().reset_index(name='count')
    
    chart = alt.Chart(time_severity_agg).mark_line(point=True).encode(
        x=alt.X('hour', title='一天中的小时'),
        y=alt.Y('count', title='事故数量'),
        color=alt.Color('accident_severity', scale=alt.Scale(domain=ACCIDENT_SEVERITY_ORDER, range=['#4C78A8', '#E34C31', '#943E2C']), title='严重程度'),
        tooltip=['hour', 'accident_severity', alt.Tooltip('count', title='事故数量')]
    ).properties(title="按小时和严重程度分组的事故趋势")
    draw_chart(chart, "每小时事故数量和严重程度趋势")

with col2:
    st.subheader("不同小时的碰撞类型分布")
    time_collision_agg = df_filtered.groupby(['hour', 'type_of_collision'], observed=True).size().reset_index(name='count')
    
    top_collisions = time_collision_agg.groupby('type_of_collision')['count'].sum().nlargest(5).index.tolist()
    time_collision_agg = time_collision_agg[time_collision_agg['type_of_collision'].isin(top_collisions)]

    chart = alt.Chart(time_collision_agg).mark_bar().encode(
        x=alt.X('type_of_collision', title='碰撞类型'),
        y=alt.Y('count', title='事故数量'),
        column=alt.Column('hour', header=alt.Header(titleOrient="bottom"), title='小时'),
        color=alt.Color('type_of_collision', title='碰撞类型', scale=alt.Scale(scheme='category10')),
        tooltip=['hour', 'type_of_collision', alt.Tooltip('count', title='事故数量')]
    ).properties(title="按小时划分的碰撞类型分布 (前 5 名)")
    draw_chart(chart, "不同小时的碰撞类型分布 (分组条形图)")
    
st.markdown("---")

st.header("4. 因素分析：贡献因素")
st.info("目标：检查驾驶员个人因素、环境条件（天气/路面）和驾驶行为对事故频率和严重程度的影响。")
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("驾驶员个人特征与严重事故数量")
    
    df_severe = df_filtered[df_filtered['accident_severity'].isin(CRITICAL_SEVERITY)].copy()
    
    st.markdown("##### 按年龄段划分的严重事故数量")
    age_agg = df_severe.groupby('age_band_of_driver', observed=True).size().reset_index(name='Severe_Count')
    chart_age = alt.Chart(age_agg).mark_bar(color='#E34C31').encode(
        x=alt.X('Severe_Count', title='严重/致命事故数量'),
        y=alt.Y('age_band_of_driver', title='年龄段', sort=None),
        tooltip=['age_band_of_driver', alt.Tooltip('Severe_Count', title='严重事故数量')]
    )
    draw_chart(chart_age, "按年龄段划分的严重事故数量")

    st.markdown("##### 按驾驶经验划分的严重事故数量")
    exp_agg = df_severe.groupby('driving_experience', observed=True).size().reset_index(name='Severe_Count')
    chart_exp = alt.Chart(exp_agg).mark_bar(color='#CC6633').encode(
        x=alt.X('Severe_Count', title='严重/致命事故数量'),
        y=alt.Y('driving_experience', title='驾驶经验', sort=None),
        tooltip=['driving_experience', alt.Tooltip('Severe_Count', title='严重事故数量')]
    )
    draw_chart(chart_exp, "按驾驶经验划分的严重事故数量")
    
    st.markdown("##### 按性别划分的严重事故数量")
    sex_agg = df_severe.groupby('sex_of_driver', observed=True).size().reset_index(name='Severe_Count')
    chart_sex = alt.Chart(sex_agg).mark_bar(color='#943E2C').encode(
        x=alt.X('Severe_Count', title='严重/致命事故数量'),
        y=alt.Y('sex_of_driver', title='驾驶员性别', sort=None),
        tooltip=['sex_of_driver', alt.Tooltip('Severe_Count', title='严重事故数量')]
    )
    draw_chart(chart_sex, "按驾驶员性别划分的严重事故数量")

with col2:
    st.subheader("天气与路面组合的影响")
    weather_surface_agg = df_filtered.groupby(['weather_conditions', 'road_surface_type'], observed=True).size().reset_index(name='count')
    
    chart = alt.Chart(weather_surface_agg).mark_rect().encode(
        x=alt.X('road_surface_type', title='路面类型'),
        y=alt.Y('weather_conditions', title='天气状况'),
        color=alt.Color('count', scale=alt.Scale(range='heatmap'), title='事故数量'),
        tooltip=['road_surface_type', 'weather_conditions', alt.Tooltip('count', title='事故数量')]
    ).properties(title="事故热力图：天气 vs. 路面")
    draw_chart(chart, "天气与路面组合的影响")

with col3:
    st.subheader("驾驶员行为与事故严重程度比例")
    
    behavior_severity_agg = df_filtered.groupby(['cause_of_accident', 'accident_severity'], observed=True).size().reset_index(name='count')
    
    total_by_cause = behavior_severity_agg.groupby('cause_of_accident')['count'].sum()
    top_10_causes = total_by_cause.nlargest(10).index.tolist()
    
    behavior_severity_agg = behavior_severity_agg[behavior_severity_agg['cause_of_accident'].isin(top_10_causes)].copy()

    chart = alt.Chart(behavior_severity_agg).mark_bar().encode(
        x=alt.X('count', stack="normalize", title='事故严重程度比例'),
        y=alt.Y('cause_of_accident', title='驾驶员行为 (前 10 原因)', 
                sort=alt.EncodingSortField(field='count', op='sum', order='descending')),
        color=alt.Color('accident_severity', scale=alt.Scale(domain=ACCIDENT_SEVERITY_ORDER, range=['#4C78A8', '#E34C31', '#943E2C']), title='严重程度'),
        tooltip=['cause_of_accident', 'accident_severity', alt.Tooltip('count', format=',', title='事故数量')]
    ).properties(title="驾驶员行为与事故严重程度比例")
    draw_chart(chart, "驾驶员行为与事故严重程度比例")

st.markdown("---")

st.header("5. 💥 碰撞类型与伤亡关系")
st.info("目标：量化不同碰撞类型（`type_of_collision`）的频率、严重程度和伤亡影响。")
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("碰撞类型频率 (前 5 名)")
    collision_counts = df_filtered['type_of_collision'].value_counts().head(5).reset_index(name='Count')
    collision_counts.columns = ['type_of_collision', 'Count']
    
    chart = alt.Chart(collision_counts).mark_arc(outerRadius=120).encode(
        theta=alt.Theta(field="Count", type="quantitative"),
        color=alt.Color(field="type_of_collision", type="nominal", title='碰撞类型', scale=alt.Scale(scheme='category10')),
        order=alt.Order("Count", sort="descending"),
        tooltip=['type_of_collision', alt.Tooltip('Count', format=',', title='事故数量')]
    ).properties(title="前 5 碰撞类型比例")
    draw_chart(chart, "碰撞类型频率")

with col2:
    st.subheader("碰撞类型与事故严重程度比例")
    collision_severity_agg = df_filtered.groupby(['type_of_collision', 'accident_severity'], observed=True).size().reset_index(name='count')
    
    chart = alt.Chart(collision_severity_agg).mark_bar().encode(
        x=alt.X('count', stack="normalize", title='事故比例'),
        y=alt.Y('type_of_collision', title='碰撞类型', sort=alt.EncodingSortField(field='count', op='sum', order='descending')),
        color=alt.Color('accident_severity', scale=alt.Scale(domain=ACCIDENT_SEVERITY_ORDER, range=['#4C78A8', '#E34C31', '#943E2C']), title='严重程度'),
        tooltip=['type_of_collision', 'accident_severity', alt.Tooltip('count', format=',', title='事故数量')]
    ).properties(title="碰撞类型与严重程度比例")
    draw_chart(chart, "碰撞类型与事故严重程度比例")

with col3:
    st.subheader("碰撞类型对平均伤亡人数的影响")
    
    casualty_agg = df_filtered.groupby('type_of_collision', observed=True)['casualty_count'].agg(
        mean='mean',
        std='std'
    ).reset_index()
    
    casualty_agg['lower_bound'] = casualty_agg['mean'] - casualty_agg['std']
    casualty_agg['upper_bound'] = casualty_agg['mean'] + casualty_agg['std']
    casualty_agg['lower_bound'] = casualty_agg['lower_bound'].apply(lambda x: max(0, x))

    bar = alt.Chart(casualty_agg).mark_bar(color='#4C78A8').encode(
        y=alt.Y('type_of_collision', title='碰撞类型', sort='-x'),
        x=alt.X('mean', title='平均伤亡人数'),
        tooltip=['type_of_collision', alt.Tooltip('mean', format='.2f', title='平均伤亡人数'), alt.Tooltip('std', format='.2f', title='标准差')]
    ).properties(title="碰撞类型 vs. 平均伤亡人数")

    error_bars = alt.Chart(casualty_agg).mark_rule().encode(
        y=alt.Y('type_of_collision', title='碰撞类型'),
        x=alt.X('lower_bound', title=''),
        x2='upper_bound'
    )
    
    chart = bar + error_bars
    draw_chart(chart, "碰撞类型 vs. 平均伤亡人数 (平均值 + 标准差)")


st.markdown("---")

st.header("6. 👤 驾驶员特征与事故严重程度相关性")
st.info("目标：探索驾驶员特征（如年龄和教育水平）与事故严重程度之间复杂的关联。")
col1, col2 = st.columns(2)

with col1:
    st.subheader("教育水平与事故严重程度比例")
    edu_severity_agg = df_filtered.groupby(['educational_level', 'accident_severity'], observed=True).size().reset_index(name='count')
    
    chart = alt.Chart(edu_severity_agg).mark_bar().encode(
        x=alt.X('educational_level', title='教育水平', sort=None), 
        y=alt.Y('count', stack="normalize", title='事故比例'),
        color=alt.Color('accident_severity', scale=alt.Scale(domain=ACCIDENT_SEVERITY_ORDER, range=['#4C78A8', '#E34C31', '#943E2C']), title='严重程度'),
        tooltip=['educational_level', 'accident_severity', alt.Tooltip('count', format=',', title='事故数量')]
    ).properties(title="教育水平 vs. 事故严重程度比例")
    draw_chart(chart, "教育水平 vs. 事故严重程度比例")

with col2:
    st.subheader("驾驶员年龄、经验与严重事故")

    df_severe = df_filtered[df_filtered['accident_severity'].isin(CRITICAL_SEVERITY)].copy()

    age_exp_agg = df_severe.groupby(['driving_experience', 'age_band_of_driver'], observed=True).size().reset_index(name='Severe_Count')

    chart = alt.Chart(age_exp_agg).mark_rect().encode(
        x=alt.X('driving_experience', title='驾驶经验', sort=None),
        y=alt.Y('age_band_of_driver', title='年龄段', sort=None),
        color=alt.Color('Severe_Count', scale=alt.Scale(range='heatmap'), title='严重事故数量'),
        tooltip=['age_band_of_driver', 'driving_experience', alt.Tooltip('Severe_Count', title='严重事故数量')]
    ).properties(title="驾驶经验 vs. 年龄段严重事故")
    draw_chart(chart, "驾驶员年龄、经验与严重事故")

st.markdown("---")

st.header("7. 💡 见解与后续步骤")

st.markdown("""
基于对五个维度的深入分析，我们可以识别出导致严重交通事故的关键风险因素，为交通安全政策的制定提供清晰的方向。
""")

st.subheader("关键见解")

st.success(
    """
    **1. 区域风险集中：**
    * **高风险区域**（如 `Office areas` 办公区、`Residential areas` 居民区）不仅总事故数量高，而且**“机动车与机动车碰撞”**的比例明显更高，这表明这些区域在高峰时段的交通管理和流量存在不足。

    **2. 傍晚和周末风险升高：**
    * **高风险时段**集中在 **17:00 至 20:00** 之间。**“追尾”**和**“侧面碰撞”**等严重事故类型的比例在这些时段增加，表明这是驾驶员疲劳、不耐烦和弱光条件综合作用的结果。

    **3. 行为因素是严重伤亡的主要原因：**
    * **驾驶员行为**分析清晰显示，特定的行为（例如 `No distancing` 未保持安全距离、`Changing lane to the right` 向右变道）占所有事故的最大比例，并且表现出最高的**严重/致命事故比例**，证实主观行为错误是导致严重后果的最直接原因。
    * **个人特征**分析表明，最大的风险集中在 **18-30 岁**和**男性**驾驶员群体，需要有针对性的公众意识宣传和执法。

    **4. 高风险碰撞类型：**
    * **平均伤亡人数条形图**突出显示，**“翻车”**（`Overturning`）和**“与固定物体碰撞”**（`Collision with fixed objects`）具有最高的平均伤亡人数和标准差，这标志着它们是高致命性/致残风险的类型。
    * **严重程度比例堆叠条形图**证实这些类型具有最高的严重/致命结果比例。

    **5. 重点关注低学历驾驶员：**
    * **教育水平**分析显示，教育水平较低的驾驶员（例如 `Elementary school` 小学、`Junior high school` 初中）贡献了大量的事故，其严重事故比例值得关注，这可能与他们对交通法规的理解和风险判断有关。
    * **年龄-经验热力图**明确指出，**18-30 岁**且具有 **2-5 年经验**的驾驶员组合是严重事故的**主要热点**，将年轻且经验适中的驾驶员确定为干预的优先目标。
    """
)

st.subheader("后续步骤和建议")

st.markdown(
    """
    基于以上数据见解，我们建议实施以下三项有针对性的行动：
    
    1.  **🎯 针对高风险行为的执法和干预：**
        * **执法重点：** 将执法从单纯的超速限制转向**危险驾驶行为**，如**“未保持安全距离”**和**不当变道**。利用自动化监控系统专门识别和处罚这些高风险行为。
        * **道路部署：** 在高密度区域（例如办公区）安装电子监控，监测频繁发生的**追尾**和**侧面碰撞**。
        
    2.  **🏗️ 针对关键时间窗口的基础设施和意识优化：**
        * **夜间照明：** 优先修复和增加道路照明，以减轻夜间事故中**环境对风险的放大作用**。
        * **意识活动：** 交通安全宣传活动应重点关注 **17:00 - 20:00** 的时间窗口，提醒驾驶员注意疲劳和情绪对驾驶性能的影响。
        
    3.  **📚 改进驾驶员培训和教育系统：**
        * **目标培训：** 专门为 **18-30 岁、2-5 年经验**的高风险群体设计强化培训课程，以提高他们的实际风险意识。
        * **风险教育：** 将高风险碰撞类型（如**翻车**和**撞击固定物体**）后果的强制性教育纳入驾驶考试和年度审查中。
        * **基础教育：** 考虑为文化程度较低或具有特定经验范围的驾驶员提供免费或强制性的**交通规则强化课程**，以提高他们的风险识别和规避能力。
    """
)

st.markdown("---")
st.markdown("专为 #EFREIDataStoriesWUT2025 创建 | 数据可视化项目")