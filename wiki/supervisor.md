### 关于restart指令
* `restart`指令是先`stop`再`start`，见源码：
```    def do_restart(self, arg):
        if not self.ctl.upcheck():
            return

        names = arg.split()

        if not names:
            self.ctl.output('Error: restart requires a process name')
            self.ctl.exitstatus = LSBInitExitStatuses.GENERIC
            self.help_restart()
            return

        self.do_stop(arg)
        self.do_start(arg)
```
而`stop`其实就是发送`stopsignal`指令：
```
    def stop(self):
        """ Administrative stop """
        self.administrative_stop = True
        self.laststopreport = 0
        return self.kill(self.config.stopsignal)
```
`stopsignal`默认是`TERM`，见[文档](http://supervisord.org/configuration.html)
* 对于Guicorn，`TERM`是安全的，[文档](https://docs.gunicorn.org/en/stable/signals.html)这么说：
  > TERM: Graceful shutdown. Waits for workers to finish their current requests up to the graceful_timeout
* 更好的重启Gunicorn的方法是发送`HUP`信号：
  >  HUP: Reload the configuration, start the new worker processes with a new configuration and gracefully shutdown older workers. If the application is not preloaded (using the preload_app option), Gunicorn will also load the new version of it.

  源码如下，参见[该贴](https://www.cnblogs.com/xybaby/p/6321929.html)的解读
```
    def handle_hup(self):
        """\
        HUP handling.
        - Reload configuration
        - Start the new worker processes with a new configuration
        - Gracefully shutdown the old worker processes
        """
        self.log.info("Hang up: %s", self.master_name)
        self.reload()

    def reload(self):
        old_address = self.cfg.address
 
        self.app.reload()
        self.setup(self.app)
 
        # reopen log files
        self.log.reopen_files()
 
        if old_address != self.cfg.address:
            # close all listeners
            [l.close() for l in self.LISTENERS]
            # init new listeners
            self.LISTENERS = create_sockets(self.cfg, self.log)
            listeners_str = ",".join([str(l) for l in self.LISTENERS])
            self.log.info("Listening at: %s", listeners_str)
 
        for i in range(self.cfg.workers):
            self.spawn_worker()
 
        self.manage_workers()
```                                                                                                                         