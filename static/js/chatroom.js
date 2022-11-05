function randomString(e) {
  e = e || 32;
  var t = "ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678",
  a = t.length,
  n = "";
  for (i = 0; i < e; i++) n += t.charAt(Math.floor(Math.random() * a));
  return n
}


token1 = "pbkdf2:sha256:260000$cN9esYVIlunzqpf8$3fc61b946ead686b20dc26b9d4b96fa1ed6b59059a1e3115c7b12e9db37d0edb"
token2 = "pbkdf2:sha256:260000$l1hAFHbhXs7oDtqD$e12b3aa3e6a0dab11dff3b59afb3ae67e0ad508ea861900d6cbf935c09177d0c"
token3 = "没有捏"

$(document).ready(function() {

    var socket = io({
      extraHeaders: {
        "token": token3
      }
    });
    var user_name = '临时用户'+randomString(4)
    console.log(user_name)

    // 连接确认消息
    socket.on("connected",function (msg) {
        if(msg.status=='success'){
            user_name=msg.user_name
            $('#chatContent').append('<li>连接成功!</li>')

        }else{
            console.log("您的登陆信息有误, 请在header加上有效token!")
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


    // 接受信息
    socket.on('message', function (msg) {
        $('#chatContent').append('<li>'+msg.user_name+': '+msg.data+'</li>')
    })

    // 聊天框发送信息
    $('form#submitForm').submit(function(event) {
        socket.emit('send_message', {data: $('#broadcast_data').val(),
                                     room: $('#roomNum').val(),
                                     user_name: user_name
        })
        return false;
     })

})