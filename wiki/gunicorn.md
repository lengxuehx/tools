* 参数`max_request`可以一定程度上避免内存泄露： 处理请求数目达到限定值的worker会被重启，
辅以`max_requests_jitte`参数，可以防止所有worker同时被重启
