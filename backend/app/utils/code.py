"""

1000: 数据库类错误
2000：书籍模块错误

"""

class Code:
    OK = 0
    UNKOWNERR = -1

StatusMap = {
    Code.OK: "Success",
    Code.UNKOWNERR: "UNKOWNERR"
}

# error_map = {
#     RET.OK: u"成功",
#     RET.DBERR: u"数据库查询错误",
#     RET.NODATA: u"无数据",
#     RET.DATAEXIST: u"数据已存在",
#     RET.DATAERR: u"数据错误",
#     RET.SESSIONERR: u"用户未登录",
#     RET.LOGINERR: u"用户登录失败",
#     RET.PARAMERR: u"参数错误",
#     RET.USERERR: u"用户不存在或未激活",
#     RET.ROLEERR: u"用户身份错误",
#     RET.PWDERR: u"密码错误",
#     RET.REQERR: u"非法请求或请求次数受限",
#     RET.IPERR: u"IP受限",
#     RET.THIRDERR: u"第三方系统错误",
#     RET.IOERR: u"文件读写错误",
#     RET.SERVERERR: u"内部错误",
#     RET.UNKOWNERR: u"未知错误",
# }
