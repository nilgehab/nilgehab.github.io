import requests
import time
import base64
import os
from datetime import datetime
import threading
import msvcrt  # Windows'ta klavye girişi için kullanılır
import git  # GitPython kütüphanesi

# Spotify uygulamanızın bilgileri
client_id = "645e194b1c514b1dbf780868d2128d0a"  # Kendi Client ID'nizi buraya yapıştırın
client_secret = "a852285a54ab4486bd162ffc458a97b7"  # Kendi Client Secret'inizi buraya yapıştırın
refresh_token = "AQCFxAbDNXiyiEtSI6sLYME93BDluh686KTg13RmFNNx7qHg7kEL1Ii7mQaAfoWr4Xn3QU1XIk8FeefZm2VaNYurMu7Uhdf0b6OtodRcWWN-kUGOlDxIQ0tvGZ9oZL_WOe4"  # Daha önce aldığınız Refresh Token

update_count = 0  # Güncelleme sayacı

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
        print("Hata:", response.text)
        return None

def format_played_at(timestamp):
    dt = datetime.fromisoformat(timestamp[:-1])  # UTC'yi çıkar
    now = datetime.now()

    # Zaman dilimini hesaplama
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
    html_content = """
    <html>
    <head>
        <title>Kişisel Linktree Sayfam</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: url('background.gif') no-repeat center center fixed; /* Arka plan GIF */
                background-size: cover;
                color: #fff;
                margin: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                text-align: center;
            }
            .card {
                background: rgba(0, 0, 0, 0.7); /* Kart arka planı */
                border-radius: 15px;
                padding: 20px;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.5);
                width: 300px; /* Kart genişliği */
                max-height: 80%; /* Kart yüksekliği */
                overflow: hidden; /* Kart içinde taşma engellendi */
            }
            .profile-image {
                width: 80px;
                height: 80px;
                border-radius: 50%;
                margin-bottom: 15px;
            }
            .social-icons {
                margin: 15px 0;
            }
            .social-icons img {
                width: 30px; /* İkon boyutu */
                margin: 0 5px; /* İkonlar arası boşluk */
            }
            h1 {
                margin: 0;
                font-size: 1.5em;
            }
            .description {
                font-size: 0.9em;
                margin: 10px 0;
            }
            .recent-tracks {
                margin-top: 20px;
                max-height: 200px; /* Son dinlediklerim bölümü yüksekliği */
                overflow-y: auto; /* Taşma durumunda kaydırma */
                scrollbar-width: thin; /* Firefox için ince kaydırma çubuğu */
                scrollbar-color: #888 #333; /* Kaydırma çubuğu ve arka plan rengi */
            }

            /* Webkit tarayıcılar için kaydırma çubuğu stilini belirleme */
            .recent-tracks::-webkit-scrollbar {
                width: 10px; /* Kaydırma çubuğunun genişliği */
            }

            .recent-tracks::-webkit-scrollbar-track {
                background: #333; /* Kaydırma çubuğunun arka planı */
                border-radius: 10px; /* Köşeleri yuvarlama */
            }

            .recent-tracks::-webkit-scrollbar-thumb {
                background-color: #888; /* Kaydırma çubuğunun rengi */
                border-radius: 10px; /* Köşeleri yuvarlatma */
            }

            .recent-tracks::-webkit-scrollbar-thumb:hover {
                background-color: #555; /* Hover durumundaki rengi */
            }

            .track-info {
                display: flex;
                align-items: center; /* Resim ve metinlerin hizalanması */
                padding: 5px 0; /* Yüksekliği ayarlamak için */
                border-bottom: 1px solid rgba(255, 255, 255, 0.3);
                cursor: pointer; /* Üzerine gelindiğinde imlecin değişmesi */
                position: relative; /* Üst bilgi için konumlandırma */
            }
            .track-image {
                width: 40px; /* Kapak resmi boyutu */
                height: 40px; /* Kapak resmi boyutu */
                border-radius: 5px; /* Hafif yuvarlatma */
            }
            .track-details {
                display: flex;
                flex-direction: column; /* Sanatçı ve parça adı dikey olarak hizalanacak */
                margin-left: 10px; /* Resim ile metin arasındaki boşluk */
                flex: 1; /* Alanın eşit şekilde paylaşılması */
                overflow: hidden; /* Taşmayı önle */
            }
            .track-name {
                font-weight: bold;
                white-space: nowrap; /* Taşmayı önle */
                overflow: hidden; /* Taşmayı önle */
                text-overflow: ellipsis; /* Taşma durumunda üç nokta */
            }
            .track-artists {
                font-size: 0.8em; /* Sanatçı adları font boyutu küçültüldü */
                color: #aaa; /* Silik bir ton */
                white-space: nowrap; /* Taşmayı önle */
                overflow: hidden; /* Taşmayı önle */
                text-overflow: ellipsis; /* Taşma durumunda üç nokta */
            }
            .played-at {
                font-size: 0.8em;
                color: #aaa;
                margin-left: auto; /* Sağ tarafa yaslamak için */
            }
        </style>
    </head>
    <body>
        <div class="card">
            <img src="profil_foto.jpg" alt="Profil Fotoğrafım" class="profile-image">
            <h1>Ad Soyad</h1>
            <p class="description">Açıklamanız burada yer alacak.</p>
            <div class="social-icons">
                <a href="https://github.com/kullanici_adi" target="_blank"><img src="github_logo.png" alt="GitHub"></a>
                <a href="https://open.spotify.com/user/kullanici_adi" target="_blank"><img src="spotify_logo.png" alt="Spotify"></a>
                <a href="https://instagram.com/kullanici_adi" target="_blank"><img src="instagram_logo.png" alt="Instagram"></a>
            </div>
            <div class="recent-tracks">
                <h2>Son Dinlediklerim</h2>
                <ul>
    """
    
    for track in recent_tracks['items']:
        track_name = track['track']['name']
        artists = ', '.join(artist['name'] for artist in track['track']['artists'])
        time_str, date_str = format_played_at(track['played_at'])  # Zaman ve tarih al
        track_url = track['track']['external_urls']['spotify']
        track_image = track['track']['album']['images'][0]['url']  # İlk kapak resmini al

        # Sanatçı adını kısaltmak için
        track_name_short = (track_name[:30] + '...') if len(track_name) > 30 else track_name
        artists_short = (artists[:30] + '...') if len(artists) > 30 else artists

        html_content += f"""
                <li class="track-info" onclick="window.open('{track_url}', '_blank');">
                    <img src="{track_image}" alt="{track_name}" class="track-image">
                    <div class="track-details">
                        <div class="track-name">{track_name_short}</div>
                        <div class="track-artists">{artists_short}</div>
                    </div>
                    <div class="played-at">{time_str} - {date_str}</div>
                </li>
        """
    
    html_content += """
                </ul>
            </div>
        </div>
    </body>
    </html>
    """

    # HTML dosyasını güncelle
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
        print("index.html dosyası güncellendi.")
def git_push():
    try:
        repo = git.Repo(os.getcwd())  # Geçerli çalışma dizinindeki Git deposunu al
        repo.git.add("index.html")  # index.html dosyasını ekle
        repo.index.commit("index.html güncellendi")  # Değişiklikleri commit et
        repo.git.push()  # Değişiklikleri GitHub'a gönder
        print("index.html dosyası GitHub'a gönderildi.")  # Push yapıldığında bildirim
    except Exception as e:
        print("Git push sırasında hata oluştu:", e)

def update_spotify_data():
    global update_count
    while True:
        access_token = get_access_token()
        if access_token:
            headers = {
                "Authorization": f"Bearer {access_token}"
            }
            response = requests.get("https://api.spotify.com/v1/me/player/recently-played", headers=headers)
            if response.status_code == 200:
                recent_tracks = response.json()
                update_html(recent_tracks)
                update_count += 1
                print(f"{update_count}. güncelleme yapıldı.")
                
                # GitHub'a push işlemini güncellemelerden sonra gerçekleştir
                git_push()

        time.sleep(120)  # 2 dakika bekle

# Ana programın başlatılması
threading.Thread(target=update_spotify_data).start()

print("Uygulama çalışıyor. Çıkmak için herhangi bir tuşa basın.")
msvcrt.getch()  # Kullanıcı bir tuşa bastığında uygulama duracak
