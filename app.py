import streamlit as st
import requests

# 작품 검색
def search_artworks(query):
    url = "https://collectionapi.metmuseum.org/public/collection/v1/search"
    params = {"q": query}
    response = requests.get(url, params=params)
    return response.json().get("objectIDs", [])[:10]

# 작품 상세 조회
def get_artwork_details(object_id):
    url = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{object_id}"
    return requests.get(url).json()

# Streamlit 앱 시작
st.title("🎨 Explore Artworks with MET Museum API")

query = st.text_input("Search for Artworks:")

if query:
    ids = search_artworks(query)
    if not ids:
        st.warning("검색 결과가 없습니다. 다른 키워드를 입력해보세요.")
    else:
        for object_id in ids:
            data = get_artwork_details(object_id)

            st.subheader(data.get("title", "Untitled"))

            image_url = data.get("primaryImageSmall")
            if image_url:
                st.image(image_url, width=300)
            else:
                st.info("이미지가 없는 작품입니다.")

            artist = data.get("artistDisplayName") or "Unknown"
            year = data.get("objectDate") or "Unknown"

            st.write(f"👤 Artist: {artist}")
            st.write(f"📅 Year: {year}")

