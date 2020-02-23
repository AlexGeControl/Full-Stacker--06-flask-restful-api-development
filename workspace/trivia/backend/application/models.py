from application import db


#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
class Question(db.Model):
  """ table questions
  """
  # follow the best practice
  __tablename__ = 'questions'
  
  id = db.Column(db.Integer, primary_key=True)

  question = db.Column(db.String)
  answer = db.Column(db.String)
  category = db.Column(db.String)
  difficulty = db.Column(db.Integer)

  def __repr__(self):
    return f'<Question id="{self.id}" question="{self.question}" answer="{self.answer}" category="{self.category}" difficulty="{self.difficulty}">'

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def to_json(self):
    return {
      'id': self.id,
      'question': self.question,
      'answer': self.answer,
      'category': self.category,
      'difficulty': self.difficulty
    }
  
  def from_json(self, json):
    self.question = json.get('question', '') 
    self.answer = json.get('answer', '') 
    self.category = json.get('category', '') 
    self.difficulty = json.get('difficulty', '') 


class Category(db.Model):
  """ table questions
  """
  # follow the best practice  
  __tablename__ = 'categories'

  id = db.Column(db.Integer, primary_key=True)

  type = db.Column(db.String)

  def to_json(self):
    return {
      'id': self.id,
      'type': self.type
    }