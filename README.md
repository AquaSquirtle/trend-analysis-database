## Платформа для анализа трендов в соц. сетях

## Функциональные требования

### Пользователь
1. **Управление аккаунтом**
   - Регистрация (имя, email, телефон)
   - Редактирование профиля

2. **Работа с компаниями**
   - Создание/удаление компаний
   - Ввод данных: категория, тип бизнеса, название, услуги, локация, описание, соцсети
   - Редактирование информации

3. **Ключевые слова и хештеги**
   - Просмотр автоматически сгенерированных тегов
   - Ручное редактирование списка

4. **Аналитика**
   - Фильтрация постов по:
     - Дате публикации
     - Типу контента
     - Показателям вовлеченности (лайки/комментарии/репосты)
     - Демографии аудитории
   - Просмотр трендов

5. **Рекомендации**
   - Получение советов по:
     - Формату контента
     - Call-to-Action (CTA)
     - Эмоциональному стилю
     - Визуальному оформлению
   - Использование готовых сводок по трендам

---

### Система
1. **Автогенерация**
   - Ключевых слов и хештегов
   - Сводок трендов:
     - Популярные теги
     - Рекомендуемые форматы
     - Оптимальное время публикации

2. **Аналитика**
   - Сбор данных из соцсетей
   - Выявление актуальных трендов
   - Формирование рекомендаций:
     - Стиль контента
     - CTA
     - Визуальные элементы
     - Тайминг публикаций

3. **Фильтрация**
   - По заданным параметрам:
     - Вовлеченность
     - Временной период
     - Тип контента

---

## ER-диаграмма 

```plantuml

entity User {
  + id [PK]
  --
  name: varchar
  email: varchar(unique)
  phone: varchar
  password_hash: varchar
  created_at: timestamp
}

entity Company {
  + id [PK]
  --
  user_id [FK -> User.id]
  category: varchar
  business_type: varchar
  name: varchar
  description: text
  location: varchar
  created_at: timestamp
}

entity SocialNetwork {
  + id [PK]
  --
  name: varchar(unique)
  (Instagram, VK, Telegram, etc.)
}

entity CompanySocialLink {
  + id [PK]
  --
  company_id [FK -> Company.id]
  social_id [FK -> SocialNetwork.id]
  url: varchar
}

entity ContentPost {
  + id [PK]
  --
  company_id [FK -> Company.id]
  social_id [FK -> SocialNetwork.id]
  external_id: varchar
  content_type: enum(text,image,video)
  text_content: text
  publish_date: timestamp
  url: varchar
}

entity PostMetric {
  + id [PK]
  --
  post_id [FK -> ContentPost.id]
  likes: integer
  comments: integer
  shares: integer
  views: integer
  updated_at: timestamp
}

entity PostDemographics {
  + id [PK]
  --
  post_id [FK -> ContentPost.id]
  age_group: varchar
  value: float
}

entity PostGender {
  + id [PK]
  --
  post_id [FK -> ContentPost.id]
  gender: enum(male, female, other)
  value: float
}

entity PostGeo {
  + id [PK]
  --
  post_id [FK -> ContentPost.id]
  region: varchar
  value: float
}

entity Keyword {
  + id [PK]
  --
  company_id [FK -> Company.id]
  keyword: varchar
  is_auto_generated: boolean
  weight: float
}

entity Hashtag {
  + id [PK]
  --
  company_id [FK -> Company.id]
  tag: varchar(unique)
  is_auto_generated: boolean
  popularity_score: float
}

entity TrendAnalysis {
  + id [PK]
  --
  company_id [FK -> Company.id]
  time_period: varchar
  summary: text
  created_at: timestamp
}

entity TrendKeyword {
  + id [PK]
  --
  trend_id [FK -> TrendAnalysis.id]
  keyword_id [FK -> Keyword.id]
  rank: integer
  score: float
}

entity TrendHashtag {
  + id [PK]
  --
  trend_id [FK -> TrendAnalysis.id]
  hashtag_id [FK -> Hashtag.id]
  rank: integer
  score: float
}

entity ContentRecommendation {
  + id [PK]
  --
  company_id [FK -> Company.id]
  title: varchar
  content_format: varchar
  emotional_tone: varchar
  visual_style: varchar
  generated_at: timestamp
}

entity PostingSchedule {
  + id [PK]
  --
  company_id [FK -> Company.id]
  best_day: varchar
  best_time: time
  effectiveness_score: float
}

entity ContentTypeAnalysis {
  + id [PK]
  --
  company_id [FK -> Company.id]
  content_type: varchar
  engagement_rate: float
}

entity PostHashtag {
  + post_id [FK -> ContentPost.id]
  + hashtag_id [FK -> Hashtag.id]
}

entity PostKeyword {
  + post_id [FK -> ContentPost.id]
  + keyword_id [FK -> Keyword.id]
}

' --- Relations ---

User ||--o{ Company

Company ||--o{ CompanySocialLink
Company ||--o{ ContentPost
Company ||--o{ Keyword
Company ||--o{ Hashtag
Company ||--o{ TrendAnalysis
Company ||--o{ ContentRecommendation
Company ||--o{ PostingSchedule
Company ||--o{ ContentTypeAnalysis

SocialNetwork ||--o{ CompanySocialLink
SocialNetwork ||--o{ ContentPost

ContentPost ||--o{ PostMetric
ContentPost ||--o{ PostDemographics
ContentPost ||--o{ PostGender
ContentPost ||--o{ PostGeo
ContentPost }o--|| PostHashtag
ContentPost }o--|| PostKeyword

Hashtag }o--|| PostHashtag
Keyword }o--|| PostKeyword

TrendAnalysis ||--o{ TrendKeyword
TrendAnalysis ||--o{ TrendHashtag

TrendKeyword }o--|| Keyword
TrendHashtag }o--|| Hashtag

```
