
-- Consultando as editorias com mais ocorrencias em 2022
SELECT extract(year from MA_DATA) AS ANO, EDITORIA, COUNT(*) AS TOTAL
FROM crawler_bucket_tvnews_prod
WHERE extract(year from MA_DATA) = 2022
GROUP BY extract(year from MA_DATA), EDITORIA
ORDER BY TOTAL DESC

-- Reporter que mais colaborarão no ano de 2023
WITH data AS (
  SELECT extract(year from MA_DATA) AS ANO, REPORTER
  FROM crawler_bucket_tvnews_prod
)
SELECT ANO, REPORTER, COUNT(*) AS TOTAL
FROM data
WHERE ANO = 2023
GROUP BY ANO, REPORTER
ORDER BY TOTAL DESC

-- Reporter e cinegrafista que mais trabalharam juntos no ano de 2023
WITH data AS (
  SELECT extract(year from MA_DATA) AS ANO, REPORTER, CINEGRAFISTA
  FROM dados
)
SELECT REPORTER, CINEGRAFISTA, COUNT(*) AS TOTAL
FROM data
WHERE ANO = 2023
GROUP BY REPORTER, CINEGRAFISTA
ORDER BY TOTAL DESC
LIMIT 10

-- Repórter e editoria e ordenados em ordem decrescente pelo número total de matérias
WITH data AS (
  SELECT extract(year from MA_DATA) AS ANO, REPORTER, EDITORIA
  FROM dados
)
SELECT REPORTER, EDITORIA, COUNT(*) AS TOTAL_MAT
FROM data
WHERE ANO = 2023
GROUP BY REPORTER, EDITORIA
ORDER BY TOTAL_MAT DESC