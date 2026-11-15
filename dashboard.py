import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


st.set_page_config(
    page_title="Bike Sharing Analysis",
    page_icon="🚲",
    layout="wide"
)

PURPLE = "#8B5CF6"
LAVENDER = "#C4B5FD"
PINK = "#F472B6"
BLUE = "#7C9CFF"
PEACH = "#FDBA74"
YELLOW = "#FCD34D"
DARK = "#2B2A4C"
MUTED = "#7A789B"
BORDER = "#ECE8FA"

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(180deg, #F6F4FF 0%, #FBF5FB 100%);
    }

    .block-container {
        padding-top: 5rem;
        max-width: 1280px;
    }

    h1, h2, h3, h4 {
        color: #2B2A4C;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #ECE8FA;
    }

    /* Judul utama */
    .hero-title {
        font-size: 2.6rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        line-height: 1.35;
        margin: 0;
        padding: 0.2rem 0 0.3rem 0;
        overflow: visible;
    }

    .hero-title .grad {
        display: inline-block;
        padding-bottom: 0.15em;
        background: linear-gradient(90deg, #4C1D95 0%, #8B5CF6 55%, #F472B6 100%);
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
        color: transparent;
    }

    .subtitle {
        color: #7A789B;
        font-size: 15px;
        margin-top: 4px;
    }

    /* Kartu ringkasan */
    .stat-card {
        display: flex;
        align-items: center;
        gap: 16px;
        background: linear-gradient(135deg, #FFFFFF 0%, #F8F5FF 100%);
        border: 1px solid #ECE8FA;
        border-radius: 18px;
        padding: 18px 20px;
        box-shadow: 0 6px 18px rgba(139, 92, 246, 0.08);
    }

    .stat-icon {
        width: 52px;
        height: 52px;
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        flex-shrink: 0;
    }

    .stat-label {
        color: #7A789B;
        font-size: 13px;
        margin: 0;
    }

    .stat-value {
        color: #2B2A4C;
        font-size: 26px;
        font-weight: 800;
        margin: 0;
        line-height: 1.2;
    }

    /* Judul section */
    .section-head {
        margin: 6px 0 2px 0;
    }

    .section-head h2 {
        font-size: 1.5rem;
        font-weight: 800;
        margin: 0;
        padding: 0;
    }

    .section-desc {
        color: #7A789B;
        font-size: 14px;
        margin: 2px 0 14px 0;
    }

    /* Kartu grafik */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #FFFFFF;
        border: 1px solid #ECE8FA !important;
        border-radius: 18px !important;
        box-shadow: 0 6px 18px rgba(139, 92, 246, 0.07);
    }

    /* Insight */
    .insight {
        background: linear-gradient(90deg, #F3EEFF 0%, #FFF1F8 100%);
        border-left: 5px solid #8B5CF6;
        padding: 14px 18px;
        border-radius: 12px;
        margin: 14px 0 18px 0;
        color: #2B2A4C;
    }

    /* Rekomendasi */
    .reco-card {
        background: #FFFFFF;
        border: 1px solid #ECE8FA;
        border-radius: 18px;
        padding: 18px 20px;
        height: 100%;
        box-shadow: 0 6px 18px rgba(139, 92, 246, 0.07);
    }

    .reco-card h4 {
        margin: 0 0 6px 0;
        font-size: 1rem;
    }

    .reco-card p {
        color: #7A789B;
        font-size: 14px;
        margin: 0;
    }

    .reco-badge {
        display: inline-flex;
        width: 30px;
        height: 30px;
        align-items: center;
        justify-content: center;
        border-radius: 10px;
        font-weight: 800;
        color: #FFFFFF;
        margin-bottom: 10px;
    }

    div[data-testid="stAlert"] {
        border-radius: 12px;
    }

    hr {
        border-color: #ECE8FA !important;
    }
</style>
""", unsafe_allow_html=True)



@st.cache_data
def load_data():
    day_df = pd.read_csv("data/day.csv")
    hour_df = pd.read_csv("data/hour.csv")

    day_df["dteday"] = pd.to_datetime(day_df["dteday"])
    hour_df["dteday"] = pd.to_datetime(hour_df["dteday"])

    return day_df, hour_df


try:
    day_df, hour_df = load_data()
except FileNotFoundError:
    st.error(
        "Dataset tidak ditemukan. Pastikan day.csv dan hour.csv "
        "berada di dalam folder data."
    )
    st.stop()


st.markdown(
    '<p class="hero-title">🚲 <span class="grad">Bike Sharing Analysis Dashboard</span></p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="subtitle">Analisis pola penyewaan sepeda '
    'berdasarkan waktu, hari, musim, dan kondisi cuaca '
    'pada periode 2011–2012.</p>',
    unsafe_allow_html=True
)

st.divider()


st.sidebar.title("⚙️ Filter Dashboard")
st.sidebar.markdown("Pilih periode analisis yang ingin ditampilkan.")

min_date = day_df["dteday"].min().date()
max_date = day_df["dteday"].max().date()

selected_dates = st.sidebar.date_input(
    "Rentang tanggal",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if len(selected_dates) == 2:
    start_date, end_date = selected_dates
else:
    start_date = selected_dates[0]
    end_date = selected_dates[0]

start_date = pd.Timestamp(start_date)
end_date = pd.Timestamp(end_date)

filtered_day = day_df[
    (day_df["dteday"] >= start_date) &
    (day_df["dteday"] <= end_date)
].copy()

filtered_hour = hour_df[
    (hour_df["dteday"] >= start_date) &
    (hour_df["dteday"] <= end_date)
].copy()

if filtered_day.empty or filtered_hour.empty:
    st.warning("Tidak ada data pada rentang tanggal yang dipilih.")
    st.stop()


def section_header(title, description):
    st.markdown(
        f"""
        <div class="section-head"><h2>{title}</h2></div>
        <p class="section-desc">{description}</p>
        """,
        unsafe_allow_html=True
    )


def stat_card(icon, label, value, bg):
    return f"""
    <div class="stat-card">
        <div class="stat-icon" style="background:{bg};">{icon}</div>
        <div>
            <p class="stat-label">{label}</p>
            <p class="stat-value">{value}</p>
        </div>
    </div>
    """


def style_axis(ax):
    ax.set_facecolor("#FFFFFF")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(BORDER)
    ax.spines["bottom"].set_color(BORDER)
    ax.tick_params(colors=MUTED)
    ax.xaxis.label.set_color(MUTED)
    ax.yaxis.label.set_color(MUTED)
    ax.grid(axis="y", linestyle="--", alpha=0.35, color=BORDER)
    ax.set_axisbelow(True)


st.subheader("📊 Ringkasan Penyewaan Sepeda")

total_rentals = filtered_day["cnt"].sum()
average_daily = filtered_day["cnt"].mean()
total_days = len(filtered_day)

col1, col2, col3 = st.columns(3)

col1.markdown(
    stat_card("🚲", "Total Penyewaan", f"{total_rentals:,.0f}", "#EDE7FF"),
    unsafe_allow_html=True
)

col2.markdown(
    stat_card("📈", "Rata-rata Penyewaan Harian", f"{average_daily:,.0f}", "#FFE4F1"),
    unsafe_allow_html=True
)

col3.markdown(
    stat_card("🗓️", "Jumlah Hari Pengamatan", f"{total_days:,} hari", "#E3ECFF"),
    unsafe_allow_html=True
)

st.caption(
    f"Periode yang dianalisis: "
    f"{start_date.strftime('%d %B %Y')} – "
    f"{end_date.strftime('%d %B %Y')}"
)

st.divider()


section_header(
    "01. Pola Penyewaan Bulanan dan Musiman",
    "Analisis ini bertujuan mengetahui perubahan rata-rata "
    "penyewaan sepeda berdasarkan bulan dan musim."
)

month_names = {
    1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr",
    5: "Mei", 6: "Jun", 7: "Jul", 8: "Agu",
    9: "Sep", 10: "Okt", 11: "Nov", 12: "Des"
}

season_names = {
    1: "Spring",
    2: "Summer",
    3: "Fall",
    4: "Winter"
}

monthly_avg = (
    filtered_day.groupby("mnth")["cnt"]
    .mean()
    .reindex(range(1, 13))
    .dropna()
)

seasonal_avg = (
    filtered_day.groupby("season")["cnt"]
    .mean()
    .reindex(range(1, 5))
    .dropna()
)

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.subheader("Rata-rata Penyewaan per Bulan")

        fig, ax = plt.subplots(figsize=(8, 4))

        labels = [month_names[int(m)] for m in monthly_avg.index]
        
        bar_colors = [
            PINK if v == monthly_avg.max() else LAVENDER
            for v in monthly_avg.values
        ]
        bars = ax.bar(labels, monthly_avg.values, color=bar_colors, width=0.65)

        ax.set_xlabel("Bulan")
        ax.set_ylabel("Rata-rata Penyewaan")
        ax.set_title("Monthly Rental Trends", color=DARK, pad=15, loc="left")

        style_axis(ax)
        ax.bar_label(bars, fmt="%.0f", padding=3, fontsize=8, color=DARK)

        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

with col2:
    with st.container(border=True):
        st.subheader("Rata-rata Penyewaan per Musim")

        fig, ax = plt.subplots(figsize=(8, 4))

        labels = [
            season_names[int(s)] for s in seasonal_avg.index
        ]

        bars = ax.bar(
            labels,
            seasonal_avg.values,
            color=[PURPLE, PINK, PEACH, BLUE][:len(labels)],
            width=0.55
        )

        ax.set_xlabel("Musim")
        ax.set_ylabel("Rata-rata Penyewaan")
        ax.set_title("Seasonal Rental Trends", color=DARK, pad=15, loc="left")

        style_axis(ax)
        ax.bar_label(bars, fmt="%.0f", padding=3, fontsize=8, color=DARK)

        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

if not monthly_avg.empty and not seasonal_avg.empty:
    highest_month = int(monthly_avg.idxmax())
    highest_season = int(seasonal_avg.idxmax())

    st.markdown(
        f"""
        <div class="insight">
        <b>💡 Insight:</b><br>
        Rata-rata penyewaan tertinggi berdasarkan bulan terjadi
        pada <b>{month_names[highest_month]}</b>, yaitu
        <b>{monthly_avg.max():,.2f}</b> penyewaan per hari.
        Sementara itu, musim dengan rata-rata penyewaan tertinggi
        adalah <b>{season_names[highest_season]}</b>, sebesar
        <b>{seasonal_avg.max():,.2f}</b> penyewaan per hari.
        </div>
        """,
        unsafe_allow_html=True
    )

st.divider()


section_header(
    "02. Pola Penyewaan Berdasarkan Jam",
    "Analisis ini membandingkan rata-rata jumlah penyewaan "
    "pada setiap jam antara hari kerja dan hari non-kerja."
)

hourly_avg = (
    filtered_hour.groupby(["hr", "workingday"])["cnt"]
    .mean()
    .unstack()
)

hourly_avg = hourly_avg.reindex(range(24))

with st.container(border=True):
    fig, ax = plt.subplots(figsize=(12, 5))

    if 1 in hourly_avg.columns:
        ax.plot(
            hourly_avg.index,
            hourly_avg[1],
            marker="o",
            markersize=5,
            linewidth=2.5,
            color=PURPLE,
            label="Hari Kerja"
        )
        ax.fill_between(
            hourly_avg.index, hourly_avg[1].fillna(0),
            color=PURPLE, alpha=0.12
        )

    if 0 in hourly_avg.columns:
        ax.plot(
            hourly_avg.index,
            hourly_avg[0],
            marker="o",
            markersize=5,
            linewidth=2.5,
            color=PINK,
            label="Hari Non-Kerja"
        )
        ax.fill_between(
            hourly_avg.index, hourly_avg[0].fillna(0),
            color=PINK, alpha=0.12
        )

    ax.set_title("Hourly Rental Patterns", color=DARK, pad=15, loc="left")
    ax.set_xlabel("Jam")
    ax.set_ylabel("Rata-rata Penyewaan")
    ax.set_xticks(range(24))
    ax.set_xticklabels([f"{h:02d}:00" for h in range(24)], rotation=45)

    style_axis(ax)
    ax.legend(frameon=False, labelcolor=DARK)

    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

peak_workday = None
peak_nonworkday = None

if 1 in hourly_avg.columns and hourly_avg[1].notna().any():
    peak_workday = int(hourly_avg[1].idxmax())
    workday_peak_value = hourly_avg[1].max()

if 0 in hourly_avg.columns and hourly_avg[0].notna().any():
    peak_nonworkday = int(hourly_avg[0].idxmax())
    nonworkday_peak_value = hourly_avg[0].max()

insight_hour = "<div class='insight'><b>💡 Insight:</b><br>"

if peak_workday is not None:
    insight_hour += (
        f"Jam puncak pada hari kerja adalah "
        f"<b>{peak_workday:02d}:00</b>, dengan rata-rata "
        f"<b>{workday_peak_value:,.2f}</b> penyewaan.<br>"
    )

if peak_nonworkday is not None:
    insight_hour += (
        f"Jam puncak pada hari non-kerja adalah "
        f"<b>{peak_nonworkday:02d}:00</b>, dengan rata-rata "
        f"<b>{nonworkday_peak_value:,.2f}</b> penyewaan."
    )

insight_hour += "</div>"

st.markdown(insight_hour, unsafe_allow_html=True)

st.divider()


section_header(
    "03. Pola Penyewaan Berdasarkan Cuaca",
    "Analisis ini melihat perbedaan rata-rata penyewaan "
    "sepeda pada berbagai kondisi cuaca."
)

weather_names = {
    1: "Cerah / Sedikit Berawan",
    2: "Berkabut / Berawan",
    3: "Hujan atau Salju Ringan",
    4: "Hujan atau Salju Lebat"
}

weather_avg = (
    filtered_day.groupby("weathersit")["cnt"]
    .mean()
    .sort_index()
)

weather_labels = [
    weather_names.get(int(w), f"Kategori {w}")
    for w in weather_avg.index
]

weather_colors = [PURPLE, BLUE, PINK, PEACH]

with st.container(border=True):
    fig, ax = plt.subplots(figsize=(10, 4))

    bars = ax.bar(
        weather_labels,
        weather_avg.values,
        color=weather_colors[:len(weather_avg)],
        width=0.55
    )

    ax.set_title("Average Rentals by Weather Condition", color=DARK, pad=15, loc="left")
    ax.set_xlabel("Kondisi Cuaca")
    ax.set_ylabel("Rata-rata Penyewaan")
    ax.tick_params(axis="x", rotation=15)

    style_axis(ax)
    ax.bar_label(bars, fmt="%.0f", padding=3, color=DARK)

    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

if not weather_avg.empty:
    best_weather = int(weather_avg.idxmax())
    lowest_weather = int(weather_avg.idxmin())

    st.markdown(
        f"""
        <div class="insight">
        <b>💡 Insight:</b><br>
        Rata-rata penyewaan tertinggi terjadi pada kondisi
        <b>{weather_names.get(best_weather, best_weather)}</b>,
        sebesar <b>{weather_avg.max():,.2f}</b> penyewaan.
        Rata-rata terendah terjadi pada kondisi
        <b>{weather_names.get(lowest_weather, lowest_weather)}</b>,
        sebesar <b>{weather_avg.min():,.2f}</b> penyewaan.
        </div>
        """,
        unsafe_allow_html=True
    )

st.divider()


section_header(
    "04. Analisis Lanjutan: Tingkat Permintaan",
    "Teknik <b>binning</b> mengelompokkan jumlah penyewaan harian "
    "menjadi tiga tingkat permintaan (rendah, sedang, tinggi) "
    "menggunakan pembagian tertil (<i>tertiles</i>), sehingga setiap "
    "kelompok mewakili bagian distribusi data yang relatif seimbang."
)

MIN_DAYS_FOR_BINNING = 3

if len(filtered_day) >= MIN_DAYS_FOR_BINNING:
    demand_df = filtered_day[["dteday", "cnt"]].copy()

    demand_df["demand_level"] = pd.qcut(
        demand_df["cnt"].rank(method="first"),
        q=3,
        labels=["Rendah", "Sedang", "Tinggi"]
    )

    demand_order = ["Rendah", "Sedang", "Tinggi"]

    demand_counts = (
        demand_df["demand_level"]
        .value_counts()
        .reindex(demand_order, fill_value=0)
    )

    demand_ranges = (
        demand_df.groupby("demand_level", observed=True)["cnt"]
        .agg(["min", "max", "mean"])
        .reindex(demand_order)
    )

    col1, col2 = st.columns([1, 1])

    with col1:
        with st.container(border=True):
            st.subheader("Distribusi Tingkat Permintaan")

            fig, ax = plt.subplots(figsize=(7, 4))

            bars = ax.bar(
                demand_counts.index,
                demand_counts.values,
                color=[BLUE, PURPLE, PINK],
                width=0.55
            )

            ax.set_ylabel("Jumlah Hari")
            ax.set_title("Demand Level Distribution", color=DARK, pad=15, loc="left")

            style_axis(ax)
            ax.bar_label(bars, padding=3, color=DARK)

            fig.tight_layout()
            st.pyplot(fig)
            plt.close(fig)

    with col2:
        with st.container(border=True):
            st.subheader("Rentang Jumlah Penyewaan")

            display_ranges = demand_ranges.copy()
            display_ranges.columns = [
                "Minimum Penyewaan",
                "Maksimum Penyewaan",
                "Rata-rata Penyewaan"
            ]

            st.dataframe(
                display_ranges.style.format("{:,.0f}"),
                use_container_width=True
            )

    st.markdown(
        """
        <div class="insight">
        <b>💡 Insight:</b><br>
        Binning membantu mengidentifikasi hari dengan permintaan
        rendah, sedang, dan tinggi. Hasil pengelompokan dapat
        digunakan sebagai dasar perencanaan ketersediaan dan
        redistribusi sepeda.
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.info(
        f"Analisis tingkat permintaan membutuhkan minimal "
        f"{MIN_DAYS_FOR_BINNING} hari data, sedangkan rentang tanggal "
        f"yang dipilih hanya berisi {len(filtered_day)} hari. "
        f"Perluas rentang tanggal pada filter di sidebar "
        f"untuk menampilkan analisis ini.",
        icon="ℹ️"
    )

st.divider()

section_header(
    "💡 Rekomendasi Bisnis",
    "Berdasarkan hasil analisis, berikut beberapa rekomendasi "
    "yang dapat dipertimbangkan oleh pengelola layanan penyewaan sepeda."
)

recommendations = [
    (
        "Perencanaan berdasarkan bulan dan musim",
        "Pengelola dapat menyesuaikan ketersediaan sepeda dan "
        "kebutuhan operasional berdasarkan periode dengan rata-rata "
        "penyewaan tinggi.",
        PURPLE
    ),
    (
        "Redistribusi sepeda berdasarkan jam",
        "Pengelola dapat menyesuaikan distribusi sepeda dengan "
        "pola permintaan pada jam sibuk hari kerja dan hari non-kerja.",
        PINK
    ),
    (
        "Antisipasi kondisi cuaca",
        "Pengelola perlu mempertimbangkan perubahan permintaan "
        "berdasarkan kondisi cuaca serta menyiapkan strategi "
        "operasional yang sesuai.",
        BLUE
    ),
    (
        "Pengelolaan berdasarkan tingkat permintaan",
        "Kategori permintaan rendah, sedang, dan tinggi dapat "
        "digunakan sebagai acuan untuk perencanaan persediaan "
        "dan redistribusi sepeda.",
        PEACH
    ),
]

reco_cols = st.columns(4)

for i, (col, (title, text, color)) in enumerate(zip(reco_cols, recommendations), start=1):
    col.markdown(
        f"""
        <div class="reco-card">
            <div class="reco-badge" style="background:{color};">{i}</div>
            <h4>{title}</h4>
            <p>{text}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

st.divider()


with st.expander("🔎 Lihat Data Penyewaan Harian"):
    st.dataframe(
        filtered_day,
        use_container_width=True
    )

with st.expander("🔎 Lihat Data Penyewaan Per Jam"):
    st.dataframe(
        filtered_hour,
        use_container_width=True
    )


st.markdown(
    """
    <div style="text-align:center; color:#7A789B;
    padding:20px;">
        <p><b>Bike Sharing Analysis Dashboard</b></p>
        <p>Data Analysis Project · 2011–2012</p>
        <p>Dataset: Bike Sharing Dataset</p>
    </div>
    """,
    unsafe_allow_html=True
)