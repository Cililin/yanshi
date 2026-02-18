package com.yanshi.service;

import com.baomidou.mybatisplus.core.metadata.IPage;
import com.yanshi.dto.ArticleQueryDTO;
import com.yanshi.dto.ArticleStatisticsDTO;
import com.yanshi.entity.Article;

import java.util.List;
import java.util.Map;

/**
 * 文章服务接口
 */
public interface ArticleService {

    IPage<Article> getArticlePage(ArticleQueryDTO query);

    Article getArticleById(Long id);

    List<Article> getRecentArticles(Integer limit);

    ArticleStatisticsDTO getStatistics();

    List<Map<String, Object>> countBySource();

    List<Map<String, Object>> countByCategory();

    List<Map<String, Object>> countByDate(String startDate, String endDate);
}
