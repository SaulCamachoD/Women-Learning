SELECT * FROM users; 
SELECT * FROM profiles; 
SELECT * FROM messages; 
SELECT* FROM blogs; 
SELECT* FROM blogs; 

SELECT users.name, blogs.id, blogs.content FROM users JOIN blogs ON users.id = blogs.user_id=1; 



SELECT users.id, users.name, users.email, profiles.age, profiles.level, profiles.native_language, profiles.language_of_interest
FROM users
JOIN profiles ON users.id = profiles.user_id
WHERE user_id = 2; 

