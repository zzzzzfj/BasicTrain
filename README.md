

# 后端接口说明

* token 

	* 发送的token都放在header
	* 除登陆页面外, 所有访问都需在header带上有效token, 否则拒绝访问
	
* IP = http://81.70.55.211:5000

* 目前数据库的内容有

	* student表(部分)

	  ```
	  id	email	password	student_number	name	age	gender	grade	classroom	major	phone_number	
	  1	123456@qq.com	123456789	SA22222222	LiHua	NULL	男	NULL	NULL	NULL	13777888888	
	  2	123456@163.com	123456789	SA22222223	Amy	NULL	女	NULL	NULL	NULL	13777888889	
	  ```
	
	* teacher表
	
	  ```
	  id	email	password	name	age	gender	phone_number	
	  1	222222@qq.com	123456789	ZhouShaohua	43	男	13773288823	
	  2	222222@163.com	123456789	TianTian	26	女	13877876889	
	  ```
	
	* admin表(类似)
	
	* class表
	
		```
		id	course_name		 course_code	
		1	算法设计与分析		CS233	
		2	组合数学		  MA111	
		3	算法导论		  CS123	
		4	美学			   AR123
		```
	
	* expression表 (可以自己通过comment添加)
	
		```
		id	grade	course_id	date_time				student_id	
		1	2		1			2022-10-13 	14:56:45	1	
		2	3		2			2022-10-13 	14:56:56	1	
		3	3		3			2022-10-13 	14:57:02	1	
		4	6		3			2022-10-13 	14:57:10	1
		```
	
	



# 接口

### 普通登陆

* 发送

	* address = IP/login
	* method = POST 
	* content = json
		* email, password, user_type('student','teacher','admin')

* 返回

	* json
		* token

* 示例

	```
	# post json内容
	{
	    "email": "123456@qq.com",
	    "password": "123456789",
	    "user_type": "student"
	}
	```

	```
	# 返回 token
	# 格式: 
	#	{"status":"success","data":{ }} 或
	#	{"status":"error","data":{"info":""}}
	{
	    "data": {
	        "token": "pbkdf2:sha256:260000$UVWRgqnbyX8josmk$b305648296b9f0d4b219b650588b5951f0440f55f622881c23c4542f093bf544"
	    },
	    "status": "success"
	}
	```



### 发送邮箱验证码

* 发送

	* address = IP/login/send_email_captcha
	* method = "POST"
	* content = json
		* email, user_type
	* 返回json, 成功与否

	```
	{
	    "email": "123456@qq.com",
	    "user_type": "student"
	}
	```

	```
	{
	    "status": "success"
	}
	```

	* 注
		* 120s后会过期, 重复发送会覆盖
		* 建议60秒冷却(验证码发送按钮)



### 通过邮箱验证码登陆

* 发送

	* address = IP/login/verify_email_captcha
	* method = "POST"
	* content = json
		* email, captcha
	* 返回json, 成功与否

	```
	{
	    "email": "123456@qq.com",
	    "captcha": ""
	}
	```

	```
	{
	    "data": {
	        "token": "pbkdf2:sha256:260000$UVWRgqnbyX8josmk$b305648296b9f0d4b219b650588b5951f0440f55f622881c23c4542f093bf544"
	    },
	    "status": "success"
	}
	```

	





### 进入课程(学生/老师)

* 发送

	* address = IP/student/enter_course
		* 如果是老师: address = IP/teacher/enter_course
	* method = GET
	* 参数
		* token
		* course_code: 如 CS231, 严格5位

* 返回

	* json
		* course_id

* 示例

	```
	http://81.70.55.211:5000/student/enter_course?course_code=CS233
	```

	```
	{
	    "data": {
	        "course_id": "1",
	        "course_name": "算法设计与分析"
	    },
	    "status": "success"
	}
	```

	

### 打分(学生)

* 发送

	* address = IP/student/comment
	* method = POST
	* content = json
		* grade: 1-6
		* course_id

* 返回: bool

	* 是否成功

* 示例

	```
	{
	    "token": "1",
	    "course_id": "2",
	    "grade": "2"
	}
	```

	```
	{
	    "data": {
	        "course_name": "组合数学",
	        "grade": "2"
	    },
	    "status": "success"
	}
	```



### 查询(老师)

* 发送

	* address = IP/teacher/query
	* method = GET
	* 参数
		* token
		* datetime_start
		* datetime_end
		* course_id
		* return_type = "json" / "excel"

* 返回:

	* student_num 
	* expression_num
	* average_grade
	* variance //方差

* 注

	* 前端1分钟调用一次, 形成图表

* 示例:

	```
	# 起始终点时间以时间戳形式给出
	http://81.70.55.211:5000/teacher/query?datetime_start=1065656175&datetime_end=1765656175&course_id=3&return_type=json
	```

	```
	{
    "data": {
        "average_grade": "2.461538461538461538461538462",
        "expression_num": "13",
        "number_of_grade1": "2",
        "number_of_grade2": "7",
        "number_of_grade3": "2",
        "number_of_grade4": "1",
        "number_of_grade5": "0",
        "number_of_grade6": "1",
        "student_num": "5",
        "variance": "21.23076923076923076923076922"
    },
    "status": "success"
    }
	```

* 注: 不做身份验证, 有有效token就能查(为了debug方便)





### 管理员查询(账号展示)

* 发送

	* address = IP/admin/query
	* method = GET
	* 参数
		* account_type  // 账户类型
		* page_size  // 每页条数
		* which_page  // 第几页

* 返回:

	* Contents: [...]  // 列表, 每个成员为json对象

* 示例

	```
	http://127.0.0.1:5000/admin/query?account_type=teacher&page_size=2&which_page=1
	```

	```
	{
	    "data": {
	        "contents": [
	            {
	                "age": 43,
	                "email": "222222@qq.com",
	                "gender": "男",
	                "id": 4,
	                "name": "ZhouShaohua",
	                "password": "123456789",
	                "phone_number": "13773288823"
	            },
	            {
	                "age": 26,
	                "email": "222222@163.com",
	                "gender": "女",
	                "id": 5,
	                "name": "TianTian",
	                "password": "123456789",
	                "phone_number": "13877876889"
	            }
	        ]
	    },
	    "status": "success"
	}
	```

	

### 管理员添加账户

* 发送

	* address = IP/admin/add_account
	* method = POST
	* json
		* account_type
		* 其他属性
			* 学生
				* 必有: email, password, name, student_number
				* 可选: age, gender, grade, classroom, major, phone_number
			* 教师/管理员
				* 必有: email, password, name
				* 可选: age, gender, phone_number

* 返回:

	* 成功或失败, 以及用户id (便于测试删除功能)

* 例:

	```
	{
	    "account_type":"student",
	    "email":"111113@qq.com",
	    "password":"123456789",
	    "name":"WOTM",
	    "student_number":"SA2314153525",
	    "gender":"男"   
	}
	```

	```
	{
	    "data": {
	        "user_id": 27
	    },
	    "status": "success"
	}
	```

	



### 管理员删除账户

* 发送

	* address = IP/admin/delete_account
	* method = POST
	* json
		* user_type
		* user_id

* 返回:

	* 成功或失败

* 例:

	```
	{
	    "account_type":"student",
	    "user_id":25
	}
	```

	```
	{
	    "status": "success"
	}
	```

	



### 退出登陆功能

* 发送

	* address = IP/logout
	* method = POST 
	* content = 无(header带上有效token即可)

* 返回

	```
	{
	    "status": "success"
	}
	```



### 讨论区(WebSocket实现)

* 接口address: http://81.70.55.211:5000

* 前端demo: http://81.70.55.211:5000

* 前端示例代码(js)

	```JavaScript
	
	token1 = "pbkdf2:sha256:260000$cN9esYVIlunzqpf8$3fc61b946ead686b20dc26b9d4b96fa1ed6b59059a1e3115c7b12e9db37d0edb"
	token2 = "pbkdf2:sha256:260000$l1hAFHbhXs7oDtqD$e12b3aa3e6a0dab11dff3b59afb3ae67e0ad508ea861900d6cbf935c09177d0c"
	
	$(document).ready(function() {
	
	    // header带token, 连接时根据token会返回user_name, 以后每次发消息请带上该user_name
	    var socket = io({
	      extraHeaders: {
	        "token": token2
	      }
	    });
	    var user_name = ""
	
	    // 连接返回消息
	    socket.on("connected",function (msg) {
	        if(msg.status=='success'){
	            user_name=msg.user_name
	            $('#chatContent').append('<li>连接成功!</li>')
	        }else{
	            alert("您的登陆信息有误, 请在header加上有效token!")
	        }
	    })
	
	    // 加入房间请求, 房间号为roomNum, 即课程id
	    $('form#joinRoom').submit(function(event) {
	        socket.emit('joinRoom', {room: $('#roomNum').val(), user_name: user_name})
	        return false;
	    });
	    // 离开房间请求, 房间号为roomNum
	    $('#leave_room').on('click', function (event) {
	        socket.emit('leaveRoom', {room: $('#roomNum').val(), user_name: user_name})
	        return false;
	    });
	
	    // 广播给房间内所有人的加入房间信息
	    socket.on("roomJoined", function (msg, cb) {
	        $('#chatContent').append('<li>'+msg.user_name+'已加入房间'+msg.room+'</li>')
	    })
	
	    // 个人离开房间的信息
	    socket.on("roomLeftPersonal", function (msg) {
	        console.log(msg.room)
	        $('#chatContent').append('<li>'+'您已离开房间'+'</li>')
	    })
	    // 广播给房间内所有人的离开房间信息
	    socket.on("roomLeft", function (msg, cb) {
	        $('#chatContent').append('<li>'+msg.user_name+'已离开房间'+msg.room+'</li>')
	    })
	
	    
	    // 聊天框发送信息
	    $('form#submitForm').submit(function(event) {
	        socket.emit('send_message', {data: $('#broadcast_data').val(),
	                                     room: $('#roomNum').val(),
	                                     user_name: user_name
	        })
	        return false;
	     })
	    // 接收信息
	    socket.on('message', function (msg) {
	        $('#chatContent').append('<li>'+msg.user_name+': '+msg.data+'</li>')
	    })
	
	
	})
	```

* 连接

	* 说明: header请带上有效token

	* 连接返回信息: `connected`

		* 成功

			```
			'connected',  
			{
				'status': 'success',
				'user_name': user_row.name
			}
			```

			> connected为消息名, {}内为消息内容

		* 失败

			```
			'connected', {'status': 'error'}
			```

	* 建议

		* 请记录下返回的user_name, 以后每次发送消息需要带上(给别的用户看)

* 进入及退出房间

	* 说明: 房间号即为课程id, 仅同房间可以接收到消息

		* 在加入课程时根据课程id进入时间

	* 进入房间

		* 发送

			* 类型: 'joinRoom'
			* 内容: 'room'(课程号)

		* 返回 (该房间内所有人会收到)

			```
			"roomJoined", 
			{
			        "room": 1,
			        'user_name': '李华'
			}
			```

	* 退出房间

		* 发送

			* 类型: 'leaveRoom'
			* 内容: 'user_name',  'room'(课程号)

		* 返回

			* 发送者会收到

				```
				"roomLeftPersonal", {
				    'user_name': '李华'
				    "room": 23
				}
				```

			* 其他人会收到

				```
				"roomLeft", {
				    'user_name': '李华'
				    "room": 23
				}
				```

			

* 发送与接收消息

	* 发送消息

		* 类型: 'send_message'
		* 内容: 'user_name', 'room',  'data'

	* 返回(同房间内所有人会收到)

		```
		'message', 
		{
			'data': '你好',
		    'user_name': '李华'
		 }
		```

		







# 功能更新

### v2 

* 重构
	* 增加登陆表: 包含user_id, user_type, token (仅退出登陆时删除表项, 重复登陆时覆盖, 不自动过期)
	* 修改用户表, 根据user_type拆分为3个表
	* 增加请求过滤
		* 登陆页面会返回token(根据user_id, user_type, 当前时间 哈希加密的长字符串)
		* 其他页面均需该token才能访问, 否则返回401状态码(要求重定向到登陆页面)

* 教师查询功能: 增加查询每个分数的总人数
* 邮箱登陆: `/login/email_captcha`接口
* 管理员账号管理:  `IP/admin/query`查询功能
* 退出登陆功能: `/logout`接口



### v3

* 管理员账号管理: 

	* 添加 / 删除功能
* 讨论区功能(socketio)



# SSH上传
git push git@github.com:zzzzzfj/BasicTrain.git