from django.core.management.base import BaseCommand
from sql_trainer.lessons.models import Lesson, Exercise

class Command(BaseCommand):
    help = 'Creates sample lessons and exercises for demonstration purposes'

    def handle(self, *args, **options):
        # Create lesson 1: Introduction to SQL
        intro_lesson, created = Lesson.objects.get_or_create(
            title="Introduction to SQL",
            slug="intro-to-sql",
            order=1,
            defaults={
                'description': "Learn the basics of SQL querying with PostgreSQL",
                'content': """
<h1>Introduction to SQL</h1>

<p>SQL (Structured Query Language) is a standard language for storing, manipulating, and retrieving data in relational databases. This lesson covers the basics of SQL queries using PostgreSQL.</p>

<h2>Basic SELECT Statement</h2>

<p>The most fundamental SQL command is the SELECT statement, which retrieves data from a database table:</p>

<pre><code class="language-sql">SELECT column1, column2, ... 
FROM table_name;</code></pre>

<p>To select all columns from a table, use the * wildcard:</p>

<pre><code class="language-sql">SELECT * FROM table_name;</code></pre>

<h2>Filtering Data with WHERE</h2>

<p>The WHERE clause allows you to filter records based on specific conditions:</p>

<pre><code class="language-sql">SELECT column1, column2, ...
FROM table_name
WHERE condition;</code></pre>

<p>For example, to find employees with a salary greater than 50000:</p>

<pre><code class="language-sql">SELECT first_name, last_name, salary
FROM employees
WHERE salary > 50000;</code></pre>

<h2>Sorting Data with ORDER BY</h2>

<p>The ORDER BY clause is used to sort the result set:</p>

<pre><code class="language-sql">SELECT column1, column2, ...
FROM table_name
ORDER BY column1 [ASC|DESC];</code></pre>

<p>For example, to sort employees by last name in alphabetical order:</p>

<pre><code class="language-sql">SELECT first_name, last_name, hire_date
FROM employees
ORDER BY last_name ASC;</code></pre>
"""
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created lesson: {intro_lesson.title}'))
        else:
            self.stdout.write(f'Lesson already exists: {intro_lesson.title}')
            
        # Create exercises for lesson 1
        exercises = [
            {
                'title': 'Select All Employees',
                'instruction': 'Write a query to select all columns from the employees table.',
                'hints': 'Use the * wildcard to select all columns.',
                'initial_query': '-- Write your query here\n',
                'solution_query': 'SELECT * FROM employees;',
                'order': 1
            },
            {
                'title': 'Filter Employees by Department',
                'instruction': 'Write a query to select all employees from the Engineering department.',
                'hints': 'Use the WHERE clause to filter by department name.',
                'initial_query': '-- Write your query here\n',
                'solution_query': "SELECT * FROM employees WHERE department = 'Engineering';",
                'order': 2
            },
            {
                'title': 'Sort Employees by Salary',
                'instruction': 'Write a query to select the name and salary of all employees, sorted by salary in descending order (highest first).',
                'hints': 'Use ORDER BY with the DESC keyword.',
                'initial_query': '-- Write your query here\n',
                'solution_query': 'SELECT name, salary FROM employees ORDER BY salary DESC;',
                'order': 3
            }
        ]
        
        for exercise_data in exercises:
            exercise, created = Exercise.objects.get_or_create(
                lesson=intro_lesson,
                title=exercise_data['title'],
                defaults={
                    'instruction': exercise_data['instruction'],
                    'hints': exercise_data['hints'],
                    'initial_query': exercise_data['initial_query'],
                    'solution_query': exercise_data['solution_query'],
                    'order': exercise_data['order']
                }
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'  - Created exercise: {exercise.title}'))
            else:
                self.stdout.write(f'  - Exercise already exists: {exercise.title}')
        
        # Create lesson 2: Advanced SQL Queries
        advanced_lesson, created = Lesson.objects.get_or_create(
            title="Advanced SQL Queries",
            slug="advanced-sql",
            order=2,
            defaults={
                'description': "Learn advanced SQL querying techniques with PostgreSQL",
                'content': """
<h1>Advanced SQL Queries</h1>

<p>This lesson covers more advanced SQL querying techniques including joins, aggregations, and subqueries.</p>

<h2>JOIN Operations</h2>

<p>Joins allow you to combine rows from two or more tables based on a related column:</p>

<pre><code class="language-sql">SELECT columns
FROM table1
JOIN table2
ON table1.column = table2.column;</code></pre>

<p>For example, to join employees with their departments:</p>

<pre><code class="language-sql">SELECT employees.name, departments.name as department
FROM employees
JOIN departments ON employees.department_id = departments.id;</code></pre>

<h2>Aggregate Functions</h2>

<p>SQL provides several aggregate functions to perform calculations on data:</p>

<ul>
  <li>COUNT(): Counts the number of rows</li>
  <li>SUM(): Calculates the sum of values</li>
  <li>AVG(): Calculates the average of values</li>
  <li>MIN(): Finds the minimum value</li>
  <li>MAX(): Finds the maximum value</li>
</ul>

<p>For example, to find the average salary by department:</p>

<pre><code class="language-sql">SELECT department, AVG(salary) as average_salary
FROM employees
GROUP BY department;</code></pre>

<h2>Subqueries</h2>

<p>A subquery is a query within another query:</p>

<pre><code class="language-sql">SELECT column
FROM table1
WHERE column = (SELECT column FROM table2 WHERE condition);</code></pre>

<p>For example, to find employees with a salary higher than the average:</p>

<pre><code class="language-sql">SELECT name, salary
FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees);</code></pre>
"""
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created lesson: {advanced_lesson.title}'))
        else:
            self.stdout.write(f'Lesson already exists: {advanced_lesson.title}')
            
        # Create exercises for lesson 2
        advanced_exercises = [
            {
                'title': 'Join Employees and Departments',
                'instruction': 'Write a query to join the employees and departments tables to display each employee name alongside their department name.',
                'hints': 'Use an INNER JOIN with the department_id foreign key.',
                'initial_query': '-- Write your query here\n',
                'solution_query': """
SELECT employees.name, departments.name as department_name
FROM employees
JOIN departments ON employees.department_id = departments.id;
""",
                'order': 1
            },
            {
                'title': 'Calculate Department Statistics',
                'instruction': 'Write a query to calculate the average salary and employee count for each department.',
                'hints': 'Use GROUP BY with aggregate functions AVG() and COUNT().',
                'initial_query': '-- Write your query here\n',
                'solution_query': """
SELECT department, AVG(salary) as average_salary, COUNT(*) as employee_count
FROM employees
GROUP BY department;
""",
                'order': 2
            },
            {
                'title': 'Find Employees with Above Average Salary',
                'instruction': 'Write a query to find all employees whose salary is above the company average.',
                'hints': 'Use a subquery to calculate the average salary.',
                'initial_query': '-- Write your query here\n',
                'solution_query': """
SELECT name, salary
FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees);
""",
                'order': 3
            }
        ]
        
        for exercise_data in advanced_exercises:
            exercise, created = Exercise.objects.get_or_create(
                lesson=advanced_lesson,
                title=exercise_data['title'],
                defaults={
                    'instruction': exercise_data['instruction'],
                    'hints': exercise_data['hints'],
                    'initial_query': exercise_data['initial_query'],
                    'solution_query': exercise_data['solution_query'],
                    'order': exercise_data['order']
                }
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'  - Created exercise: {exercise.title}'))
            else:
                self.stdout.write(f'  - Exercise already exists: {exercise.title}')
                
        # Summary
        self.stdout.write(self.style.SUCCESS(f'Successfully created {Lesson.objects.count()} lessons with {Exercise.objects.count()} exercises'))