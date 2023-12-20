# database-homework-T8
## 目标
- 建立一个OJ系统的提交查询页面
### 主要功能
- 登录界面（普通用户/管理员用户）
- 提交代码
- 查询提交记录
### 主要结构
#### 前端
- 登录页面
- 代码提交页面
- 提交记录查询页面
- 代码展示页面

#### 后端
- 不完整，待补充
- **提交记录：** **subbmit_id**[bigint unsigned], code[blob], *language_code*, code_len[int unsigned], *status_code*, *problem_id*, time_slot[timestamp], *user_id*
  - 提交状态：**status_code**[smallint unsigned], status_name[tinytext]
  - 语言：**language_code**[int unsigned], language_name[tinytext]
- **问题：** **problem_id**[int unsigned], problem[blob]
- **用户：** **user_id**[int unsigned], user_name[tinytext]

