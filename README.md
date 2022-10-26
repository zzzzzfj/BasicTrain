

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

	* column_name: []  // 列名数组
	* Contents: [[], [], [],...]  // 内容二维数组

* 示例

	```
	http://127.0.0.1:5000/admin/query?account_type=student&page_size=3&which_page=2
	```

	```
	{
	    "data": {
	        "column_name": [
	            "id",
	            "email",
	            "password",
	            "student_number",
	            "name",
	            "age",
	            "gender",
	            "grade",
	            "classroom",
	            "major",
	            "phone_number"
	        ],
	        "contents": [
	            [
	                4,
	                "654321@qq.com",
	                "123456789",
	                "SA22232222",
	                "Jone",
	                15,
	                null,
	                null,
	                null,
	                null,
	                "13777888888"
	            ],
	            [
	                5,
	                "654321@163.com",
	                "123456789",
	                "SA22672223",
	                "Mike",
	                20,
	                null,
	                null,
	                null,
	                null,
	                "13777888889"
	            ],
	            [
	                6,
	                "654321@ustc.edu.cn",
	                "123456789",
	                "SA12222224",
	                "ZhouTian",
	                21,
	                null,
	                null,
	                null,
	                null,
	                "13777888886"
	            ]
	        ]
	    },
	    "status": "success"
	}
	```

	

### 管理员添加账户





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





# 功能更新

### v2 

* 重构
	* 增加登陆表: 包含user_id, user_type, token (仅退出登陆时删除表项, 重复登陆时覆盖, 不自动过期)
	* 修改用户表, 根据user_type拆分为3个表
	* 增加请求过滤
		* 登陆页面会返回token(根据user_id, user_type, 当前时间 哈希加密的长字符串)
		* 其他页面均需该token才能访问, 否则返回401状态码(要求重定向到登陆页面)

* 图表功能: 查询每个分数的总人数

	* 例

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

* 邮箱登陆: `/login/email_captcha`接口

* 管理员账号管理:  `IP/admin`各接口

	* 查询
	* 添加 / 删除: 等v3再做

* 退出登陆功能: `/logout`接口

	* 清除登录表中该项





# SSH上传
git push git@github.com:zzzzzfj/BasicTrain.git