import requests

# Daha önce aldığınız Access Token'ı buraya yapıştırın
access_token = "BQDobwQsw9sftdqGQi3SW4it49GXQJNWCgeOdIw0jvDM3W9SPAxr0pJ0W7bcZcczDetgzlfS6aB2YeUJZWqDXoxu4GgPU2Kz221ElGM8YJwk2TUnptV5F-ld7_w3PzZ4YBTRLh3ucTLLpa5nicYY6Uk6RbFiiUIOajmIv8N83cWvZHKRT4_BN_wvgGPrckCN76i_P34ilyowGahb75WjoL8"

# API isteği için başlıklar
headers = {
    "Authorization": f"Bearer {access_token}"
}

# En son dinlediklerinizi almak için istek
response = requests.get("https://api.spotify.com/v1/me/player/recently-played", headers=headers)

if response.status_code == 200:
    recently_played = response.json()
    for item in recently_played['items']:
        track = item['track']
        print(f"Şarkı: {track['name']}, Sanatçı: {', '.join(artist['name'] for artist in track['artists'])}, Albüm: {track['album']['name']}")
else:
    print("Hata:", response.text)
