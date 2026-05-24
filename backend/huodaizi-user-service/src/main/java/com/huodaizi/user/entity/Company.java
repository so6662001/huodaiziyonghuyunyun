package com.huodaizi.user.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import com.huodaizi.domain.entity.BaseEntity;
import lombok.Data;
import lombok.EqualsAndHashCode;

import java.time.LocalDateTime;

@Data
@EqualsAndHashCode(callSuper = true)
@TableName(value = "companies", autoResultMap = true)
public class Company extends BaseEntity {

    @TableId(type = IdType.INPUT)
    private String companyId;

    private String businessLicenseNo;

    private String name;

    private String legalPerson;

    private String legalPersonIdHash;

    private String registeredAddress;

    private String operatingAddress;

    private String province;

    private String city;

    private String district;

    private String industry;

    /** small / medium / large */
    private String scale;

    @TableField(typeHandler = com.baomidou.mybatisplus.extension.handlers.JacksonTypeHandler.class)
    private String ocrData;

    private Boolean manualFilled;

    private Boolean verified;

    /** L1 / L2 / L3 / L4 */
    private String verificationLevel;

    private LocalDateTime verifiedAt;
}
