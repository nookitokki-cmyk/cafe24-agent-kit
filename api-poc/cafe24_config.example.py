# cafe24_config.example.py
# 이 파일을 복사해서 cafe24_config.py 로 만들고 값을 채우세요.
# cafe24_config.py 는 .gitignore 로 git 추적에서 제외됩니다.

# 카페24 운영 몰 아이디 (호출 주소 https://{MALL_ID}.cafe24api.com 에 쓰임)
MALL_ID = ""

# 개발자센터에서 발급한 Admin API 앱 자격증명
CLIENT_ID = ""
CLIENT_SECRET = ""

# OAuth 리다이렉트 URI — 개발자센터 앱 설정에 "동일한 값"을 등록해야 함
REDIRECT_URI = "http://localhost:8888/callback"

# 요청할 권한 (읽기 검증용). 쓰기는 mall.write_design (별도 카페24 승인 필요)
SCOPE = "mall.read_design"

# API 버전 (문서 최신값)
API_VERSION = "2026-03-01"
