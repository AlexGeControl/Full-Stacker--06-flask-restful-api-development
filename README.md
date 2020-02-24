# Udacity Full Stack Development Nanodegree

This is the project for **RESTful API development** of Udacity's Full Stack Development Nanodegree

---

## Up & Running

### Build Images

```bash
docker-compose build
```

### Identify Postgres Instance

```bash
docker ps -a
```

### Restore Database

```bash
# enter postgres instance:
docker exec -it trivia_db_1_ac29f1755358 bash
# restore db:
psql -U udacity -d triviaapp < trivia.psql
```

---