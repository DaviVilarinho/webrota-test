# webrota-test

Uma solução fullstack

Para executar:

```
docker-compose --env-file .env up --build -V
```

## Desafios

- Primeiro contato sério com Flask, embora não com Python
- Primeiro contato com soluções cartográficas, não consegui em verdade fazer um polígono, deveria ter investigado ainda mais essas libs antes de começar o projeto, mas a natureza do problema não me permitia pelo tempo, mas as lib que mais se aproximaram foram:
    - a do `google-maps` que não quis correr risco de arriscar expor minha chave e ser cobrado
    - a do `yandex`, mas temia não ter as funcionalidades e já era tarde no projeto
    - a do `leaflet`, mas teria que refazer tudo e não ia ter o port simples para o Vue que já estava pronto naquele momento.
- Entretanto eu implementei:
    - API Flask com Autenticação
    - Autenticação baseada em hash com salt no back-end
    - DB Redis (sei que é cache, mas como é simples e chave valor funciona bem como NoSQL. [Uso de Redis como DB](https://redis.io/blog/redis-cache-vs-redis-primary-database-in-90-seconds/))
    - Front com autenticação
    - Cálculo de distância utilizando a função Haversine. A natureza das coordenadas geográficas exigem um cálculo complexo considerando as cordas formadas pelos marcadores, e não a velha distância euclidiana.
    - É possível adicionar novos pontos
    - Pela API, seria possível criar novos marcadores e pelos meus testes para zona sul deu 5km, Monte Alegre somou uns 80km, então me pareceu correto.
    - Tudo com contêineres

## Conclusão

Foi uma oportunidade legal, embora com tempo reduzido em decorrência das minhas mais atividades que só de verdade me permitiram trabalhar no problema em um dia (domingo).
