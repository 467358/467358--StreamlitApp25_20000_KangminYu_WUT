import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

DATA_PATH = 'RTA Dataset.csv'
ACCIDENT_SEVERITY_ORDER = ['轻微伤害', '严重伤害', '致命伤害']
CRITICAL_SEVERITY = ['严重伤害', '致命伤害']

st.set_page_config(
    page_title="道路交通事故仪表盘：多维度精细化事故分析",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data(show_spinner="正在加载和预处理数据...")
def load_data(path: str) -> pd.DataFrame:
    """加载原始数据集，清理列名并设置数据类型。"""

    df = pd.read_csv(path)

    df.columns = df.columns.str.replace('[^A-Za-z0-9_]+', '', regex=True).str.lower()

    df = df.replace(['Unknown', 'unknown', 'na', '-1', 'Other'], np.nan)

    df['time'] = pd.to_datetime(df['time'], format='%H:%M:%S', errors='coerce').dt.time
    df['hour'] = df['time'].apply(lambda x: x.hour if pd.notna(x) else np.nan)

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
    df['accident_severity'] = df['accident_severity'].map(severity_mapping).fillna(df['accident_severity'])
    df['accident_severity'] = pd.Categorical(
        df['accident_severity'], 
        categories=ACCIDENT_SEVERITY_ORDER, 
        ordered=True
    )

    df['casualty_count'] = pd.to_numeric(df['number_of_casualties'], errors='coerce')

    age_mapping = {
        'Under 18': '18岁以下',
        '18-30': '18-30岁',
        '31-50': '31-50岁',
        'Over 51': '51岁以上'
    }
    df['age_band_of_driver'] = df['age_band_of_driver'].map(age_mapping).fillna(df['age_band_of_driver'])
    AGE_BANDS = ['18岁以下', '18-30岁', '31-50岁', '51岁以上']
    df['age_band_of_driver'] = pd.Categorical(df['age_band_of_driver'], categories=AGE_BANDS, ordered=True)
    
    edu_mapping = {
        'Illiterate': '文盲',
        'Elementary school': '小学',
        'Junior high school': '初中',
        'High school graduate': '高中',
        'Above high school': '高中以上',
        'College & above': '大学及以上'
    }
    df['educational_level'] = df['educational_level'].map(edu_mapping).fillna(df['educational_level'])
    EDU_LEVELS = ['文盲', '小学', '初中', '高中', '高中以上', '大学及以上']
    df['educational_level'] = pd.Categorical(df['educational_level'], categories=EDU_LEVELS, ordered=True)
    
    df['sex_of_driver'] = df['sex_of_driver'].map({'Male': '男性', 'Female': '女性'}).fillna(df['sex_of_driver'])
    df['driving_experience'] = df['driving_experience'].map({
        'Below 1yr': '1年以下',
        '1-2yr': '1-2年',
        '2-5yr': '2-5年',
        '5-10yr': '5-10年',
        'Above 10yr': '10年以上'
    }).fillna(df['driving_experience'])
    df['weather_conditions'] = df['weather_conditions'].map({
        'Normal': '正常',
        'Raining': '下雨',
        'Snowing': '下雪',
        'Foggy': '有雾',
        'Windy': '大风'
    }).fillna(df['weather_conditions'])
    df['road_surface_type'] = df['road_surface_type'].map({
        'Asphalt roads': '沥青路',
        'Concrete roads': '水泥路',
        'Gravel roads': '碎石路',
        'Dirt roads': '土路',
        'Other': '其他'
    }).fillna(df['road_surface_type'])
    
    return df

def draw_chart(chart, title):
    """工具函数：统一图表样式和交互效果。"""
    chart = chart.properties(title=title).interactive()
    st.altair_chart(chart, use_container_width=True)

df_data = load_data(DATA_PATH)

with st.sidebar:

    st.image("微信图片_20251123203603_26_25.jpg", width=100) 
    st.image("微信图片_20251123203604_27_25.jpg", width=100) 
    st.markdown(
        '''
        <div style="line-height:1.1; font-size:14px;">
          <strong>于康敏</strong><br>
          <a href="mailto:kangmin.yu@efrei.net">kangmin.yu@efrei.net</a>
          <div style="height:6px;"></div>
          <strong>马诺·约瑟夫·马修</strong><br>
          <a href="mailto:mano.mathew@efrei.fr">mano.mathew@efrei.fr</a>
        </div>
        ''',
        unsafe_allow_html=True
    )
    st.markdown("---")
    st.markdown("**Course: Data Visualization 2025**")
    st.markdown("**Prof. Mano Mathew**")
    st.markdown("[Check out this LinkedIn](https://www.linkedin.com/in/manomathew/)", unsafe_allow_html=True)
    
    st.title("数据筛选器")
    
    st.header("1. 事故严重程度")
    selected_severity = st.multiselect(
        "关注的严重程度等级：",
        options=ACCIDENT_SEVERITY_ORDER,
        default=ACCIDENT_SEVERITY_ORDER,
        help="选择要包含在图表和关键指标中的事故严重程度。"
    )
    
    st.header("2. 地理区域筛选")
    areas = df_data['area_accident_occured'].dropna().unique().tolist()
    selected_areas = st.multiselect(
        "按事故发生区域筛选：",
        options=areas,
        default=areas
    )
    
    st.markdown("---")

df_filtered = df_data[
    (df_data['accident_severity'].isin(selected_severity)) &
    (df_data['area_accident_occured'].isin(selected_areas))
].copy()

st.title("道路交通事故仪表盘：多维度精细化分析")
st.caption("项目概述：针对埃塞俄比亚道路交通事故（RTA）数据，通过五个定制化分析维度进行可视化与深度分析。")
st.markdown("---")

st.header("1. 🚨 项目叙事：从问题到分析框架")
st.markdown("---")

st.subheader("核心问题：埃塞俄比亚道路上的沉默危机")
st.error(
    """
    道路交通事故（RTA）是全球范围内严峻的公共卫生和经济挑战，在发展中国家尤为突出。埃塞俄比亚正面临着高比例的严重事故和死亡案例。传统事故报告往往仅关注总体数量统计，缺乏制定有效政策干预所需的精细化、多维度洞察。**核心问题在于缺乏可行动的情报**——政策制定者需要明确了解*谁*、*何时*、*何地*以及*为何*会发生最危险的事故。
    """
)

st.subheader("数据解决方案：为何选择该数据集？")
st.info(
    """
    本项目选用的**埃塞俄比亚道路交通事故数据集**具有丰富的关联变量，超越了简单的时间/地点数据。它包含关键的**驾驶员特征**（年龄、教育程度、驾驶经验）、**环境因素**（天气、路面状况）、**行为原因**（事故成因）以及详细的**严重程度**结果。这使得分析能够从简单的计数转变为**因果关系和预测性分析**。

    项目通过五个分析维度将原始数据转化为有针对性的洞察（分析阶段）：
    
    * **地理风险：** 高风险区域在哪里？
    * **时间模式：** 高风险时段/日期是什么时候？
    * **成因因素：** 哪些驾驶员行为和条件会导致事故？
    * **碰撞机制：** 哪些碰撞类型最具致命性？
    * **驾驶员人口统计：** 哪些驾驶员群体最脆弱或最具风险？
    """
)
st.markdown("---")

col1, col2, col3 = st.columns(3)
col1.metric("筛选后总事故数", f"{len(df_filtered):,}")
col2.metric("平均每起事故伤亡人数", f"{df_filtered['casualty_count'].mean():.2f}")
critical_rate = (len(df_filtered[df_filtered['accident_severity'].isin(CRITICAL_SEVERITY)]) / len(df_filtered) * 100) if len(df_filtered) > 0 else 0
col3.metric("严重/致命事故率", f"{critical_rate:.1f}%")

st.markdown("---")

st.header("2. 🗺️ 地理区域事故对比分析 ")
st.info("分析目标：识别高风险地理区域，并分析其主要碰撞特征。")
col1, col2 = st.columns(2)

with col1:
    st.subheader("各区域事故严重程度分布")
    area_agg_severity = df_filtered.groupby(['area_accident_occured', 'accident_severity'], observed=True).size().reset_index(name='事故数量')
    
    chart = alt.Chart(area_agg_severity).mark_circle(opacity=0.8).encode(
        x=alt.X('accident_severity', title='事故严重程度', sort=ACCIDENT_SEVERITY_ORDER),
        y=alt.Y('area_accident_occured', title='事故发生区域', sort=alt.EncodingSortField(field='事故数量', op='sum', order='descending')),
        size=alt.Size('事故数量', title='事故数量', scale=alt.Scale(range=[50, 600])),
        color=alt.Color('accident_severity', scale=alt.Scale(domain=ACCIDENT_SEVERITY_ORDER, range=['#4C78A8', '#E34C31', '#943E2C']), title='严重程度'),
        tooltip=['area_accident_occured', 'accident_severity', '事故数量']
    ).properties(title="区域事故严重程度分布")
    draw_chart(chart, "区域事故严重程度分布")

with col2:
    st.subheader("各区域主要碰撞类型分布")
    area_collision_agg = df_filtered.groupby(['area_accident_occured', 'type_of_collision'], observed=True).size().reset_index(name='事故数量')
    
    chart = alt.Chart(area_collision_agg).mark_bar().encode(
        x=alt.X('事故数量', stack="normalize", title='碰撞类型占比'),
        y=alt.Y('area_accident_occured', title='事故发生区域', sort=alt.EncodingSortField(field='事故数量', op='sum', order='descending')),
        color=alt.Color('type_of_collision', title='碰撞类型', scale=alt.Scale(scheme='category10')),
        tooltip=['area_accident_occured', 'type_of_collision', alt.Tooltip('事故数量', format=',')]
    ).properties(title="区域碰撞类型占比分布")
    draw_chart(chart, "各区域主要碰撞类型分布")

st.markdown("---")

st.header("3. ⏱️ 事故时间模式分析")
st.info("分析目标：确定一天中的高风险时间段，并观察碰撞类型的时间变化规律。")
col1, col2 = st.columns(2)
with col1:
    st.subheader("每小时事故数量及严重程度趋势")
    time_severity_agg = df_filtered.groupby(['hour', 'accident_severity'], observed=True).size().reset_index(name='事故数量')
    
    chart = alt.Chart(time_severity_agg).mark_line(point=True).encode(
        x=alt.X('hour', title='一天中的小时'),
        y=alt.Y('事故数量', title='事故数量'),
        color=alt.Color('accident_severity', scale=alt.Scale(domain=ACCIDENT_SEVERITY_ORDER, range=['#4C78A8', '#E34C31', '#943E2C']), title='严重程度'),
        tooltip=['hour', 'accident_severity', '事故数量']
    ).properties(title="按小时和严重程度划分的事故趋势")
    draw_chart(chart, "每小时事故数量及严重程度趋势")

with col2:
    st.subheader("不同时段碰撞类型分布")
    time_collision_agg = df_filtered.groupby(['hour', 'type_of_collision'], observed=True).size().reset_index(name='事故数量')
    
    top_collisions = time_collision_agg.groupby('type_of_collision')['事故数量'].sum().nlargest(5).index.tolist()
    time_collision_agg = time_collision_agg[time_collision_agg['type_of_collision'].isin(top_collisions)]

    chart = alt.Chart(time_collision_agg).mark_bar().encode(
        x=alt.X('type_of_collision', title='碰撞类型'),
        y=alt.Y('事故数量', title='事故数量'),
        column=alt.Column('hour', header=alt.Header(titleOrient="bottom"), title='小时'),
        color=alt.Color('type_of_collision', title='碰撞类型', scale=alt.Scale(scheme='category10')),
        tooltip=['hour', 'type_of_collision', '事故数量']
    ).properties(title="按小时划分的碰撞类型分布（前5类）")
    draw_chart(chart, "不同时段碰撞类型分布")
    
st.markdown("---")

st.header("4. 📊 事故影响因素分析")
st.info("分析目标：考察驾驶员个人因素、环境条件（天气/路面）和驾驶行为对事故频率和严重程度的影响。")
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("驾驶员个人特征与严重事故数量")
    
    df_severe = df_filtered[df_filtered['accident_severity'].isin(CRITICAL_SEVERITY)].copy()
    
    st.markdown("##### 按年龄组统计的严重事故数量")
    age_agg = df_severe.groupby('age_band_of_driver', observed=True).size().reset_index(name='严重事故数量')
    chart_age = alt.Chart(age_agg).mark_bar(color='#E34C31').encode(
        x=alt.X('严重事故数量', title='严重/致命事故数量'),
        y=alt.Y('age_band_of_driver', title='年龄组', sort=None),
        tooltip=['age_band_of_driver', '严重事故数量']
    )
    draw_chart(chart_age, "按年龄组统计的严重事故数量")

    st.markdown("##### 按驾驶经验统计的严重事故数量")
    exp_agg = df_severe.groupby('driving_experience', observed=True).size().reset_index(name='严重事故数量')
    chart_exp = alt.Chart(exp_agg).mark_bar(color='#CC6633').encode(
        x=alt.X('严重事故数量', title='严重/致命事故数量'),
        y=alt.Y('driving_experience', title='驾驶经验', sort=None),
        tooltip=['driving_experience', '严重事故数量']
    )
    draw_chart(chart_exp, "按驾驶经验统计的严重事故数量")
    
    st.markdown("##### 按性别统计的严重事故数量")
    sex_agg = df_severe.groupby('sex_of_driver', observed=True).size().reset_index(name='严重事故数量')
    chart_sex = alt.Chart(sex_agg).mark_bar(color='#943E2C').encode(
        x=alt.X('严重事故数量', title='严重/致命事故数量'),
        y=alt.Y('sex_of_driver', title='驾驶员性别', sort=None),
        tooltip=['sex_of_driver', '严重事故数量']
    )
    draw_chart(chart_sex, "按性别统计的严重事故数量")

with col2:
    st.subheader("天气与路面条件组合的影响")
    weather_surface_agg = df_filtered.groupby(['weather_conditions', 'road_surface_type'], observed=True).size().reset_index(name='事故数量')
    
    chart = alt.Chart(weather_surface_agg).mark_rect().encode(
        x=alt.X('road_surface_type', title='路面类型'),
        y=alt.Y('weather_conditions', title='天气条件'),
        color=alt.Color('事故数量', scale=alt.Scale(range='heatmap'), title='事故数量'),
        tooltip=['road_surface_type', 'weather_conditions', '事故数量']
    ).properties(title="事故热力图：天气 vs 路面条件")
    draw_chart(chart, "天气与路面条件组合的影响")

with col3:
    st.subheader("驾驶员行为与事故严重程度占比")
    
    behavior_severity_agg = df_filtered.groupby(['cause_of_accident', 'accident_severity'], observed=True).size().reset_index(name='事故数量')
    
    total_by_cause = behavior_severity_agg.groupby('cause_of_accident')['事故数量'].sum()
    top_10_causes = total_by_cause.nlargest(10).index.tolist()
    
    behavior_severity_agg = behavior_severity_agg[behavior_severity_agg['cause_of_accident'].isin(top_10_causes)].copy()

    chart = alt.Chart(behavior_severity_agg).mark_bar().encode(
        x=alt.X('事故数量', stack="normalize", title='事故严重程度占比'),
        y=alt.Y('cause_of_accident', title='驾驶员行为（前10大成因）', 
                sort=alt.EncodingSortField(field='事故数量', op='sum', order='descending')),
        color=alt.Color('accident_severity', scale=alt.Scale(domain=ACCIDENT_SEVERITY_ORDER, range=['#4C78A8', '#E34C31', '#943E2C']), title='严重程度'),
        tooltip=['cause_of_accident', 'accident_severity', alt.Tooltip('事故数量', format=',')]
    ).properties(title="按驾驶员行为划分的事故严重程度占比")
    draw_chart(chart, "驾驶员行为与事故严重程度占比")

st.markdown("---")

st.header("5. 💥 碰撞类型与伤亡人数关系分析")
st.info("分析目标：量化不同碰撞类型（type_of_collision）的发生频率、严重程度和伤亡影响。")
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("碰撞类型发生频率（前5类）")
    collision_counts = df_filtered['type_of_collision'].value_counts().head(5).reset_index(name='数量')
    collision_counts.columns = ['type_of_collision', '数量']
    
    chart = alt.Chart(collision_counts).mark_arc(outerRadius=120).encode(
        theta=alt.Theta(field="数量", type="quantitative"),
        color=alt.Color(field="type_of_collision", type="nominal", title='碰撞类型', scale=alt.Scale(scheme='category10')),
        order=alt.Order("数量", sort="descending"),
        tooltip=['type_of_collision', alt.Tooltip('数量', format=',')]
    ).properties(title="前5类碰撞类型占比")
    draw_chart(chart, "碰撞类型发生频率")

with col2:
    st.subheader("碰撞类型与事故严重程度占比")
    collision_severity_agg = df_filtered.groupby(['type_of_collision', 'accident_severity'], observed=True).size().reset_index(name='事故数量')
    
    chart = alt.Chart(collision_severity_agg).mark_bar().encode(
        x=alt.X('事故数量', stack="normalize", title='事故占比'),
        y=alt.Y('type_of_collision', title='碰撞类型', sort=alt.EncodingSortField(field='事故数量', op='sum', order='descending')),
        color=alt.Color('accident_severity', scale=alt.Scale(domain=ACCIDENT_SEVERITY_ORDER, range=['#4C78A8', '#E34C31', '#943E2C']), title='严重程度'),
        tooltip=['type_of_collision', 'accident_severity', alt.Tooltip('事故数量', format=',')]
    ).properties(title="碰撞类型与严重程度占比")
    draw_chart(chart, "碰撞类型与事故严重程度占比")

with col3:
    st.subheader("碰撞类型对平均伤亡人数的影响")
    
    casualty_agg = df_filtered.groupby('type_of_collision', observed=True)['casualty_count'].agg(
        平均值='mean',
        标准差='std'
    ).reset_index()
    
    casualty_agg['下限'] = casualty_agg['平均值'] - casualty_agg['标准差']
    casualty_agg['上限'] = casualty_agg['平均值'] + casualty_agg['标准差']
    casualty_agg['下限'] = casualty_agg['下限'].apply(lambda x: max(0, x))

    bar = alt.Chart(casualty_agg).mark_bar(color='#4C78A8').encode(
        y=alt.Y('type_of_collision', title='碰撞类型', sort='-x'),
        x=alt.X('平均值', title='平均伤亡人数'),
        tooltip=['type_of_collision', alt.Tooltip('平均值', format='.2f', title='平均伤亡人数'), alt.Tooltip('标准差', format='.2f', title='标准差')]
    ).properties(title="碰撞类型与平均伤亡人数")

    error_bars = alt.Chart(casualty_agg).mark_rule().encode(
        y=alt.Y('type_of_collision', title='碰撞类型'),
        x=alt.X('下限', title=''),
        x2='上限'
    )
    
    chart = bar + error_bars
    draw_chart(chart, "碰撞类型对平均伤亡人数的影响（均值+标准差）")

st.markdown("---")

st.header("6. 👤 驾驶员特征与事故严重程度相关性")
st.info("分析目标：探索驾驶员特征（如年龄、教育程度）与事故严重程度之间的复杂关系。")
col1, col2 = st.columns(2)

with col1:
    st.subheader("教育程度与事故严重程度占比")
    edu_severity_agg = df_filtered.groupby(['educational_level', 'accident_severity'], observed=True).size().reset_index(name='事故数量')
    
    chart = alt.Chart(edu_severity_agg).mark_bar().encode(
        x=alt.X('educational_level', title='教育程度', sort=None), 
        y=alt.Y('事故数量', stack="normalize", title='事故占比'),
        color=alt.Color('accident_severity', scale=alt.Scale(domain=ACCIDENT_SEVERITY_ORDER, range=['#4C78A8', '#E34C31', '#943E2C']), title='严重程度'),
        tooltip=['educational_level', 'accident_severity', alt.Tooltip('事故数量', format=',')]
    ).properties(title="教育程度与事故严重程度占比")
    draw_chart(chart, "教育程度与事故严重程度占比")

with col2:
    st.subheader("驾驶员年龄、经验与严重事故关系")

    df_severe = df_filtered[df_filtered['accident_severity'].isin(CRITICAL_SEVERITY)].copy()

    age_exp_agg = df_severe.groupby(['driving_experience', 'age_band_of_driver'], observed=True).size().reset_index(name='严重事故数量')

    chart = alt.Chart(age_exp_agg).mark_rect().encode(
        x=alt.X('driving_experience', title='驾驶经验', sort=None),
        y=alt.Y('age_band_of_driver', title='年龄组', sort=None),
        color=alt.Color('严重事故数量', scale=alt.Scale(range='heatmap'), title='严重事故数量'),
        tooltip=['age_band_of_driver', 'driving_experience', '严重事故数量']
    ).properties(title="驾驶经验 vs 年龄组 严重事故热力图")
    draw_chart(chart, "驾驶员年龄、经验与严重事故关系")

st.markdown("---")

st.header("数据质量与缺失值报告")
st.info("缺失值、重复项和简单验证检查摘要。使用分析结果前请参考本部分内容。")

missing = df_data.isna().sum().reset_index()
missing.columns = ['字段名', '缺失数量']
missing['缺失比例(%)'] = (missing['缺失数量'] / len(df_data) * 100).round(2)
missing = missing.sort_values('缺失比例(%)', ascending=False)

st.subheader("各字段缺失值统计")
st.write(f"数据集总行数：{len(df_data):,}")
st.table(missing)

top_missing = missing[missing['缺失数量'] > 0].head(20)
if not top_missing.empty:
    chart = alt.Chart(top_missing).mark_bar(color='#CC6666').encode(
        x=alt.X('缺失比例(%)', title='缺失比例(%)'),
        y=alt.Y('字段名', sort=alt.SortField('缺失比例(%)', order='descending')),
        tooltip=[alt.Tooltip('缺失数量', title='缺失数量'), alt.Tooltip('缺失比例(%)', title='缺失比例(%)')]
    ).properties(height=400)
    draw_chart(chart, "缺失比例最高的20个字段")
else:
    st.success("数据集中未检测到缺失值。")

dup_count = df_data.duplicated().sum()
st.subheader("重复行检查")
st.write(f"检测到的重复行数：{dup_count}")
if dup_count > 0:
    st.write("重复行预览：")
    st.dataframe(df_data[df_data.duplicated()].head(5))

st.subheader("行级缺失值分布")
row_missing = df_data.isna().sum(axis=1).value_counts().reset_index()
row_missing.columns = ['缺失字段数', '行数']
row_missing = row_missing.sort_values('缺失字段数')
st.bar_chart(row_missing.set_index('缺失字段数'))

st.markdown("---")

st.header("7. 💡 核心洞察与后续行动建议")

st.markdown("""
基于五个维度的深入分析，我们识别出导致严重交通事故的关键风险因素，为交通安全政策制定提供明确方向。
""")

st.subheader("核心洞察")

st.success(
    """
    **1. 区域风险集中化：**
    * **高风险区域**（办公区、居民区）不仅事故总量高，且**'车辆与车辆碰撞'** 占比显著更高，表明这些区域在高峰时段的交通管理和车流疏导存在不足。

    **2. 傍晚和周末风险升高：**
    * **高风险时段**集中在**17:00-20:00**（傍晚）。此时间段内，**'追尾'** 和**'侧面碰撞'** 等严重事故类型占比上升，反映出驾驶员疲劳、急躁情绪和光线不足的综合影响。

    **3. 行为因素是严重伤亡的主要诱因：**
    * 驾驶员行为分析明确显示，特定行为（如`未保持安全距离`、`违规向右变道`）不仅占所有事故的比例最大，且**严重/致命事故占比最高**，证实主观行为失误是导致严重后果的最直接原因。
    * 个人特征分析表明，**18-30岁**和**男性**驾驶员是风险最高的群体，需要针对性的公众意识宣传和执法干预。

    **4. 高风险碰撞类型：**
    * 平均伤亡人数柱状图显示，**'翻车'** 和**'与固定物体碰撞'** 的平均伤亡人数和标准差最高，是导致死亡/残疾的高风险类型。
    * 严重程度占比堆叠图进一步证实，这些类型的严重/致命事故占比最高。

    **5. 低教育水平驾驶员需重点关注：**
    * 教育水平分析显示，低教育水平驾驶员（如`小学`、`初中`学历）的事故数量较多，且严重事故占比值得关注，这可能与交通法规理解和风险判断能力相关。
    * 年龄-经验热力图明确识别出**18-30岁**且具有**2-5年驾驶经验**的驾驶员组合是**严重事故的主要热点**，将年轻且有一定经验的驾驶员列为干预优先级目标。
    """
)

st.subheader("后续行动与建议")

st.markdown(
    """
    基于上述数据洞察，我们建议实施以下三项针对性行动：
    
    1.  **🎯 高风险行为的执法与干预：**
        * **执法重点：** 将执法重心从单纯的限速转向**危险驾驶行为**，如**`未保持安全距离`** 和**违规变道**。利用自动化监控系统专门识别和处罚这些高风险行为。
        * **道路部署：** 在高密度区域（如办公区）安装电子监控，重点监测频繁发生的**追尾**和**侧面碰撞**事故。
        
    2.  **🏗️ 关键时间段的基础设施与意识优化：**
        * **夜间照明：** 优先修复和增设道路照明设施，减轻夜间事故中**环境因素对风险的放大效应**。
        * **意识宣传：** 交通安全宣传应聚焦**17:00-20:00**时段，提醒驾驶员注意疲劳和情绪对驾驶表现的影响。
        
    3.  **📚 驾驶员培训与教育体系完善：**
        * **针对性培训：** 为**18-30岁、驾驶经验2-5年**的高风险群体设计强化培训课程，提升其实际风险意识。
        * **风险教育：** 将高风险碰撞类型（如**翻车**、**撞击固定物体**）的后果教育纳入驾照考试和年度审核的必备内容。
        * **基础教育：** 考虑为低教育背景或特定经验范围的驾驶员提供免费或强制性的**交通法规强化课程**，提升其风险识别和规避能力。
    """
)

st.markdown("---")
st.markdown("为 #EFREIDataStoriesWUT2025 项目创建 | 数据可视化项目")