### 关于django-session
* jango.contrib.sessions.backends.signed_cookies

   加密后的cookie保存在客户端，形如：`.eJxVjDsOwjAQBe-yNbLkbJwgSnrOYO3HiwPIluKkQtwdIqUg7ZuZ94ZI65Lj2tIcJ4ULdHD635jkmcoG9EHlXp3UsswTu01xO23uVjW9rrt7OMjU8q8Wr0nIEM9kAwpq4I7ZQgjo-0FN0HsarYfPFwxAMfE:1hm7p0:Q-BpxUBNSza_vIrUAyCAUvQWTqQ`，
   其中`.eJxVjDsOwjAQBe-yNbLkbJwgSnrOYO3HiwPIluKkQtwdIqUg7ZuZ94ZI65Lj2tIcJ4ULdHD635jkmcoG9EHlXp3UsswTu01xO23uVjW9rrt7OMjU8q8Wr0nIEM9kAwpq4I7ZQgjo-0FN0HsarYfPFwxAMfE:1hm7p0`
   是value，`Q-BpxUBNSza_vIrUAyCAUvQWTqQ`是signature，`1hm7p0`是timestamp，客户端访问服务端时，
   要先验证签名是否合法，即服务端对value签名后看看是不是`Q-BpxUBNSza_vIrUAyCAUvQWTqQ`
   验证签名合法后，再进行base64解码、zlib解压缩，即得到最终数据，类似如下形式：
   
      {
        '_auth_user_backend': 'django.contrib.auth.backends.ModelBackend',
        '_auth_user_hash': 'c1decaf338af63c3d5b2bbf5553146dfc311a7f4',
        '_auth_user_id': '2'
      }
   其中`_auth_user_hash`是用户的`password(加密后的)`和`salt`经过*hmac*后的值，
   服务端还要做一次*hmac*，以验证结果是不是`c1decaf338af63c3d5b2bbf5553146dfc311a7f4`
 
 * django.contrib.sessions.backends.cache
 
   客户端只保存session_id，服务端根据session_id从cache取出session_data，形式和上面解码、解密后的一样：
      
       {
        '_auth_user_backend': 'django.contrib.auth.backends.ModelBackend',
        '_auth_user_hash': 'c1decaf338af63c3d5b2bbf5553146dfc311a7f4',
        '_auth_user_id': '2'
       }
    后面的_auth_user_hash验证也和上面一样

    
### 关于django-filter
* ModelChoiceFilter 

      assignees = django_filters.ModelChoiceFilter(
        field_name='assignees', method='filter_assignees', queryset=models.Member.objects.all()
      ) 
    
      def filter_assignees(self, queryset, name, value):     
           split_values = value.split(',')               
           return queryset.filter(assignees__in=split_values)
    
   这里*value*会被转成*assignees*对应的object也就是Member，而不是原始的查询字段，如"1,2"；如果写成下面这样，则value就是原始的查询
   字符"1,2"了。如果不想写filter method，查询语句就用多key的形式：key=1&key=2，且filte field选用ModelChoiceFilter即可
   
      assignees = django_filters.CharFilter(field_name='assignees', method='filter_assignees')`
      
      def filter_assignees(self, queryset, name, value):
          split_values = value.split(',')
          return queryset.filter(assignees__in=split_values)
          
### WSGI & ASGI
* WSGi只支持HTTP协议
* ASGI支持HTTP, HTTP/2, WebSockets

### django-channels
* channel的认证：客户端可以先通过http请求取得token，然后在与服务端建立连接时带上token，服务端认证成功后，双方以后就可以在
此连接上通讯了（连接成功后，客户端发送消息时不需要在带上token了，相见[这里](https://stackoverflow.com/a/32619655/2272451)
和[这里](https://devcenter.heroku.com/articles/websocket-security#validate-server-data)

### WSGI
* wsgi server和wsgi client的最小实现

       def run_application(application):
        """Server code."""
        # This is where an application/framework stores
        # an HTTP status and HTTP response headers for the server
        # to transmit to the client
        headers_set = []
        # Environment dictionary with WSGI/CGI variables
        environ = {}

        def start_response(status, response_headers, exc_info=None):
            headers_set[:] = [status, response_headers]
    
        # Server invokes the ‘application' callable and gets back the
        # response body
        result = application(environ, start_response)
        # Server builds an HTTP response and transmits it to the client
        ...
    
        def app(environ, start_response):
            """A barebones WSGI app."""
            start_response('200 OK', [('Content-Type', 'text/plain')])
            return [b'Hello world!']
        
        run_application(app)
        
 * [how it works](https://ruslanspivak.com/lsbaws-part2/):
   * The framework provides an ‘application’ callable (The WSGI specification doesn’t prescribe how that should be implemented)
   * The server invokes the ‘application’ callable for each request it receives from an HTTP client. It passes a dictionary ‘environ’ containing WSGI/CGI variables and a ‘start_response’ callable as arguments to the ‘application’ callable.
   * The framework/application generates an HTTP status and HTTP response headers and passes them to the ‘start_response’ callable for the server to store them. The framework/application also returns a response body.
   * The server combines the status, the response headers, and the response body into an HTTP response and transmits it to the client (This step is not part of the specification but it’s the next logical step in the flow and I added it for clarity)
   
   
## allow hosts
  * 如果nginx的server_name没有添加域名的话，则报如下错误：
    ```
    <html>
        <head>
            <title>403 Forbidden</title></head>
            <body bgcolor="white">
                <center><h1>403 Forbidden</h1></center>
                <hr><center>nginx/1.14.0 (Ubuntu)</center>
            </body>
    </html>
    ```
  * 如果django.settings的ALLOWED_HOSTS没有将添加域名的话，则报如下错误：
  
     ```<h1>Bad Request (400)</h1>```
     
## select_related 和 prefetch_related
* `select_related`用于one-to-one和foreignkey，一对多(包括foreignkey的反查)和多对多都是不行的，详见[此贴](https://timmyomahony.com/blog/misconceptions-select_related-in-django/)

* `select_related`实际用的的Inner Join，详见[此贴](https://learnbatta.com/blog/working-with-select_related-in-django-89/)，文档这么说：
  > prefetch_related in most cases will be implemented using an SQL query that uses the ‘IN’ operator. This means that for a large QuerySet a large ‘IN’ clause could be generated, 
  which, depending on the database, might have performance problems of its own when it comes to parsing or executing the SQL query. Always profile for your use case!

* `select_related`规避1对多，是怕join导致行数过多(规模变化是倍乘的，详见[该贴](https://stackoverflow.com/a/45377282/2272451))

* `select_related`是一次数据库查询，而`prefetch_related`是多次数据库查询(先查到IDs列表然后用`SELECT ... WHERE pk IN (...,...,...)`)，详见[此贴](https://stackoverflow.com/a/31237071/2272451)

* `Pizza.objects.all().prefetch_related('toppings')`查询了两次数据库，文档这么说：
     
    > We can reduce to just two queries using prefetch_related
    
* `Restaurant.objects.prefetch_related('pizzas__toppings')`查询了三次数据库，文档这么说：
    > This will prefetch all pizzas belonging to restaurants, and all toppings belonging to those pizzas. This will result in a total of 3 database queries - one for the restaurants, 
    > one for the pizzas, and one for the toppings.
     
* `prefetch_related` 会导致查询立即生效，而不是等到evaluate的时候，文档这么说：
    > Note that the result cache of the primary QuerySet and all specified related objects will then be fully loaded into memory. This changes the typical behavior of QuerySets, 
    which normally try to avoid loading all objects into memory before they are needed, even after a query has been executed in the database.

* 两者区别，django文档这么说：
    > select_related works by creating an SQL join and including the fields of the related object in the SELECT statement. For this reason, select_related gets the related objects in the same database query. However, to avoid the much larger result set that would result from joining across a ‘many’ relationship, select_related is limited to single-valued relationships - foreign key and one-to-one.
    
    > prefetch_related, on the other hand, does a separate lookup for each relationship, and does the ‘joining’ in Python. This allows it to prefetch many-to-many and many-to-one objects, which cannot be done using select_related, in addition to the foreign key and one-to-one relationships that are supported by select_related.
    
## 数据库连接 
* django默认会把`CONN_MAX_AG`设置为0，结果就是每个请求都会打开一个连接，结束后关闭连接，参见
[该贴](https://andrewkowalik.com/posts/django-database-connnections-in-kafka/)、
[该贴](https://stackoverflow.com/questions/19937257/what-is-a-good-value-for-conn-max-age-in-django)
和[这个讨论](https://groups.google.com/forum/#!topic/django-developers/NwY9CHM4xpU)
* 如果想提高性能，保持连接，可以设置`CONN_MAX_AGE`大于0，见[该贴](https://www.revsys.com/tidbits/django-performance-simple-things/)
* 关闭连接是通过信号来做的：`signals.request_finished.connect(close_connection)`,[该贴](https://stackoverflow.com/a/1346401/2272451)
非常值得一读：
  > It turns out Django uses signals.request_finished.connect(close_connection) to close the database connection it normally uses. Since nothing normally happens in Django that doesn't involve a request, you take this behavior for granted.

  > In my case, though, there was no request because the job was scheduled. No request means no signal. No signal means the database connection was never closed.