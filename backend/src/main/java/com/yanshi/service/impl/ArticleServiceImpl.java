package com.yanshi.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.core.metadata.IPage;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.yanshi.dto.ArticleQueryDTO;
import com.yanshi.dto.ArticleStatisticsDTO;
import com.yanshi.entity.Article;
import com.yanshi.mapper.ArticleMapper;
import com.yanshi.service.ArticleService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;
import org.springframework.util.StringUtils;

import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.List;
import java.util.Map;

/**
 * 文章服务实现
 */
@Service
public class ArticleServiceImpl extends ServiceImpl<ArticleMapper, Article> implements ArticleService {

    private static final Logger log = LoggerFactory.getLogger(ArticleServiceImpl.class);

    private final ArticleMapper articleMapper;

    public ArticleServiceImpl(ArticleMapper articleMapper) {
        this.articleMapper = articleMapper;
    }

    @Override
    public IPage<Article> getArticlePage(ArticleQueryDTO query) {
        Page<Article> page = new Page<>(query.getPage(), query.getPageSize());
        return articleMapper.selectArticlePage(page, query);
    }

    @Override
    public Article getArticleById(Long id) {
        return articleMapper.selectById(id);
    }

    @Override
    public List<Article> getRecentArticles(Integer limit) {
        Page<Article> page = new Page<>(1, limit);
        LambdaQueryWrapper<Article> wrapper = new LambdaQueryWrapper<>();
        wrapper.orderByDesc(Article::getPublishDate, Article::getId);
        IPage<Article> result = articleMapper.selectPage(page, wrapper);
        return result.getRecords();
    }

    @Override
    public ArticleStatisticsDTO getStatistics() {
        ArticleStatisticsDTO dto = new ArticleStatisticsDTO();
        dto.setTotalCount(articleMapper.selectCount(null));

        List<Map<String, Object>> sourceStats = countBySource();
        for (Map<String, Object> stat : sourceStats) {
            String source = (String) stat.get("source");
            Long count = ((Number) stat.get("count")).longValue();
            if ("新华网".equals(source)) {
                dto.setXinhuaCount(count);
            } else if ("人民网".equals(source)) {
                dto.setPeopleCount(count);
            }
        }

        try {
            Map<String, Object> dateRange = articleMapper.getDateRange();
            if (dateRange != null) {
                dto.setMinDate((LocalDate) dateRange.get("minDate"));
                dto.setMaxDate((LocalDate) dateRange.get("maxDate"));
            }
        } catch (Exception e) {
            log.error("获取日期范围失败", e);
        }

        try {
            dto.setTodayCount(articleMapper.countToday());
        } catch (Exception e) {
            log.error("获取今日数量失败", e);
            dto.setTodayCount(0L);
        }

        return dto;
    }

    @Override
    public List<Map<String, Object>> countBySource() {
        return articleMapper.countBySource();
    }

    @Override
    public List<Map<String, Object>> countByCategory() {
        return articleMapper.countByCategory();
    }

    @Override
    public List<Map<String, Object>> countByDate(String startDate, String endDate) {
        LocalDate start = StringUtils.hasText(startDate) ?
            LocalDate.parse(startDate, DateTimeFormatter.ISO_LOCAL_DATE) : null;
        LocalDate end = StringUtils.hasText(endDate) ?
            LocalDate.parse(endDate, DateTimeFormatter.ISO_LOCAL_DATE) : null;
        return articleMapper.countByDate(start, end);
    }
}
