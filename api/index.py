from flask import Flask, request, Response, jsonify
import random
import requests
import time
import json  # استخدام مكتبة JSON المدمجة

app = Flask(__name__)

HEADERS = {
    'Accept': '*/*',
    'Accept-Language': 'ar-AE,ar;q=0.9,en-IN;q=0.8,en;q=0.7,en-US;q=0.6',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://checker1.visatk.com',
    'Pragma': 'no-cache',
    'Referer': 'https://checker1.visatk.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
}
CHECK_URL = 'https://checker1.visatk.com/api.php'
BOT_LINK = 'https://t.me/APIZXLLLL'
BY_LINE = 'BY: HP LVL'

saroty = ('2031', '2024', '2023', '2025', '2026', '2027', '2028', '2029', '2030')
bn = ('536498', '527519', '483698', '422061')
sa = ('01', '02', '03', '04', '05', '06', '10', '11', '12', '13', '14')
Q = '0123456789'

def generate_card():
    bin_number = random.choice(bn)
    account_number = ''.join(random.choices(Q, k=10))
    expiry_year = random.choice(saroty)
    expiry_month = random.choice(sa)
    cvv = ''.join(random.choices(Q, k=3))
    return f"{bin_number}{account_number}|{expiry_year}|{cvv}"

def check_visa(card):
    data = {'data': card}
    response = requests.post(CHECK_URL, headers=HEADERS, data=data)
    if response.status_code == 200:
        return response.json()
    else:
        return {"status": "error", "message": "Failed to check visa"}

@app.route('/gen_check', methods=['GET'])
def generate_and_check():
    try:
        count = int(request.args.get('count', 3))
        if count <= 0 or count > 100:
            return jsonify({
                "status": "error",
                "message": "Invalid count value. Must be between 1 and 100.",
                "by": BY_LINE,
                "link": BOT_LINK
            })
        
        def generate_stream():
            yield '{"status": "streaming", "by": "' + BY_LINE + '", "link": "' + BOT_LINK + '", "results": ['
            first = True
            for _ in range(count):
                if not first:
                    yield ','
                card = generate_card()
                result = check_visa(card)
                output = {
                    "visa": card,
                    "result": result.get('status', 'Unknown'),
                    "message": result.get('message', 'No message'),
                    "valid": result.get('status', '').lower() == 'success'
                }
                yield json.dumps(output)  # استخدام مكتبة JSON لتنسيق البيانات
                first = False
                time.sleep(0.5)
            yield ']}'

        return Response(generate_stream(), content_type='application/json')

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "by": BY_LINE,
            "link": BOT_LINK
        })

if __name__ == '__main__':
    app.run(debug=True)
