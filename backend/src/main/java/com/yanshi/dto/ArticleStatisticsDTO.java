package com.yanshi.dto;

import java.time.LocalDate;

/**
 * 文章统计DTO
 */
public class ArticleStatisticsDTO {

    private Long totalCount;
    private Long xinhuaCount;
    private Long peopleCount;
    private LocalDate minDate;
    private LocalDate maxDate;
    private Long todayCount;

    public Long getTotalCount() { return totalCount; }
    public void setTotalCount(Long totalCount) { this.totalCount = totalCount; }

    public Long getXinhuaCount() { return xinhuaCount; }
    public void setXinhuaCount(Long xinhuaCount) { this.xinhuaCount = xinhuaCount; }

    public Long getPeopleCount() { return peopleCount; }
    public void setPeopleCount(Long peopleCount) { this.peopleCount = peopleCount; }

    public LocalDate getMinDate() { return minDate; }
    public void setMinDate(LocalDate minDate) { this.minDate = minDate; }

    public LocalDate getMaxDate() { return maxDate; }
    public void setMaxDate(LocalDate maxDate) { this.maxDate = maxDate; }

    public Long getTodayCount() { return todayCount; }
    public void setTodayCount(Long todayCount) { this.todayCount = todayCount; }
}
