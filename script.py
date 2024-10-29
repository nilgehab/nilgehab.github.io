import requests
import base64

# Spotify uygulamanızın bilgilerini buraya ekleyin
client_id = "645e194b1c514b1dbf780868d2128d0a"  # Kendi Client ID'nizi buraya yapıştırın
client_secret = "a852285a54ab4486bd162ffc458a97b7"  # Kendi Client Secret'inizi buraya yapıştırın
redirect_uri = "http://localhost:8888/callback"  # Redirect URI
auth_code = "AQC5BaGrt8aHJZzzxuXHHyT1c9e9Um67sNds3eKmV5pkGR1Blp4aAUsdvfIdevbqb-VhPCi5bALtX31WjGe4NnFsSBf9T0xXC3ri_KNn9cNTEuhPIwDjG8lxXCPt293outNfrdZ0EaX4s4J8eKWIVbJbNpiq_MLzUrBOalHYJdQC5prrkM-6KdfNKNbC2aOQ28dTLwqAaNBPP4T-vg"  # Aldığınız kodu buraya yapıştırın

# Yetkilendirme için Base64 kodlama
auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()

# İstek verileri
headers = {
    "Authorization": f"Basic {auth_header}",
    "Content-Type": "application/x-www-form-urlencoded"
}
data = {
    "grant_type": "authorization_code",
    "code": auth_code,
    "redirect_uri": redirect_uri
}

# Token alma isteği
response = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=data)

if response.status_code == 200:
    tokens = response.json()
    print("Access Token:", tokens["access_token"])
    print("Refresh Token:", tokens["refresh_token"])
else:
    print("Hata:", response.text)
