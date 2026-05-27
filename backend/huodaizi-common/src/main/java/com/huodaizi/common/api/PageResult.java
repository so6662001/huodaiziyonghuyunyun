package com.huodaizi.common.api;

import lombok.Data;
import lombok.NoArgsConstructor;

import java.io.Serializable;
import java.util.List;

/**
 * 分页响应
 *
 * @param <T> 列表项类型
 */
@Data
@NoArgsConstructor
public class PageResult<T> implements Serializable {

    private List<T> items;

    private Pagination pagination;

    public PageResult(List<T> items, long total, long pageSize, String nextPageToken) {
        this.items = items;
        this.pagination = new Pagination(pageSize, total, nextPageToken, nextPageToken != null);
    }

    @Data
    @NoArgsConstructor
    public static class Pagination {
        private Long pageSize;
        private Long total;
        private String nextPageToken;
        private Boolean hasMore;

        public Pagination(Long pageSize, Long total, String nextPageToken, Boolean hasMore) {
            this.pageSize = pageSize;
            this.total = total;
            this.nextPageToken = nextPageToken;
            this.hasMore = hasMore;
        }
    }
}
