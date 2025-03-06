import requests
import time
import base64
import os
import colorama
from datetime import datetime, timedelta
import git
colorama.init()

# Kişisel Bilgi Kartı Bilgileri
profile_image = "https://i.hizliresim.com/lje98hq.jpg"
user_name = "Ahmet Bilgehan Dedelin"
description = 'hippity hoppity.'
github_link = "https://github.com/nilgehab"
spotify_link = "https://open.spotify.com/user/314kcnraoymjo3eui6awap7vrr5u"
instagram_link = "https://www.instagram.com/bilgehandle/"
github_logo = "https://i.hizliresim.com/kut8c3h.png"
spotify_logo = "https://i.hizliresim.com/li3rhc7.png"
instagram_logo = "https://i.hizliresim.com/emp8i5p.png"
web_project_link = "https://nilgehab.github.io/webmat"

# Spotify API Bilgileri
client_id = "645e194b1c514b1dbf780868d2128d0a"
client_secret = "a852285a54ab4486bd162ffc458a97b7"
refresh_token = "AQCFxAbDNXiyiEtSI6sLYME93BDluh686KTg13RmFNNx7qHg7kEL1Ii7mQaAfoWr4Xn3QU1XIk8FeefZm2VaNYurMu7Uhdf0b6OtodRcWWN-kUGOlDxIQ0tvGZ9oZL_WOe4"

previous_tracks = []

def get_update_time():
    now = datetime.now()
    return now.strftime("%H:%M")

def get_access_token():
    auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    headers = {
        "Authorization": f"Basic {auth_header}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": client_id,
        "client_secret": client_secret
    }

    response = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=data)
    return response.json()["access_token"] if response.status_code == 200 else None

def format_played_at(timestamp):
    dt = datetime.fromisoformat(timestamp[:-1]) + timedelta(hours=3)
    now = datetime.now() + timedelta(hours=3)
    date_diff = (now.date() - dt.date()).days
    
    if date_diff == 0:
        date_str = "Bugün"
    elif date_diff == 1:
        date_str = "Dün"
    else:
        date_str = f"{date_diff} gün önce"
    
    return dt.strftime("%H:%M"), date_str

def format_update_time():
    now = datetime.now() + timedelta(hours=0)
    return f"Bugün {now.strftime('%H:%M')}"

def get_currently_playing(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get("https://api.spotify.com/v1/me/player/currently-playing", headers=headers)
    return response.json() if response.status_code == 200 and response.json().get("is_playing") else None

def update_html(recent_tracks, currently_playing):
    last_update_time = format_update_time()
    
    # Müzik içeriğini oluştur
    music_content = []
    
    if currently_playing:
        track_info = currently_playing.get("item")
        if track_info:
            track_name = track_info.get("name")
            artists = ", ".join([artist["name"] for artist in track_info.get("artists", [])])
            track_url = track_info.get("external_urls", {}).get("spotify", "#")
            
            currently_playing_item = f"""
            <a href="{track_url}" target="_blank" class="track-item currently-playing">
                <img src="{track_info['album']['images'][0]['url']}" class="album-art">
                <div class="track-info">
                    <div class="track-title">{track_name}</div>
                    <div class="track-artist">{artists}</div>
                </div>
                <div class="play-time">
                    Şu anda çalıyor
                </div>
            </a>
            """
            music_content.append(currently_playing_item)
    
    for track in recent_tracks:
        track_info = track.get("track")
        if track_info:
            track_name = track_info.get("name")
            artists = ", ".join([artist["name"] for artist in track_info.get("artists", [])])
            played_at_time, played_at_date = format_played_at(track["played_at"])
            track_url = track_info.get("external_urls", {}).get("spotify", "#")
            
            music_item = f"""
            <a href="{track_url}" target="_blank" class="track-item">
                <img src="{track_info['album']['images'][0]['url']}" class="album-art">
                <div class="track-info">
                    <div class="track-title">{track_name}</div>
                    <div class="track-artist">{artists}</div>
                </div>
                <div class="play-time">
                    {played_at_time}<br>
                    <span style="font-size:0.7em">{played_at_date}</span>
                </div>
            </a>
            """
            music_content.append(music_item)
    
    # Tüm HTML şablonu
    html_content = f"""
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>bilgehan, bilgehan.</title>
    <link rel="icon" href="https://i.hizliresim.com/l8rigkg.png" type="image/png">
    <meta name="description"bilgehan. - Nevşehir Matematik Özel Ders - Geliştirici / Editör">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
        }}

        body {{
            background: url('https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExNXp5eHhzZGs1NTJvYTVtcDd0azdma3ZuNnA5NWkxa21sanNsdTU3OSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/pVGsAWjzvXcZW4ZBTE/giphy.gif') no-repeat center center fixed;
            background-size: cover;
            color: #e8e8e8;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
            overflow: hidden;
        }}

        .main-card {{
            background: rgba(26, 26, 26, 0.9);
            border-radius: 16px;
            width: 100%;
            max-width: 440px;
            padding: 30px;
            box-shadow: 0 12px 24px rgba(0,0,0,0.25);
            animation: cardEnter 0.6s cubic-bezier(0.23, 1, 0.32, 1);
            max-height: 90vh;
            height: 700px;
            display: flex;
            flex-direction: column;
        }}

        @keyframes cardEnter {{
            from {{ transform: translateY(20px); opacity: 0; }}
            to {{ transform: translateY(0); opacity: 1; }}
        }}

        .profile-section {{
            text-align: center;
            margin-bottom: 28px;
        }}

        .profile-image {{
            width: 96px;
            height: 96px;
            border-radius: 50%;
            margin-bottom: 18px;
            border: 2px solid #404040;
            object-fit: cover;
            transition: transform 0.3s ease;
        }}

        .profile-image:hover {{
            transform: rotate(8deg);
        }}

        .name {{
            font-size: 1.6rem;
            margin-bottom: 6px;
            color: #f0f0f0;
            letter-spacing: -0.5px;
        }}

        .bio {{
            color: #909090;
            font-size: 0.95rem;
            margin-bottom: 24px;
        }}

        .social-links {{
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-bottom: 32px;
        }}

        .social-icon {{
            width: 28px;
            height: 28px;
            transition: all 0.3s ease;
            opacity: 0.8;
        }}

        .social-icon:hover {{
            transform: translateY(-3px);
            opacity: 1;
        }}

        .tab-bar {{
            display: flex;
            gap: 8px;
            margin-bottom: 24px;
        }}

        .tab-button {{
            flex: 1;
            padding: 12px;
            background: #252525;
            border: none;
            border-radius: 10px;
            color: #a0a0a0;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }}

        .tab-button.active {{
            background: linear-gradient(135deg, #2a2a2a, #1f1f1f);
            color: #fff;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }}

        .content-section {{
            background: rgba(37, 37, 37, 0.9);
            border-radius: 12px;
            padding: 20px;
            flex: 1;
            overflow: hidden;
            display: none;
            opacity: 0;
            transform: translateY(10px);
            animation: contentShow 0.4s forwards;
            flex-direction: column;
        }}

        .content-section.active {{
            display: flex;
            opacity: 1;
            transform: translateY(0);
        }}

        @keyframes contentShow {{
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        /* Matematik Sekmesi */
        .math-content {{
            text-align: center;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            gap: 20px;
            height: 100%;
        }}

        .whatsapp-button {{
            background: #25D366;
            color: white;
            padding: 14px 24px;
            border-radius: 8px;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 10px;
            transition: transform 0.3s, box-shadow 0.3s;
        }}

        .whatsapp-button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(37, 211, 102, 0.3);
        }}

        .whatsapp-icon {{
            width: 24px;
            height: 24px;
        }}

        /* Teknoloji Sekmesi */
        .tech-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 12px;
            margin-bottom: 20px;
            flex: 1;
            overflow-y: auto;
            padding-bottom: 10px;
        }}

        .tech-card {{
            background: #333;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
            transition: transform 0.3s;
        }}

        .tech-card:hover {{
            transform: translateY(-3px);
        }}

        .tech-icon {{
            width: 32px;
            height: 32px;
            margin-bottom: 10px;
            filter: invert(0.8);
        }}

        .ae-logo-wrapper {{
            background: white;
            padding: 4px;
            border-radius: 4px;
            display: inline-block;
        }}

        .ps-logo-wrapper {{
            background: #001D26;
            padding: 4px;
            border-radius: 4px;
            display: inline-block;
        }}

        .tech-title {{
            font-size: 0.85rem;
            color: #ccc;
        }}

        /* WebMat Kutusu */
        .webmat-box {{
            background: #333;
            border-radius: 8px;
            padding: 15px;
            margin-top: auto;
            transition: transform 0.3s;
            text-decoration: none;
            display: block;
        }}

        .webmat-header {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}

        .webmat-logo-wrapper {{
            background: white;
            padding: 6px;
            border-radius: 8px;
            display: inline-flex;
        }}

        .webmat-logo {{
            width: 40px;
            height: 40px;
        }}

        .webmat-title {{
            font-size: 1rem;
            color: #fff;
            margin-bottom: 6px;
        }}

        .webmat-desc {{
            font-size: 0.8rem;
            color: #999;
            line-height: 1.4;
        }}

        /* Müzik Sekmesi */
        .track-list {{
            display: grid;
            gap: 16px;
            flex: 1;
            overflow-y: auto;
            padding-right: 8px;
        }}

        .track-item {{
            display: flex;
            align-items: center;
            padding: 12px;
            background: #303030;
            border-radius: 8px;
            transition: transform 0.3s;
            text-decoration: none;
            color: inherit;
        }}

        .track-item:hover {{
            transform: translateX(8px);
        }}

        .album-art {{
            width: 48px;
            height: 48px;
            border-radius: 6px;
            margin-right: 16px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }}

        .track-info {{
            flex: 1;
        }}

        .track-title {{
            font-size: 0.95rem;
            margin-bottom: 4px;
        }}

        .track-artist {{
            font-size: 0.85rem;
            color: #909090;
        }}

        .play-time {{
            font-size: 0.85rem;
            color: #707070;
            margin-left: 12px;
        }}

        .last-update {{
            font-size: 0.75rem;
            color: #a0a0a0;
            text-align: center;
            margin-top: 10px;
        }}

        /* Mevcut stillere şu değişiklikleri ekle */

        .profile-section {{
            margin-bottom: 12px; /* 28px'den 20px'e düşürüldü */
        }}

        .social-links {{
            margin-bottom: 12px; /* 32px'den 24px'e düşürüldü */
        }}

        .tab-bar {{
            margin-bottom: 8px; /* 24px'den 16px'e düşürüldü */
        }}

        .tech-grid {{
            margin-bottom: 15px; /* Alt boşluğu azalt */
            flex: 1;
            overflow-y: auto;
        }}

        .webmat-box {{
            margin-top: 0; /* Auto yerine sabit değer */
            width: 100%;
            flex-shrink: 0; /* Kutu boyutunun korunması için */
        }}

        .content-section {{
            gap: 15px; /* Grid ile WebMat kutusu arası boşluk */
        }}

        /* Yeni eklenen stiller */
        #tech .content-section {{
            display: flex;
            flex-direction: column;
            padding: 0; /* İç padding'i kaldır */
        }}

        #tech .tech-grid {{
            padding: 20px; /* İçeriye padding ekle */
            margin-bottom: 0;
        }}

        #tech .webmat-box {{
            border-radius: 0 0 12px 12px; /* Alt köşeleri yuvarla */
            margin-top: auto;
        }}

        @media (max-width: 480px) {{
            .main-card {{
                height: 90vh;
                padding: 20px;
                border-radius: 12px;
            }}
            
            .tech-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}
            
            .profile-image {{
                width: 84px;
                height: 84px;
            }}
            
            .name {{
                font-size: 1.4rem;
            }}
            
            .tab-button {{
                font-size: 0.9rem;
                padding: 10px;
            }}
            
            .tech-card {{
                padding: 12px;
            }}
        }}

        /* Teknoloji Grid Güncellemeleri */
        .tech-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(90px, 1fr));
            gap: 8px;
            padding: 12px !important;
            flex: 1;
            overflow-y: auto;
        }}

        .tech-card {{
            padding: 12px;
            border-radius: 6px;
        }}

        .tech-icon {{
            width: 28px;
            height: 28px;
            margin-bottom: 8px;
        }}

        .tech-title {{
            font-size: 0.75rem;
            line-height: 1.2;
        }}

        /* WebMat Kutusu Güncellemesi */
        .webmat-box {{
            padding: 12px;
            border-radius: 0 0 12px 12px;
        }}

        .webmat-logo {{
            width: 36px;
            height: 36px;
        }}

        .webmat-title {{
            font-size: 0.9rem;
        }}

        .webmat-desc {{
            font-size: 0.75rem;
        }}

        /* Responsive İyileştirmeler */
        @media (max-width: 480px) {{
            .tech-grid {{
                grid-template-columns: repeat(auto-fit, minmax(80px, 1fr));
                gap: 6px;
                padding: 8px !important;
            }}
            
            .tech-card {{
                padding: 8px;
            }}
            
            .tech-icon {{
                width: 24px;
                height: 24px;
            }}
            
            .tech-title {{
                font-size: 0.7rem;
            }}
            
            .tab-button {{
                font-size: 0.8rem;
                padding: 8px;
            }}
            
            .webmat-header {{
                gap: 8px;
            }}
        }}

        @media (max-width: 350px) {{
            .tech-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}
        }}

        .currently-playing {{
            background-color: #1DB954;
            color: white;
        }}
        
        .currently-playing .track-title, .currently-playing .track-artist {{
            color: white;
        }}
        
        .currently-playing .play-time {{
            color: white;
        }}
    </style>
</head>
<body>
    <div class="main-card">
        <div class="profile-section">
            <img src="{profile_image}" class="profile-image" alt="Profile">
            <h1 class="name">{user_name}</h1>
            <p class="bio">{description}</p>
            <div class="social-links">
                <a href="{github_link}" target="_blank">
                    <img src="{github_logo}" class="social-icon" alt="GitHub">
                </a>
                <a href="{spotify_link}" target="_blank">
                    <img src="{spotify_logo}" class="social-icon" alt="Spotify">
                </a>
                <a href="{instagram_link}" target="_blank">
                    <img src="{instagram_logo}" class="social-icon" alt="Instagram">
                </a>
            </div>
        </div>

        <div class="tab-bar">
            <button class="tab-button active" onclick="showContent(event, 'math')">Matematik</button>
            <button class="tab-button" onclick="showContent(event, 'tech')">Teknoloji</button>
            <button class="tab-button" onclick="showContent(event, 'music')">Son Dinlediklerim</button>
        </div>

        <!-- Matematik Sekmesi -->
        <div id="math" class="content-section active">
            <div class="math-content">
                <h3>Matematik Özel Dersleri</h3>
                <p align="left">YKS-LGS sınavlarına yönelik, kişiselleştirilmiş ve dijital araçlarla güçlendirilmiş dersler için:</p>
                <a href="https://wa.me/5557172838" class="whatsapp-button" target="_blank">
                    <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" class="whatsapp-icon">
                    Daha fazla bilgi almak için WhatsApp'tan ulaşın!
                </a>
            </div>
        </div>

        <!-- Teknoloji Sekmesi -->
        <div id="tech" class="content-section">
            <div class="tech-grid">
                <div class="tech-card">
                    <img src="https://cdn-icons-png.flaticon.com/512/1051/1051277.png" class="tech-icon">
                    <div class="tech-title">Web Geliştirme</div>
                </div>
                
                <div class="tech-card">
                    <img src="https://cdn-icons-png.flaticon.com/512/919/919825.png" class="tech-icon">
                    <div class="tech-title">Node.js</div>
                </div>
                
                <div class="tech-card">
                    <img src="https://cdn-icons-png.flaticon.com/512/2103/2103791.png" class="tech-icon">
                    <div class="tech-title">Yapay Zeka</div>
                </div>
                
                <div class="tech-card">
                    <img src="https://cdn-icons-png.flaticon.com/512/919/919852.png" class="tech-icon">
                    <div class="tech-title">Python</div>
                </div>
                
                <div class="tech-card">
                    <div class="ae-logo-wrapper">
                        <img src="https://cdn.worldvectorlogo.com/logos/after-effects-2019.svg" 
                             class="tech-icon">
                    </div>
                    <div class="tech-title">After Effects</div>
                </div>
                
                <div class="tech-card">
                    <div class="ps-logo-wrapper">
                        <img src="https://upload.wikimedia.org/wikipedia/commons/a/af/Adobe_Photoshop_CC_icon.svg" 
                             class="tech-icon">
                    </div>
                    <div class="tech-title">Photoshop</div>
                </div>
            </div>

            <a href="{web_project_link}" target="_blank" class="webmat-box">
                <div class="webmat-header">
                    <div class="webmat-logo-wrapper">
                        <img src="https://webmat.org/images/logo.png" class="webmat-logo" alt="WebMat Logo">
                    </div>
                    <div>
                        <div class="webmat-title">WebMat Projesi</div>
                        <div class="webmat-desc">
                            Matematik öğretmenleri için geliştirilmiş dijital araç rehberi.
                        </div>
                    </div>
                </div>
            </a>
        </div>

        <!-- Müzik Sekmesi -->
        <div id="music" class="content-section">
        <div class="last-update">Son Güncelleme: {last_update_time}</div>
        
            <div class="track-list">
                {"".join(music_content)}
            </div>
        </div>
    </div>
    <script>
        function showContent(event, contentId) {{
            document.querySelectorAll('.content-section').forEach(content => {{
                content.classList.remove('active');
            }});
            document.querySelectorAll('.tab-button').forEach(button => {{
                button.classList.remove('active');
            }});
            document.getElementById(contentId).classList.add('active');
            event.currentTarget.classList.add('active');
        }}
    </script>
</body>
</html>
    """

    with open("index.html", "w", encoding="utf-8") as file:
        file.write(html_content)

def get_recent_tracks(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get("https://api.spotify.com/v1/me/player/recently-played?limit=20", headers=headers)
    return response.json().get("items", []) if response.status_code == 200 else []

def git_push():
    repo = git.Repo(".")

    # **Sadece index.html, CNAME ve sitemap.xml dosyalarını ekle**
    repo.git.add("index.html")
    repo.git.add("CNAME")
    repo.git.add("sitemap.xml")

    # Commit işlemi
    repo.index.commit("Spotify verileriyle HTML güncellendi")

    # Push işlemi
    repo.git.push('origin', 'vds', '--force')

    # Commit geçmişini al
    commits = list(repo.iter_commits('vds'))
    old_commit_count = len(commits)  # Commit temizlemeden önceki sayı
    commit_message = ""

    if old_commit_count > 5:
        # **EN YENİ 5 COMMIT KALSIN, GERİ KALANI SİL**
        newest_commit_to_keep = commits[4].hexsha  # En yeni 5. commit'in hash'i

        # **Sadece en yeni 5 commit'i bırak**
        repo.git.execute(["git", "reset", "--hard", newest_commit_to_keep])
        repo.git.execute(["git", "reflog", "expire", "--expire=now", "--all"])
        repo.git.execute(["git", "gc", "--prune=now"])
        repo.git.execute(["git", "push", "--force"])  # Değişiklikleri zorla gönder

        # Yeni commit sayısını al
        new_commit_count = len(list(repo.iter_commits('vds')))

        commit_message = f"\033[92m✅ Eski commitler temizlendi! (Önce: {old_commit_count}, Sonra: {new_commit_count})\033[0m"
    else:
        commit_message = f"\033[93m⚠️ Commit temizleme işlemi yapılmadı! (Toplam commit sayısı: {old_commit_count})\033[0m"

    # Konsolu temizle ve mesajı banner ile göster
    clear_console()
    print_banner()
    print(commit_message)  # Bannerın altında mesajı göster




def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner(commit_message=""):
    banner = f"""
\033[95m
██╗  ██╗ █████╗ ███╗   ██╗
██║  ██║██╔══██╗████╗  ██║
███████║███████║██╔██╗ ██║
██╔══██║██╔══██║██║╚██╗██║
██║  ██║██║  ██║██║ ╚████║
╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝
\033[0m
"""
    print(banner)
    if commit_message:
        print(commit_message)  # Commit mesajını göster


def main():
    global previous_tracks
    total_updates = 0
    updates_with_changes = 0
    updates_without_changes = 0
    last_playing_track = None

    while True:
        clear_console()
        print_banner()
        access_token = get_access_token()
        currently_playing_str = "Yok"
        if access_token:
            recent_tracks = get_recent_tracks(access_token)
            currently_playing = get_currently_playing(access_token)
            if currently_playing:
                track_info = currently_playing.get("item")
                if track_info:
                    track_name = track_info.get("name")
                    artists = ", ".join([artist["name"] for artist in track_info.get("artists", [])])
                    currently_playing_str = f"{track_name} - {artists}"
                    last_playing_track = currently_playing
            else:
                if last_playing_track:
                    recent_tracks.insert(0, {"track": last_playing_track.get("item"), "played_at": (datetime.now() - timedelta(hours=3)).isoformat()})
                last_playing_track = None
            
            if recent_tracks:
                current_track_ids = [t["track"]["id"] for t in recent_tracks]
                previous_track_ids = [t["track"]["id"] for t in previous_tracks]
                
                if current_track_ids != previous_track_ids or currently_playing:
                    update_html(recent_tracks, currently_playing)
                    git_push()
                    previous_tracks = recent_tracks
                    updates_with_changes += 1
                else:
                    updates_without_changes += 1
            else:
                updates_without_changes += 1
        else:
            updates_without_changes += 1

        total_updates = updates_with_changes + updates_without_changes
        clear_console()
        print_banner()
        print(f"\033[92mToplam güncelleme sayısı: {updates_with_changes}/{total_updates}\033[0m")
        print(f"\033[93mŞu anda çalan: {currently_playing_str}\033[0m")
        print(f"\033[94mSistem aktif ve çalışıyor!\033[0m")
        
        time.sleep(60)

if __name__ == "__main__":
    main()