package com.huodaizi.user.controller;

import cn.dev33.satoken.annotation.SaCheckLogin;
import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.huodaizi.common.api.ErrorCode;
import com.huodaizi.common.api.Result;
import com.huodaizi.common.exception.BusinessException;
import com.huodaizi.common.util.IdGenerator;
import com.huodaizi.user.entity.Company;
import com.huodaizi.user.mapper.CompanyMapper;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import jakarta.validation.constraints.NotBlank;
import lombok.Data;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

@Tag(name = "Companies", description = "企业管理")
@RestController
@RequestMapping("/api/v1/companies")
@RequiredArgsConstructor
public class CompanyController {

    private final CompanyMapper companyMapper;

    @Operation(summary = "创建企业账户")
    @SaCheckLogin
    @PostMapping
    public Result<Company> create(@Valid @RequestBody CreateCompanyRequest request) {
        Company existing = companyMapper.selectOne(
                new LambdaQueryWrapper<Company>()
                        .eq(Company::getBusinessLicenseNo, request.getBusinessLicenseNo())
        );
        if (existing != null) {
            throw new BusinessException(ErrorCode.COMPANY_ALREADY_EXISTS);
        }

        Company company = new Company();
        company.setCompanyId(IdGenerator.companyId());
        company.setBusinessLicenseNo(request.getBusinessLicenseNo());
        company.setName(request.getName());
        company.setLegalPerson(request.getLegalPerson());
        company.setRegisteredAddress(request.getRegisteredAddress());
        company.setIndustry(request.getIndustry());
        company.setManualFilled(true);
        company.setVerified(false);
        company.setVerificationLevel("L1");
        companyMapper.insert(company);

        return Result.success(company);
    }

    @Operation(summary = "OCR 识别营业执照")
    @SaCheckLogin
    @PostMapping(value = "/ocr", consumes = "multipart/form-data")
    public Result<OcrResponse> ocr(@RequestParam("image") MultipartFile image) {
        // TODO: 调用 ai-service 的 OCR 接口
        OcrResponse response = new OcrResponse();
        response.setBusinessLicenseNo("MOCK-" + System.currentTimeMillis());
        response.setCompanyName("（OCR 结果待 AI 服务接入）");
        response.setOcrConfidence(0.0);
        return Result.success(response);
    }

    @Operation(summary = "查询企业")
    @GetMapping("/{id}")
    public Result<Company> get(@PathVariable("id") String companyId) {
        Company company = companyMapper.selectById(companyId);
        if (company == null) {
            throw new BusinessException(ErrorCode.COMPANY_NOT_FOUND);
        }
        return Result.success(company);
    }

    @Data
    public static class CreateCompanyRequest {
        @NotBlank
        private String businessLicenseNo;

        @NotBlank
        private String name;

        private String legalPerson;
        private String registeredAddress;
        private String industry;
    }

    @Data
    public static class OcrResponse {
        private String businessLicenseNo;
        private String companyName;
        private String legalPerson;
        private String registeredAddress;
        private Double ocrConfidence;
    }
}
