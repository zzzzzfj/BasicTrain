# SSH上传
git push git@github.com:zzzzzfj/BasicTrain.git

# 后端接口说明

* token 

	* 发送的token都放在header

	* 用户端通过login获得token, 以后每次访问要带上token

	* 目前内容就是 user_id, 未加密, 之后再搞

* IP = http://81.70.55.211:5000

* 目前数据库的内容有

	* user表

		```
		id	email					password	user_type	
		1	123456@qq.com			123456789	student	
		2	654321@163.com			123456789	teacher	
		3	hhh@ustc.mail.edu.cn	123456789	admin	
		4	11111@ustc.mail.edu.cn	123456789	student	
		5	11111@ustc.mail.edu.cn	123456789	student	
		6	11111@ustc.mail.edu.cn	123456789	student	
		```

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
		5	3		4			2022-10-13 	14:57:15	1	
		6	3		1			2022-10-13 	14:57:32	4	
		7	6		2			2022-10-13 	14:57:43	4	
		8	1		3			2022-10-13 	14:57:53	4	
		9	5		3			2022-10-13 	14:57:56	4	
		10	6		4			2022-10-13 	14:58:09	4	
		11	6		4			2022-10-13 	14:58:09	4	
		12	2		1			2022-10-13 	14:58:23	6	
		13	1		2			2022-10-13 	14:58:27	6	
		14	6		2			2022-10-13 	14:58:30	6	
		15	6		3			2022-10-13 	14:58:34	6	
		16	6		1			2022-10-13 	14:58:46	4	
		```

	



# 接口

### 登陆

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
	"status": "success"
		"data":{
			"token": 1 		
		}
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
	        "average_grade": "4.2",
	        "expression_num": "5",
	        "student_num": "3",
	        "variance": "18.80"
	    },
	    "status": "success"
	}
	```

	



### 创建课程

* 不急

