### 用requests发送数据时，使用data参数，content-type是application/x-www-form-urlencoded；使用json参数，content-type是application/json；同时使用data和files参数，content-type是multipart/form-data

* json:

`r = requests.post('http://192.168.89.37:8001/animation_pipeline/entity/', json={'p': [1,2]})`

`r.request.headers`

`{'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate', 'Connection': 'keep-alive', 'Content-Type': 'application/json', 'User-Agent': 'python-requests/2.19.1', 'Content-Length': '13'}`

* data:

`r = requests.post('http://192.168.89.37:8001/animation_pipeline/entity/', data={'p': [1,2]})`

`r.request.headers`

 `{'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate', 'Connection': 'keep-alive', 'Content-Type': 'multipart/form-data; boundary=9e4553945e3c3c5e70d75345e3fb2ff8', 'User-Agent': 'python-requests/2.19.1', 'Content-Length': '506'}`

`r.request.body`

`'p=1&p=2`

* 同时有data和file参数 

`r = requests.post('http://192.168.89.37:8001/animation_pipeline/entity/', data={'name': 'st12', 'code': 'st12', 'project_id': [1,2]},  files={'file': f})`

r.request.headers

`{'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate', 'Connection': 'keep-alive', 'Content-Type': 'multipart/form-data; boundary=9e4553945e3c3c5e70d75345e3fb2ff8', 'User-Agent': 'python-requests/2.19.1', 'Content-Length': '506'}`

 `r.request.body`

 `b'--9e4553945e3c3c5e70d75345e3fb2ff8\r\nContent-Disposition: form-data; name="name"\r\n\r\nst12\r\n--9e4553945e3c3c5e70d75345e3fb2ff8\r\nContent-Disposition: form-data; name="project_id"\r\n\r\n1\r\n--9e4553945e3c3c5e70d75345e3fb2ff8\r\nContent-Disposition: form`
`-data; name="project_id"\r\n\r\n2\r\n--9e4553945e3c3c5e70d75345e3fb2ff8\r\nContent-Disposition: form-data; name="code"\r\n\r\nst12\r\n--9e4553945e3c3c5e70d75345e3fb2ff8\r\nContent-Disposition: form-data; name="file"; filename="timg.jpg"\r\n\r\n\r\n--9e4553945e3c3c5e70d75`
`345e3fb2ff8--\r\n'`

* 接受数据

在drf端，接受数据时，取数组的方式也是不一样的：对于json，直接取：request.data['p']；而对于application/x-www-form-urlencoded，则要用request.data.getlist('p'),如果只用request.data['p'], 则只能取到数组的最后一个值。




