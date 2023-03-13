# [SixJar](http://sixjar.ddns.net/)
## [專案連結]
[網站](http://sixjar.ddns.net/)
## [專案理念]
	藉由平時使用的記帳方法，訓練新觀念與技術的開發，完成一個網站前後端技術的了解

## [專案技術]

### 後端
1. Flask(MVC)(ORM)(Blueprint) 
2. MySql
3. Redis
4. Authentication
	1. flask-login
	2. JWT (API)
	3. CSRF protection
5. RestApi 
	1. webargs 資料驗證篩選
	2. [api docs](http://sixjar.ddns.net/apispec/)
6. Celery
7. SSE

### 前端
1. Template,Form 
	1. Flask-WTF
	2. Jinja2
2. JS
	1. AJAX (Fetch)
	2. ES6語法
3. Bootstrap
4. jQuery
5. Plotly
6. RWD

### 功能
1. plotly圖表資料呈現
2. 記帳資料的ＣＲＵＤ(重要操作密碼驗證)
3. 帳號驗證
4. 隨機大資料模擬(Celery＋SSE)

