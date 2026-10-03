import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import pickle
import random
import time
from difflib import get_close_matches

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Netflix AI Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# GLOBAL CSS
# =====================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

html, body{
    margin:0;
    padding:0;
    background:#141414;
    color:white;
    font-family:'Poppins',sans-serif;
    overflow-x:hidden;
}

.stApp{
    background:#141414;
}

/* Hide Streamlit */

header{
    visibility:hidden;
}

footer{
    visibility:hidden;
}

[data-testid="stToolbar"]{
    display:none;
}

/* Sidebar */

section[data-testid="stSidebar"]{
    background:#0b0b0b;
}

section[data-testid="stSidebar"] *{
    color:white !important;
}

/* Inputs */

.stTextInput input{
    background:#1f1f1f !important;
    color:white !important;
    border-radius:8px !important;
    border:1px solid #333 !important;
    height:50px;
}

.stSelectbox div[data-baseweb="select"]{
    background:#1f1f1f !important;
    color:white !important;
}

/* Buttons */

.stButton button{
    background:#E50914 !important;
    color:white !important;
    border:none !important;
    border-radius:8px !important;
    height:50px !important;
    font-weight:600 !important;
    font-size:16px !important;
}

.stButton button:hover{
    background:#ff1f1f !important;
    transform:scale(1.03);
}

/* Section */

.section-title{
    font-size:30px;
    font-weight:700;
    margin:30px 0 20px 10px;
}

.block-container{
    padding-top:1rem !important;
}

/* CINEMA STRIP */

.cinema-strip{
    width:100%;
    height:8px;
    background:linear-gradient(
        90deg,
        #000,
        #E50914,
        #000,
        #E50914,
        #000
    );
    margin-top:-5px;
    animation:cinemaGlow 3s linear infinite;
}

@keyframes cinemaGlow{

    0%{
        filter:brightness(1);
    }

    50%{
        filter:brightness(1.8);
    }

    100%{
        filter:brightness(1);
    }

}

/* AUTO CAROUSEL */

.carousel{
    width:100%;
    overflow:hidden;
    margin-top:20px;
}

.carousel-track{
    display:flex;
    width:max-content;
    gap:20px;
    animation:scroll 30s linear infinite;
}

.carousel-track img{
    width:300px;
    height:170px;
    object-fit:cover;
    border-radius:12px;
}

@keyframes scroll{

    0%{
        transform:translateX(0);
    }

    100%{
        transform:translateX(-50%);
    }

}

</style>
""", unsafe_allow_html=True)

# =====================================================
# LOAD DATA
# =====================================================

movies = pd.read_csv("movie_titles_cleaned.csv")

with open("model_results.pkl", "rb") as f:
    model_results = pickle.load(f)

movie_titles = movies["Movie_Title"].values

# =====================================================
# RECOMMEND FUNCTION
# =====================================================

def recommend(movie_name):

    match = get_close_matches(
        movie_name,
        movie_titles,
        n=1,
        cutoff=0.4
    )

    if not match:
        return []

    recommendations = random.sample(
        list(movie_titles),
        12
    )

    return recommendations

# =====================================================
# OFFLINE POSTERS + TRAILERS
# =====================================================

def fetch_tmdb(movie_name):

    movie_database = {

        "Inception": {
            "poster":"https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?q=80&w=1200&auto=format&fit=crop",
            "trailer":"https://www.youtube.com/embed/YoHD9XEInc0"
        },

        "Interstellar": {
            "poster":"https://images.unsplash.com/photo-1517604931442-7e0c8ed2963c?q=80&w=1200&auto=format&fit=crop",
            "trailer":"https://www.youtube.com/embed/zSWdZVtXT7E"
        },

        "Avatar": {
            "poster":"https://images.unsplash.com/photo-1478720568477-152d9b164e26?q=80&w=1200&auto=format&fit=crop",
            "trailer":"https://www.youtube.com/embed/5PSNL1qE6VY"
        },

        "Titanic": {
            "poster":"https://images.unsplash.com/photo-1512149177596-f817c7ef5d4c?q=80&w=1200&auto=format&fit=crop",
            "trailer":"https://www.youtube.com/embed/kVrqfYjkTdQ"
        },

        "Joker": {
            "poster":"https://images.unsplash.com/photo-1440404653325-ab127d49abc1?q=80&w=1200&auto=format&fit=crop",
            "trailer":"https://www.youtube.com/embed/zAGVQLHvwOY"
        }

    }

    default_data = {
        "poster":"https://picsum.photos/400/600",
        "trailer":"https://www.youtube.com/embed/b9EkMc79ZSU"
    }

    data = movie_database.get(movie_name, default_data)

    return data["poster"], data["trailer"]

# =====================================================
# CARD COMPONENT
# =====================================================

def card(title, rating):

    poster, trailer = fetch_tmdb(title)

    return f"""

    <html>

    <head>

    <style>

    body{{
        margin:0;
        padding:0;
        background:#141414;
        font-family:Poppins;
        overflow:hidden;
    }}

    .movie-card{{
        background:#181818;
        border-radius:14px;
        overflow:hidden;
        transition:0.4s;
        color:white;
        position:relative;
        cursor:pointer;
        box-shadow:0 0 15px rgba(0,0,0,0.5);
    }}

    .movie-card:hover{{
        transform:scale(1.05);
        box-shadow:0 0 30px rgba(229,9,20,0.6);
    }}

    .movie-card img{{
        width:100%;
        height:320px;
        object-fit:cover;
        display:block;
        transition:0.5s;
    }}

    iframe{{
        width:100%;
        height:320px;
        border:none;
        display:none;
    }}

    .movie-card:hover iframe{{
        display:block;
    }}

    .movie-card:hover img{{
        display:none;
    }}

    .overlay{{
        position:absolute;
        top:0;
        left:0;
        width:100%;
        height:100%;
        background:linear-gradient(
            to top,
            rgba(0,0,0,0.95),
            rgba(0,0,0,0.1)
        );
        opacity:0;
        transition:0.5s;
        display:flex;
        justify-content:center;
        align-items:center;
        flex-direction:column;
    }}

    .movie-card:hover .overlay{{
        opacity:1;
    }}

    .play-btn{{
        width:70px;
        height:70px;
        border-radius:50%;
        background:#E50914;
        display:flex;
        justify-content:center;
        align-items:center;
        font-size:30px;
        margin-bottom:15px;
        animation:pulse 1.5s infinite;
    }}

    @keyframes pulse{{
        0%{{transform:scale(1);}}
        50%{{transform:scale(1.08);}}
        100%{{transform:scale(1);}}
    }}

    .movie-info{{
        padding:14px;
    }}

    .movie-title{{
        font-size:18px;
        font-weight:600;
    }}

    .movie-rating{{
        color:#46d369;
        margin-top:8px;
        font-size:15px;
    }}

    </style>

    </head>

    <body>

    <div class="movie-card">

        <img src="{poster}">

        <iframe
            src="{trailer}?autoplay=1&mute=1">
        </iframe>

        <div class="overlay">

            <div class="play-btn">
                ▶
            </div>

        </div>

        <div class="movie-info">

            <div class="movie-title">
                {title}
            </div>

            <div class="movie-rating">
                ⭐ {rating}
            </div>

        </div>

    </div>

    </body>

    </html>

    """

# =====================================================
# LOGIN SYSTEM
# =====================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:

    st.markdown("""
    <h1 style='
        color:#E50914;
        font-size:80px;
        text-align:center;
        font-weight:900;
        letter-spacing:5px;
    '>
    NETFLIX
    </h1>
    """, unsafe_allow_html=True)

    st.markdown("## 🔐 Login")

    email = st.text_input("Email")

    password = st.text_input("Password", type="password")

    if st.button("Login"):

        if email and password:

            st.session_state.logged_in = True

            st.success("Login Successful")

            time.sleep(1)

            st.rerun()

        else:

            st.error("Enter credentials")

    st.stop()

# =====================================================
# WATCHLIST
# =====================================================

if "watchlist" not in st.session_state:
    st.session_state.watchlist = []

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.markdown("## 🎬 Netflix AI")

    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/0/0b/Netflix-avatar.png",
        width=120
    )

    profile = st.text_input(
        "👤 Profile Name",
        "Netflix User"
    )

    scroll_html = """

    <style>

    .scroll-wrapper{
        height:500px;
        overflow:hidden;
        position:relative;
        background:#111;
        border-radius:12px;
        padding:10px;
        margin-top:20px;
    }

    .scroll-content{
        position:absolute;
        width:100%;
        animation:scrollMovies 20s linear infinite;
    }

    .movie{
        background:#1f1f1f;
        padding:14px;
        margin-bottom:12px;
        border-radius:10px;
        text-align:center;
        color:white;
        font-size:16px;
        font-weight:500;
    }

    .movie:hover{
        background:#E50914;
    }

    @keyframes scrollMovies{

        0%{
            transform:translateY(100%);
        }

        100%{
            transform:translateY(-100%);
        }

    }

    </style>

    <h2 style="text-align:center;color:#E50914;">
        🔥 Trending Movies 🔥
    </h2>

    <div class="scroll-wrapper">

        <div class="scroll-content">

            <div class="movie">🔥 Inception</div>
            <div class="movie">🔥 Interstellar</div>
            <div class="movie">🔥 Avatar</div>
            <div class="movie">🔥 Titanic</div>
            <div class="movie">🔥 Joker</div>
            <div class="movie">🔥 Parasite</div>
            <div class="movie">🔥 John Wick</div>
            <div class="movie">🔥 Oppenheimer</div>
            <div class="movie">🔥 Avengers Endgame</div>
            <div class="movie">🔥 Dark Knight</div>

        </div>

    </div>

    """

    components.html(scroll_html, height=620)

# =====================================================
# NAVBAR
# =====================================================

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🏠 Home",
    "📺 TV Shows",
    "🎥 Movies",
    "⭐ Watchlist",
    "🤖 AI Chatbot",
    "📊 Insights"
])

# =====================================================
# HOME
# =====================================================

with tab1:

    components.html("""

    <style>

    .hero{
        position:relative;
        height:88vh;

        background-image:
        linear-gradient(to top, #141414 5%, transparent 40%),
        linear-gradient(to right, rgba(0,0,0,0.88), transparent 60%),
        url('https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?q=80&w=1800&auto=format&fit=crop');

        background-size:cover;
        background-position:center;

        display:flex;
        align-items:center;

        padding-left:70px;
        border-radius:20px;

        overflow:hidden;
    }

    .hero-content{
        max-width:650px;
        color:white;
        margin-top:80px;
    }

    .netflix-logo{
        color:#E50914;
        font-size:75px;
        font-weight:900;
        letter-spacing:4px;
        margin-bottom:20px;
        text-shadow:0 0 25px rgba(229,9,20,0.9);
        animation:glow 2s infinite alternate;
    }

    @keyframes glow{

        from{
            text-shadow:0 0 10px rgba(229,9,20,0.5);
        }

        to{
            text-shadow:0 0 35px rgba(229,9,20,1);
        }

    }

    .hero-title{
        font-size:100px;
        line-height:0.9;
        margin-bottom:20px;
        font-weight:700;
    }

    .hero-desc{
        font-size:18px;
        color:#d2d2d2;
        line-height:1.7;
        margin-bottom:30px;
    }

    .hero-buttons{
        display:flex;
        gap:15px;
    }

    .play-btn{
        background:white;
        color:black;
        padding:14px 34px;
        border-radius:6px;
        font-weight:600;
    }

    .info-btn{
        background:rgba(109,109,110,0.7);
        color:white;
        padding:14px 34px;
        border-radius:6px;
        font-weight:600;
    }

    </style>

    <div class="hero">

        <div class="hero-content">

            <div class="netflix-logo">
                NETFLIX
            </div>

            <div class="hero-title">
                STRANGER<br>THINGS
            </div>

            <div class="hero-desc">
                When a young boy disappears, a small town uncovers
                a mystery involving secret experiments,
                supernatural forces, and one strange little girl.
            </div>

            <div class="hero-buttons">

                <div class="play-btn">
                    ▶ Play
                </div>

                <div class="info-btn">
                    More Info
                </div>

            </div>

        </div>

    </div>

    """, height=700)

    st.markdown(
        '<div class="cinema-strip"></div>',
        unsafe_allow_html=True
    )

    # =====================================================
    # AUTOPLAY CAROUSEL
    # =====================================================

    carousel_html = """

    <div class="carousel">

        <div class="carousel-track">

            <img src="https://picsum.photos/500/300?1">
            <img src="https://picsum.photos/500/300?2">
            <img src="https://picsum.photos/500/300?3">
            <img src="https://picsum.photos/500/300?4">
            <img src="https://picsum.photos/500/300?5">
            <img src="https://picsum.photos/500/300?6">

        </div>

    </div>

    """

    components.html(carousel_html, height=200)

    # =====================================================
    # SEARCH
    # =====================================================

    st.markdown(
        '<div class="section-title">🔍 Find Your Movie</div>',
        unsafe_allow_html=True
    )

    text = st.text_input("Type movie name")

    selected = st.selectbox(
        "Or choose movie",
        movie_titles
    )

    col1, col2 = st.columns(2)

    with col1:
        btn1 = st.button("🎯 Recommend")

    with col2:
        btn2 = st.button("🎲 Surprise Me")

    final = ""

    if btn1:

        st.toast("🍿 Loading cinematic recommendations...")

        time.sleep(1)

        st.balloons()

        final = text if text else selected

    if btn2:

        st.toast("🎬 Finding surprise movies...")

        time.sleep(1)

        st.balloons()

        final = random.choice(movie_titles)

    # =====================================================
    # RECOMMENDATIONS
    # =====================================================

    if final:

        recs = recommend(final)

        st.markdown(
            f'<div class="section-title">✨ Because You Watched {final}</div>',
            unsafe_allow_html=True
        )

        cols = st.columns(4)

        for i, movie in enumerate(recs):

            with cols[i % 4]:

                components.html(
                    card(
                        movie,
                        round(random.uniform(7.5, 9.5), 1)
                    ),
                    height=430
                )

                if st.button(f"⭐ Add {i}"):

                    st.session_state.watchlist.append(movie)

                    st.success(f"{movie} added")

# =====================================================
# TV SHOWS
# =====================================================

with tab2:

    st.title("📺 TV Shows")

    shows = [
        "Breaking Bad",
        "Money Heist",
        "Dark",
        "Lucifer",
        "Wednesday",
        "The Witcher",
        "Squid Game",
        "Stranger Things"
    ]

    cols = st.columns(4)

    for i, show in enumerate(shows):

        with cols[i % 4]:

            components.html(
                card(show, round(random.uniform(8, 9.9), 1)),
                height=430
            )

# =====================================================
# MOVIES
# =====================================================

with tab3:

    st.title("🎥 Movies")

    movies_page = [
        "Interstellar",
        "Avatar",
        "Titanic",
        "Joker",
        "Inception",
        "John Wick",
        "Oppenheimer",
        "Avengers"
    ]

    cols = st.columns(4)

    for i, movie in enumerate(movies_page):

        with cols[i % 4]:

            components.html(
                card(movie, round(random.uniform(8, 9.9), 1)),
                height=430
            )

# =====================================================
# WATCHLIST
# =====================================================

with tab4:

    st.title("⭐ My Watchlist")

    if st.session_state.watchlist:

        for movie in st.session_state.watchlist:

            st.markdown(f"🎬 {movie}")

    else:

        st.info("No movies added yet")

# =====================================================
# AI CHATBOT
# =====================================================

with tab5:

    st.title("🤖 Netflix AI Assistant")

    msg = st.text_input("Ask movie suggestions")

    if st.button("Send"):

        responses = [

            "🔥 You should watch Interstellar",

            "🎬 Try Stranger Things",

            "🍿 Oppenheimer is trending now",

            "👀 Watch Dark if you love mystery",

            "💀 Try Money Heist tonight"
        ]

        st.success(random.choice(responses))

# =====================================================
# INSIGHTS
# =====================================================

with tab6:

    st.title("📊 Model Performance")

    rows = []

    for m, v in model_results.items():

        rows.append({
            "Model": m,
            "RMSE": v["RMSE"],
            "MAPE": v["MAPE"]
        })

    df = pd.DataFrame(rows)

    st.dataframe(df, use_container_width=True)

    st.subheader("RMSE Comparison")

    st.bar_chart(
        df.set_index("Model")["RMSE"]
    )

    st.subheader("MAPE Comparison")

    st.bar_chart(
        df.set_index("Model")["MAPE"]
    )

# =====================================================
# FOOTER
# =====================================================

st.markdown("""

<hr style="border:1px solid #333">

<center>

<h3 style="color:#E50914;">
NETFLIX AI RECOMMENDER
</h3>

<p style="color:gray;">
Powered by AI 🎬
</p>

</center>

""", unsafe_allow_html=True)