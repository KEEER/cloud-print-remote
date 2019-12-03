Cloud Print Remote
==================
  This is the document describing the structure and tasks of this project.
  
分工
---
- account_related
  - [x] Request Job Codes (Egamad)
  - [x] Request Job Token (Queue)
  - [x] Delete Job Token (Queue)
  - [x] Print (Queue)
  - [ ] Login (Andy)
- independent
  - [x] Calculate Price (Egamad)
- printer_related
  - [ ] Request Printer IPs (Welen)
  - [ ] Update Printer IP (Welen)
  - [ ] Status Report (Andy)


APIs
---
| API               | 描述                                                 |
| ----------------- | ---------------------------------------------------- |
| Login             | 登录（或注册）Cloud Print打印服务                    |
| DeleteJobToken    | 删除打印任务                                         |
| RequestJobCodes   | 列举用户下的所有打印任务的打印码                     |
| RequestJobToken   | 每一次文件上传或需求更改时索求用以标明身份的打印口令 |
| RequestPrinterIPs | 索求打印机群的最新内网IP地址                         |
| UpdatePrinterIP   | 更新打印机IP地址                                     |
| CalculatePrice    | 基于打印配置计算价格                                 |
| Print             | 支付并打印一项打印任务                               |
| StatusReport      | 报告打印机状态                                       |

###### Login 登录（或注册）

  `GET /`

  该接口将反馈一个重定向至KAS的自定义登录页进行继续操作；完成后一个名为 `kas-account-token` 会跳转至主页。

  

###### RequestJobCodes

  `GET /_api/codes`

  列举用户下的所有打印任务的打印码



返回参数

| 参数名    | 参数类型      | 是否一定存在 | 解释                                            |
| --------- | ------------- | ------------ | ----------------------------------------------- |
| codes     | Array<string> | 是           | 所有打印码的列表                                |
| timestamp | int           | 是           | 时间戳                                          |
| sign      | String<32>    | 是           | 对于打印码以`','`连接后与时间戳直接拼接后的签名 |

###### RequestJobToken（索求打印口令）

  `GET /_api/job-token`

  该接口将通过用户的KAS口令（存储于cookie）换取一个可以表明让终端服务器信任的身份的打印口令。

请求参数

| 参数名 | 参数类型 | 是否一定存在 | 解释                                                     |
|--------|----------|--------------|----------------------------------------------------------|
| code   | string   | 否           | 用于在终端服务器输入开始打印任务的唯一打印码；新任务留空 |

  返回参数

| 参数名    | 参数类型   | 是否一定存在 | 解释                                                         |
| --------- | ---------- | ------------ | ------------------------------------------------------------ |
| code      | string     | 是           | 用于在终端服务器输入开始打印任务的唯一打印码                 |
| timestamp | int        | 是           | 时间戳                                                       |
| sign      | String(32) | 是           | 使用RSA加密过的包含之前两项以字符串形式拼接的SHA256哈希签名，解密方式为使用终端服务器的公钥进行解密。 |

###### DeleteJobToken（删除打印任务）

  `GET /_api/delete-job-token`

  该接口将通过用户的KAS口令（存储于cookie）删除一个打印任务。如果存在签名项，则通过签名确认发起调用者身份，确认后将任务删除


请求参数

| 参数名 | 参数类型 | 是否一定存在 | 解释                                                     |
|--------|----------|--------------|----------------------------------------------------------|
| code   | string   | 是           | 用于标明即将删除的打印任务。 |
| sign   | string   | 否           |  终端服务器调用时存在。使用RSA加密过的包含`code`的SHA256哈希签名，解密方式为使用终端服务器的公钥进行解密。 |

###### RequestPrinterIPs（索求打印机地址）

  `GET /_api/printer-ips`

  该接口将通过用户的打印服务会话口令换取全部打印机的IP地址（以供测试是否可访问）

  请求参数：无

  返回参数

| 参数名 | 参数类型     | 是否一定存在 | 解释               |
|--------|--------------|--------------|--------------------|
|        | List<String> | 是           | 全部打印机的IP地址 |

- 对于 `printer-ips` 参数的进一步解释：

```json
[
  "172.17.136.183",
  "172.17.134.178",
  "172.17.58.96",
  "172.17.147.32"
]
```

  

###### UpdatePrinterIP（更新打印机IP地址）

  `POST /_api/printer-ip`

  终端在IP地址变更时异步请求该接口更新打印机IP地址。

  请求参数

| 参数名 | 参数类型   | 是否必须 | 解释         |
|--------|------------|----------|--------------|
| id     | String     | 是       | 打印机编码   |
| ip     | String     | 是       | 当前打印机IP |
| sign   | String(32) | 是       | 对于签名     |

  返回参数

  此API成功调用后无返回值（返回为头状态码200的空字符串）

###### CalculatePrice（计算价格）

  `GET /_api/calculate-price`

  该接口允许用户通过打印配置计算价格。

  请求参数

| 参数名 | 参数类型     | 是否必须 | 解释     |
| ------ | ------------ | -------- | -------- |
| id     | string       | 是       | 打印机ID |
| config | Object(Json) | 是       | 打印配置 |

  返回参数

| 参数名 | 参数类型 | 是否一定存在 | 解释           |
|--------|----------|--------------|----------------|
| price  | int      | 是           | 价格，单位为分 |

###### Print（打印并支付）

  `GET /_api/print`

  请求参数

| 参数名 | 参数类型   | 是否必须 | 解释                       |
| ------ | ---------- | -------- | -------------------------- |
| code   | string     | 是       | 打印码                     |
| config | String     | 是       | 打印参数，JSON编码         |
|        | string     | 是       | 打印机ID                   |
| sign   | String<32> | 是       | 对于前两项字符串拼接的签名 |

   - 对于 `configs` 的进一步解释如下：

```json
{
   "page-count": 1,
   "colored": true,
   "double-sided": false
}
```

  返回参数

| 参数名  | 参数类型 | 是否一定存在 | 解释                           |
|---------|----------|--------------|--------------------------------|
| status  | int      | 是           | 支付结果状态                   |
| message | string   | 是           | 来自服务器对支付结果状态的解释 |

###### StatusReport

`POST /_api/status-report`

报告打印机异常状态

请求参数 打印机 `GET /status` 的消息，或连接错误信息

返回参数 无


Some Helpful Things to copy-paste
---
```
# [In-project modules]

# [Python native modules]

# [Third-party modules]

```

draft
---
```
[printer1]
max = 10
black = 1,2,3,4,5,6,7,8,10
colored = 2,4,6,8,10,12,14,16,18,20

{}
```
