# [SixJar](http://sixjar.ddns.net/)

## [Concept]
	Train the development of new concepts and technologies through accounting methods
1. Complete the understanding of front-end and back-end technologies of the website
2. Advance towards large-flow data processing

## [Technology Used]

### Backend
1. Flask(MVC)(ORM)(Blueprint) 
2. MySql
3. Redis
4. Authentication
	1. flask-login
	2. JWT (API)
	3. CSRF protection
5. RestApi 
	1. webargs 
	2. [api docs](http://sixjar.ddns.net/apispec/)
	
6. Plotly Express
7. Celery
8. SSE
9. Unit Test
10. Deploy
	1. Docker(file & compose)
	2. GoogleCloundEngine(use [noip](https://www.noip.com/) to apply domain and DNS)
### Frontend
1. Template,Form 
	1. Flask-WTF
	2. Jinja2
2. JS
	1. AJAX (Fetch)
	2. ES6、ES7
3. Bootstrap
4. jQuery
5. Plotly
6. RWD

### Features
1. Data visualization(Plotly)
2. Data CRUD(important data need input password)
3. Authentication
4. Random big data simulation(Celery＋SSE)
5. Check Jwt and request user consistency 

### Todo(next version)
1. celery periodic tasks exchange rate api write in redis
2. redis cache route
3. redis record web views


