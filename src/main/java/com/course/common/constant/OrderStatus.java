package com.course.common.constant;

import com.baomidou.mybatisplus.annotation.EnumValue;
import com.fasterxml.jackson.annotation.JsonValue;
import lombok.Getter;

@Getter
public enum OrderStatus {
    PENDING(0, "待支付"),
    PAID(1, "已支付"),
    CANCELLED(2, "已取消");

    @EnumValue // 告诉 MyBatis-Plus 数据库存的是这个 code
    @JsonValue // 告诉 Jackson JSON 序列化时返回这个 code
    private final int code;
    private final String name;

    OrderStatus(int code, String name) {
        this.code = code;
        this.name = name;
    }
}