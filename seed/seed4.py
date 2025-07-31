def seed(cur, fake, COUNT):
    cur.execute('SELECT id FROM Company')
    company_ids = [row[0] for row in cur.fetchall()]
    
    cur.execute('SELECT id FROM ContentPost')
    post_ids = [row[0] for row in cur.fetchall()]
    
    if not company_ids or not post_ids:
        print("Warning: No companies or posts found. Please seed those first.")
        return
    keyword_ids = []
    used_keyword = []
    for company_id in company_ids:
        for _ in range(fake.random_int(5, 10)):
            t = 0
            keyword = fake.word()
            while t < 10 and keyword in used_keyword:
                keyword = fake.word()
                t += 1
            if t >= 10:
                continue                
            used_keyword.append(keyword)
            cur.execute(
                'INSERT INTO Keyword('
                '  company_id, keyword, is_auto_generated, weight'
                ') VALUES (%s, %s, %s, %s) RETURNING id',
                (
                    company_id,
                    keyword,
                    fake.boolean(30),
                    fake.random.uniform(0.1, 1.0)
                )
            )
            keyword_id = cur.fetchone()[0]
            keyword_ids.append(keyword_id)
    hashtag_ids = []
    used_hashtags = []
    for company_id in company_ids:
        for _ in range(fake.random_int(5, 15)):
            t = 0
            tag = "#" + fake.word()
            while t < 10 and tag in used_hashtags:
                tag = "#" + fake.word()
                t += 1
            used_hashtags.append(tag)
            if t >= 10:
                continue
            try:
                cur.execute(
                    'INSERT INTO Hashtag('
                    '  company_id, tag, is_auto_generated, popularity_score'
                    ') VALUES (%s, %s, %s, %s) RETURNING id',
                    (
                        company_id,
                        tag,
                        fake.boolean(25),
                        fake.random.uniform(0.1, 1.0)
                    )
                )
                hashtag_id = cur.fetchone()[0]
                hashtag_ids.append(hashtag_id)
            except:
                continue

    for post_id in post_ids:
        hashtags_for_post = fake.random_elements(hashtag_ids, length=fake.random_int(3, 8), unique=True)
        for hashtag_id in hashtags_for_post:
            cur.execute(
                'INSERT INTO PostHashtag('
                '  post_id, hashtag_id'
                ') VALUES (%s, %s) ON CONFLICT DO NOTHING',
                (post_id, hashtag_id)
            )
    for post_id in post_ids:
        keywords_for_post = fake.random_elements(keyword_ids, length=fake.random_int(2, 5), unique=True)
        for keyword_id in keywords_for_post:
            cur.execute(
                'INSERT INTO PostKeyword('
                '  post_id, keyword_id'
                ') VALUES (%s, %s) ON CONFLICT DO NOTHING',
                (post_id, keyword_id)
            )