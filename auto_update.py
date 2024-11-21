import requests
import time
import base64
import os
import colorama
from datetime import datetime, timedelta
import git  # GitPython kütüphanesi
colorama.init()

# Kişisel Bilgi Kartı Bilgileri
profile_image = "https://i.hizliresim.com/lje98hq.jpg"  # Profil fotoğrafı
user_name = "Ahmet Bilgehan Dedelin"  # Kullanıcı adı
description = 'hippity hoppity. <a href="https://nilgehab.github.io/webmat" style="color: #fff; text-decoration: underline;">webmat projesi yakında.</a>'
github_link = "https://github.com/nilgehab"  # GitHub linki
spotify_link = "https://open.spotify.com/user/314kcnraoymjo3eui6awap7vrr5u"  # Spotify linki
instagram_link = "https://www.instagram.com/bilgehandle/"  # Instagram linki
github_logo = "https://i.hizliresim.com/kut8c3h.png"  # GitHub logosu
spotify_logo = "https://i.hizliresim.com/li3rhc7.png"  # Spotify logosu
instagram_logo = "https://i.hizliresim.com/emp8i5p.png"  # Instagram logosu
web_project_link = "https://nilgehab.github.io/webmat"  # Web projenizin bağlantısı

# Spotify uygulamanızın bilgileri
client_id = "645e194b1c514b1dbf780868d2128d0a"  # Kendi Client ID'nizi buraya yapıştırın
client_secret = "a852285a54ab4486bd162ffc458a97b7"  # Kendi Client Secret'inizi buraya yapıştırın
refresh_token = "AQCFxAbDNXiyiEtSI6sLYME93BDluh686KTg13RmFNNx7qHg7kEL1Ii7mQaAfoWr4Xn3QU1XIk8FeefZm2VaNYurMu7Uhdf0b6OtodRcWWN-kUGOlDxIQ0tvGZ9oZL_WOe4"  # Daha önce aldığınız Refresh Token

previous_tracks = []  # Önceki şarkılar listesi

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
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        print("\033[91mHata:\033[0m", response.text)  # Hataları kırmızı yap
        return None

def format_played_at(timestamp):
    dt = datetime.fromisoformat(timestamp[:-1]) + timedelta(hours=3)  # UTC'yi Türkiye saatine çevirmek için 3 saat ekle
    now = datetime.now() + timedelta(hours=3)  # Şu anı da Türkiye saati ile al
    time_diff = now - dt
    if time_diff.days == 0:
        date_str = "Bugün"
    elif time_diff.days == 1:
        date_str = "Dün"
    else:
        date_str = f"{time_diff.days} gün önce" if time_diff.days > 0 else "Bugün"

    time_str = dt.strftime("%H:%M")  # Saat formatı
    return time_str, date_str  # Saat ve tarih ayrı döndürülüyor
def update_html(recent_tracks):
    html_content = f"""
    <html>
    <head>
        <title>bilgehan</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background: url('https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExNXp5eHhzZGs1NTJvYTVtcDd0azdma3ZuNnA5NWkxa21sanNsdTU3OSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/pVGsAWjzvXcZW4ZBTE/giphy.gif') no-repeat center center fixed;
                background-size: cover;
                color: #fff;
                margin: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                text-align: center;
            }}

a {{
    color: #fff; /* Metin rengini beyaz yap */
    text-decoration: none; /* Altı çizgiyi kaldır */
}}

a:hover {{
    color: #ddd; /* Üzerine gelindiğinde rengini açık gri yap */
}}

            .card {{
                background: rgba(0, 0, 0, 0.7);
                border-radius: 15px;
                padding: 30px;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
                width: 90%;
                max-width: 500px;
                height: auto;
                max-height: 90%;
                overflow: hidden;
                margin: 0 10px;
            }}
            .profile-image {{
                width: 100px;
                height: 100px;
                border-radius: 50%;
                margin-bottom: 20px;
            }}
            .social-icons {{
                margin: 20px 0;
            }}
            .social-icons img {{
                width: 40px;
                margin: 0 10px;
            }}
            h1 {{
                margin: 0;
                font-size: 2em;
            }}
            .description {{
                font-size: 1.1em;
                margin: 10px 0;
            }}
            .recent-tracks {{
                margin-top: 20px;
                max-height: 250px;
                overflow-y: auto;
                scrollbar-width: thin;
                scrollbar-color: #888 #333;
            }}
            .recent-tracks::-webkit-scrollbar {{
                width: 12px;
            }}
            .recent-tracks::-webkit-scrollbar-track {{
                background: #333;
                border-radius: 10px;
            }}
            .recent-tracks::-webkit-scrollbar-thumb {{
                background-color: #888;
                border-radius: 10px;
            }}
            .recent-tracks::-webkit-scrollbar-thumb:hover {{
                background-color: #555;
            }}
            .track-info {{
                display: flex;
                align-items: center;
                padding: 10px 0;
                border-bottom: 1px solid rgba(255, 255, 255, 0.3);
                cursor: pointer;
            }}
            .track-image {{
                width: 60px;
                height: 60px;
                border-radius: 5px;
                margin-right: 15px;  /* Görsel ile parça adı arasındaki boşluk */
            }}
            .track-details {{
                flex: 1;  /* Alanın eşit şekilde paylaşılması */
                display: flex;
                flex-direction: column; /* Parça adı ve sanatçı adı dikey olarak hizalanacak */
            }}
            .track-name {{
                font-weight: bold;
                font-size: 1em;
                margin-bottom: 5px; /* Parça adı ile sanatçı adı arasındaki boşluk */
            }}
            .track-artists {{
                font-size: 0.9em;
                color: #aaa;
            }}
            .played-at {{
                font-size: 0.9em;
                color: #aaa;
                margin-left: auto; /* Sağ tarafa yaslamak için */
            }}
            @media (max-width: 600px) {{
                .card {{
                    width: 95%;
                }}
                h1 {{
                    font-size: 1.8em;
                }}
                .description {{
                    font-size: 1em;
                }}
            }}
            @media (max-width: 400px) {{
                h1 {{
                    font-size: 1.5em;
                }}
                .description {{
                    font-size: 0.9em;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="card">
            <img src="{profile_image}" alt="Profil Fotoğrafım" class="profile-image">
            <h1>{user_name}</h1>
            <p class="description">{description}</p>
            <div class="social-icons">
                <a href="{github_link}" target="_blank"><img src="{github_logo}" alt="GitHub"></a>
                <a href="{spotify_link}" target="_blank"><img src="{spotify_logo}" alt="Spotify"></a>
                <a href="{instagram_link}" target="_blank"><img src="{instagram_logo}" alt="Instagram"></a>
            </div>

            <h2>Son Dinlediklerim</h2>
            <div class="recent-tracks">
    """

    for track in recent_tracks:
        track_info = track.get("track")
        if track_info:
            track_name = track_info.get("name")
            artists = ", ".join([artist["name"] for artist in track_info.get("artists", [])])
            played_at = format_played_at(track["played_at"])
            html_content += f"""
                <div class="track-info">
                    <a href="{track_info['external_urls']['spotify']}" target="_blank" style="display: flex; align-items: center; width: 100%;">
                        <img src="{track_info['album']['images'][0]['url']}" class="track-image">
                        <div class="track-details">
                            <div class="track-name">{track_name}</div>
                            <div class="track-artists">{artists}</div>
                        </div>
                        <div class="played-at">{played_at[0]}<br>{played_at[1]}</div>
                    </a>
                </div>
            """

    html_content += """
            </div>
        </div>
    </body>
    </html>
    """

    with open("index.html", "w", encoding="utf-8") as file:
        file.write(html_content)




def get_recent_tracks(access_token):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get("https://api.spotify.com/v1/me/player/recently-played", headers=headers)
    if response.status_code == 200:
        return response.json()["items"]
    else:
        print("\033[91mHata:\033[0m", response.text)  # Hataları kırmızı yap
        return []

def git_push():
    repo = git.Repo(".")
    repo.git.add("index.html")  # Sadece index.html dosyasını ekle
    repo.index.commit("HTML güncellendi. Son 3 saatin müzikleri eklendi.")  # Commit yap
    repo.git.push('--force')  # Push yap

def main():
    global previous_tracks
    while True:
        access_token = get_access_token()
        if access_token:
            recent_tracks = get_recent_tracks(access_token)
            if recent_tracks:
                new_tracks = [track for track in recent_tracks if track["track"]["id"] not in [t["track"]["id"] for t in previous_tracks]]
                if new_tracks:
                    update_html(recent_tracks)
                    print(f"\033[92m{len(new_tracks)} yeni parça bulundu ve HTML güncellendi!\033[0m")
                    git_push()  # Burada git_push() çağrılıyor
                    previous_tracks = recent_tracks  # Önceki parçaları güncelle
                else:
                    print("\033[93mYeni parça yok.\033[0m")  # Sarı uyarı
            else:
                print("\033[93mSon dinlenilen parça bilgisi alınamadı.\033[0m")
        time.sleep(60)  # 1 dakika bekle

if __name__ == "__main__":
    main()