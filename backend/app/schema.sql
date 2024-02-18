DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;

CREATE TABLE user
(
    id       INTEGER PRIMARY KEY AUTO_INCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT        NOT NULL
);

CREATE TABLE post
(
    id        INTEGER PRIMARY KEY AUTO_INCREMENT,
    author_id INTEGER   NOT NULL,
    created   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title     TEXT      NOT NULL,
    body      TEXT      NOT NULL,
    FOREIGN KEY (author_id) REFERENCES user (id)
);