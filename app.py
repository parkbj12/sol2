from flask import Flask, render_template_string,redirect, request, jsonify
import openai
import pandas as pd


# OpenAI API 키 설정 (본인의 OpenAI API 키를 사용하세요)
app = Flask(__name__)

# CSV 파일 로드 (파일 경로를 본인의 CSV 파일 경로로 변경하세요)
try:
    data = pd.read_csv('C:\chat-gpt-prg\ch06\서울시 생활체육포털 우리동네 프로그램.csv', encoding='cp949')
except FileNotFoundError:
    print("CSV file not found. Please check the file path.")
    data = pd.DataFrame()  

# Print column names to check the correct column name
print(data.columns)

template = '''
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>서울시 피트니스 네트워크</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box; 
        }
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            padding: 20px;
        }
        header {
            background-color: #333;
            color: #fff;
            padding: 1rem;
            text-align: center;
        }
        .container {
            max-width: 800px;
            margin: 20px auto;
        }
        .chat-container {
            margin: 20px 0;
        }
        .chat-box {
            width: 100%;
            height: 300px;
            border: 1px solid #ccc;
            padding: 10px;
            overflow-y: scroll;
        }
        .chat-input {
            margin-top: 10px;
            display: flex;
        }
        .chat-input input {
            width: 80%;
            padding: 10px;
        }
        .chat-input button {
            width: 20%;
            padding: 10px;
            background-color: #007bff;
            color: white;
            border: none;
            cursor: pointer;
        }
        .api-key-container {
            margin-bottom: 20px;
        }
        .api-key-input {
            width: 100%;
            padding: 10px;
            margin-bottom: 10px;
            border: 1px solid #ccc;
            border-radius: 4px;
        }
        .user-message {
            float: right;
            background-color: #f0f0f0;
            padding: 8px;
            border-radius: 10px;
            margin: 5px 0;
            max-width: 80%;
            display: inline-block;
            clear: both;
        }
        .bot-response {
            float: left;
            background-color: #d0f0c0;
            padding: 8px;
            border-radius: 10px;
            margin: 5px 0;
            max-width: 80%;
            display: inline-block;
            clear: both;
        }
    </style>
</head>
<body>
    <header>
        <h1>서울시 피트니스 네트워크</h1>
    </header>
    <div class="container">
        <!-- API 키 입력란 -->
        <div class="api-key-container">
            <h3>OpenAI API 키 입력</h3>
            <input type="text" id="api-key" class="api-key-input" placeholder="API 키를 입력하세요">
        </div>
    </section>

    <section id="map">
  <div class="banner">
    <h2>서울특별시 지역 선택</h2>
    <img src="https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyMzEwMDNfMjYy%2FMDAxNjk2MzI5NDU4Nzc2.aOCTdfY18de7L41hBjp9pYCZHF1wDKHaFaoaAZiVM8sg.3YLCSSm8RdNwOPhtFkSsgcQWy0Xsh-lwyfa6mSDTH40g.PNG.sunstory77%2Fimage.png&type=sc960_832" alt="서울특별시 지도" usemap="#seoul-map">
      
    <map name="seoul-map">
            <area target="" alt="강서구" title="강서구" href="/강서구" coords="129,256,34" shape="circle">
            <area target="" alt="양천구" title="양천구" href="/양천구" coords="180,332,28" shape="circle">
            <area target="" alt="은평구" title="은평구" href="/은평구" coords="289,148,34" shape="circle">
            <area target="" alt="도봉구" title="도봉구" href="/도봉구" coords="438,95,23" shape="circle">
            <area target="" alt="노원구" title="노원구" href="/노원구" coords="501,136,24" shape="circle">
            <area target="" alt="강북구" title="강북구" href="/강북구" coords="416,140,21" shape="circle">
            <area target="" alt="중랑구" title="중랑구" href="/중랑구" coords="526,195,26" shape="circle">
            <area target="" alt="강동구" title="강동구" href="/강동구" coords="599,270,22" shape="circle">
            <area target="" alt="송파구" title="송파구" href="/송파구" coords="548,346,24" shape="circle">
            <area target="" alt="성북구" title="성북구" href="/성북구" coords="416,201,25" shape="circle">
            <area target="" alt="동대문구" title="동대문구" href="/동대문구" coords="466,226,24" shape="circle">
            <area target="" alt="광진구" title="광진구" href="/광진구" coords="517,283,24" shape="circle">
            <area target="" alt="종로구" title="종로구" href="/종로구" coords="356,222,24" shape="circle">
            <area target="" alt="서대문구" title="서대문구" href="/서대문구" coords="287,231,30" shape="circle">
            <area target="" alt="중구" title="중구" href="/중구" coords="382,267,24" shape="circle">
            <area target="" alt="성동구" title="성동구" href="/성동구" coords="446,279,25" shape="circle">
            <area target="" alt="마포구" title="마포구" href="/마포구" coords="277,285,24" shape="circle">
            <area target="" alt="용산구" title="용산구" href="/용산구" coords="357,312,26" shape="circle">
            <area target="" alt="강남구" title="강남구" href="/강남구" coords="469,369,30" shape="circle">
            <area target="" alt="서초구" title="서초구" href="/서초구" coords="403,389,28" shape="circle">
            <area target="" alt="동작구" title="동작구" href="/동작구" coords="323,361,26" shape="circle">
            <area target="" alt="영등포구" title="영등포구" href="/영등포구" coords="261,334,25" shape="circle">
            <area target="" alt="관악구" title="관악구" href="/관악구" coords="309,423,27" shape="circle">
            <area target="" alt="금천구" title="금천구" href="/금천구" coords="240,425,24" shape="circle">
            <area target="" alt="구로구" title="구로구" href="/구로구" coords="151,378,26" shape="circle">
    </map>
  </div>
</section>


    <section id="chatbot">
    <!-- 챗봇 영역 -->
        <div class="chat-container">
            <h3>🏋️GYM 챗봇🏋️</h3>
            <div id="chat-box" class="chat-box">
                <div class="bot-response"><strong>챗봇:</strong> 안녕하세요! 무엇을 도와드릴까요?</div>
            </div>
            <div class="chat-input">
                <input type="text" id="user-input" placeholder="질문을 입력하세요..." onkeyup="handleEnter(event)">
                <button onclick="sendMessage()">전송</button>
            </div>
        </div>
    </div>

    <script>
        let apiKey = "";

        // API 키 설정
        document.getElementById('api-key').addEventListener('input', (event) => {
            apiKey = event.target.value;
        });

        function handleEnter(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }

        // 메시지 전송 함수
        function sendMessage() {
            const userInput = document.getElementById('user-input').value;
            const chatBox = document.getElementById('chat-box');
            const userMessage = `<div class="user-message"><strong>사용자:</strong> ${userInput}</div>`;
            chatBox.innerHTML += userMessage;
            document.getElementById('user-input').value = ''; // 입력란 초기화

            // API 호출
            fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: userInput, api_key: apiKey }),
            })
            .then(response => response.json())
            .then(data => {
                const botMessage = `<div class="bot-response"><strong>챗봇:</strong> ${data.response}</div>`;
                chatBox.innerHTML += botMessage;
                chatBox.scrollTop = chatBox.scrollHeight; // 스크롤 최신 메시지로 이동
            });
        }
    </script>
</body>
</html>
'''

# OpenAI API 호출 함수
def generate_response(api_key, user_input):
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input}
        ],
        max_tokens=100
    )
    return response.choices[0].message['content'].strip()

@app.route('/')
def home():
    return render_template_string(template)

# 각 구에 대한 라우트 추가
# 용산, 은평 데이터는 X

@app.route('/<district>', methods=['GET', 'POST'])
def get_district_data(district):
    # 특정 구에 해당하는 데이터 필터링
    district_data = data[data['지역구'] == district].head(300)
    
    # 검색어 처리: lambda와 apply 함수로 검색어 포함 행 필터링
    search_query = request.form.get('search', '').lower()
    if search_query:
        district_data = district_data[district_data.apply(
            lambda row: search_query in row.astype(str).str.lower().to_string(), axis=1)]
    
    # 첫 번째 컬럼(일련번호)을 제외한 데이터를 HTML로 변환
    district_content = district_data.iloc[:, 1:].to_html(index=False, classes='table table-striped')
    
    # HTML 템플릿 및 스타일 포함
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{{ district }} 데이터</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            body {
                font-family: Arial, sans-serif;
                line-height: 1.6;
            }
            header {
                background-color: #333;
                color: #fff;
                padding: 1rem;
                text-align: center;
            }
            .container {
                max-width: 1200px;
                margin: 20px auto;
                padding: 20px;
            }
            input[type="text"] {
                padding: 10px;
                width: 300px;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
            button {
                padding: 10px 20px;
                background-color: #28a745;
                color: white;
                border: none;
                border-radius: 4px;
                cursor: pointer;
            }
            button:hover {
                background-color: #218838;
            }
            .table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }
            .table th, .table td {
                padding: 12px;
                text-align: left;
                border: 1px solid #ddd;
            }
            .table-striped tbody tr:nth-child(odd) {
                background-color: #f9f9f9;
            }
        </style>
    </head>
    <body>
        <header>
            <h1>{{ district }} 데이터</h1>
        </header>
        <div class="container">
            <form action="/" method="get" style="text-align: right;">
                <button type="submit">홈으로 돌아가기</button>
            </form>
            <h2>{{ district }}의 시설 목록</h2>
            <form method="post" style="margin: 20px 0;">
                <input type="text" name="search" placeholder="검색어 입력">
                <button type="submit">검색</button>
            </form>
            {{ content|safe }}
        </div>
    </body>
    </html>
    ''', content=district_content, district=district)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get('message')
    api_key = data.get('api_key')

    if not api_key or not user_input:
        return jsonify({'response': 'API 키와 메시지를 입력해주세요.'})

    try:
        response = generate_response(api_key, user_input)
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'response': f"오류가 발생했습니다: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)

    
