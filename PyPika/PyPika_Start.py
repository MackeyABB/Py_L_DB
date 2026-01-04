'''
introduction:
'''

from pypika import Query, Table, Field, Order

q = Query.from_('customers').select('id', 'fname', 'lname', 'phone')

print(str(q))

print(q.get_sql())

'''
# Example of using Table and Field
'''
customers = Table('customers')
q = Query.from_(customers).select('id', 'fname', 'lname', 'phone').orderby('id', order=Order.desc)
print(str(q))


'''
# Example of using Table and Field with explicit field references'''
customers = Table('customers')
q = Query.from_(customers).select(customers.id, customers.fname, customers.lname, customers.phone)
print(str(q))

'''
# Example of using Table with alias'''
customers = Table('x_view_customers').as_('customers')
q = Query.from_(customers).select(customers.id, customers.phone)
print(str(q))


'''# Example of using Schema with Table
'''
from pypika import Table, Query, Schema

views = Schema('views')
q = Query.from_(views.customers).select(customers.id, customers.phone)
print(str(q))