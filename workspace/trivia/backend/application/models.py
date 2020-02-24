from application import db


#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
class Question(db.Model):
  """ table questions
  """
  # follow the best practice
  __tablename__ = 'questions'
  
  # primary key:
  id = db.Column(db.Integer, primary_key=True)

  # attributes:
  question = db.Column(db.Text, nullable=False)
  answer = db.Column(db.Text, nullable=False)
  difficulty = db.Column(db.Integer, nullable=False)

  # relationship
  category_id = db.Column(
    db.Integer, 
    db.ForeignKey(
      'categories.id', 
      onupdate='CASCADE', ondelete='SET NULL'
    ), 
    nullable=True
  )

  def __repr__(self):
    return f'<Question id="{self.id}" question="{self.question}" answer="{self.answer}" difficulty="{self.difficulty}" category_id="{self.category_id}">'

  def to_json(self):
    return {
      'id': self.id,
      'question': self.question,
      'answer': self.answer,
      'difficulty': self.difficulty,
      'category_id': self.category_id
    }
  
  def from_json(self, json):
    self.question = json['question'] 
    self.answer = json['answer'] 
    self.difficulty = int(json['difficulty'])
    self.category_id = int(json['category_id']) 


class Category(db.Model):
  """ table questions
  """
  # follow the best practice  
  __tablename__ = 'categories'
  
  # primary key:
  id = db.Column(db.Integer, primary_key=True)

  # attributes:
  type = db.Column(db.Text, nullable=False)

  # relationship:
  questions = db.relationship('Question', backref='category', lazy=True)

  def __repr__(self):
    return f'<Category id="{self.id}" type="{self.type}">'

  def to_json(self):
    return {
      'id': self.id,
      'type': self.type
    }

  def from_json(self, json):
    self.type = json['type'] 