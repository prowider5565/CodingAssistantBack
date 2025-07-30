Table User {
  id bigint pk
  username varchar
  email varchar
  password varchar
  interests array[]
  profession varchar
  age int
  bio text
  joined_at date
}

Table Interests{
  id bigint pk
  user_id bigint [ref: > User.id]
  name text
}

Table Tests {
  id bigint pk
  created_at date
}

Table Questions {
  id bigint pk
  test_id bigint [ref: > Tests.id]
  question_type QuestionType
  text text
}

Table Answers {
  id bigint pk
  choice text
  question_id bigint [ref: > Questions.id]
}
Table Submissions {
  id bigint pk
  test_id bigint [ref:> Tests.id]
  score int
  question_count int
  submitted_at date
}

Table CodingTasks {
  id bigint pk
  title varchar
  user_id bigint [ref:> User.id]
  task_goal text
  time_limit int // in minutes
  started boolean
  completed boolean
}
Table CodingTaskSubmissions {
  id bigint pk
  task_id bigint [ref:> CodingTasks.id]
  feedback text
  runtime int // e.g 0.002 in seconds
  memory int // e.g 15.87 in mb
}

Table ChatSession {
  id bigint pk
  user_id bigint [ref:>User.id]
  topic_name varchar
}

Table ChatMessages {
  id bigint pk
  message text
  user Author // tracks whether who wrote the message
  session_id bigint [ref:> ChatSession.id]
  date date
}
Table GeneralMemory {
  id bigint pk
  user_id bigint [ref:> User.id]
  text text
}
Enum QuestionType {
  FreeText
  MultipleChoice
}

Enum Author {
  User
  ChatBot
}