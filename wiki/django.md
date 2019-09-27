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
   
   
  ##allow hosts
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