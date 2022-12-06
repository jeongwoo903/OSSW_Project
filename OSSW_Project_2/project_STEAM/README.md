# 프로젝트 2 동기
스팀(steam)은 전세계에 게임을 판매하는 플랫폼입니다. 스팀은 정기적으로 게임 할인을 진행하고 있습니다. 저희는 '할인하는 게임만을 모아두는 서비스를 제작해보면 어떨까?'라는 아이디어가 떠올라 이 서비스를 제작하게 되었습니다.

# 프로젝트 2 사용 기술 및 흐름
프로젝트 1과 같이 프론트엔드는 HTML과 SCSS, 백엔드는 python 기반의 웹프레임워크인 장고(django)를 사용하였습니다.
   
스팀에 있는 게임과 관련된 정보는 [steam 공식 REST API](https://stackoverflow.com/questions/46330864/steam-api-all-games)와 [steamspy 사이트 REST API](http://steamspy.com/api.php)를 사용하였습니다. 파이썬에서 REST API를 호출할 때는 requests, requests_cache라는 오픈소스 라이브러리를 사용하였습니다.
   
프로젝트 2 서비스의 전체적인 작동 흐름은 다음과 같습니다.
   
웹페이지 접속 → steamspy 사이트 API를 통해 2주간 Top 100 게임 목록을 불러와 저장 → 불러온 게임 목록을 for문을 통해 하나씩 탐색 → 할인이 진행되는 게임의 경우 steam 공식 API를 통해 게임의 이미지, 가격 등 게임의 세부 정보를 불러와 저장 → 장고에서 HTML 파일 렌더 시 할인이 진행되는 게임 목록과 정보를 인자로 HTML 파일에 전달해줌 → 전달받은 값을 화면에 출력해줌

# 프로젝트 2 재밌는 점
할인하는 게임이 없다면 때로는 빈 페이지가 나오기도 하지만 그것도 나름대로 재미요소라고 생각합니다..😆

# 프로젝트 2 어려웠던 점
## 할인되는 게임만을 찾는 것의 어려움
steam 공식 REST API는 스팀 내 존재하는 모든 게임 목록을 불러오는 기능과 각 게임별 세부 판매 정보를 불러오는 기능을 제공합니다. 현재 스팀에는 1만개가 넘는 게임이 존재합니다. 그렇기에 스팀 게임의 모든 목록을 API를 통해 불러온 후 게임별로 할인이 진행되는지 하나씩 API로 쿼리하는 것은 속도나 효율성 측면에서 어렵다고 판단하였습니다.
   
따라서 저희는 '사람들이 많이 찾는 게임은 할인을 할 확률이 높지 않을까?'라는 생각을 바탕으로 Top 100 게임 목록 내에서 할인하는 것만을 보여주는 것으로 탐색 대상을 줄였습니다. Top 100 목록을 얻는 것은 steamspy 사이트에서 제공하는 REST API를 통해 2주간 Top 100 게임 목록을 불러오는 것으로 해결하였습니다.

## REST API 사용의 한계
### REST API로 데이터를 불러올 때 속도의 한계
steamspy REST API로 Top 100 게임 목록을 불러오는 것은 많은 시간이 들지 않았습니다. 하지만 가격, 이미지 등 할인하는 게임의 정보를 불러오고자 steam 공식 REST API로 각 게임마다 데이터를 가져오는 부분에서는 시간이 많이 사용됨을 파악하였습니다. 데이터를 가져오는 시간이 늘어나니 페이지를 로딩하는 속도 또한 많이 느려지는 문제점이 있었습니다.

### steam 공식 API의 할당량 제한
steam 공식 API의 경우 ip당 5분에 최대 200개의 요청만을 처리하도록 api 할당량 제한이 있었습니다. 만약 100개의 게임 목록 중 50개가 할인을 진행한다면 4번의 새로고침만으로도 api 할당량 제한에 걸리는 문제점이 있었습니다.

### 해결법 (캐시 도입)
위 2가지 문제점을 해결하고자 저희는 캐시를 도입하였습니다. 기본적으로 파이썬의 requests 라이브러리를 이용하여 REST API를 호출할 경우 캐시가 생성되지 않습니다. 따라서 requests 라이브러리 기능에 캐시를 도입한 requests_cache 라이브러리를 통해 REST API에서 불러온 데이터를 캐시하는 방식을 도입하였습니다. 그래서 처음 REST API를 호출하는 경우 응답 받은 데이터를 requests_cache 라이브러리가 자동으로 sqlite 파일에 캐시하게 설정하였습니다.

## 동적인 리스트 페이지 & 4열 리스트의 구현
이번 프로젝트의 프론트 파트를 구현하는 것에 있어서 신경을 썻던 부분은 레이아웃 이였습니다. 할인된 게임 리스트가 HTML에 정적으로 삽입 되어있는 것이 아니라 API를 통해 동적으로 값을 불러왔기 때문에 어느 크기만큼의 게임 리스트가 들어갈지를 알 수 없었습니다. 또한 디자인 적으로 4열로 구성된 페이지를 구현 하고 싶었습니다. 두 문제를 한 번에 해결하기 위해 장고에서 제공하는 HTML 문법을 이용하여 document element를 동적으로 생성하여 HTML에 집어 넣었고 Grid css를 사용하여 nx4 형태의 구조를 완성할 수 있었습니다. 

이 프로젝트가 만약 JS를 이용하여 구현 되었다면, JS파일을 하나 더 만들어 객체를 생성하고 axios를 통해 서버로 부터 값을 받아 온 뒤, 생성해둔 객체에 값을 집어 넣고 반복문을 사용하여 HTML에 document element를 동적으로 삽입하여야 했을 것입니다.

# 프로젝트 2 완성
https://user-images.githubusercontent.com/48091866/205693092-1f290049-ba07-4f39-9449-80cb60f9d03e.mp4