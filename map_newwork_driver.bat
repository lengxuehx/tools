:: no password
net use z: \\example.com\share /PERSISTENT:Yes


::need password
net use /delete s:
net use s: \\example.com\fileserver "@O&V423*" /user:fileserver /PERSISTENT:Yes
net use /delete s:
net use s: \\example.com\fileserver  /savecred /PERSISTENT:Yes
pause