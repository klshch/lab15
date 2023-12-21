from flask import url_for

from app import db

from .base import BaseTestCase

from app.todo.models import Todo



class TodoTest(BaseTestCase):

    '''Тест чи додається новий ToDo'''
    def test_todo_add(self):

        with self.client:
            response = self.client.post(url_for('todo.add'), 
                                        data=dict(title='tests'), 
                                        follow_redirects=True)
            
            self.assertEqual(response.status_code, 200)
            self.assertIn('Додано.'.encode('utf-8'), response.data)
            
            todo = Todo.query.filter_by(title='tests').first()
            self.assertIsNotNone(todo)
            

    '''Тест чи оновлюється ToDo'''    
    def test_todo_update(self):

        todo = Todo(title='tests', complete=False)

        db.session.add(todo)
        db.session.commit()

        response = self.client.get(url_for('todo.update', todo_id=todo.id))

        self.assertEqual(response.status_code, 302) 

        updated_todo = Todo.query.get(todo.id)

        self.assertIsNotNone(updated_todo)


    '''Тест чи видаляється ToDo'''      
    def test_delete_todo(self):

        todo = Todo(title='tests', complete=False)

        db.session.add(todo)
        db.session.commit()

        response = self.client.get(url_for('todo.delete', todo_id=todo.id))

        self.assertEqual(response.status_code, 302) 

        deleted_todo = Todo.query.get(todo.id)

        self.assertIsNone(deleted_todo)