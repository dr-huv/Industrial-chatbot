"""
Database schema and model definitions
"""


class Product:
    """Product model for database representation"""

    def __init__(self, id, name, category, description, price=None, launch_date=None):
        self.id = id
        self.name = name
        self.category = category
        self.description = description
        self.price = price
        self.launch_date = launch_date

    @classmethod
    def from_dict(cls, data):
        """Create a Product instance from a dictionary"""
        return cls(
            id=data.get('id'),
            name=data.get('name'),
            category=data.get('category'),
            description=data.get('description'),
            price=data.get('price'),
            launch_date=data.get('launch_date')
        )

    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'description': self.description,
            'price': self.price,
            'launch_date': self.launch_date
        }


class Complaint:
    """Complaint model for database representation"""

    def __init__(self, id, product_id, issue_type, description, solution, frequency=None):
        self.id = id
        self.product_id = product_id
        self.issue_type = issue_type
        self.description = description
        self.solution = solution
        self.frequency = frequency

    @classmethod
    def from_dict(cls, data):
        """Create a Complaint instance from a dictionary"""
        return cls(
            id=data.get('id'),
            product_id=data.get('product_id'),
            issue_type=data.get('issue_type'),
            description=data.get('description'),
            solution=data.get('solution'),
            frequency=data.get('frequency')
        )

    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'product_id': self.product_id,
            'issue_type': self.issue_type,
            'description': self.description,
            'solution': self.solution,
            'frequency': self.frequency
        }


class FAQ:
    """FAQ model for database representation"""

    def __init__(self, id, product_id, question, answer, category):
        self.id = id
        self.product_id = product_id
        self.question = question
        self.answer = answer
        self.category = category

    @classmethod
    def from_dict(cls, data):
        """Create a FAQ instance from a dictionary"""
        return cls(
            id=data.get('id'),
            product_id=data.get('product_id'),
            question=data.get('question'),
            answer=data.get('answer'),
            category=data.get('category')
        )

    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'product_id': self.product_id,
            'question': self.question,
            'answer': self.answer,
            'category': self.category
        }
