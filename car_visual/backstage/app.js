const express = require('express');
const mysql = require('mysql');
const cors = require('cors');

// 创建 Express 应用
const app = express();
const PORT = 3000;

// 允许跨域请求
app.use(cors());

// 配置数据库连接
const db = mysql.createConnection({
    host: '127.0.0.1',
    "port":"3306",
    user: 'root',  // 替换为你的数据库用户名
    password: '123456',  // 替换为你的数据库密码
    database: '2024-04-14-300'  // 替换为你的数据库名
});

// 连接到数据库
db.connect(err => {
    if (err) {
        throw err;
    }
    console.log('Connected to database');
});

// 定义一个路由来获取所有车辆数据
app.get('/cars', (req, res) => {
    console.log(req.body);
    const sql = 'SELECT * FROM car';
    db.query(sql, (err, results) => {
        if (err) throw err;
        res.json(results);
    });
});

const bodyParser = require('body-parser');

// 使用 bodyParser 中间件来解析请求体
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

// 处理 POST 请求
app.post('/login', (req, res) => {
    console.log(req.body);
    const phone = req.body.phone; // 使用 req.body 获取请求体中的参数
    const sql = `SELECT * FROM user WHERE phone = ${phone}`;
    db.query(sql, (err, results) => {
        if (err) throw err;
        res.json(results);
    });
});

// 注册用户
app.post('/register', (req, res) => {
    const { phone, password } = req.body;

    // 检查用户是否已经存在
    const checkUserSql = 'SELECT * FROM user WHERE phone = ?';
    db.query(checkUserSql, [phone], (err, results) => {
        if (err) {
            console.error(err);
            res.status(500).json({ message: "Error checking user existence" });
            return;
        }
        if (results.length > 0) {
            // 如果找到了用户，说明手机号已经被注册了
            res.status(400).json({ message: "User already exists" });
        } else {
            // 用户不存在，可以安全地插入新用户
            // 这里使用参数化查询来避免SQL注入
            const insertSql = 'INSERT INTO user (phone, password) VALUES (?, ?)';
            db.query(insertSql, [phone, password], (err, results) => {
                if (err) {
                    console.error(err);
                    res.status(500).json({ message: "Error creating new user" });
                    return;
                }
                res.json({ message: "User registered successfully", userId: results.insertId });
            });
        }
    });
});

// 启动服务器
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
