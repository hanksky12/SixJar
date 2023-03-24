# [SixJar](http://sixjar.ddns.net/)

## [Concept]
	Train the development of new concepts and technologies through accounting methods
1. Complete the understanding of front-end and back-end technologies of the website
2. Advance towards large-flow data processing

## [Technology Used]

### Backend
1. Flask(MVC)(ORM)(Blueprint) 
2. DB
    1. MySql
    2. Redis
3. Authentication
    1. flask-login(session-based)
    2. JWT (API)
    3. CSRF protection
4. RestApi 
    1. webargs 
    2. [api docs](http://sixjar.ddns.net/apispec/)	
5. Plotly Express
6. Celery(Routing tasks、Periodic tasks)
7. Redis
    1. Cache-aside (Lazy-loading)
    2. Record web views
8. SSE
9. Unit Test
10. Deploy
     1. Docker(file & compose)
     2. GoogleCloudEngine(Use [No-Ip](https://www.noip.com/) to apply for Domain and DNS)
### Frontend
1. Template,Form 
	1. Flask-WTF
	2. Jinja2
2. JS(Ajax (Fetch))
3. Bootstrap
4. jQuery
5. Plotly
6. RWD

### Features
1. Data visualization(Plotly)
2. Data CRUD(important data need user password input)
3. Authentication
4. Random big data simulation(Asynchronous task：Celery+SSE)
5. Check Jwt and request user consistency 
6. Redis cache (based on Cache-aside (Lazy-loading))
7. Periodic tasks crawler exchange rate 

### Todo(next)
1. Wsgi + Nginx docker setting


