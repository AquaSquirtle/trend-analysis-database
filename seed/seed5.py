def seed(cur, fake, COUNT):
    cur.execute('SELECT id FROM Company')
    company_ids = [row[0] for row in cur.fetchall()]
    
    cur.execute('SELECT id FROM Keyword')
    keyword_ids = [row[0] for row in cur.fetchall()]
    
    cur.execute('SELECT id FROM Hashtag')
    hashtag_ids = [row[0] for row in cur.fetchall()]
    
    if not company_ids or not keyword_ids or not hashtag_ids:
        print("Warning: Missing required data. Please seed companies, keywords, and hashtags first.")
        return
    
    time_periods = ['Last 7 days', 'Last 30 days', 'Last quarter', 'Last 6 months']
    trend_ids = []
    
    for company_id in company_ids:
        for _ in range(fake.random_int(2, 4)):
            cur.execute(
                'INSERT INTO TrendAnalysis('
                '  company_id, time_period, summary, created_at'
                ') VALUES (%s, %s, %s, %s) RETURNING id',
                (
                    company_id,
                    fake.random_element(time_periods),
                    fake.paragraph(nb_sentences=3),
                    fake.date_time_this_year()
                )
            )
            trend_id = cur.fetchone()[0]
            trend_ids.append(trend_id)

            keywords_for_trend = fake.random_elements(keyword_ids, 
                                                    length=fake.random_int(5, 10), 
                                                    unique=True)
            for rank, keyword_id in enumerate(keywords_for_trend, 1):
                cur.execute(
                    'INSERT INTO TrendKeyword('
                    '  trend_id, keyword_id, rank, score'
                    ') VALUES (%s, %s, %s, %s)',
                    (
                        trend_id,
                        keyword_id,
                        rank,
                        fake.random.uniform(0.1, 1.0)
                    )
                )
            hashtags_for_trend = fake.random_elements(hashtag_ids, 
                                                   length=fake.random_int(5, 10), 
                                                   unique=True)
            for rank, hashtag_id in enumerate(hashtags_for_trend, 1):
                cur.execute(
                    'INSERT INTO TrendHashtag('
                    '  trend_id, hashtag_id, rank, score'
                    ') VALUES (%s, %s, %s, %s)',
                    (
                        trend_id,
                        hashtag_id,
                        rank,
                        fake.random.uniform(0.1, 1.0)
                    )
                )
    content_formats = ['Blog post', 'Infographic', 'Video', 'Podcast', 'Case study', 'Interview']
    emotional_tones = ['Inspirational', 'Educational', 'Humorous', 'Provocative', 'Emotional']
    visual_styles = ['Minimalist', 'Bold colors', 'Dark mode', 'Retro', 'Futuristic']
    
    for company_id in company_ids:
        for _ in range(fake.random_int(3, 6)):
            cur.execute(
                'INSERT INTO ContentRecommendation('
                '  company_id, title, content_format, emotional_tone, visual_style, generated_at'
                ') VALUES (%s, %s, %s, %s, %s, %s)',
                (
                    company_id,
                    fake.sentence(nb_words=6),
                    fake.random_element(content_formats),
                    fake.random_element(emotional_tones),
                    fake.random_element(visual_styles),
                    fake.date_time_this_month()
                )
            )
            